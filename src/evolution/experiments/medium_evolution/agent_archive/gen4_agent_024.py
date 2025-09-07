"""
Evolutionary Agent: gen4_agent_024
==================================

Metadata:
{
  "generation": 4,
  "fitness": 58.95999999999735,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: f794af80f960ca07
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.3 if len(state) > 5 else False
    my_blocking = state[6] > 0.3 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.3 if len(state) > 16 else False
    opp_blocking = state[17] > 0.3 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Enhanced tactical ranges for balanced fighting
    point_blank = 0.04
    strike_sweet_spot = 0.10
    close_combat = 0.18
    mid_close = 0.26
    medium_range = 0.38
    mid_far = 0.52
    long_range = 0.70
    max_range = 0.85
    
    # Advanced aggression calculation with multiple factors
    base_aggression = 0.65
    health_modifier = health_advantage * 0.25
    distance_modifier = math.sin((1.0 - distance) * math.pi / 2) * 0.15
    momentum_modifier = min(0.1, abs(my_velocity_x) * 0.2)
    current_aggression = max(0.15, min(0.90, base_aggression + health_modifier + distance_modifier + momentum_modifier))
    
    # Movement and prediction analysis
    closing_speed = abs(my_velocity_x + opp_velocity_x) if (my_velocity_x * opp_velocity_x < 0) else 0
    opponent_approach = -opp_velocity_x * relative_pos if relative_pos != 0 else 0
    my_approach = my_velocity_x * relative_pos if relative_pos != 0 else 0
    unpredictability = random.random()
    
    # Combat readiness assessment
    my_ready_to_attack = my_attack_cooldown < 0.12
    my_can_block = my_block_cooldown < 0.08
    my_can_projectile = my_projectile_cooldown < 0.15
    opp_vulnerable = opp_stunned or (opp_attack_cooldown > 0.35 and not opp_blocking)
    opp_dangerous = opp_attacking or (opp_projectile_cooldown < 0.12 and distance > medium_range)
    opp_ready_to_attack = opp_attack_cooldown < 0.15
    
    # Position assessment
    corner_pressure = 0.0
    if my_pos_x < 0.15:
        corner_pressure = -0.2
    elif my_pos_x > 0.85:
        corner_pressure = -0.2
    elif opp_pos_x < 0.15 or opp_pos_x > 0.85:
        corner_pressure = 0.15
    
    # Emergency situations - immediate responses
    if my_stunned:
        if distance < close_combat and opp_attacking:
            return 6 if my_can_block else 3
        elif distance < strike_sweet_spot:
            if my_can_block:
                return 7 if relative_pos > 0 else 8
            else:
                return 3
        else:
            return 6 if my_can_block else 0
    
    # Critical health management
    if my_health < 0.12:
        if health_advantage < -0.6:
            # Desperate situation
            if distance > mid_far and my_can_projectile:
                return 9
            elif distance < strike_sweet_spot and opp_vulnerable and my_ready_to_attack:
                return 5 if unpredictability < 0.4 else 4
            elif opp_attacking and distance < medium_range:
                return 6 if my_can_block else 3
            else:
                if distance > medium_range:
                    return 9 if my_can_projectile else 6
                else:
                    return 1 if relative_pos > 0 else 2
        else:
            # Low health but careful play
            if distance < close_combat and (opp_dangerous or opp_ready_to_attack):
                if my_can_block:
                    return 6
                else:
                    return 3 if distance < point_blank else (1 if relative_pos > 0 else 2)
            elif distance > long_range and my_can_projectile:
                return 9
    
    # Exploit opponent vulnerabilities
    if opp_stunned:
        if distance > mid_close:
            # Rush for punish
            return 2 if relative_pos > 0 else 1
        elif distance > strike_sweet_spot:
            # Position for optimal punish
            return 2 if relative_pos > 0 else 1
        elif my_ready_to_attack:
            # Execute punish based on health advantage
            if health_advantage > 0.3:
                return 5  # High damage when ahead
            elif distance < point_blank:
                return 4  # Safe close range
            else:
                punish_choice = unpredictability
                if punish_choice < 0.5:
                    return 4
                elif punish_choice < 0.8:
                    return 5
                else:
                    return 3  # Jump attack mix-up
        else:
            # Wait for cooldown while positioning
            if distance > point_blank:
                return