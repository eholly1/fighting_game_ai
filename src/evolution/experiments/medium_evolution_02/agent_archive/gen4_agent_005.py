"""
Evolutionary Agent: gen4_agent_005
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: f3dee504dd400944
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
    
    # Define tactical ranges with improved thresholds
    very_close_range = 0.06
    close_range = 0.14
    medium_close_range = 0.28
    medium_range = 0.45
    far_range = 0.65
    
    # Health situation thresholds
    critical_health = 0.18
    low_health = 0.32
    medium_health = 0.55
    good_health = 0.72
    excellent_health = 0.85
    
    # Combat state analysis with refined timing
    can_attack = my_attack_cooldown < 0.03
    can_projectile = my_projectile_cooldown < 0.03
    am_blocking = my_block_status > 0.04
    
    opponent_attacking = opponent_attack_cooldown > 0.05
    opponent_blocking = opponent_block_status > 0.05
    opponent_vulnerable = opponent_attack_cooldown < 0.02 and opponent_block_status < 0.02
    opponent_recovering = opponent_attack_cooldown > 0.15
    
    # Enhanced movement analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.06) or (relative_pos < 0 and opponent_velocity_x < -0.06)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.06) or (relative_pos < 0 and opponent_velocity_x > 0.06)
    opponent_stationary = abs(opponent_velocity_x) < 0.04
    opponent_aggressive_approach = abs(opponent_velocity_x) > 0.12 and opponent_approaching
    
    am_moving_toward = (relative_pos > 0 and my_velocity_x > 0.04) or (relative_pos < 0 and my_velocity_x < -0.04)
    am_moving_away = (relative_pos > 0 and my_velocity_x < -0.04) or (relative_pos < 0 and my_velocity_x > 0.04)
    am_stationary = abs(my_velocity_x) < 0.04
    
    # Positional analysis with stage control
    am_cornered = abs(my_pos_x) > 0.78
    opponent_cornered = abs(opponent_pos_x) > 0.78
    stage_center = abs(my_pos_x) < 0.2
    opponent_center = abs(opponent_pos_x) < 0.2
    wall_behind_me = (my_pos_x > 0.75 and relative_pos < 0) or (my_pos_x < -0.75 and relative_pos > 0)
    wall_behind_opponent = (opponent_pos_x > 0.75 and relative_pos > 0) or (opponent_pos_x < -0.75 and relative_pos < 0)
    
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
    am_medium_health = low_health <= my_health < good_health
    am_healthy = my_health >= good_health
    am_excellent = my_health >= excellent_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    opponent_healthy = opponent_health >= good_health
    
    # Match state analysis with refined thresholds
    am_winning_huge = health_advantage > 0.5
    am_winning_big = health_advantage > 0.3
    am_winning = health_advantage > 0.12
    even_match = abs(health_advantage) <= 0.12
    am_losing = health_advantage < -0.12
    am_losing_big = health_advantage < -0.3
    am_losing_huge = health_advantage < -0.5
    
    # Adaptive aggression calculation with multiple factors
    base_aggression = 0.55
    
    # Health advantage modifier
    if am_winning_huge:
        advantage_mod = 0.85
    elif am_winning_big:
        advantage_mod = 0.75
    elif am_winning:
        advantage_mod = 0.65
    elif even_match:
        advantage_mod = 0.5
    elif am_losing:
        advantage_mod = 0.35
    elif am_losing_big:
        advantage_mod = 0.25
    else:
        advantage_mod = 0.15
    
    # My health modifier
    if am_critical:
        health_mod = 0.1
    elif am_low_health:
        health_mod = 0.25
    elif am_medium_health:
        health_mod = 0.5
    elif am_healthy:
        health_mod = 0.75
    else:
        health_mod = 0.85
    
    # Opponent health modifier
    if opponent_critical:
        opp_health_mod = 0.9
    elif opponent_low:
        opp_health_mod = 0.7
    else:
        opp_health_mod = 0.5
    
    # Position modifier
    if opponent_cornered:
        pos_mod = 0.8
    elif am_cornered:
        pos_mod = 0.2
    elif stage_center:
        pos_mod = 0.6
    else:
        pos_mod = 0.5