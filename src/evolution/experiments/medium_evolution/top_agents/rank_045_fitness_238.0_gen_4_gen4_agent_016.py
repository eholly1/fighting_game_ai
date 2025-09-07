"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_016
Rank: 45/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 238.04
- Win Rate: 0.0%
- Average Reward: 238.04

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
    
    # Extract my fighter status with defensive bounds checking
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cooldown = max(0.0, state[8])
    my_attack_cooldown = max(0.0, state[9])
    my_block_cooldown = max(0.0, state[10])
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cooldown = max(0.0, state[19])
    opp_attack_cooldown = max(0.0, state[20])
    opp_block_cooldown = max(0.0, state[21])
    
    # Enhanced hybrid tactical ranges
    melee_range = 0.08
    optimal_strike = 0.14
    close_combat = 0.22
    transition_zone = 0.32
    medium_range = 0.45
    long_range = 0.60
    max_effective = 0.80
    
    # Advanced aggression system with multiple factors
    base_aggression = 0.65
    health_aggression = health_advantage * 0.35
    momentum_factor = min(0.15, abs(my_x_velocity) * 0.3)
    distance_pressure = max(0.0, (0.35 - distance) * 0.4)
    current_aggression = max(0.25, min(0.90, base_aggression + health_aggression + momentum_factor + distance_pressure))
    
    # Defensive priority system
    base_defense = 0.45
    health_defense = max(0.0, -health_advantage * 0.4)
    critical_defense = 0.3 if my_health < 0.25 else 0.0
    defense_priority = min(0.85, base_defense + health_defense + critical_defense)
    
    # Tactical state assessment
    my_ready_attack = my_attack_cooldown < 0.12
    my_ready_block = my_block_cooldown < 0.08
    my_ready_projectile = my_projectile_cooldown < 0.15
    opp_vulnerable = opp_stunned or (opp_attack_cooldown > 0.3 and not opp_blocking)
    opp_dangerous = opp_attacking or (my_health < opp_health and distance < close_combat)
    
    # Position and movement analysis
    wall_left = my_x_pos < 0.18
    wall_right = my_x_pos > 0.82
    near_wall = wall_left or wall_right
    opp_cornered = opp_x_pos < 0.12 or opp_x_pos > 0.88
    
    # Velocity and momentum analysis
    closing_speed = 0.0
    if relative_pos > 0:
        closing_speed = my_x_velocity - opp_x_velocity
    else:
        closing_speed = opp_x_velocity - my_x_velocity
    
    opponent_approaching = closing_speed > 0.05
    opponent_retreating = closing_speed < -0.05
    
    # Pattern recognition variables
    randomness = random.random()
    tactical_choice = random.random()
    combo_selector = random.random()
    
    # Critical situation handling - highest priority
    if my_stunned:
        if distance < close_combat and opp_attacking:
            return 6 if my_ready_block else 0
        elif distance < optimal_strike and opponent_approaching:
            # Escape stun with defensive movement
            if near_wall:
                return 3 if randomness < 0.6 else 6
            else:
                return 7 if relative_pos > 0 else 8
        elif distance > medium_range and my_ready_projectile:
            return 9
        else:
            return 6 if my_ready_block else 0
    
    # Emergency health management
    if my_health < 0.18:
        if health_advantage < -0.6:
            # Desperate comeback attempt
            if distance > long_range and my_ready_projectile:
                return 9
            elif distance < optimal_strike and opp_vulnerable and my_ready_attack:
                # All-in desperation
                return 5 if tactical_choice < 0.65 else 4
            elif distance < close_combat and opp_dangerous:
                # Survival mode
                if my_ready_block:
                    return 6
                elif near_wall:
                    return 3
                else:
                    return 1 if relative_pos > 0 else 2
            else:
                # Cautious zoning
                if distance < transition_zone:
                    return 7 if relative_pos > 0 else 8
                else:
                    return 9 if my_ready_projectile else 6
        else:
            # Low health but competitive
            if distance < melee_range and opp_attacking:
                return 6 if my_ready_block else 3
            elif distance > medium_range:
                return 9 if my_ready_projectile else (2 if relative_pos > 0 else 1)
    
    # Exploit stunned opponent maximally
    if opp_stunned:
        if distance > optimal_strike:
            # Rush in for maximum punish
            return 2 if relative_pos > 0 else 1
        elif distance < melee_range and my_ready_attack:
            # Devastating close-range combo
            if combo_selector < 0.4:
                return 5  # Heavy damage
            elif combo_selector < 0.75:
                return 4  # Quick combo
            else:
                return 9 if my_ready_projectile else 5
        elif my_ready_attack:
            # Optimal range punish
            return 5 if current_aggression > 0.7 else 4
        else:
            # Position for punish
            if distance > melee_range:
                return 2 if relative_pos > 0 else 1
            else:
                return 0
    
    # Advanced defensive responses
    if opp_attacking:
        if distance < melee_range:
            # Point blank defense
            if my_ready_block:
                return 6
            else:
                return 3 if randomness < 0.7 else 0
        elif distance < optimal_strike:
            # Optimal counter-attack range
            if my_ready_block and defense_priority > 0.6:
                # Defensive block with positioning
                if tactical_choice < 0.5:
                    return 8 if relative_pos > 0 else 7
                else:
                    return