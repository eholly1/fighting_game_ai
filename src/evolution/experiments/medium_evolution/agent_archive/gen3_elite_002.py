"""
Evolutionary Agent: gen3_elite_002
==================================

Metadata:
{
  "generation": 3,
  "fitness": 218.2713333333319,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 6d7cb763b1102f3f
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
    
    # Extract my fighter status with defensive bounds checking
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cooldown = max(0.0, state[8])
    my_attack_cooldown = max(0.0, state[9])
    my_block_cooldown = max(0.0, state[10])
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cooldown = max(0.0, state[19])
    opp_attack_cooldown = max(0.0, state[20])
    opp_block_cooldown = max(0.0, state[21])
    
    # Hybrid fighter tactical ranges - balanced approach
    point_blank_range = 0.06
    close_range = 0.15
    medium_range = 0.28
    far_range = 0.45
    max_range = 0.7
    
    # Dynamic aggression system based on multiple factors
    base_aggression = 0.7
    health_aggression_modifier = health_advantage * 0.4
    distance_aggression_modifier = max(0.0, (0.3 - distance) * 0.5)
    current_aggression = max(0.2, min(0.95, base_aggression + health_aggression_modifier + distance_aggression_modifier))
    
    # Defensive priority calculation
    defense_priority = 0.6 - (health_advantage * 0.3) + (0.4 if my_health < 0.3 else 0.0)
    defense_priority = max(0.1, min(0.9, defense_priority))
    
    # Counter-attack window detection
    counter_window = not opp_attacking and opp_attack_cooldown > 0.2 and my_attack_cooldown < 0.15
    
    # Positioning awareness
    wall_distance_left = my_x_pos
    wall_distance_right = 1.0 - my_x_pos
    near_wall = wall_distance_left < 0.2 or wall_distance_right < 0.2
    opp_cornered = (opp_x_pos < 0.15 or opp_x_pos > 0.85)
    
    # Movement prediction
    opp_closing_in = (relative_pos > 0 and opp_x_velocity > 0.1) or (relative_pos < 0 and opp_x_velocity < -0.1)
    opp_retreating = (relative_pos > 0 and opp_x_velocity < -0.1) or (relative_pos < 0 and opp_x_velocity > 0.1)
    
    # Critical situation handling - highest priority
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6 if my_block_cooldown < 0.3 else 0
        elif opp_closing_in:
            return 6 if my_block_cooldown < 0.5 else 0
        else:
            # Try to create space while stunned
            if distance < medium_range:
                return 7 if relative_pos < 0 else 8
            else:
                return 9 if my_projectile_cooldown < 0.2 else 6
    
    # Emergency health situations
    if my_health < 0.2:
        if distance > far_range and my_projectile_cooldown < 0.1:
            return 9  # Desperate projectile spam
        elif distance < close_range and opp_attacking:
            return 6  # Survival blocking
        elif distance < close_range and not opp_blocking and my_attack_cooldown < 0.1:
            # All-in desperation attack
            return 5 if random.random() < 0.7 else 4
        else:
            # Evasive movement with blocking
            if near_wall:
                return 8 if wall_distance_left < wall_distance_right else 7
            else:
                return 7 if relative_pos > 0 else 8
    
    # Capitalize on stunned opponent
    if opp_stunned:
        if distance < close_range and my_attack_cooldown < 0.1:
            # Maximize damage on stunned opponent
            combo_choice = random.random()
            if combo_choice < 0.6:
                return 5  # Heavy damage
            elif combo_choice < 0.85:
                return 4  # Quick follow-up
            else:
                return 9 if my_projectile_cooldown < 0.1 else 5
        elif distance >= close_range:
            # Rush in for combo opportunity
            return 2 if relative_pos > 0 else 1
        else:
            return 0  # Wait for attack cooldown
    
    # Defensive responses to opponent attacks
    if opp_attacking:
        if distance < point_blank_range:
            return 6 if my_block_cooldown < 0.2 else 0
        elif distance < close_range:
            # Block with positioning for counter
            if my_block_cooldown < 0.1:
                spacing_direction = 2 if relative_pos > 0 else 1
                return 8 if spacing_direction == 2 else 7
            else:
                # Evasive movement
                if not near_wall:
                    return 3 if random.random() < 0.4 else (1 if relative_pos > 0 else 2)
                else:
                    return 3
        elif distance < medium_range:
            # Medium range defense with gap closing
            return 8 if relative_pos > 0 else 7
        else:
            # Long range - projectile counter or movement
            if my_projectile_cooldown < 0.1 and random.random() < 0.6:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Range-specific hybrid tactics
    if distance <= point_blank_range:
        # Point blank - explosive mixups
        if my_attack_cooldown < 0.05:
            if opp_blocking:
                # Guard break sequences
                if my_projectile_cooldown < 0.1 and random.random() < 0.3:
                    return 9  # Point blank projectile surprise
                elif random.random() < 0.6:
                    return 5  # Power through block
                else:
                    # Micro spacing for better angle
                    if random.random() < 0.5:
                        return 1 if relative_pos > 0.3 else 2