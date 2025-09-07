"""
Hall of Fame Agent
==================

Agent ID: gen2_elite_001
Rank: 54/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 218.75
- Win Rate: 0.0%
- Average Reward: 312.49

Created: 2025-06-01 02:16:30
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
    
    # Extract my fighter information
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_block_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_block_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Define hybrid fighter thresholds
    close_range = 0.13
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_margin = 0.15
    losing_margin = -0.15
    edge_threshold = 0.15
    
    # Calculate tactical variables
    is_near_left_edge = my_x_pos < edge_threshold
    is_near_right_edge = my_x_pos > (1.0 - edge_threshold)
    is_cornered = is_near_left_edge or is_near_right_edge
    opponent_closing_fast = abs(opp_x_velocity) > 0.3 and distance < 0.3
    height_disadvantage = height_diff < -0.2
    
    # Emergency defensive responses
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health survival mode
    if my_health < critical_health and health_advantage < -0.3:
        if opp_attacking and distance < close_range:
            if my_block_cooldown < 0.2:
                return 6  # Block immediate threat
            else:
                return 0  # Wait for block cooldown
        elif distance > medium_range:
            if my_projectile_cooldown < 0.3:
                return 9  # Keep distance with projectiles
            else:
                # Maintain distance while waiting
                if relative_pos > 0 and not is_near_right_edge:
                    return 2  # Move away
                elif relative_pos < 0 and not is_near_left_edge:
                    return 1  # Move away
                else:
                    return 6  # Block if cornered
        else:
            # Medium range escape
            if is_cornered:
                return 6  # Block when cornered
            else:
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
    
    # Opponent stunned - maximum punishment
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                # Mix heavy and light attacks for optimal damage
                if random.random() < 0.75:
                    return 5  # Prefer kicks for damage
                else:
                    return 4  # Mix in punches for speed
            else:
                # Position for next attack
                if abs(relative_pos) > 0.3:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 0  # Wait in optimal position
        elif distance < medium_range:
            # Close distance quickly
            return 2 if relative_pos > 0 else 1
        else:
            # Too far for melee, use projectile
            if my_projectile_cooldown < 0.2:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Counter opponent attacks
    if opp_attacking:
        if distance < close_range:
            if my_block_cooldown < 0.2:
                # Block and counter-move based on position
                if is_cornered:
                    return 6  # Pure block when cornered
                elif random.random() < 0.6:
                    return 6  # Standard block
                else:
                    # Mobile blocking
                    return 7 if relative_pos > 0 else 8
            else:
                # Cannot block - evade
                if not is_cornered:
                    return 1 if relative_pos > 0 else 2
                else:
                    return 0  # Stay put if cornered
        elif distance < medium_range and opponent_closing_fast:
            # Prepare for incoming pressure
            if my_block_cooldown < 0.3:
                return 8 if relative_pos < 0 else 7  # Block while repositioning
            else:
                return 6  # Standard block
    
    # Winning strategy - controlled aggression
    if health_advantage > winning_margin:
        aggression_factor = min(1.2, 0.8 + (health_advantage * 0.8))
        
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                if opp_blocking:
                    # Break guard tactics
                    action_roll = random.random()
                    if action_roll < 0.4:
                        return 5  # Heavy kick to break block
                    elif action_roll < 0.7:
                        return 4  # Quick punch
                    else:
                        # Reposition for angle attack
                        if not is_cornered:
                            return 2 if relative_pos < 0 else 1