"""
Evolutionary Agent: gen1_elite_002
==================================

Metadata:
{
  "generation": 1,
  "fitness": 226.92479999999827,
  "fighting_style": "pressure_fighter",
  "win_rate": 0.5
}

Code Hash: ab23d0e627e440bb
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cooldown = state[8]
    my_attack_cooldown = state[9]
    my_block_cooldown = state[10]
    
    # Extract opponent information
    opp_health = state[12] if state[12] >= 0 else 0.5
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cooldown = state[19]
    opp_attack_cooldown = state[20]
    opp_block_cooldown = state[21]
    
    # Define strategic constants for pressure fighter
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    corner_distance = 0.1
    aggression_base = 0.8
    retreat_threshold = -0.4
    
    # Calculate dynamic aggression based on health and position
    aggression_modifier = 1.0
    if health_advantage > 0.2:
        aggression_modifier = 1.3  # More aggressive when winning
    elif health_advantage < -0.2:
        aggression_modifier = 0.6  # Less aggressive when losing
    
    current_aggression = aggression_base * aggression_modifier
    
    # Emergency defensive situations
    if my_stunned:
        return 6  # Block if stunned
    
    if my_health < 0.2 and health_advantage < -0.3:
        # Desperate situation - try to survive
        if distance > 0.3:
            return 9 if my_projectile_cooldown < 0.1 else 6
        else:
            return 6  # Block and hope
    
    # Opponent is attacking - defensive response
    if opp_attacking and distance < 0.2:
        if my_block_cooldown < 0.1:
            # Can block - decide based on position
            if distance < 0.08:
                return 6  # Pure block at very close range
            else:
                # Block while positioning
                if relative_pos > 0:
                    return 8  # Block and move right
                else:
                    return 7  # Block and move left
        else:
            # Can't block - try to escape
            if relative_pos > 0:
                return 2  # Move right away
            else:
                return 1  # Move left away
    
    # Opponent is stunned - capitalize immediately
    if opp_stunned and distance < 0.3:
        if distance < close_range:
            # Close enough for melee
            if my_attack_cooldown < 0.1:
                return 5 if random.random() < 0.7 else 4  # Prefer kicks when stunned
            else:
                # Move closer while they're stunned
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        else:
            # Move in for the kill
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    # Core pressure fighter strategy based on range
    if distance < close_range:
        # Very close range - maximum pressure
        if my_attack_cooldown < 0.1:
            # Can attack
            if opp_blocking:
                # Opponent blocking - mix up timing and try to break guard
                if random.random() < 0.4:
                    # Sometimes wait/reposition against blockers
                    if relative_pos > 0:
                        return 2  # Slight repositioning
                    else:
                        return 1
                else:
                    # Keep pressure with varied attacks
                    return 5 if random.random() < 0.6 else 4
            else:
                # Opponent not blocking - attack aggressively
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Quick punch
                elif attack_choice < 0.8:
                    return 5  # Strong kick
                else:
                    # Occasional projectile at close range for surprise
                    return 9 if my_projectile_cooldown < 0.1 else 4
        else:
            # Attack on cooldown - maintain pressure through positioning
            if abs(relative_pos) > 0.5:
                # Opponent trying to escape - chase
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                # Stay close and ready
                if random.random() < 0.3:
                    return 6  # Occasional block to mix up rhythm
                else:
                    return 0  # Stay ready for next attack
    
    elif distance < medium_range:
        # Medium range - close the gap aggressively
        approach_modifier = 1.0
        
        # More aggressive approach if opponent is weakened
        if health_advantage > 0.1:
            approach_modifier = 1.2
        
        # Consider opponent's movement
        if abs(opp_x_velocity) > 0.1:
            # Opponent is moving - predict and intercept
            if opp_x_velocity > 0:
                # Opponent moving right
                if relative_pos > 0:
                    return 2  # Chase
                else:
                    return 1  # Cut off
            else:
                # Opponent moving left
                if relative_pos < 0:
                    return 1  # Chase
                else:
                    return 2  # Cut off
        
        # Standard approach based on position
        if random.random() < current_aggression:
            # Aggressive approach
            if relative_pos > 0.1:
                return 2  # Move right toward opponent
            elif relative_pos < -0.1:
                return 1  # Move left toward opponent
            else:
                # Very close to optimal position - prepare for engagement
                if my_projectile_cooldown < 0.1 and random.random() < 0.3:
                    return 9  # Surprise projectile
                else:
                    return 0  # Wait for perfect moment
        else:
            # Cautious approach with blocking
            if relative_pos > 0:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
    
    elif distance < far_range:
        # Far range - decide between closing distance or projectile pressure
        
        # Check if opponent is also at range and likely to projectile
        if opp_projectile_cooldown < 0.1 and distance > 0.3:
            # Opponent might projectile - either rush or counter-projectile
            if random.random() < 0.6:
                # Rush approach - pressure fighter style
                if relative_pos > 0:
                    return 2