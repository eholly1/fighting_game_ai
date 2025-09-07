"""
Evolutionary Agent: gen3_agent_025
==================================

Metadata:
{
  "generation": 3,
  "fitness": -19.41999999999976,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: b6896b8c1a244e60
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
    
    # Enhanced tactical ranges for improved hybrid combat
    point_blank_range = 0.08
    close_range = 0.16
    medium_range = 0.32
    far_range = 0.48
    max_range = 0.7
    
    # Advanced aggression calculation with momentum factors
    base_aggression = 0.72
    health_aggression = health_advantage * 0.45
    distance_aggression = max(0.0, (0.35 - distance) * 0.6)
    momentum_bonus = 0.15 if (abs(my_x_velocity) > 0.2 or abs(my_y_velocity) > 0.2) else 0.0
    current_aggression = max(0.25, min(0.92, base_aggression + health_aggression + distance_aggression + momentum_bonus))
    
    # Enhanced defensive priority with situational awareness
    base_defense = 0.55
    health_defense_modifier = (0.5 - my_health) * 0.8
    pressure_defense_modifier = 0.3 if (opp_attacking or distance < close_range) else 0.0
    defense_priority = max(0.15, min(0.85, base_defense + health_defense_modifier + pressure_defense_modifier))
    
    # Advanced positioning analysis
    wall_distance_left = my_x_pos
    wall_distance_right = 1.0 - my_x_pos
    near_wall = wall_distance_left < 0.18 or wall_distance_right < 0.18
    in_corner = wall_distance_left < 0.12 or wall_distance_right > 0.88
    opp_cornered = (opp_x_pos < 0.15 or opp_x_pos > 0.85)
    
    # Enhanced movement prediction and pattern recognition
    opp_closing_fast = (relative_pos > 0 and opp_x_velocity > 0.15) or (relative_pos < 0 and opp_x_velocity < -0.15)
    opp_retreating_fast = (relative_pos > 0 and opp_x_velocity < -0.15) or (relative_pos < 0 and opp_x_velocity > 0.15)
    opp_stationary = abs(opp_x_velocity) < 0.05 and abs(opp_y_velocity) < 0.05
    
    # Counter-attack timing system
    perfect_counter_window = not opp_attacking and opp_attack_cooldown > 0.25 and my_attack_cooldown < 0.1
    good_counter_window = not opp_attacking and opp_attack_cooldown > 0.15 and my_attack_cooldown < 0.2
    
    # Frame advantage calculation
    my_frame_advantage = (opp_attack_cooldown + opp_block_cooldown) - (my_attack_cooldown + my_block_cooldown)
    
    # Critical situation handling - highest priority
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6 if my_block_cooldown < 0.25 else 0
        elif opp_closing_fast:
            return 6 if my_block_cooldown < 0.4 else 0  
        else:
            # Enhanced recovery positioning
            if distance < medium_range:
                if in_corner:
                    return 3  # Jump to escape corner
                else:
                    return 7 if relative_pos < 0 else 8
            else:
                return 9 if my_projectile_cooldown < 0.15 else 6
    
    # Emergency health situations with improved decision making
    if my_health < 0.22:
        if distance > far_range and my_projectile_cooldown < 0.08:
            return 9  # Desperation projectile spam
        elif distance < close_range and opp_attacking:
            return 6  # Survival blocking
        elif distance < close_range and not opp_blocking and my_attack_cooldown < 0.08 and health_advantage > -0.6:
            # Calculated desperation attack when not too far behind
            return 5 if random.random() < 0.75 else 4
        elif opp_health < 0.25 and distance < medium_range:
            # Both low health - aggressive finish attempt
            if my_attack_cooldown < 0.12:
                return 4 if random.random() < 0.6 else 5
            else:
                return 2 if relative_pos > 0 else 1
        else:
            # Enhanced evasive movement
            if in_corner:
                # Corner escape priority
                if wall_distance_left < wall_distance_right:
                    return 8 if my_block_cooldown < 0.3 else 2
                else:
                    return 7 if my_block_cooldown < 0.3 else 1
            elif near_wall:
                return 8 if wall_distance_left < wall_distance_right else 7
            else:
                return 7 if relative_pos > 0 else 8
    
    # Enhanced stunned opponent punishment
    if opp_stunned:
        if distance < close_range and my_attack_cooldown < 0.08:
            # Optimized combo selection based on positioning
            if abs(height_diff) > 0.3:
                return 3  # Jump attack for height advantage
            else:
                combo_choice = random.random()
                if combo_choice < 0.5:
                    return 5  # Heavy damage priority
                elif combo_choice < 0.75:
                    return 4  # Quick follow-up
                else:
                    return 9 if my_projectile_cooldown < 0.05 else 5
        elif distance < medium_range:
            # Improved rush-in logic
            if abs(height_diff) > 0.25:
                return