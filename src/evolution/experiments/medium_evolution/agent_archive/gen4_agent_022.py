"""
Evolutionary Agent: gen4_agent_022
==================================

Metadata:
{
  "generation": 4,
  "fitness": -1.2799999999996685,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 167650b50a64abf7
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
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_pos_x = max(0.0, min(1.0, state[0])) if len(state) > 0 else 0.5
    my_pos_y = state[2] if len(state) > 2 else 0.0
    my_velocity_x = max(-1.0, min(1.0, state[3])) if len(state) > 3 else 0.0
    my_velocity_y = max(-1.0, min(1.0, state[4])) if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.4 if len(state) > 5 else False
    my_blocking = state[6] > 0.4 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_attack_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_block_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_projectile_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opp_pos_x = max(0.0, min(1.0, state[11])) if len(state) > 11 else 0.5
    opp_pos_y = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = max(-1.0, min(1.0, state[14])) if len(state) > 14 else 0.0
    opp_velocity_y = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.4 if len(state) > 16 else False
    opp_blocking = state[17] > 0.4 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_attack_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_block_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_projectile_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Define evolved tactical ranges for hybrid fighting
    point_blank = 0.05
    ultra_close = 0.10
    close_range = 0.18
    mid_close = 0.28
    medium_range = 0.42
    mid_far = 0.58
    far_range = 0.75
    
    # Enhanced positioning analysis
    left_wall = 0.15
    right_wall = 0.85
    center_zone = 0.5
    corner_danger_zone = 0.2
    
    my_cornered = my_pos_x < left_wall or my_pos_x > right_wall
    opp_cornered = opp_pos_x < left_wall or opp_pos_x > right_wall
    near_wall = my_pos_x < corner_danger_zone or my_pos_x > (1.0 - corner_danger_zone)
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    
    # Cooldown and readiness assessment
    can_attack = my_attack_cooldown < 0.2
    can_block = my_block_cooldown < 0.25
    can_projectile = my_projectile_cooldown < 0.3
    
    opp_can_attack = opp_attack_cooldown < 0.25
    opp_can_projectile = opp_projectile_cooldown < 0.35
    
    # Advanced threat detection
    immediate_danger = opp_attacking and distance < close_range
    projectile_threat = opp_can_projectile and distance > medium_range and not opp_blocking
    combo_threat = opp_attacking and my_attacking and distance < ultra_close
    
    # Movement pattern recognition
    opp_advancing = (relative_pos > 0 and opp_velocity_x > 0.15) or (relative_pos < 0 and opp_velocity_x < -0.15)
    opp_retreating = (relative_pos > 0 and opp_velocity_x < -0.15) or (relative_pos < 0 and opp_velocity_x > 0.15)
    opp_circling = abs(opp_velocity_x) > 0.25 and not opp_advancing and not opp_retreating
    opp_aggressive = opp_attacking or opp_advancing or abs(opp_velocity_x) > 0.3
    opp_defensive = opp_blocking or opp_retreating
    
    # Health thresholds for strategy adaptation
    critical_health = 0.15
    low_health = 0.35
    good_health = 0.65
    dominant_health = 0.85
    
    # Dynamic aggression calculation based on multiple factors
    base_aggression = 0.65  # Hybrid baseline
    
    # Health-based aggression modifier
    health_ratio = my_health / max(0.1, opp_health)
    if health_ratio > 1.8:
        aggression_mod = 0.25
    elif health_ratio > 1.3:
        aggression_mod = 0.15
    elif health_ratio < 0.5:
        aggression_mod = -0.35
    elif health_ratio < 0.7:
        aggression_mod = -0.20
    else:
        aggression_mod = 0.0
    
    # Position-based aggression modifier
    if opp_cornered and not my_cornered:
        aggression_mod += 0.20
    elif my_cornered and not opp_cornered:
        aggression_mod -= 0.25
    elif near_wall:
        aggression_mod -= 0.10
    
    # Distance-based fine tuning
    if distance < close_range:
        aggression_mod += 0.10
    elif distance > medium_range:
        aggression_mod -= 0.05
    
    current_aggression = max(0.2, min(0.9, base_aggression + aggression_mod))
    
    # Cannot act while stunned - wait for recovery
    if my_stunned:
        return 0
    
    # Crisis management - critical health protocols
    if my_health <= critical_health:
        if immediate_danger and can_block:
            return 6
        
        if distance < ultra_close:
            if my_cornered:
                if abs(height_diff) < 0.3 and my_velocity_y > -0.2:
                    return