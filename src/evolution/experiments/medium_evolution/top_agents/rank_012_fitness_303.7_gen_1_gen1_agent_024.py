"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_024
Rank: 12/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 303.66
- Win Rate: 50.0%
- Average Reward: 303.66

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
    
    # Extract my fighter status
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
    
    # Define pressure fighter ranges and thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.28
    far_range = 0.45
    
    # Calculate pressure intensity based on game state
    base_aggression = 0.85
    health_multiplier = 1.0
    
    if health_advantage > 0.3:
        health_multiplier = 1.4  # Maximum aggression when dominating
    elif health_advantage > 0.1:
        health_multiplier = 1.2  # High aggression when winning
    elif health_advantage < -0.3:
        health_multiplier = 0.5  # Defensive when losing badly
    elif health_advantage < -0.1:
        health_multiplier = 0.7  # Cautious when behind
    
    pressure_intensity = base_aggression * health_multiplier
    
    # Emergency situations - highest priority
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6  # Block when stunned and under attack
        elif distance > medium_range:
            return 9 if my_projectile_cooldown < 0.2 else 6
        else:
            return 6  # Default to blocking when stunned
    
    # Critical health situations
    if my_health < 0.15:
        if distance > far_range:
            return 9 if my_projectile_cooldown < 0.1 else 6
        elif distance < very_close_range and not opp_attacking:
            # Desperate all-in attack
            return 5 if my_attack_cooldown < 0.1 else 4
        else:
            return 6  # Survive mode
    
    # Capitalize on stunned opponent immediately
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                # Choose optimal attack for stunned opponent
                return 5 if random.random() < 0.8 else 4
            else:
                # Get into perfect position while they're stunned
                if distance > very_close_range:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 0  # Wait for attack cooldown
        else:
            # Rush in while they can't defend
            return 2 if relative_pos > 0 else 1
    
    # Counter opponent attacks with smart defense
    if opp_attacking:
        if distance < close_range:
            if my_block_cooldown < 0.1:
                # Block with positioning to maintain pressure
                if distance < very_close_range:
                    return 6  # Pure block at point blank
                else:
                    # Block while positioning for counter
                    counter_direction = 2 if relative_pos > 0 else 1
                    return 8 if counter_direction == 2 else 7
            else:
                # Can't block - evasive movement
                if abs(my_x_velocity) < 0.1:  # Not already moving
                    return 2 if relative_pos < 0 else 1  # Move away from attack
                else:
                    return 3  # Jump to avoid
        elif distance < medium_range:
            # Medium range attack incoming - close gap with block
            return 8 if relative_pos > 0 else 7
    
    # Primary pressure fighter tactics by range
    if distance < very_close_range:
        # Point blank range - maximum aggression
        if my_attack_cooldown < 0.05:
            if opp_blocking:
                # Break guard with varied timing
                guard_break_chance = 0.6 + (health_advantage * 0.2)
                if random.random() < guard_break_chance:
                    # Mix heavy and light attacks vs blockers
                    return 5 if random.random() < 0.7 else 4
                else:
                    # Reposition slightly to find opening
                    micro_adjust = random.random()
                    if micro_adjust < 0.4:
                        return 1 if relative_pos > 0.5 else 2
                    else:
                        return 0  # Wait for opening
            else:
                # Unblocked opponent - devastating combos
                combo_choice = random.random()
                if combo_choice < 0.4:
                    return 4  # Fast punch starter
                elif combo_choice < 0.75:
                    return 5  # Power kick
                else:
                    # Surprise close range projectile
                    return 9 if my_projectile_cooldown < 0.1 else 4
        else:
            # Attack cooling down - maintain suffocating pressure
            if opp_block_cooldown > 0.3:
                # Opponent can't block soon - stay close
                pressure_action = random.random()
                if pressure_action < 0.5:
                    return 0  # Stay ready
                elif pressure_action < 0.8:
                    # Micro movements to stay optimal
                    return 2 if relative_pos < -0.2 else 1 if relative_pos > 0.2 else 0
                else:
                    return 6  # Brief block to mix rhythm
            else:
                # Keep close pressure alive
                return 0 if random.random() < 0.6 else 6
    
    elif distance < close_range:
        # Close range - primary engagement zone
        if my_attack_cooldown < 0.1:
            # Ready to attack
            if opp_attacking:
                # Counter attack opportunity
                return 5 if random.random() < 0.8 else 4
            elif opp_blocking:
                # Pressure blocker with mix-ups
                if random.random() < pressure_intensity:
                    attack_mix = random.random()
                    if attack_mix < 0.5:
                        return 4  # Quick punch
                    elif attack_mix < 0.8:
                        return 5