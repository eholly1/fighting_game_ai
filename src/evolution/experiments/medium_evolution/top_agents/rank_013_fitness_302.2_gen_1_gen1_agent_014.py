"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_014
Rank: 13/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 302.18
- Win Rate: 50.0%
- Average Reward: 302.18

Created: 2025-06-01 01:24:51
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
    
    # Extract comprehensive fighter information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = state[8] if len(state) > 8 else 0.0
    my_attack_cooldown = state[9] if len(state) > 9 else 0.0
    my_block_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = state[19] if len(state) > 19 else 0.0
    opp_attack_cooldown = state[20] if len(state) > 20 else 0.0
    opp_block_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid fighter strategic parameters
    close_range = 0.14
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    dominant_health = 0.3
    desperate_health = -0.5
    
    # Calculate adaptive aggression based on multiple factors
    base_aggression = 0.65  # Balanced baseline
    aggression_modifier = 1.0
    
    # Health-based aggression adjustment
    if health_advantage > dominant_health:
        aggression_modifier = 1.2  # More aggressive when winning
    elif health_advantage < desperate_health:
        aggression_modifier = 1.4  # Desperate aggression when losing badly
    elif health_advantage < -0.2:
        aggression_modifier = 0.8  # More cautious when losing
    
    # Distance-based aggression
    if distance < close_range:
        aggression_modifier *= 1.1  # Slightly more aggressive up close
    elif distance > far_range:
        aggression_modifier *= 0.9  # Slightly more cautious at range
    
    current_aggression = min(1.0, base_aggression * aggression_modifier)
    
    # Emergency situations - highest priority
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6  # Block while stunned
        elif distance > medium_range:
            return 9 if my_projectile_cooldown < 0.1 else 6
        else:
            return 6  # Default to blocking when stunned
    
    # Critical health emergency protocols
    if my_health < critical_health and health_advantage < desperate_health:
        if distance > far_range:
            # Try to maintain distance and use projectiles
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                return 6  # Block while waiting for cooldown
        elif distance < close_range and opp_attacking:
            return 6  # Defensive blocking
        elif distance < close_range:
            # Desperate close combat
            return 5 if random.random() < 0.6 else 4
        else:
            # Try to get to optimal range
            if relative_pos > 0:
                return 8  # Move with blocking
            else:
                return 7
    
    # Opponent stunned - capitalize with hybrid approach
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                return 5 if random.random() < 0.7 else 4  # Prefer heavy attacks
            else:
                return 0  # Wait for attack cooldown
        elif distance < medium_range:
            # Close distance quickly
            if relative_pos > 0:
                return 2
            else:
                return 1
        else:
            # Use projectile if available, otherwise close distance
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Opponent attacking - hybrid defensive response
    if opp_attacking:
        if distance < close_range:
            if my_block_cooldown < 0.1:
                # Smart blocking with positioning
                if health_advantage > 0.1:
                    # Counter-attack when ahead
                    if random.random() < 0.4:
                        return 5 if my_attack_cooldown < 0.1 else 6
                    else:
                        return 6
                else:
                    # Pure defense when behind
                    return 6
            else:
                # Can't block - try to reposition
                if abs(relative_pos) > 0.3:
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    return 3  # Jump to avoid attack
        elif distance < medium_range:
            # Medium range against attacking opponent
            if health_advantage > 0.2:
                # Rush in for counter when winning
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                # Cautious approach when not winning
                if relative_pos > 0:
                    return 8
                else:
                    return 7
        else:
            # Far range - projectile duel or close gap
            if my_projectile_cooldown < 0.1 and random.random() < 0.5:
                return 9
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Opponent blocking - hybrid pressure tactics
    if opp_blocking:
        if distance < close_range:
            # Close range guard breaking
            if my_attack_cooldown < 0.1:
                guard_break_roll = random.random()
                if guard_break_roll < 0.35:
                    return 5  # Heavy kick to break guar