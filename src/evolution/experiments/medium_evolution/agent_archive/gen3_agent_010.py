"""
Evolutionary Agent: gen3_agent_010
==================================

Metadata:
{
  "generation": 3,
  "fitness": 28.359999999998884,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 744ba8ab011086c2
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
    
    # Hybrid fighter tactical ranges
    ultra_close_range = 0.08
    close_range = 0.14
    medium_range = 0.28
    far_range = 0.45
    max_range = 0.65
    
    # Advanced positioning analysis
    stage_center = 0.5
    left_edge = 0.12
    right_edge = 0.88
    corner_buffer = 0.18
    
    is_near_left_edge = my_x_pos < left_edge
    is_near_right_edge = my_x_pos > right_edge
    is_cornered = is_near_left_edge or is_near_right_edge
    opp_cornered = opp_x_pos < left_edge or opp_x_pos > right_edge
    
    # Cooldown readiness checks
    projectile_ready = my_projectile_cooldown < 0.15
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.18
    
    # Opponent threat assessment
    opp_projectile_ready = opp_projectile_cooldown < 0.18
    opp_attack_ready = opp_attack_cooldown < 0.15
    immediate_threat = opp_attacking and distance < close_range
    incoming_projectile = opp_projectile_ready and distance > medium_range
    
    # Movement pattern analysis
    opponent_advancing = (relative_pos > 0 and opp_x_velocity > 0.2) or (relative_pos < 0 and opp_x_velocity < -0.2)
    opponent_retreating = (relative_pos > 0 and opp_x_velocity < -0.2) or (relative_pos < 0 and opp_x_velocity > 0.2)
    opponent_stationary = abs(opp_x_velocity) < 0.15
    
    # Health-based strategy modifiers
    critical_health = 0.18
    low_health = 0.35
    winning_margin = 0.25
    losing_margin = -0.25
    
    # Aggression calculation based on health and position
    base_aggression = 0.75
    if health_advantage > winning_margin:
        aggression_level = 0.85
    elif health_advantage < losing_margin:
        aggression_level = 0.45
    else:
        aggression_level = base_aggression
    
    # Defensive zone adjustment
    if my_health < critical_health:
        aggression_level *= 0.3
    elif my_health < low_health:
        aggression_level *= 0.6
    
    # Cannot act while stunned
    if my_stunned:
        return 0
    
    # Critical health survival mode
    if my_health <= critical_health:
        if immediate_threat and block_ready:
            return 6  # Emergency block
        
        if distance < close_range:
            if is_cornered:
                if height_diff > -0.2 and my_y_velocity < 0.1:
                    return 3  # Jump escape from corner
                elif block_ready:
                    return 6  # Block in corner
                else:
                    return 0  # Wait for recovery
            else:
                # Escape from close range
                if relative_pos > 0 and not is_near_left_edge:
                    return 7  # Retreat left with block
                elif not is_near_right_edge:
                    return 8  # Retreat right with block
                else:
                    return 6 if block_ready else 0
        
        elif distance < medium_range:
            if projectile_ready and not incoming_projectile:
                return 9  # Chip damage projectile
            elif relative_pos > 0 and not is_near_left_edge:
                return 1  # Create distance left
            elif not is_near_right_edge:
                return 2  # Create distance right
            else:
                return 6 if block_ready else 0
        
        else:
            # Safe distance - chip and survive
            if projectile_ready and not opp_blocking:
                return 9
            else:
                return 0  # Wait safely
    
    # Maximum punishment when opponent is stunned
    if opp_stunned:
        if distance <= ultra_close_range:
            if attack_ready:
                # Optimized stun combo
                combo_choice = random.random()
                if combo_choice < 0.4:
                    return 5  # Heavy kick for max damage
                elif combo_choice < 0.8:
                    return 4  # Quick punch to extend stun
                else:
                    return 5  # Another heavy
            else:
                return 0  # Wait for attack cooldown