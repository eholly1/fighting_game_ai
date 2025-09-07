"""
Evolutionary Agent: gen4_agent_021
==================================

Metadata:
{
  "generation": 4,
  "fitness": -2.079999999999849,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: bc28856b8d9d062b
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
    
    # Enhanced tactical ranges for evolved balanced fighting
    point_blank = 0.06
    melee_optimal = 0.10
    striking_range = 0.16
    close_combat = 0.25
    mid_close = 0.35
    medium_range = 0.50
    mid_far = 0.65
    long_range = 0.80
    
    # Advanced aggression system with momentum consideration
    base_aggression = 0.65
    health_modifier = health_advantage * 0.35
    momentum_modifier = min(0.2, abs(my_velocity_x) * 0.4)
    pressure_modifier = (1.0 - distance) * 0.25
    opponent_weakness = (opp_attack_cooldown + opp_block_cooldown) * 0.15
    
    dynamic_aggression = max(0.15, min(0.92, 
        base_aggression + health_modifier + momentum_modifier + 
        pressure_modifier + opponent_weakness))
    
    # Situational awareness variables
    approaching_enemy = (relative_pos > 0 and my_velocity_x > 0.1) or (relative_pos < 0 and my_velocity_x < -0.1)
    retreating = (relative_pos > 0 and my_velocity_x < -0.1) or (relative_pos < 0 and my_velocity_x > 0.1)
    airborne = abs(my_velocity_y) > 0.2
    opp_airborne = abs(opp_velocity_y) > 0.2
    
    # Enhanced readiness calculations
    my_ready_to_attack = my_attack_cooldown < 0.12
    my_can_block_effective = my_block_cooldown < 0.08
    my_projectile_ready = my_projectile_cooldown < 0.15
    
    opp_vulnerable_window = opp_stunned or (opp_attack_cooldown > 0.35 and not opp_blocking)
    opp_immediate_threat = opp_attacking or (distance < striking_range and opp_ready_to_attack)
    opp_ready_to_attack = opp_attack_cooldown < 0.12
    opp_projectile_threat = opp_projectile_cooldown < 0.15 and distance > medium_range
    
    # Unpredictability with weighted randomness
    chaos_factor = random.random()
    tactical_variance = random.uniform(0.85, 1.15)
    
    # Emergency handling - absolute priority
    if my_stunned:
        if distance < close_combat:
            if opp_attacking and my_can_block_effective:
                return 6
            elif distance < point_blank:
                # Escape desperate situation
                escape_direction = 1 if relative_pos > 0 else 2
                if my_can_block_effective and chaos_factor < 0.3:
                    return 7 if relative_pos > 0 else 8
                return escape_direction
            else:
                return 6 if my_can_block_effective else 0
        else:
            # Recover at distance
            if my_projectile_ready and distance > mid_far:
                return 9
            return 6 if my_can_block_effective else 0
    
    # Critical health management
    if my_health < 0.20:
        if health_advantage < -0.4:
            # Desperate scenarios - high risk/reward
            if distance > medium_range:
                if my_projectile_ready:
                    return 9
                else:
                    # Approach carefully
                    return 2 if relative_pos > 0 else 1
            elif distance < melee_optimal and opp_vulnerable_window and my_ready_to_attack:
                # All-in desperation with smarter timing
                if opp_health < 0.25:
                    return 5  # Go for knockout
                elif chaos_factor < 0.65:
                    return 4  # Safer option
                else:
                    return 5  # Risk for reward
            else:
                # Ultra-defensive positioning
                if opp_immediate_threat and my_can_block_effective:
                    return 6
                elif distance < striking_range:
                    return 7 if relative_pos > 0 else 8
                else:
                    return 6 if my_can_block_effective else 0
        else:
            # Conservative play when low but competitive
            if distance < close_combat and opp_immediate_threat:
                if my_can_block_effective:
                    return 6
                else:
                    return 1 if relative_pos > 0 else 2
            elif distance > mid_far and my_projectile_ready:
                return 9
    
    # Exploit opponent vulnerabilities - enhanced timing
    if opp_stunned:
        if distance > striking_range and distance < medium_range:
            # Rush in for optimal punish
            return 2