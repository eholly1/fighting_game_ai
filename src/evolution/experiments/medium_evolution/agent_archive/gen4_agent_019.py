"""
Evolutionary Agent: gen4_agent_019
==================================

Metadata:
{
  "generation": 4,
  "fitness": -8.839999999999598,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 4e42e3ec16e65a7b
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
    
    # Extract my fighter status with defensive bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(0.0, min(1.0, state[0] if len(state) > 0 else 0.5))
    my_velocity_x = max(-1.0, min(1.0, state[3] if len(state) > 3 else 0.0))
    my_velocity_y = max(-1.0, min(1.0, state[4] if len(state) > 4 else 0.0))
    my_attacking = state[5] > 0.3 if len(state) > 5 else False
    my_blocking = state[6] > 0.3 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, min(1.0, state[8] if len(state) > 8 else 0.0))
    my_attack_cooldown = max(0.0, min(1.0, state[9] if len(state) > 9 else 0.0))
    my_block_cooldown = max(0.0, min(1.0, state[10] if len(state) > 10 else 0.0))
    
    # Extract opponent status with defensive bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = max(0.0, min(1.0, state[11] if len(state) > 11 else 0.5))
    opp_velocity_x = max(-1.0, min(1.0, state[14] if len(state) > 14 else 0.0))
    opp_velocity_y = max(-1.0, min(1.0, state[15] if len(state) > 15 else 0.0))
    opp_attacking = state[16] > 0.3 if len(state) > 16 else False
    opp_blocking = state[17] > 0.3 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, min(1.0, state[19] if len(state) > 19 else 0.0))
    opp_attack_cooldown = max(0.0, min(1.0, state[20] if len(state) > 20 else 0.0))
    opp_block_cooldown = max(0.0, min(1.0, state[21] if len(state) > 21 else 0.0))
    
    # Advanced hybrid tactical ranges for balanced fighting
    point_blank = 0.04
    striking_distance = 0.08
    optimal_close = 0.12
    close_range = 0.18
    close_medium = 0.25
    medium_range = 0.35
    medium_far = 0.45
    far_range = 0.60
    max_range = 0.80
    
    # Enhanced positional awareness
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    opp_wall_proximity = min(opp_pos_x, 1.0 - opp_pos_x)
    corner_pressure = wall_proximity < 0.15
    opponent_cornered = opp_wall_proximity < 0.15
    near_wall = wall_proximity < 0.25
    opponent_near_wall = opp_wall_proximity < 0.25
    
    # Combat readiness assessment
    my_ready_attack = my_attack_cooldown < 0.12
    my_ready_block = my_block_cooldown < 0.08
    my_ready_projectile = my_projectile_cooldown < 0.15
    my_optimal_projectile = my_projectile_cooldown < 0.05
    
    opp_ready_attack = opp_attack_cooldown < 0.12
    opp_ready_block = opp_block_cooldown < 0.08
    opp_ready_projectile = opp_projectile_cooldown < 0.15
    
    # Advanced opponent behavior analysis
    opp_vulnerable = opp_stunned or (opp_attack_cooldown > 0.4 and not opp_blocking)
    opp_dangerous = opp_attacking or (opp_ready_attack and distance < close_range)
    opp_zoning = distance > medium_range and opp_ready_projectile
    opp_aggressive = opp_attacking or (abs(opp_velocity_x) > 0.2 and distance < medium_range)
    opp_retreating = (relative_pos > 0 and opp_velocity_x > 0.15) or (relative_pos < 0 and opp_velocity_x < -0.15)
    opp_advancing = (relative_pos > 0 and opp_velocity_x < -0.15) or (relative_pos < 0 and opp_velocity_x > 0.15)
    opp_defensive = opp_blocking or (opp_ready_block and not opp_attacking)
    
    # Dynamic aggression calculation with hybrid balance
    base_aggression = 0.65
    aggression_modifier = 0.0
    
    # Health-based aggression with nuanced scaling
    if health_advantage > 0.6:
        aggression_modifier += 0.25
    elif health_advantage > 0.3:
        aggression_modifier += 0.15
    elif health_advantage > 0.1:
        aggression_modifier += 0.05
    elif health_advantage < -0.6:
        aggression_modifier -= 0.4
    elif health_advantage < -0.3:
        aggression_modifier -= 0.25
    elif health_advantage < -0.1:
        aggression_modifier -= 0.1
    
    # Position-based adjustments
    if opponent_cornered and not corner_pressure:
        aggression_modifier += 0.2
    elif corner_pressure and not opponent_cornered:
        aggression_modifier -= 0.25
    elif near_wall and not opponent_near_wall:
        aggression_modifier -= 0.1
    
    # Opponent behavior adjustments
    if opp_vulnerable and distance < medium_range:
        aggression_modifier += 0.3
    elif opp_dangerous and my_health < opp_health:
        aggression_modifier -= 0.2
    elif opp_defensive and distance < close_medium:
        aggression_modifier += 0.15
    elif opp_zoning and distance > medium_range:
        aggression_modifier -= 0.1
    
    # Distance-based fine-tuning
    if distance < optimal_close:
        aggression_modifier += 0.1
    elif distance > far_range:
        aggression_modifier -= 0.15
    
    current_aggression = max(0.2, min(0.9, base_aggression + aggression_modifier))
    
    # Randomness for unpredictability
    unpredictability = random.random()