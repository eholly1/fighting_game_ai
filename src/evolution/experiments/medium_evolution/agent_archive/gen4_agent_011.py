"""
Evolutionary Agent: gen4_agent_011
==================================

Metadata:
{
  "generation": 4,
  "fitness": -10.719999999999553,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 9d7d2c3525e4d67f
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
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(0.0, min(1.0, state[0] if len(state) > 0 else 0.5))
    my_pos_y = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with defensive bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = max(0.0, min(1.0, state[11] if len(state) > 11 else 0.5))
    opp_pos_y = state[13] if len(state) > 13 else 0.5
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Enhanced tactical ranges for refined control
    point_blank_range = 0.08
    close_range = 0.16
    medium_close_range = 0.24
    medium_range = 0.32
    medium_far_range = 0.45
    far_range = 0.6
    
    # Dynamic fighting parameters
    base_aggression = 0.68
    wall_threshold = 0.12
    critical_health = 0.22
    comfortable_health = 0.65
    
    # Enhanced situational awareness
    near_left_wall = my_pos_x < wall_threshold
    near_right_wall = my_pos_x > (1.0 - wall_threshold)
    opp_near_left_wall = opp_pos_x < wall_threshold
    opp_near_right_wall = opp_pos_x > (1.0 - wall_threshold)
    
    # Advanced momentum and prediction system
    my_momentum = abs(my_velocity_x)
    opp_momentum = abs(opp_velocity_x)
    
    # Predict opponent movement
    predicted_distance = distance
    if opp_momentum > 0.2:
        velocity_prediction = opp_velocity_x * 0.08
        if opp_velocity_x * relative_pos < 0:  # Approaching
            predicted_distance = max(0.0, distance - abs(velocity_prediction))
        else:  # Retreating
            predicted_distance = min(1.0, distance + abs(velocity_prediction))
    
    # Enhanced health ratio analysis
    health_ratio = my_health / max(0.05, opp_health)
    health_differential = my_health - opp_health
    
    # Multi-layered aggression calculation
    situational_aggression = base_aggression
    
    # Health-based adjustments
    if health_advantage > 0.3:
        situational_aggression = min(0.88, base_aggression + 0.25)
    elif health_advantage > 0.1:
        situational_aggression = min(0.8, base_aggression + 0.15)
    elif health_advantage < -0.3:
        situational_aggression = max(0.35, base_aggression - 0.25)
    elif health_advantage < -0.1:
        situational_aggression = max(0.45, base_aggression - 0.15)
    
    # Momentum adjustments
    if my_momentum > 0.3:
        momentum_bonus = 0.08 if my_velocity_x * relative_pos > 0 else -0.05
        situational_aggression += momentum_bonus
    
    # Pressure assessment
    opponent_pressure = 0.0
    if opp_attacking or (distance < medium_range and opp_momentum > 0.25):
        opponent_pressure = 0.12
    if opp_projectile_cooldown < 0.1 and distance > medium_range:
        opponent_pressure += 0.08
    
    situational_aggression = max(0.2, situational_aggression - opponent_pressure)
    
    # Cannot act while stunned - minimal movement only
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6 if my_block_cooldown < 0.2 else 0
        return 0
    
    # Critical health emergency protocols
    if my_health < critical_health:
        if health_advantage < -0.4:
            # Desperate situation management
            if opp_attacking and distance < medium_range:
                if my_block_cooldown < 0.15:
                    if near_left_wall:
                        return 8  # Block right
                    elif near_right_wall:
                        return 7  # Block left
                    else:
                        return 6  # Standard block
                else:
                    # Evasive maneuvers
                    if distance < close_range:
                        return 3  # Jump away
                    else:
                        return 1 if my_pos_x > 0.6 else 2
            
            elif distance > medium_far_range:
                if my_projectile_cooldown < 0.25:
                    return 9  # Desperate projectile
                else:
                    return 6  # Defensive wait
            
            elif distance > medium_range:
                # Maintain distance
                if relative_pos > 0 and not near_right_wall:
                    return 2  # Move away right
                elif relative_pos < 0 and not near_left_wall:
                    return 1  # Move away left
                else:
                    return 6