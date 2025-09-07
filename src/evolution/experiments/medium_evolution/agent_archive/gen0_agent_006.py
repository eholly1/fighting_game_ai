"""
Evolutionary Agent: gen0_agent_006
==================================

Metadata:
{
  "generation": 0,
  "fitness": -15.239999999999743,
  "fighting_style": "counter_puncher",
  "win_rate": 0.0
}

Code Hash: 6764dbff8433c934
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_block_status = state[6]
    opponent_block_status = state[17]
    my_attack_status = state[5]
    opponent_attack_status = state[16]
    my_projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    height_diff = state[24]
    
    # Define tactical ranges and thresholds
    close_range = 0.12
    medium_range = 0.28
    counter_distance = 0.18
    health_critical = 0.25
    health_advantage_threshold = 0.3
    
    # Counter-puncher core strategy: wait and punish
    punish_opportunity = False
    retreat_needed = False
    setup_counter = False
    
    # Detect opponent vulnerability for counter-attacks
    if opponent_attack_status > 0.5:
        # Opponent is attacking, prime counter opportunity
        punish_opportunity = True
    elif opponent_block_status < 0.1 and distance < counter_distance:
        # Opponent not blocking in counter range
        punish_opportunity = True
    elif my_projectile_cooldown < 0.1 and distance > 0.4:
        # Safe projectile counter opportunity
        punish_opportunity = True
    
    # Assess need for defensive positioning
    if my_health < health_critical:
        retreat_needed = True
    elif health_advantage < -0.4:
        retreat_needed = True
    elif opponent_attack_status > 0.7 and distance < 0.1:
        retreat_needed = True
    
    # Determine counter setup positioning
    if distance > counter_distance + 0.05 and distance < medium_range:
        setup_counter = True
    elif opponent_projectile_cooldown > 0.3 and distance > 0.35:
        setup_counter = True
    
    # Emergency defensive situations
    if my_health < 0.15:
        if distance < close_range:
            if opponent_attack_status > 0.5:
                return 6  # Block immediate threat
            elif relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            if my_projectile_cooldown < 0.2:
                return 9  # Desperate projectile
            else:
                return 6  # Block and wait
        else:
            return 9 if my_projectile_cooldown < 0.1 else 6
    
    # Counter-attack execution phase
    if punish_opportunity and not retreat_needed:
        if distance < close_range:
            # Close range punishment
            if opponent_block_status > 0.5:
                # Opponent blocking, mix up timing
                if random.random() < 0.3:
                    return 0  # Wait for block to drop
                elif random.random() < 0.6:
                    return 5  # Strong kick to break guard
                else:
                    return 4  # Quick punch
            else:
                # Opponent open, punish hard
                if health_advantage > 0.2:
                    return 5  # Kick for damage
                elif opponent_attack_status > 0.7:
                    return 4  # Fast counter punch
                else:
                    return 5 if random.random() < 0.7 else 4
        
        elif distance < counter_distance:
            # Optimal counter range
            if opponent_attack_status > 0.6:
                # Opponent committing to attack
                if relative_pos > 0.1:
                    return 1  # Move in for counter
                elif relative_pos < -0.1:
                    return 2  # Move in for counter
                else:
                    return 4  # Counter punch
            else:
                # Setup for counter
                if my_projectile_cooldown < 0.1:
                    return 9  # Projectile pressure
                else:
                    return 0  # Patient wait
        
        elif distance < medium_range:
            # Medium range counter setup
            if my_projectile_cooldown < 0.1 and opponent_block_status < 0.3:
                return 9  # Projectile counter
            elif opponent_attack_status < 0.2:
                # Opponent passive, close distance
                if relative_pos > 0.1:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                return 0  # Wait for opening
        
        else:
            # Long range counter
            if my_projectile_cooldown < 0.1:
                return 9  # Long range punishment
            else:
                return 0  # Wait for cooldown
    
    # Defensive retreat and repositioning
    if retreat_needed:
        if distance < close_range:
            if opponent_attack_status > 0.5:
                return 6  # Block immediate danger
            elif relative_pos > 0:
                # Opponent to right, move left
                if opponent_attack_status > 0.3:
                    return 7  # Move left with block
                else:
                    return 1  # Move left
            else:
                # Opponent to left, move right
                if opponent_attack_status > 0.3:
                    return 8  # Move right with block
                else:
                    return 2  # Move right
        
        elif distance < medium_range:
            if my_projectile_cooldown < 0.2:
                return 9  # Create space with projectile
            elif opponent_attack_status > 0.4:
                return 6  # Block and assess
            else:
                # Create more distance
                if relative_pos > 0:
                    return 1  # Move away left
                else:
                    return 2  # Move away right
        
        else:
            # Already at safe distance
            if my_projectile_cooldown < 0.1:
                return 9  # Safe projectile
            else:
                return 6  # Block and recover
    
    # Counter setup positioning
    if setup_counter:
        target_distance = counter_distance
        distance_error = distance - target_distance
        
        if abs(distance_error) < 0.03:
            # Perfect counter distance, wait
            if opponent_projectile_cooldown > 0.5:
                return 0  # Patient wait
            elif my_projectile_cooldown < 0.1:
                return 9  # Pressure with projectile
            else:
                return 0  # Wait for opportunity
        
        elif distance_error > 0:
            # Too far, move closer
            if relative_pos > 0.1:
                if opponent_attack_status > 0.4:
                    return 8  # Approach with block
                else:
                    return 2  # Move right
            elif relative_pos < -0.1:
                if opponent_attack_status > 0.4:
                    return 7  # Approach with block
                else:
                    return 1  # Move left
            else:
                return 0  # Wait for clear direction
        
        else:
            # Too close, back up slightly
            if my_projectile_cooldown < 0.1:
                return 9  # Back up with projectile
            elif relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away