"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_028
Rank: 24/100
Generation: 0
Fighting Style: pressure_fighter

Performance Metrics:
- Fitness: 264.92
- Win Rate: 0.0%
- Average Reward: 264.92

Created: 2025-06-01 00:36:59
Lineage: Original

Tournament Stats:
None
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
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cooldown = state[8] if len(state) > 8 else 0.0
    
    # Extract opponent information
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    opp_stunned = state[18] if len(state) > 18 else 0.0
    
    # Define pressure fighter strategic parameters
    close_range_threshold = 0.15
    medium_range_threshold = 0.3
    far_range_threshold = 0.5
    aggression_multiplier = 1.2
    corner_distance_threshold = 0.8
    health_desperation_threshold = -0.4
    winning_threshold = 0.3
    
    # Emergency survival mode when health is critically low
    if health_advantage < health_desperation_threshold and my_health < 0.3:
        if distance < close_range_threshold and opp_attacking > 0.5:
            return 6  # Block incoming attack
        elif distance > medium_range_threshold and my_projectile_cooldown < 0.3:
            return 9  # Projectile to maintain distance
        elif distance > close_range_threshold:
            # Maintain distance while low health
            if relative_pos > 0:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
    
    # Opponent is stunned - maximum aggression opportunity
    if opp_stunned > 0.5:
        if distance < close_range_threshold:
            # Close range - mix up attacks for maximum damage
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 5  # Kick for higher damage
            elif attack_choice < 0.8:
                return 4  # Punch for speed
            else:
                return 5  # Another kick
        elif distance < medium_range_threshold:
            # Rush in for the kill
            if relative_pos > 0:
                return 2  # Move right toward stunned opponent
            else:
                return 1  # Move left toward stunned opponent
        else:
            # Too far for immediate pressure
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile while closing distance
            else:
                # Move closer aggressively
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # I'm stunned - defensive recovery
    if my_stunned > 0.5:
        if distance < close_range_threshold and opp_attacking > 0.3:
            return 6  # Block to minimize damage
        elif distance < medium_range_threshold:
            # Try to create space while stunned
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            return 6  # Just block and recover
    
    # Opponent is attacking - pressure fighter response
    if opp_attacking > 0.5:
        if distance < close_range_threshold:
            # In close range during opponent attack
            block_or_counter = random.random()
            if health_advantage < -0.2:
                return 6  # Block when losing
            elif block_or_counter < 0.3:
                return 6  # Sometimes block for safety
            elif block_or_counter < 0.65:
                return 4  # Fast counter punch
            else:
                return 5  # Counter kick
        elif distance < medium_range_threshold:
            # Medium range - rush in during their attack recovery
            if relative_pos > 0:
                return 2  # Aggressive advance right
            else:
                return 1  # Aggressive advance left
    
    # Corner pressure strategy - key to pressure fighting
    stage_position = my_x_pos
    opp_stage_position = opp_x_pos
    
    # Determine if opponent is near corner
    opp_near_left_corner = opp_stage_position < 0.2
    opp_near_right_corner = opp_stage_position > 0.8
    my_near_left_corner = stage_position < 0.2
    my_near_right_corner = stage_position > 0.8
    
    # If I'm cornered, try to escape with movement
    if my_near_left_corner or my_near_right_corner:
        if distance < close_range_threshold and opp_attacking > 0.3:
            # Cornered and under attack - block and move
            if my_near_left_corner:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
        elif distance < medium_range_threshold:
            # Try to jump out or create space
            escape_method = random.random()
            if escape_method < 0.4:
                return 3  # Jump to escape corner
            elif my_near_left_corner:
                return 2  # Move right to escape
            else:
                return 1  # Move left to escape
    
    # Opponent is cornered - maximum pressure opportunity
    if opp_near_left_corner or opp_near_right_corner:
        if distance < close_range_threshold:
            # Perfect position for corner pressure
            if opp_blocking > 0.5:
                # Opponent is blocking - mix up attacks to break guard
                mixup_choice = random.random()
                if mixup_choice < 0.3:
                    return 5  # Heavy kick to break block
                elif mixup_choice < 0.6:
                    return 4  # Fast punch
                else:
                    return 3  # Jump attack to confuse
            else:
                # Opponent not blocking - aggressive attack
                corner_attack = random.random()
                if corner_attack < 0.6:
                    return 5  # Strong kick
                else:
                    return 4  # Fast punch
        elif distance < medium_range_threshold:
            # Close the distance for corner pressure
            if relative_pos > 0:
                return 2  # Move right to maintain corner pressure
            else:
                return 1