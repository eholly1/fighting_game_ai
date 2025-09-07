"""
Evolutionary Agent: gen4_agent_017
==================================

Metadata:
{
  "generation": 4,
  "fitness": -6.300000000000217,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: c2b9f78dc66fbb1d
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
    
    # Extract opponent status with defensive bounds checking
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
    
    # Enhanced tactical ranges for evolved hybrid fighting
    danger_threshold = 0.03
    point_blank = 0.07
    ultra_close = 0.12
    close_combat = 0.19
    mid_close = 0.28
    optimal_range = 0.40
    far_combat = 0.55
    zoning_range = 0.72
    max_range = 0.90
    
    # Evolved fighting parameters with better balance
    base_aggression = 0.68
    counter_aggression = 0.85
    defensive_threshold = 0.55
    combo_window = 0.15
    adaptation_rate = 0.75
    
    # Advanced health assessment with more granular thresholds
    health_ratio = my_health / max(0.03, opp_health)
    critical_health = my_health < 0.05
    emergency_health = my_health < 0.12
    low_health = my_health < 0.28
    medium_health = my_health > 0.45
    good_health = my_health > 0.70
    excellent_health = my_health > 0.85
    
    dominant_advantage = health_advantage > 0.50
    strong_advantage = health_advantage > 0.25
    slight_advantage = health_advantage > 0.08
    slight_disadvantage = health_advantage < -0.08
    strong_disadvantage = health_advantage < -0.25
    critical_disadvantage = health_advantage < -0.50
    
    # Dynamic aggression calculation with improved scaling
    if dominant_advantage:
        aggression_modifier = 0.95
        risk_tolerance = 0.90
        zone_control = 0.25
    elif strong_advantage:
        aggression_modifier = 0.82
        risk_tolerance = 0.78
        zone_control = 0.40
    elif slight_advantage:
        aggression_modifier = 0.74
        risk_tolerance = 0.68
        zone_control = 0.55
    elif slight_disadvantage:
        aggression_modifier = 0.62
        risk_tolerance = 0.58
        zone_control = 0.72
    elif strong_disadvantage:
        aggression_modifier = 0.48
        risk_tolerance = 0.35
        zone_control = 0.85
    else:
        aggression_modifier = 0.32
        risk_tolerance = 0.18
        zone_control = 0.95
    
    # Enhanced cooldown and ability tracking
    my_projectile_ready = my_projectile_cooldown < 0.02
    my_projectile_soon = my_projectile_cooldown < 0.08
    my_attack_ready = my_attack_cooldown < 0.01
    my_block_ready = my_block_cooldown < 0.03
    
    opp_projectile_ready = opp_projectile_cooldown < 0.04
    opp_attack_ready = opp_attack_cooldown < 0.02
    opp_vulnerable = opp_attack_cooldown > 0.20 and not opp_blocking
    opp_recovery = opp_attack_cooldown > 0.15
    
    # Advanced movement and positioning analysis
    my_momentum = abs(my_velocity_x)
    opp_momentum = abs(opp_velocity_x)
    
    opp_advancing = ((relative_pos > 0 and opp_velocity_x < -0.06) or 
                    (relative_pos < 0 and opp_velocity_x > 0.06))
    opp_retreating = ((relative_pos > 0 and opp_velocity_x > 0.10) or 
                     (relative_pos < 0 and opp_velocity_x < -0.10))
    opp_airborne = abs(height_diff) > 0.12
    opp_landing_soon = opp_airborne and abs(opp_velocity_y) < 0.03
    
    # Enhanced stage positioning awareness
    stage_left_edge = my_pos_x < -0.60
    stage_right_edge = my_pos_x > 0.60
    stage_center = abs(my_pos_x) < 0.25
    corner_trapped = my_pos_x < -0.75 or my_pos_x > 0.75
    wall_nearby = my_pos_x < -0.50 or my_pos_x > 0.50
    
    opp_cornered = opp_pos_x < -0.70 or opp_pos_x > 0.70
    opp_near_wall = opp_pos_x < -0.45 or opp_pos_x > 0.45
    positional_advantage = opp_corn