"""
Evolutionary Agent: gen3_agent_008
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 2c1ec2bb500f100c
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
    
    # Extract my fighter state with bounds checking
    my_health = max(0.0, min(1.0, state[1] if state[1] >= 0 else 0.5))
    my_pos_x = max(-1.0, min(1.0, state[2] if abs(state[2]) <= 1.0 else 0.0))
    my_velocity_x = max(-2.0, min(2.0, state[4] if abs(state[4]) <= 2.0 else 0.0))
    my_attack_cooldown = max(0.0, state[7] if state[7] >= 0 else 0.0)
    my_block_status = max(0.0, state[8] if state[8] >= 0 else 0.0)
    my_projectile_cooldown = max(0.0, state[9] if state[9] >= 0 else 0.0)
    
    # Extract opponent fighter state with bounds checking
    opponent_health = max(0.0, min(1.0, state[12] if state[12] >= 0 else 0.5))
    opponent_pos_x = max(-1.0, min(1.0, state[13] if abs(state[13]) <= 1.0 else 0.0))
    opponent_velocity_x = max(-2.0, min(2.0, state[15] if abs(state[15]) <= 2.0 else 0.0))
    opponent_attack_cooldown = max(0.0, state[18] if state[18] >= 0 else 0.0)
    opponent_block_status = max(0.0, state[19] if state[19] >= 0 else 0.0)
    
    # Define adaptive strategic ranges
    very_close_range = 0.08
    close_range = 0.15
    medium_close_range = 0.25
    medium_range = 0.4
    far_range = 0.6
    
    # Health thresholds
    critical_health = 0.2
    low_health = 0.35
    medium_health = 0.6
    good_health = 0.75
    
    # Combat state analysis
    can_attack = my_attack_cooldown < 0.04
    can_projectile = my_projectile_cooldown < 0.04
    am_blocking = my_block_status > 0.05
    
    opponent_attacking = opponent_attack_cooldown > 0.06
    opponent_blocking = opponent_block_status > 0.06
    opponent_vulnerable = opponent_attack_cooldown < 0.03 and opponent_block_status < 0.03
    
    # Movement analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.08) or (relative_pos < 0 and opponent_velocity_x < -0.08)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.08) or (relative_pos < 0 and opponent_velocity_x > 0.08)
    opponent_stationary = abs(opponent_velocity_x) < 0.05
    
    am_moving_toward = (relative_pos > 0 and my_velocity_x > 0.05) or (relative_pos < 0 and my_velocity_x < -0.05)
    am_moving_away = (relative_pos > 0 and my_velocity_x < -0.05) or (relative_pos < 0 and my_velocity_x > 0.05)
    
    # Positional analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    stage_center = abs(my_pos_x) < 0.25
    wall_behind_me = (my_pos_x > 0.8 and relative_pos < 0) or (my_pos_x < -0.8 and relative_pos > 0)
    
    # Range classification
    is_very_close = distance < very_close_range
    is_close = distance < close_range
    is_medium_close = distance < medium_close_range
    is_medium = distance < medium_range
    is_far = distance < far_range
    is_very_far = distance >= far_range
    
    # Health situation analysis
    am_critical = my_health < critical_health
    am_low_health = my_health < low_health
    am_healthy = my_health > medium_health
    am_dominant_health = my_health > good_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    opponent_healthy = opponent_health > medium_health
    
    # Match state analysis
    am_winning_big = health_advantage > 0.4
    am_winning = health_advantage > 0.15
    even_match = abs(health_advantage) <= 0.15
    am_losing = health_advantage < -0.15
    am_losing_big = health_advantage < -0.4
    
    # Hybrid fighting style - adaptive aggression based on situation
    base_aggression = 0.5
    
    # Adjust aggression based on health advantage
    if am_winning_big:
        aggression_modifier = 0.8
    elif am_winning:
        aggression_modifier = 0.65
    elif even_match:
        aggression_modifier = 0.5
    elif am_losing:
        aggression_modifier = 0.35
    else:  # losing big
        aggression_modifier = 0.2
    
    # Adjust aggression based on my health
    if am_critical:
        health_aggression = 0.1
    elif am_low_health:
        health_aggression = 0.3
    elif am_healthy:
        health_aggression = 0.7
    else:
        health_aggression = 0.5
    
    # Adjust aggression based on opponent health
    if opponent_critical:
        opponent_aggression = 0.9
    elif opponent_low:
        opponent_aggression = 0.7
    else:
        opponent_aggression = 0.5
    
    # Calculate final aggression level
    final_aggression = (aggression_modifier + health_aggression + opponent_aggression) / 3.0
    final_aggression = max(0.1, min(0.9, final_aggression))
    
    # Emergency survival mode - top priority
    if am_critical and my_health < 0.15:
        if opponent_attacking and (is_very_close or is_close):
            # Immediate survival response
            if random.random() < 0.9:
                return 6  # Block
            else:
                if wall_behind_me:
                    # Can't retreat, must block
                    return 6
                else:
                    if relative_pos > 0:
                        return 7  # Move left block
                    else:
                        return 8  # Move right block
        
        elif is_very_far and can_projectile:
            return 9  # Safe projectile harassment
        
        elif is_far or is_medium:
            if opponent_approaching and can_projectile and not opponent_blocking:
                return 9  # Slow their approach
            elif opponent_attacking:
                return 6  # Block incoming
            else:
                if can_projectile and not opponent_blocking:
                    return 9