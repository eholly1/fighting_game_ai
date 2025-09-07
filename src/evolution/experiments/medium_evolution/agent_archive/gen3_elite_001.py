"""
Evolutionary Agent: gen3_elite_001
==================================

Metadata:
{
  "generation": 3,
  "fitness": 236.19013333333683,
  "fighting_style": "evolved",
  "win_rate": 0.16666666666666666
}

Code Hash: 39f20a471a159a00
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
    
    # Define hybrid fighter tactical ranges
    point_blank_range = 0.06
    very_close_range = 0.12
    close_range = 0.18
    medium_close_range = 0.25
    medium_range = 0.35
    medium_far_range = 0.45
    far_range = 0.6
    
    # Hybrid fighting parameters - balanced approach
    base_aggression = 0.75
    defensive_threshold = 0.6
    pressure_threshold = 0.8
    zoning_threshold = 0.4
    
    # Calculate dynamic fighting style based on game state
    health_ratio = my_health / max(opp_health, 0.1)
    momentum_factor = health_advantage * 0.5
    
    # Determine current tactical mode
    if health_advantage > 0.4:
        tactical_mode = "dominant"
        aggression_level = 0.9
    elif health_advantage > 0.1:
        tactical_mode = "winning"
        aggression_level = 0.8
    elif health_advantage > -0.1:
        tactical_mode = "even"
        aggression_level = 0.75
    elif health_advantage > -0.4:
        tactical_mode = "losing"
        aggression_level = 0.6
    else:
        tactical_mode = "desperate"
        aggression_level = 0.4
    
    # Emergency priority situations
    if my_stunned and distance < close_range:
        if opp_attacking:
            return 6  # Block while stunned
        elif my_block_cooldown < 0.1:
            return 6  # Stay defensive
        else:
            # Try to create space while stunned
            if distance < very_close_range:
                return 1 if relative_pos > 0 else 2
            else:
                return 6
    
    # Critical health management
    if my_health < 0.2:
        if tactical_mode == "desperate":
            if distance > medium_range:
                # Desperate zoning
                if my_projectile_cooldown < 0.2:
                    return 9
                else:
                    return 6  # Block and wait
            elif distance < very_close_range and not opp_attacking:
                # All-in desperation attack
                if my_attack_cooldown < 0.05:
                    return 5 if random.random() < 0.7 else 4
                else:
                    return 6
            else:
                # Defensive positioning
                return 6 if my_block_cooldown < 0.2 else 0
    
    # Capitalize on opponent vulnerabilities
    if opp_stunned:
        if distance < medium_range:
            if distance > close_range:
                # Rush in for punish
                return 2 if relative_pos > 0 else 1
            elif my_attack_cooldown < 0.1:
                # Optimal punish combo
                punish_choice = random.random()
                if punish_choice < 0.6:
                    return 5  # Heavy punish
                elif punish_choice < 0.85:
                    return 4  # Quick punish
                else:
                    return 9 if my_projectile_cooldown < 0.1 else 5
            else:
                # Position for punish
                if distance > very_close_range:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 0  # Wait for attack cooldown
        else:
            # Close distance quickly
            return 2 if relative_pos > 0 else 1
    
    # Opponent attack response - hybrid defensive tactics
    if opp_attacking:
        if distance < close_range:
            # Close range defense with positioning
            if my_block_cooldown < 0.1:
                if tactical_mode in ["losing", "desperate"]:
                    return 6  # Pure defense when behind
                elif distance < very_close_range:
                    return 6  # Block at point blank
                else:
                    # Block with positioning for counter
                    return 8 if relative_pos > 0 else 7
            else:
                # Evasive movement when can't block
                evasion_choice = random.random()
                if evasion_choice < 0.4:
                    return 1 if relative_pos > 0 else 2  # Lateral movement
                elif evasion_choice < 0.7:
                    return 3  # Jump evasion
                else:
                    return 0  # Stay and brace
        elif distance < medium_range:
            # Medium range - maintain spacing or advance with block
            if tactical_mode in ["winning", "dominant"]:
                return 8