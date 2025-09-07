"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_007
Rank: 96/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 131.48
- Win Rate: 0.0%
- Average Reward: 187.83

Created: 2025-06-01 03:58:23
Lineage: Original

Tournament Stats:
None
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
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.3 if len(state) > 5 else False
    my_blocking = state[6] > 0.3 if len(state) > 6 else False
    my_stunned = state[7] > 0.3 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.3 if len(state) > 16 else False
    opp_blocking = state[17] > 0.3 if len(state) > 17 else False
    opp_stunned = state[18] > 0.3 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Enhanced tactical ranges with precision tuning
    point_blank = 0.04
    very_close = 0.08
    close_range = 0.14
    medium_close = 0.22
    medium_range = 0.32
    medium_far = 0.45
    far_range = 0.60
    max_range = 0.8
    
    # Core hybrid fighter parameters
    base_aggression = 0.58
    base_patience = 0.45
    adaptation_factor = 0.35
    tactical_variance = 0.25
    
    # Calculate advanced fighting metrics
    health_ratio = my_health / max(opp_health, 0.01)
    momentum_my = abs(my_velocity_x) + abs(my_velocity_y * 0.7)
    momentum_opp = abs(opp_velocity_x) + abs(opp_velocity_y * 0.7)
    velocity_difference = momentum_my - momentum_opp
    
    # Enhanced cooldown status
    can_attack = my_attack_cooldown < 0.12
    can_block = my_block_cooldown < 0.08
    can_projectile = my_projectile_cooldown < 0.18
    opp_can_attack = opp_attack_cooldown < 0.12
    opp_can_projectile = opp_projectile_cooldown < 0.18
    
    # Sophisticated opponent analysis
    opp_is_rushing = momentum_opp > 0.12 and distance > very_close
    opp_is_retreating = opp_velocity_x * relative_pos < -0.08
    opp_is_stationary = momentum_opp < 0.04
    opp_is_vulnerable = opp_stunned or (opp_attacking and distance < close_range)
    opp_is_aggressive = opp_attacking and momentum_opp > 0.06
    opp_is_defensive = opp_blocking or (distance < medium_range and momentum_opp < 0.03)
    opp_is_zoning = opp_can_projectile and distance > medium_range
    
    # Dynamic fighting mode determination
    if health_advantage > 0.6:
        fight_mode = "dominating"
        aggression_level = 0.88
        defensive_level = 0.15
        risk_tolerance = 0.8
    elif health_advantage > 0.25:
        fight_mode = "winning"
        aggression_level = 0.72
        defensive_level = 0.28
        risk_tolerance = 0.65
    elif health_advantage > -0.05:
        fight_mode = "competitive"
        aggression_level = 0.58
        defensive_level = 0.42
        risk_tolerance = 0.5
    elif health_advantage > -0.3:
        fight_mode = "behind"
        aggression_level = 0.45
        defensive_level = 0.55
        risk_tolerance = 0.35
    else:
        fight_mode = "critical"
        aggression_level = 0.25
        defensive_level = 0.75
        risk_tolerance = 0.2
    
    # Tactical randomization for unpredictability
    primary_dice = random.random()
    secondary_dice = random.random()
    combat_dice = random.random()
    movement_dice = random.random()
    
    # Emergency protocols
    if my_stunned and distance < medium_range:
        if opp_attacking and can_block:
            return 6  # Emergency defensive block
        elif distance < close_range:
            # Desperate escape based on positioning
            if abs(my_pos_x) > 0.75:  # Near stage edge
                return 6 if can_block else 3  # Block or jump
            elif relative_pos > 0:
                return 7 if can_block else 1  # Move left with protection
            else:
                return 8 if can_block else 2  # Move right with protection
        else:
            return 6 if can_block else 0
    
    # Critical health management
    if my_health < 0.12 or health_advantage < -0.65:
        if distance > medium_far:
            if can_projectile and not opp_is_rushing:
                return 9  # Desperation projectile
            elif opp_can_projectile:
                return 6 if can_block else 0  # Defensive positioning
            else:
                return 0  # Wait for opening
        elif distance < very_close and opp_is_vulnerable:
            # All-or-nothing attack
            if can_attack and primary_dice < 0.85:
                return 5 if combat_dice < 0.65 else 4
            else:
                return 6 if can_block else 0
        else:
            # Maintain safe distance
            if relative_pos > 0:
                return 7 if can_block else 1
            else:
                return