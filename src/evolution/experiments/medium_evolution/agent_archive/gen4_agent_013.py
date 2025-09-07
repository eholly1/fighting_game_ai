"""
Evolutionary Agent: gen4_agent_013
==================================

Metadata:
{
  "generation": 4,
  "fitness": -2.1999999999998794,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 46aa0f844e58c580
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
    
    # Extract my fighter status with comprehensive bounds checking
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
    
    # Extract opponent status with comprehensive bounds checking
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
    
    # Evolved tactical ranges with optimized spacing
    instant_range = 0.02
    melee_range = 0.08
    striking_range = 0.14
    close_combat = 0.22
    mid_close = 0.30
    medium_range = 0.42
    mid_far = 0.58
    long_range = 0.75
    max_range = 0.90
    
    # Enhanced situational analysis
    wall_distance = min(my_pos_x, 1.0 - my_pos_x)
    opp_wall_distance = min(opp_pos_x, 1.0 - opp_pos_x)
    i_am_cornered = wall_distance < 0.10
    opponent_cornered = opp_wall_distance < 0.10
    i_am_near_wall = wall_distance < 0.20
    opponent_near_wall = opp_wall_distance < 0.20
    
    # Advanced combat state analysis
    my_ready_attack = my_attack_cooldown < 0.12
    my_ready_block = my_block_cooldown < 0.08
    my_ready_projectile = my_projectile_cooldown < 0.25
    opp_ready_attack = opp_attack_cooldown < 0.12
    opp_ready_projectile = opp_projectile_cooldown < 0.25
    
    # Opponent behavioral pattern analysis
    opp_aggressive = opp_attacking or (abs(opp_velocity_x) > 0.15 and distance < medium_range)
    opp_very_aggressive = opp_attacking and abs(opp_velocity_x) > 0.20
    opp_defensive = opp_blocking or (abs(opp_velocity_x) < 0.05 and distance > close_combat)
    opp_mobile = abs(opp_velocity_x) > 0.12
    opp_approaching = (relative_pos > 0 and opp_velocity_x > 0.08) or (relative_pos < 0 and opp_velocity_x < -0.08)
    opp_retreating = (relative_pos > 0 and opp_velocity_x < -0.08) or (relative_pos < 0 and opp_velocity_x > 0.08)
    
    # Calculate momentum and pressure dynamics
    health_ratio = my_health / max(0.1, opp_health)
    momentum_score = 0.0
    
    # Health-based momentum
    if health_advantage > 0.25:
        momentum_score += 0.35
    elif health_advantage > 0.10:
        momentum_score += 0.15
    elif health_advantage < -0.25:
        momentum_score -= 0.35
    elif health_advantage < -0.10:
        momentum_score -= 0.15
    
    # Position-based momentum
    if opponent_cornered and not i_am_cornered:
        momentum_score += 0.30
    elif i_am_cornered and not opponent_cornered:
        momentum_score -= 0.30
    elif opponent_near_wall and not i_am_near_wall:
        momentum_score += 0.15
    elif i_am_near_wall and not opponent_near_wall:
        momentum_score -= 0.15
    
    # State-based momentum
    if opp_stunned:
        momentum_score += 0.40
    elif my_stunned:
        momentum_score -= 0.40
    
    if opp_defensive and not opp_mobile:
        momentum_score += 0.20
    elif opp_very_aggressive and health_advantage < 0:
        momentum_score -= 0.25
    
    # Dynamic aggression calculation with momentum integration
    base_aggression = 0.60  # Balanced hybrid baseline
    momentum_modifier = momentum_score * 0.5
    
    # Distance-based aggression fine-tuning
    distance_modifier = 0.0
    if distance < striking_range:
        distance_modifier = 0.15
    elif distance < close_combat:
        distance_modifier = 0.10
    elif distance > mid_far:
        distance_modifier = -0.10
    
    # Health ratio fine-tuning
    health_modifier = 0.0
    if health_ratio > 1.3:
        health_modifier = 0.15
    elif health_ratio < 0.7:
        health_modifier = -0.20
    
    current_