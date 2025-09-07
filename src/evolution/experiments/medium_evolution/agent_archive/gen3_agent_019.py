"""
Evolutionary Agent: gen3_agent_019
==================================

Metadata:
{
  "generation": 3,
  "fitness": -12.099999999999628,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: a62315a5581347cf
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
    
    # Enhanced tactical ranges for hybrid fighting
    danger_zone = 0.04
    point_blank = 0.08
    very_close = 0.14
    close_combat = 0.22
    mid_close = 0.32
    ideal_range = 0.42
    zoning_range = 0.55
    max_range = 0.80
    
    # Adaptive fighting parameters
    base_aggression = 0.73
    pressure_threshold = 0.78
    defensive_mode = 0.62
    counter_window = 0.18
    zone_control = 0.69
    
    # Enhanced health assessment
    health_ratio = my_health / max(0.05, opp_health)
    critical_health = my_health < 0.08
    emergency_health = my_health < 0.18
    low_health = my_health < 0.35
    good_health = my_health > 0.65
    dominant_health = health_advantage > 0.45
    desperate_health = health_advantage < -0.45
    
    # Dynamic tactical adaptation
    if dominant_health:
        aggression_factor = 0.92
        zone_priority = 0.35
        risk_tolerance = 0.85
    elif health_advantage > 0.15:
        aggression_factor = 0.81
        zone_priority = 0.52
        risk_tolerance = 0.72
    elif health_advantage > -0.15:
        aggression_factor = base_aggression
        zone_priority = zone_control
        risk_tolerance = 0.65
    elif desperate_health:
        aggression_factor = 0.38
        zone_priority = 0.88
        risk_tolerance = 0.25
    else:
        aggression_factor = 0.55
        zone_priority = 0.75
        risk_tolerance = 0.45
    
    # Advanced cooldown tracking
    my_projectile_ready = my_projectile_cooldown < 0.03
    my_projectile_soon = my_projectile_cooldown < 0.12
    my_attack_ready = my_attack_cooldown < 0.02
    my_block_ready = my_block_cooldown < 0.05
    
    opp_projectile_threat = opp_projectile_cooldown < 0.06
    opp_attack_threat = opp_attack_cooldown < 0.04
    opp_vulnerable = opp_attack_cooldown > 0.25 and not opp_blocking
    
    # Enhanced movement analysis
    my_momentum = abs(my_velocity_x)
    opp_momentum = abs(opp_velocity_x)
    
    opp_approaching = ((relative_pos > 0 and opp_velocity_x < -0.08) or 
                      (relative_pos < 0 and opp_velocity_x > 0.08))
    opp_retreating = ((relative_pos > 0 and opp_velocity_x > 0.12) or 
                     (relative_pos < 0 and opp_velocity_x < -0.12))
    opp_airborne = abs(height_diff) > 0.15
    opp_landing = opp_airborne and abs(opp_velocity_y) < 0.05
    
    # Advanced positioning awareness
    stage_left = my_pos_x < -0.55
    stage_right = my_pos_x > 0.55
    stage_center = abs(my_pos_x) < 0.3
    corner_danger = my_pos_x < -0.72 or my_pos_x > 0.72
    
    opp_cornered = opp_pos_x < -0.68 or opp_pos_x > 0.68
    wall_advantage = opp_cornered and not corner_danger
    
    # Critical emergency responses
    if critical_health:
        if opp_attacking and distance < close_combat:
            if my_block_ready:
                return 6
            else:
                # Desperate evasion
                if not corner_danger:
                    return 1 if relative_pos > 0 else 2
                else:
                    return 3  # Jump escape
        
        if distance < point_blank and not corner_danger:
            # Emergency spacing
            if relative_pos > 0 and not stage_left:
                return 1
            elif not stage_right:
                return 2
            else:
                return 3  # Vertical escape
        
        # Desperate projectile spam when able
        if my_projectile_ready and distance > mid_close:
            return 9
        
        # Default emergency block
        if my_block_ready:
            return 6
        else:
            return 0  # Wait for