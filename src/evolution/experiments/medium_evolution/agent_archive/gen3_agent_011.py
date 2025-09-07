"""
Evolutionary Agent: gen3_agent_011
==================================

Metadata:
{
  "generation": 3,
  "fitness": 12.400000000000006,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: a52d47649f1e3a36
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
    
    # Advanced tactical range definitions
    danger_zone = 0.08
    close_range = 0.15
    mid_close_range = 0.22
    medium_range = 0.32
    ideal_range = 0.45
    far_range = 0.65
    
    # Hybrid fighter parameters - evolved balance
    base_aggression = 0.72
    balance_factor = 0.58
    counter_window = 0.18
    defensive_priority = 0.62
    
    # Stage positioning analysis
    stage_center = 0.5
    left_wall = 0.1
    right_wall = 0.9
    corner_threshold = 0.2
    
    my_near_left = my_x_pos < left_wall + corner_threshold
    my_near_right = my_x_pos > right_wall - corner_threshold
    opp_near_left = opp_x_pos < left_wall + corner_threshold
    opp_near_right = opp_x_pos > right_wall - corner_threshold
    
    im_cornered = my_near_left or my_near_right
    opp_cornered = opp_near_left or opp_near_right
    
    # Enhanced status calculations
    projectile_ready = my_projectile_cooldown < 0.08
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.15
    
    opp_projectile_threat = opp_projectile_cooldown < 0.1
    opp_attack_threat = opp_attack_cooldown < 0.15
    
    # Movement pattern recognition
    opp_closing = (relative_pos > 0 and opp_x_velocity < -0.2) or (relative_pos < 0 and opp_x_velocity > 0.2)
    opp_retreating = (relative_pos > 0 and opp_x_velocity > 0.2) or (relative_pos < 0 and opp_x_velocity < -0.2)
    opp_jumping = abs(height_diff) > 0.15
    
    # Health-based strategic adaptation
    critical_health = my_health < 0.15
    low_health = my_health < 0.35
    winning_big = health_advantage > 0.4
    losing_bad = health_advantage < -0.4
    
    # Dynamic aggression calculation
    current_aggression = base_aggression
    if winning_big:
        current_aggression = min(0.95, base_aggression + 0.25)
    elif losing_bad:
        current_aggression = max(0.4, base_aggression - 0.35)
    elif low_health:
        current_aggression = max(0.45, base_aggression - 0.27)
    
    # Emergency responses
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health survival protocol
    if critical_health:
        if opp_attacking and distance < close_range:
            if block_ready:
                return 6  # Emergency block
            else:
                return 0  # Wait for recovery
        
        if distance < danger_zone:
            # Desperate escape
            if im_cornered:
                if abs(height_diff) < 0.2:
                    return 3  # Jump escape attempt
                else:
                    return 6  # Corner block
            else:
                # Mobile escape with blocking
                if relative_pos > 0 and not my_near_left:
                    return 7  # Block retreat left
                elif not my_near_right:
                    return 8  # Block retreat right
                else:
                    return 6  # Standard block
        
        elif distance < medium_range:
            # Create safe distance
            if projectile_ready and distance > close_range:
                return 9  # Desperation projectile
            else:
                # Move to safety
                if relative_pos > 0 and not my_near_left:
                    return 1  # Move away left
                elif not my_near_right:
                    return 2  # Move away right
                else:
                    return 6  # Block if trapped
        
        else:
            # Safe range behavior
            if projectile_ready:
                return 9  # Chip damage attempt
            else:
                return 0  # Wait safely
    
    # Maximum punishment for stunned opponent
    if opp_stunned:
        if distance < close_range:
            if attack_ready:
                # Optimized stun combo
                combo_choice = random.random()
                if distance < danger_zone:
                    if combo_choice < 0.4:
                        return 5  # Heavy damage up close
                    else:
                        return 4