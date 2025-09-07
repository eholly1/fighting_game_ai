"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_007
Rank: 53/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 220.52
- Win Rate: 50.0%
- Average Reward: 315.03

Created: 2025-06-01 03:09:14
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
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
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
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Hybrid tactical ranges - refined for balanced fighting
    point_blank = 0.05
    striking_range = 0.12
    close_combat = 0.20
    mid_close = 0.28
    medium_range = 0.40
    mid_far = 0.55
    long_range = 0.75
    
    # Dynamic aggression calculation
    base_aggression = 0.7
    health_modifier = health_advantage * 0.3
    distance_modifier = (1.0 - distance) * 0.2
    current_aggression = max(0.2, min(0.95, base_aggression + health_modifier + distance_modifier))
    
    # Momentum and prediction variables
    combined_momentum = abs(my_velocity_x) + abs(opp_velocity_x)
    approach_rate = -my_velocity_x * relative_pos if relative_pos != 0 else 0
    unpredictability = random.random()
    
    # Calculate tactical state
    my_ready_to_attack = my_attack_cooldown < 0.15
    my_can_block = my_block_cooldown < 0.10
    my_can_projectile = my_projectile_cooldown < 0.20
    opp_vulnerable = opp_stunned or (opp_attack_cooldown > 0.4 and not opp_blocking)
    opp_dangerous = opp_attacking or (opp_projectile_cooldown < 0.15 and distance > medium_range)
    
    # Emergency situations - highest priority
    if my_stunned:
        if distance < close_combat and opp_attacking:
            return 6 if my_can_block else 0
        elif distance < striking_range:
            # Try to escape stun situation
            if my_can_block:
                return 7 if relative_pos > 0 else 8
            else:
                return 1 if relative_pos > 0 else 2
        else:
            return 6 if my_can_block else 0
    
    # Critical health scenarios
    if my_health < 0.15:
        if health_advantage < -0.5:
            # Desperate all-in or defensive play
            if distance > medium_range:
                if my_can_projectile:
                    return 9  # Zone from safety
                else:
                    return 6  # Defensive
            elif distance < striking_range and opp_vulnerable and my_ready_to_attack:
                # All-in desperation
                return 5 if unpredictability < 0.6 else 4
            else:
                # Ultra defensive
                if my_can_block:
                    return 6
                else:
                    return 1 if relative_pos > 0 else 2
        else:
            # Careful play when low health but not desperate
            if distance < close_combat and opp_dangerous:
                return 6 if my_can_block else (7 if relative_pos > 0 else 8)
            elif distance > mid_far and my_can_projectile:
                return 9
    
    # Exploit opponent vulnerabilities - high priority
    if opp_stunned and distance < medium_range:
        if distance > striking_range:
            # Rush in for punish
            return 2 if relative_pos > 0 else 1
        elif my_ready_to_attack:
            # Optimal punish combo
            if health_advantage > 0.2:
                return 5  # Go for damage when ahead
            elif unpredictability < 0.7:
                return 4  # Safe punish
            else:
                return 5  # Risk for reward
        else:
            # Position for punish
            if distance > point_blank:
                return 2 if relative_pos > 0 else 1
            else:
                return 0
    
    # Defensive responses to opponent attacks
    if opp_attacking:
        if distance < close_combat:
            # Close range defense with hybrid approach
            if my_can_block:
                if current_aggression > 0.8 and distance > point_blank:
                    # Aggressive blocking with positioning
                    counter_choice = unpredictability
                    if counter_choice < 0.4:
                        return 8 if relative_pos > 0 else 7  # Block and position
                    elif counter_choice < 0.7:
                        return 6  # Pure block
                    else:
                        return 3  # Jump counter
                else:
                    return 6  # Standard block
            else:
                # Can't block - evasive maneuvers
                if distance < point_blank:
                    return 3  # Jump out
                elif unpredictability < 0.5:
                    return 1 if relative_pos > 0 else 2
                else:
                    return 3
        elif distance < medium_range:
            # Medium range response
            if current_aggression > 0.75:
                # Advance with protection
                return