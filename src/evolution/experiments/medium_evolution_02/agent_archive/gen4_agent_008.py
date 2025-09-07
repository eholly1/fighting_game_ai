"""
Evolutionary Agent: gen4_agent_008
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 4f527d181de300e4
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
    
    # Extract detailed fighter status with bounds checking
    my_pos_x = max(-1.0, min(1.0, state[0])) if len(state) > 0 else 0.0
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_velocity_x = max(-2.0, min(2.0, state[3])) if len(state) > 3 else 0.0
    my_velocity_y = max(-2.0, min(2.0, state[4])) if len(state) > 4 else 0.0
    my_block_status = max(0.0, min(1.0, state[5])) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, min(1.0, state[6])) if len(state) > 6 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_projectile_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    opponent_pos_x = max(-1.0, min(1.0, state[11])) if len(state) > 11 else 0.0
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_velocity_x = max(-2.0, min(2.0, state[14])) if len(state) > 14 else 0.0
    opponent_velocity_y = max(-2.0, min(2.0, state[15])) if len(state) > 15 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[17])) if len(state) > 17 else 0.0
    opponent_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opponent_projectile_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Enhanced tactical range definitions
    ultra_close = 0.08
    close_range = 0.16
    medium_range = 0.35
    far_range = 0.55
    max_range = 0.8
    
    # Dynamic health thresholds
    critical_health = 0.2
    low_health = 0.4
    moderate_health = 0.6
    good_health = 0.8
    
    # Situation analysis
    is_ultra_close = distance < ultra_close
    is_close = ultra_close <= distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health status assessment
    am_critical = my_health < critical_health
    am_low_health = my_health < low_health
    am_healthy = my_health > moderate_health
    am_winning_big = health_advantage > 0.4
    am_losing_bad = health_advantage < -0.4
    am_winning = health_advantage > 0.15
    am_losing = health_advantage < -0.15
    
    # Opponent analysis
    opponent_attacking = opponent_attack_status > 0.5 or opponent_attack_cooldown > 0.1
    opponent_blocking = opponent_block_status > 0.3
    opponent_vulnerable = opponent_attack_cooldown < 0.05 and opponent_block_status < 0.2
    opponent_critical = opponent_health < critical_health
    opponent_moving_fast = abs(opponent_velocity_x) > 0.3
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    
    # My capabilities
    can_attack = my_attack_cooldown < 0.08
    can_projectile = my_projectile_cooldown < 0.08
    am_blocking = my_block_status > 0.3
    am_attacking = my_attack_status > 0.5
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    
    # Advanced threat calculation
    immediate_threat = 0.0
    if opponent_attacking and (is_ultra_close or is_close):
        immediate_threat += 0.5
    if opponent_approaching and distance < medium_range:
        immediate_threat += 0.3
    if opponent_moving_fast and distance < close_range:
        immediate_threat += 0.2
    if opponent_attack_cooldown > 0.1 and distance < close_range:
        immediate_threat += 0.3
    
    # Momentum tracking
    offensive_momentum = 0.0
    defensive_momentum = 0.0
    
    if health_advantage > 0.1:
        offensive_momentum += 0.3
    if opponent_vulnerable:
        offensive_momentum += 0.4
    if can_attack and distance < medium_range:
        offensive_momentum += 0.3
    
    if immediate_threat > 0.4:
        defensive_momentum += 0.5
    if am_low_health:
        defensive_momentum += 0.4
    if opponent_attacking:
        defensive_momentum += 0.3
    
    # Crisis management - survival first
    if am_critical and immediate_threat > 0.6:
        if is_ultra_close or is_close:
            if not am_blocking:
                return 6  # Emergency block
            elif am_cornered:
                if relative_pos > 0:
                    return 8  # Escape right while blocking
                else:
                    return 7  # Escape left while blocking
            else:
                if my_pos_x < 0:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
        elif is_medium:
            if opponent_approaching:
                if relative_pos > 0:
                    return 7  # Retreat left blocking
                else:
                    return 8  # Retreat right blocking
            else:
                return 6  # Defensive block
        else:
            if can_projectile and not opponent_blocking:
                return 9  # Desperate projectile
            else:
                return 6  # Wait defensively
    
    # Advanced counter-opportunity detection
    if (opponent_attack_status > 0.7 and am_blocking and 
        distance < close_range and can_attack):
        counter_probability = 0.45
        if am_winning:
            counter_probability = 0.65
        elif am_losing_bad:
            counter_probability = 0.25
        
        if random.random() < counter_probability:
            if opponent_critical:
                return