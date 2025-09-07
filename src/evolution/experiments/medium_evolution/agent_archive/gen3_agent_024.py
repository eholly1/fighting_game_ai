"""
Evolutionary Agent: gen3_agent_024
==================================

Metadata:
{
  "generation": 3,
  "fitness": 29.29999999999896,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 506cb4c61f02b6eb
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_velocity_y = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_stunned = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_velocity_y = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_stunned = state[20] if len(state) > 20 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define evolved tactical ranges with more granular control
    point_blank_range = 0.05
    ultra_close_range = 0.10
    close_range = 0.16
    medium_close_range = 0.25
    medium_range = 0.38
    medium_far_range = 0.55
    far_range = 0.70
    max_range = 0.85
    
    # Advanced aggression calculation with opponent pattern recognition
    base_aggression = 0.72
    health_factor = 1.0
    distance_factor = 1.0
    momentum_factor = 1.0
    adaptation_factor = 1.0
    
    # Enhanced health-based aggression with non-linear scaling
    health_ratio = my_health / max(0.1, opponent_health)
    if health_advantage > 0.5:
        health_factor = 1.4 + (health_advantage - 0.5) * 0.6
    elif health_advantage > 0.3:
        health_factor = 1.25
    elif health_advantage > 0.1:
        health_factor = 1.1
    elif health_advantage > -0.15:
        health_factor = 0.95
    elif health_advantage > -0.35:
        health_factor = 0.75
    else:
        health_factor = 0.55 - abs(health_advantage) * 0.3
    
    # Dynamic distance-based aggression with velocity consideration
    if distance < ultra_close_range:
        distance_factor = 1.35
    elif distance < close_range:
        distance_factor = 1.2
    elif distance < medium_close_range:
        distance_factor = 1.05
    elif distance > medium_far_range:
        distance_factor = 0.85
    elif distance > far_range:
        distance_factor = 0.75
    
    # Advanced momentum and positioning analysis
    opponent_approaching = False
    my_approaching = False
    
    if relative_pos > 0.1 and opponent_velocity_x > 0.15:
        opponent_approaching = True
    elif relative_pos < -0.1 and opponent_velocity_x < -0.15:
        opponent_approaching = True
    
    if relative_pos > 0.1 and my_velocity_x > 0.15:
        my_approaching = True
    elif relative_pos < -0.1 and my_velocity_x < -0.15:
        my_approaching = True
    
    # Momentum-based tactical adjustments
    if opponent_approaching and distance < medium_range:
        momentum_factor = 1.15
    elif my_approaching and distance > close_range:
        momentum_factor = 1.08
    elif abs(my_velocity_x) < 0.05 and distance > medium_close_range:
        momentum_factor = 0.92
    
    # Corner position detection and adaptation
    corner_pressure = 0.0
    if my_pos_x < 0.15 or my_pos_x > 0.85:
        corner_pressure = 0.3
        if distance < medium_range:
            corner_pressure = 0.5
    
    opponent_cornered = opponent_pos_x < 0.15 or opponent_pos_x > 0.85
    if opponent_cornered and distance < medium_range:
        adaptation_factor = 1.2
    
    current_aggression = min(1.0, max(0.3, base_aggression * health_factor * distance_factor * momentum_factor * adaptation_factor - corner_pressure))
    
    # Enhanced emergency protocols
    if my_stunned > 0.4:
        if opponent_attack_status > 0.6 and distance < close_range:
            return 6
        elif distance > medium_range and my_projectile_cooldown < 0.25:
            if random.random() < 0.7:
                return 9
            else:
                return 6
        elif distance < ultra_close_range and opponent_stunned > 0.3:
            return 4 if random.random() < 0.6 else 5
        else:
            return 6
    
    # Critical health advanced tactics
    if my_health < 0.15:
        if opponent_stunned > 0.4:
            if distance < medium_close_range:
                if distance > ultra_close_range:
                    return 2 if relative_pos > 0 else 1
                else:
                    kill_attempt = random.random()
                    if kill_attempt < 0.5:
                        return 5
                    elif kill_attempt < 0.8:
                        return 4
                    else:
                        return 9 if my_projectile_cooldown < 0.1 else 5
            else:
                return 2 if relative_pos > 0 else 1
        elif distance > far_range:
            if my_projectile_cooldown < 0.15:
                return 9
            elif opponent_approaching:
                return 6
            else:
                return 8 if relative_pos > 0 else 7
        elif distance < point_blank_range and opponent_attack_status < 0.2:
            if random.random() < 0.65:
                return 5
            else:
                return 4
        else:
            if opponent_attack_status > 0.7:
                return 6
            elif distance < medium_range and opponent_block_status < 0.3:
                desperation_roll = random.random()
                if desperation_roll < 0.4:
                    return 5
                elif desperation_roll < 0.7:
                    return 4
                else:
                    return