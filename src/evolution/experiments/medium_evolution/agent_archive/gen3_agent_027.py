"""
Evolutionary Agent: gen3_agent_027
==================================

Metadata:
{
  "generation": 3,
  "fitness": -18.4,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 12fd6259bc7121c8
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
    
    # Enhanced tactical ranges for evolved fighter
    point_blank_range = 0.05
    melee_range = 0.12
    close_range = 0.2
    mid_close_range = 0.28
    medium_range = 0.4
    mid_far_range = 0.52
    far_range = 0.7
    
    # Evolved fighting parameters - adaptive balanced approach
    base_aggression = 0.8
    momentum_multiplier = 1.5
    adaptation_factor = 0.3
    
    # Advanced state analysis
    health_ratio = my_health / max(opp_health, 0.01)
    momentum_score = health_advantage + (my_velocity_x * relative_pos * 0.2)
    positioning_advantage = abs(my_pos_x - 0.5) - abs(opp_pos_x - 0.5)
    
    # Dynamic tactical assessment
    if health_advantage > 0.5:
        combat_stance = "dominating"
        aggression_level = 0.95
        risk_tolerance = 0.8
    elif health_advantage > 0.2:
        combat_stance = "controlling"
        aggression_level = 0.85
        risk_tolerance = 0.7
    elif health_advantage > -0.1:
        combat_stance = "balanced"
        aggression_level = 0.75
        risk_tolerance = 0.6
    elif health_advantage > -0.3:
        combat_stance = "pressured"
        aggression_level = 0.65
        risk_tolerance = 0.4
    else:
        combat_stance = "survival"
        aggression_level = 0.3
        risk_tolerance = 0.2
    
    # Emergency response system
    if my_stunned:
        if distance < melee_range and opp_attacking:
            return 6  # Priority block when stunned and in danger
        elif my_block_cooldown < 0.15:
            return 6  # Defensive stance
        elif distance < close_range:
            return 1 if relative_pos > 0 else 2  # Escape movement
        else:
            return 0  # Wait for recovery
    
    # Critical health protocols
    if my_health < 0.15:
        if distance > medium_range:
            if my_projectile_cooldown < 0.3:
                return 9  # Desperate zoning
            else:
                return 6  # Block and preserve
        elif distance < melee_range and opp_stunned:
            if my_attack_cooldown < 0.1:
                return 5  # All-in for finish
            else:
                return 4  # Quick strike
        elif opp_attacking:
            return 6 if my_block_cooldown < 0.2 else 0
        else:
            return 6  # Defensive positioning
    
    # Opportunity exploitation
    if opp_stunned:
        if distance > close_range:
            return 2 if relative_pos > 0 else 1  # Rush for punish
        elif my_attack_cooldown < 0.15:
            punish_selection = random.random()
            if distance < point_blank_range:
                return 5 if punish_selection < 0.8 else 4  # Heavy punish up close
            elif distance < melee_range:
                return 4 if punish_selection < 0.6 else 5  # Mixed punish
            else:
                return 9 if my_projectile_cooldown < 0.1 else 4  # Range punish
        else:
            return 2 if relative_pos > 0 else 1  # Position for punish
    
    # Advanced opponent attack response
    if opp_attacking:
        if distance < melee_range:
            if my_block_cooldown < 0.1:
                if combat_stance in ["survival", "pressured"]:
                    return 6  # Pure defense when behind
                elif distance < point_blank_range:
                    return 6  # Block at point blank
                else:
                    # Intelligent block movement
                    block_move_chance = random.random()
                    if block_move_chance < 0.6:
                        return 8 if relative_pos > 0 else 7  # Block with positioning
                    else:
                        return 6  # Pure block
            else:
                # Enhanced evasion tactics
                evasion_roll = random.random()
                if evasion_roll < 0.35:
                    return 1 if relative_pos > 0 else 2  # Lateral escape
                elif evasion_roll < 0.65:
                    return 3  # Jump evasion
                else:
                    return