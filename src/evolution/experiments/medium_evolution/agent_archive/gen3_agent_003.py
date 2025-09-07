"""
Evolutionary Agent: gen3_agent_003
==================================

Metadata:
{
  "generation": 3,
  "fitness": 65.97226666666567,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 414f7323f5f86ace
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
    
    # Enhanced tactical range definitions
    point_blank_range = 0.05
    very_close_range = 0.10
    close_range = 0.15
    medium_close_range = 0.22
    medium_range = 0.30
    medium_far_range = 0.40
    far_range = 0.55
    max_range = 0.70
    
    # Evolved fighting parameters - adaptive balanced approach
    base_aggression = 0.78
    defensive_threshold = 0.65
    counter_attack_window = 0.85
    pressure_threshold = 0.75
    zoning_efficiency = 0.60
    
    # Advanced state analysis
    health_ratio = my_health / max(opp_health, 0.01)
    momentum_factor = health_advantage * 0.6 + (my_health - opp_health) * 0.4
    
    # Movement prediction based on opponent velocity
    predicted_distance = distance + (opp_velocity_x * relative_pos * 0.3)
    predicted_distance = max(0.0, min(1.0, predicted_distance))
    
    # Determine enhanced tactical mode with momentum consideration
    if health_advantage > 0.5 and momentum_factor > 0.3:
        tactical_mode = "overwhelming"
        aggression_level = 0.95
        defense_priority = 0.20
    elif health_advantage > 0.25:
        tactical_mode = "controlling"
        aggression_level = 0.85
        defense_priority = 0.35
    elif health_advantage > 0:
        tactical_mode = "slight_edge"
        aggression_level = 0.80
        defense_priority = 0.45
    elif health_advantage > -0.15:
        tactical_mode = "contested"
        aggression_level = 0.75
        defense_priority = 0.55
    elif health_advantage > -0.35:
        tactical_mode = "disadvantaged"
        aggression_level = 0.65
        defense_priority = 0.70
    else:
        tactical_mode = "critical"
        aggression_level = 0.45
        defense_priority = 0.85
    
    # Adaptive cooldown management
    can_attack = my_attack_cooldown < 0.08
    can_block = my_block_cooldown < 0.12
    can_projectile = my_projectile_cooldown < 0.15
    
    # Emergency response system
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6 if can_block else 3  # Block or jump
        elif distance < very_close_range:
            # Escape stunned state with movement
            if my_pos_x < 0.2:  # Near left wall
                return 2
            elif my_pos_x > 0.8:  # Near right wall
                return 1
            else:
                return 1 if relative_pos > 0 else 2
        else:
            return 6 if can_block else 0
    
    # Critical health management with aggressive comeback potential
    if my_health < 0.25:
        if tactical_mode == "critical":
            # High-risk comeback strategy
            if distance > medium_range and can_projectile:
                return 9  # Desperate zoning
            elif distance < close_range and not opp_blocking and can_attack:
                # All-in attack when opponent not blocking
                return 5 if random.random() < 0.75 else 4
            elif distance < very_close_range and opp_attacking:
                return 6 if can_block else 3  # Defensive survival
            else:
                # Positioning for opportunity
                if distance > medium_close_range:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 6 if can_block else 0
    
    # Enhanced opportunity exploitation
    if opp_stunned:
        if distance > medium_range:
            # Rush in for maximum punish
            return 2 if relative_pos > 0 else 1
        elif distance > close_range:
            # Optimal approach distance
            advance_choice = random.random()
            if advance_choice < 0.7:
                return 2 if relative_pos > 0 else 1
            elif advance_choice < 0.9 and can_projectile:
                return 9  # Projectile setup
            else:
                return 3  # Jump approach
        elif can_attack:
            # Maximum damage punish combo
            punish_roll = random.random()
            if punish_roll < 0.65:
                return 5  # Heavy punishment
            elif punish_roll < 0.85:
                return 4