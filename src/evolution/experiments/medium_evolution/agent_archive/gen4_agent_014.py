"""
Evolutionary Agent: gen4_agent_014
==================================

Metadata:
{
  "generation": 4,
  "fitness": -17.2599999999997,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: a129171d2da0e240
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information with defensive bounds
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract comprehensive fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_pos_y = state[2] if len(state) > 2 else 0.5
    my_vel_x = state[3] if len(state) > 3 else 0.0
    my_vel_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.4 if len(state) > 5 else False
    my_blocking = state[6] > 0.4 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_proj_cd = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_att_cd = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cd = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_pos_y = state[13] if len(state) > 13 else 0.5
    opp_vel_x = state[14] if len(state) > 14 else 0.0
    opp_vel_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.4 if len(state) > 16 else False
    opp_blocking = state[17] > 0.4 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_proj_cd = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_att_cd = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cd = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Evolved hybrid tactical ranges - more refined spacing
    ultra_close = 0.04
    point_blank = 0.08
    striking_distance = 0.14
    close_combat = 0.22
    mid_close = 0.32
    medium_range = 0.42
    mid_far = 0.52
    long_range = 0.68
    max_range = 0.85
    
    # Advanced readiness calculations
    my_ready_strike = my_att_cd < 0.12
    my_can_block = my_block_cd < 0.08
    my_proj_ready = my_proj_cd < 0.15
    opp_ready_strike = opp_att_cd < 0.12
    opp_can_block = opp_block_cd < 0.08
    opp_proj_ready = opp_proj_cd < 0.15
    
    # Enhanced vulnerability assessment
    opp_vulnerable = opp_stunned or (opp_att_cd > 0.5 and not opp_blocking)
    opp_dangerous = opp_attacking or (opp_ready_strike and distance < striking_distance)
    opp_zoning = opp_proj_ready and distance > medium_range
    
    # Dynamic aggression system based on multiple factors
    base_aggression = 0.72
    health_factor = health_advantage * 0.35
    distance_factor = (1.0 - distance) * 0.15
    momentum_factor = min(0.2, abs(my_vel_x) * 0.25)
    
    current_aggression = max(0.25, min(0.95, 
        base_aggression + health_factor + distance_factor + momentum_factor))
    
    # Adaptive fighting modes
    if health_advantage > 0.5:
        fight_mode = "dominating"
        aggression_mult = 1.2
    elif health_advantage > 0.2:
        fight_mode = "winning"
        aggression_mult = 1.1
    elif health_advantage > -0.1:
        fight_mode = "balanced"
        aggression_mult = 1.0
    elif health_advantage > -0.4:
        fight_mode = "behind"
        aggression_mult = 0.8
    else:
        fight_mode = "critical"
        aggression_mult = 0.6
    
    effective_aggression = current_aggression * aggression_mult
    
    # Momentum and prediction calculations
    relative_velocity = my_vel_x - opp_vel_x
    approach_rate = -relative_velocity * relative_pos if relative_pos != 0 else 0
    combined_speed = abs(my_vel_x) + abs(opp_vel_x)
    
    # Randomization for unpredictability
    tactical_random = random.random()
    micro_random = random.random()
    
    # EMERGENCY RESPONSES - Highest Priority
    if my_stunned:
        if distance < close_combat and opp_dangerous:
            if my_can_block:
                return 6
            elif distance > point_blank:
                return 1 if relative_pos > 0 else 2
            else:
                return 3  # Jump escape
        elif distance < striking_distance:
            if my_can_block:
                return 7 if relative_pos > 0 else 8  # Block and reposition
            else:
                return 1 if relative_pos > 0 else 2  # Escape movement
        else:
            return 6 if my_can_block else 0
    
    # CRITICAL HEALTH SCENARIOS
    if my_health < 0.18:
        if fight_mode == "critical":
            if distance > mid_far:
                # Desperate long range play
                if my_proj_ready:
                    return 9
                elif opp_zoning:
                    return 6  # Defensive block
                else:
                    return 2 if relative_pos > 0 else 1  # Careful approach
            elif distance < point_blank and opp_vulnerable and my_ready_strike:
                # All-in desperation - go for kill
                return 5 if tactical_random < 0.7 else 4
            else:
                # Ultra defensive when critical
                if my_can_block and opp_dangerous:
                    return 6
                elif distance > medium_range:
                    if my_proj_ready:
                        return 9
                    else:
                        return 6
                else:
                    return 1 if relative_pos > 0 else 2
    
    # EXPLOIT OPPONENT VULNERABILITIES - High Priority  
    if opp_stunned:
        if distance > close_combat:
            # Rush in for maximum punish
            return