"""
Evolutionary Agent: gen3_agent_013
==================================

Metadata:
{
  "generation": 3,
  "fitness": 10.640000000000194,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 80f7a2fa35dde55a
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
    
    # Extract my fighter information with defensive bounds checking
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
    
    # Extract opponent information with defensive bounds checking
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
    
    # Define evolved hybrid tactical ranges
    micro_range = 0.05    # Almost touching
    ultra_close = 0.11    # Minimum combat range
    close_range = 0.17    # Primary melee range
    mid_close = 0.26      # Transition zone
    medium_range = 0.39   # Balanced zone
    mid_far = 0.54        # Projectile preferred
    far_range = 0.72      # Pure projectile zone
    
    # Critical thresholds
    critical_health = 0.22
    low_health = 0.4
    dominant_health = 0.75
    winning_threshold = 0.2
    losing_threshold = -0.2
    desperation_threshold = -0.4
    
    # Positional awareness
    left_edge = 0.12
    right_edge = 0.88
    near_left_edge = my_x_pos < left_edge
    near_right_edge = my_x_pos > right_edge
    is_cornered = near_left_edge or near_right_edge
    
    # Advanced tactical calculations
    velocity_threat = abs(opp_x_velocity) > 0.25
    closing_rapidly = velocity_threat and distance < 0.35
    height_advantage = height_diff > 0.15
    height_disadvantage = height_diff < -0.15
    
    # Dynamic aggression calculation based on multiple factors
    base_aggression = 0.72
    
    # Health-based aggression modifier
    if health_advantage > 0.35:
        health_modifier = 1.4
    elif health_advantage > 0.15:
        health_modifier = 1.2
    elif health_advantage > -0.05:
        health_modifier = 1.0
    elif health_advantage > -0.25:
        health_modifier = 0.75
    else:
        health_modifier = 0.5
    
    # Distance-based aggression modifier
    if distance < close_range:
        distance_modifier = 1.3
    elif distance < medium_range:
        distance_modifier = 1.1
    elif distance < mid_far:
        distance_modifier = 0.9
    else:
        distance_modifier = 0.7
    
    # Opponent state modifier
    if opp_stunned:
        state_modifier = 2.0
    elif opp_blocking:
        state_modifier = 1.1
    elif opp_attacking:
        state_modifier = 0.8
    else:
        state_modifier = 1.0
    
    current_aggression = min(1.5, base_aggression * health_modifier * distance_modifier * state_modifier)
    
    # Emergency stunned state handling
    if my_stunned:
        if opp_attacking and distance < close_range:
            if my_block_cooldown < 0.25:
                return 6
            else:
                return 0
        elif distance > medium_range and my_projectile_cooldown < 0.3:
            return 9
        else:
            return 6
    
    # Critical health survival protocols
    if my_health < critical_health:
        # Last resort offensive when opponent is vulnerable
        if opp_stunned and distance < mid_close:
            if distance > ultra_close:
                return 2 if relative_pos > 0 else 1
            else:
                return 5 if random.random() < 0.8 else 4
        
        # Desperate spacing attempts
        if distance < close_range and opp_attacking:
            if is_cornered:
                return 6 if my_block_cooldown < 0.3 else 0
            else:
                return 7 if relative_pos > 0 else 8
        
        # Long range survival
        if distance > mid_far:
            if my_projectile_cooldown < 0.25:
                return 9
            else:
                return 6
        
        # Medium range evasion
        if distance < medium_range:
            if opp_attacking:
                return 6 if my_block_cooldown < 0.3 else 0
            elif not is_cornered:
                return 1 if relative_pos > 0 else 2
            else:
                return 6
        
        # Default desperate defense
        return 6
    
    # Maximum punishment for stunned opponent
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.15:
                # Optimized punishment sequence
                punish_roll = random.random()
                if distance < micro_range:
                    # Point blank maximum damage
                    if punish_roll < 0.8:
                        return 5  # Heavy damage kick
                    else:
                        return 4  # Quick