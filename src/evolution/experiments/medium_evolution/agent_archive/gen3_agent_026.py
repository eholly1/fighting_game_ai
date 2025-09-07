"""
Evolutionary Agent: gen3_agent_026
==================================

Metadata:
{
  "generation": 3,
  "fitness": 9.499999999999583,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 39813fb2f04df3bc
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
    my_pos_y = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_pos_y = state[13] if len(state) > 13 else 0.5
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Define evolved hybrid tactical ranges
    point_blank = 0.05
    very_close = 0.11
    close_range = 0.16
    medium_close = 0.23
    medium_range = 0.32
    medium_far = 0.42
    far_range = 0.55
    extreme_range = 0.7
    
    # Advanced state analysis
    health_ratio = my_health / max(opp_health, 0.01)
    position_advantage = abs(my_pos_x - 0.5) < abs(opp_pos_x - 0.5)
    height_advantage = height_diff > 0.1
    velocity_advantage = abs(my_velocity_x) > abs(opp_velocity_x) + 0.02
    
    # Opponent movement patterns
    opp_advancing = (relative_pos > 0 and opp_velocity_x > 0.03) or (relative_pos < 0 and opp_velocity_x < -0.03)
    opp_retreating = (relative_pos > 0 and opp_velocity_x < -0.03) or (relative_pos < 0 and opp_velocity_x > 0.03)
    opp_mobile = abs(opp_velocity_x) > 0.04
    
    # Combat style recognition
    opp_aggressive = opp_attacking and distance < medium_range
    opp_defensive = opp_blocking or (opp_retreating and health_advantage < 0)
    opp_zoner = opp_projectile_cooldown < 0.2 and distance > medium_range
    opp_rusher = opp_advancing and not opp_blocking
    
    # Dynamic aggression calculation
    base_aggression = 0.65
    health_factor = health_advantage * 0.3
    distance_factor = max(0, (medium_range - distance) * 0.5)
    cooldown_factor = -0.2 if my_attack_cooldown > 0.3 else 0.1
    momentum_factor = 0.15 if velocity_advantage else -0.1
    
    current_aggression = max(0.2, min(0.9, base_aggression + health_factor + distance_factor + cooldown_factor + momentum_factor))
    
    # Tactical mode determination
    if health_advantage > 0.5:
        mode = "dominating"
    elif health_advantage > 0.2:
        mode = "winning"
    elif health_advantage > -0.2:
        mode = "balanced"
    elif health_advantage > -0.5:
        mode = "losing"
    else:
        mode = "critical"
    
    # Emergency protocols
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6  # Emergency block
        elif distance < very_close:
            return 1 if relative_pos > 0 else 2  # Escape movement
        else:
            return 6 if my_block_cooldown < 0.2 else 0
    
    # Critical health management
    if my_health < 0.15:
        if mode == "critical":
            if distance > medium_range and my_projectile_cooldown < 0.15:
                return 9  # Desperate zoning
            elif distance < very_close and not opp_attacking and my_attack_cooldown < 0.1:
                return 5 if random.random() < 0.6 else 4  # Last stand attack
            else:
                return 6  # Defensive stance
    
    # Opportunity exploitation
    if opp_stunned:
        if distance > medium_range:
            return 2 if relative_pos > 0 else 1  # Close distance
        elif distance > close_range:
            if my_projectile_cooldown < 0.1:
                return 9  # Safe projectile punish
            else:
                return 2 if relative_pos > 0 else 1  # Move in for melee
        elif my_attack_cooldown < 0.1:
            punish_roll = random.random()
            if punish_roll < 0.5:
                return 5  # Heavy punish
            elif punish_roll < 0.8:
                return 4  # Quick punish
            else:
                return 3  # Jump punish
        else:
            return 0  # Wait for cooldown
    
    # Finishing opportunities
    if opp_health < 0.12 and health_advantage > 0.3:
        if distance < medium_close:
            if my_attack_cooldown < 0.15:
                return 5 if random.random() < 0.7 else 4  # Go for finish
            else:
                return 2