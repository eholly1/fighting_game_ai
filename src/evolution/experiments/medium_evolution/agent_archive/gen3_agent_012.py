"""
Evolutionary Agent: gen3_agent_012
==================================

Metadata:
{
  "generation": 3,
  "fitness": -22.639999999999866,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 8e8827106254e6df
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
    
    # Extract my fighter information with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_block_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information with bounds checking
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_block_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Enhanced balanced fighter parameters
    close_range = 0.11
    medium_range = 0.28
    far_range = 0.45
    optimal_close = 0.08
    optimal_medium = 0.35
    critical_health = 0.18
    low_health = 0.35
    winning_threshold = 0.25
    decisive_advantage = 0.4
    
    # Advanced stage positioning
    stage_center = 0.5
    left_danger = 0.12
    right_danger = 0.88
    left_wall = 0.18
    right_wall = 0.82
    is_near_left_wall = my_x_pos < left_wall
    is_near_right_wall = my_x_pos > right_wall
    is_cornered = my_x_pos < left_danger or my_x_pos > right_danger
    opp_cornered = opp_x_pos < left_danger or opp_x_pos > right_danger
    center_control = abs(my_x_pos - stage_center) < 0.25
    
    # Enhanced movement and timing analysis
    opponent_advancing = (relative_pos > 0 and opp_x_velocity < -0.15) or (relative_pos < 0 and opp_x_velocity > 0.15)
    opponent_retreating = (relative_pos > 0 and opp_x_velocity > 0.2) or (relative_pos < 0 and opp_x_velocity < -0.2)
    opponent_closing_fast = opponent_advancing and abs(opp_x_velocity) > 0.3
    projectile_ready = my_projectile_cooldown < 0.08
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.1
    can_counter = attack_ready and not my_attacking
    
    # Opponent threat analysis
    opp_projectile_threat = opp_projectile_cooldown < 0.1 and distance > medium_range
    opp_attack_threat = opp_attack_cooldown < 0.12 and distance < medium_range
    opp_combo_threat = opp_attacking and opp_attack_cooldown < 0.05
    immediate_danger = (opp_attacking or opp_attack_threat) and distance < close_range
    projectile_incoming = opp_projectile_threat and distance > 0.3
    
    # Adaptive aggression based on performance
    base_aggression = 0.6
    health_factor = (my_health - opp_health) * 0.3
    position_factor = 0.2 if center_control else -0.1 if is_cornered else 0.0
    range_factor = 0.15 if distance < optimal_close or (distance > 0.25 and distance < optimal_medium) else -0.1
    aggression_level = max(0.2, min(0.9, base_aggression + health_factor + position_factor + range_factor))
    
    # Emergency responses
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health - enhanced survival tactics
    if my_health <= critical_health:
        if immediate_danger:
            if block_ready:
                if is_cornered:
                    return 6  # Block in place
                else:
                    # Escape block
                    if relative_pos > 0 and not is_near_left_wall:
                        return 7  # Block retreat left
                    elif not is_near_right_wall:
                        return 8  # Block retreat right
                    else:
                        return 6  # Standard block
            else:
                return 0  # Wait for block recovery
        
        if distance < close_range:
            # Emergency escape tactics
            if is_cornered:
                if height_diff > -0.2 and abs(my_y_velocity) < 0.1:
                    return 3  # Jump escape attempt
                elif block_ready:
                    return 6  # Defensive block
                else:
                    return 0  # Wait
            else:
                # Mobile escape
                escape_direction = 1 if relative_pos > 0 and not is_near_left_wall else 2
                if block_ready and (opp_attack_threat or opp_attacking):
                    return 7 if escape_direction == 1 else 8  # Block while escaping
                else:
                    return escape_direction  # Quick escape
        
        elif distance < medium_range:
            # Create distance while looking for opportunities
            if projectile_ready and not opp_blocking:
                return 9  # Safe projectile
            elif relative_pos > 0 and not is_near_left_wall:
                return 1