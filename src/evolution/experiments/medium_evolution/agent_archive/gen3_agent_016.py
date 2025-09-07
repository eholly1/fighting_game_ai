"""
Evolutionary Agent: gen3_agent_016
==================================

Metadata:
{
  "generation": 3,
  "fitness": 24.05999999999895,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: a180c5ae979bb402
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
    
    # Enhanced tactical ranges with more precision
    point_blank = 0.05
    very_close = 0.10
    close_range = 0.17
    medium_close = 0.25
    medium_range = 0.35
    medium_far = 0.50
    far_range = 0.65
    max_range = 0.8
    
    # Advanced hybrid parameters
    base_aggression = 0.65
    base_patience = 0.4
    adaptation_rate = 0.3
    tactical_variance = 0.2
    
    # Calculate dynamic fighting variables
    health_ratio = my_health / max(opp_health, 0.05)
    momentum_my = abs(my_velocity_x) + abs(my_velocity_y)
    momentum_opp = abs(opp_velocity_x) + abs(opp_velocity_y)
    relative_momentum = momentum_my - momentum_opp
    
    # Determine current tactical state
    if health_advantage > 0.5:
        fight_mode = "dominating"
        aggression_level = 0.85
        defensive_level = 0.2
    elif health_advantage > 0.2:
        fight_mode = "winning"
        aggression_level = 0.75
        defensive_level = 0.3
    elif health_advantage > -0.1:
        fight_mode = "competitive"
        aggression_level = 0.65
        defensive_level = 0.4
    elif health_advantage > -0.35:
        fight_mode = "behind"
        aggression_level = 0.5
        defensive_level = 0.55
    else:
        fight_mode = "critical"
        aggression_level = 0.3
        defensive_level = 0.7
    
    # Advanced cooldown management
    can_attack = my_attack_cooldown < 0.15
    can_block = my_block_cooldown < 0.1
    can_projectile = my_projectile_cooldown < 0.2
    opp_can_attack = opp_attack_cooldown < 0.15
    opp_can_projectile = opp_projectile_cooldown < 0.2
    
    # Enhanced opponent behavior analysis
    opp_is_rushing = momentum_opp > 0.15 and distance > very_close
    opp_is_retreating = opp_velocity_x * relative_pos < -0.1
    opp_is_stationary = momentum_opp < 0.05
    opp_is_vulnerable = opp_stunned or (opp_attacking and not opp_blocking)
    opp_is_defensive = opp_blocking or (not opp_attacking and distance < medium_range)
    
    # Randomization for tactical unpredictability
    tactical_dice = random.random()
    combat_dice = random.random()
    positioning_dice = random.random()
    
    # Critical emergency responses
    if my_stunned and distance < close_range:
        if opp_attacking and can_block:
            return 6  # Emergency block
        elif distance < very_close:
            # Desperate escape
            if relative_pos > 0:
                return 7 if can_block else 1
            else:
                return 8 if can_block else 2
        else:
            return 6 if can_block else 0
    
    # Severe health disadvantage protocol
    if my_health < 0.15 and health_advantage < -0.5:
        if distance > medium_range:
            if can_projectile and not opp_is_rushing:
                return 9  # Desperate zoning
            elif opp_can_projectile:
                return 6 if can_block else 0  # Turtle up
            else:
                return 0  # Wait for opportunity
        elif distance < very_close and not opp_attacking:
            # All-in desperation
            if can_attack and tactical_dice < 0.8:
                return 5 if combat_dice < 0.6 else 4
            else:
                return 6 if can_block else 0
        else:
            # Maintain distance desperately
            if relative_pos > 0:
                return 7 if can_block else 1
            else:
                return 8 if can_block else 2
    
    # Capitalize on opponent vulnerability
    if opp_is_vulnerable:
        if distance < medium_range:
            if distance > close_range and not opp_stunned:
                # Rush in for punish
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif can_attack:
                # Optimal punish selection
                punish_roll = combat_dice
                if opp_stunned:
                    # Maximum damage punish
                    if punish_roll < 0.65:
                        return 5  # Heavy kick
                    elif punish_roll < 0.85:
                        return 4