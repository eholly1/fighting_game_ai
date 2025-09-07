"""
Evolutionary Agent: gen0_agent_019
==================================

Metadata:
{
  "generation": 0,
  "fitness": 31.81999999999877,
  "fighting_style": "patient_defender",
  "win_rate": 0.0
}

Code Hash: fd4bc58f62f007f0
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
    
    # Extract player status information
    my_health = max(0.0, min(1.0, state[3]))
    opponent_health = max(0.0, min(1.0, state[14]))
    my_block_status = state[6]
    opponent_attack_status = state[17]
    my_projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    height_diff = state[24]
    
    # Define tactical ranges and thresholds
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_threshold = 0.3
    losing_threshold = -0.3
    
    # Patient defender core parameters
    block_preference = 0.75
    counter_attack_chance = 0.4
    retreat_health_threshold = 0.3
    perfect_counter_distance = 0.08
    
    # Emergency survival mode - critical health
    if my_health < critical_health:
        if distance < close_range:
            if opponent_attack_status > 0.5:
                return 6  # Block incoming attack
            elif distance < perfect_counter_distance and random.random() < 0.3:
                return 5  # Quick counter kick
            else:
                # Retreat while blocking
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        else:
            # Try to maintain distance and use projectiles
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile attack
            else:
                return 6  # Defensive blocking
    
    # Winning decisively - slightly more aggressive but still patient
    if health_advantage > winning_threshold:
        if distance < close_range:
            if opponent_attack_status > 0.5:
                return 6  # Still block first
            elif random.random() < 0.6:
                # Controlled aggression
                if random.random() < 0.4:
                    return 4  # Quick punch
                else:
                    return 5  # Stronger kick
            else:
                return 6  # Default to blocking
        
        elif distance < medium_range:
            if random.random() < 0.4:
                # Advance cautiously
                if relative_pos > 0:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
            else:
                return 6  # Patient waiting
        
        else:
            # Long range when winning
            if my_projectile_cooldown < 0.1 and random.random() < 0.5:
                return 9  # Projectile to maintain pressure
            else:
                return 6  # Defensive patience
    
    # Losing badly - ultra defensive
    elif health_advantage < losing_threshold:
        if distance < close_range:
            if opponent_attack_status > 0.5:
                return 6  # Block everything
            elif distance < perfect_counter_distance and random.random() < 0.25:
                return 4  # Desperate quick counter
            else:
                # Try to create distance
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
        
        elif distance < medium_range:
            # Maintain defensive distance
            if random.random() < 0.8:
                return 6  # Heavy blocking focus
            else:
                # Slight repositioning
                if abs(relative_pos) > 0.3:
                    if relative_pos > 0:
                        return 7  # Move left with block
                    else:
                        return 8  # Move right with block
                else:
                    return 6  # Stay and block
        
        else:
            # Long range defensive
            if my_projectile_cooldown < 0.1 and random.random() < 0.3:
                return 9  # Occasional projectile
            else:
                return 6  # Defensive blocking
    
    # Balanced fight - core patient defender strategy
    else:
        if distance < close_range:
            # Close range - highest blocking priority
            if opponent_attack_status > 0.5:
                return 6  # Block incoming attacks
            elif distance < perfect_counter_distance:
                # Perfect counter distance
                if random.random() < counter_attack_chance:
                    if random.random() < 0.3:
                        return 4  # Quick counter punch
                    else:
                        return 5  # Counter kick
                else:
                    return 6  # Patient blocking
            else:
                # Very close but not perfect counter range
                if random.random() < block_preference:
                    return 6  # Prefer blocking
                else:
                    # Slight repositioning for better counter position
                    if distance > 0.08:
                        if relative_pos > 0:
                            return 2  # Move closer
                        else:
                            return 1  # Move closer
                    else:
                        return 6  # Too close, just block
        
        elif distance < medium_range:
            # Medium range - patient positioning
            if opponent_attack_status > 0.5 and distance < 0.2:
                return 6  # Block if opponent is attacking nearby
            elif random.random() < 0.6:
                return 6  # Patient waiting for opportunity
            else:
                # Careful positioning
                if distance < 0.18:
                    # A bit too close, maintain slight distance
                    if relative_pos > 0:
                        return 7  # Move left with block
                    else:
                        return 8  # Move right with block
                elif distance > 0.25:
                    # A bit far, move closer cautiously
                    if relative_pos > 0:
                        return 8  # Move right with block
                    else:
                        return 7  # Move left with block
                else:
                    return 6  # Perfect medium distance, just block and wait
        
        else:
            # Long range - patient projectile game
            if distance > far_range:
                if my_projectile_cooldown < 0.1:
                    if random.random() < 0.4:
                        return 9  # Measured projectile use
                    else:
                        return 6  # Still prefer blocking
                else:
                    # Move closer while maintaining defense
                    if relative_pos > 0:
                        return 8  # Move right with block
                    else:
                        return 7  # Move left with block
            else:
                # Medium-far range
                if opponent_projectile_cooldown < 0.1:
                    return 6  # Expect projectile, block it
                elif random.random() < 0.5:
                    return 6  # Patient blocking
                else:
                    # Gradual approach
                    if relative_pos > 0:
                        return 8  # Move right with block
                    else:
                        return 7  # Move left with block
    
    # Ultimate fallback - should never reach here
    return 6  # Default to blocking - true to patient defender style