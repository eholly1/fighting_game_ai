"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_007
Rank: 61/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 209.10
- Win Rate: 0.0%
- Average Reward: 209.10

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
    # Extract and validate key strategic information with defensive bounds
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract my fighter status
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = max(0.0, min(1.0, state[0]))
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[5]
    my_blocking = state[6]
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cd = max(0.0, state[10]) if len(state) > 10 else 1.0
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_pos = max(0.0, min(1.0, state[11]))
    opp_y_pos = state[12]
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16]
    opp_blocking = state[17]
    opp_stunned = state[18] if len(state) > 18 else 0.0
    opp_projectile_cd = max(0.0, state[21]) if len(state) > 21 else 1.0
    
    # Enhanced tactical parameters for evolved hybrid style
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.2
    winning_edge = 0.2
    losing_edge = -0.2
    wall_threshold = 0.12
    
    # Dynamic aggression calculation with momentum consideration
    base_aggression = 0.55
    health_ratio = my_health / max(0.1, opp_health)
    momentum_factor = 0.0
    
    # Calculate momentum based on recent position changes
    if abs(my_x_vel) > 0.3:
        momentum_factor = 0.1 if my_x_vel * relative_pos > 0 else -0.1
    
    # Adaptive aggression based on multiple factors
    if health_advantage > winning_edge:
        dynamic_aggression = min(0.8, base_aggression + 0.2 + momentum_factor)
    elif health_advantage < losing_edge:
        dynamic_aggression = max(0.3, base_aggression - 0.2 + momentum_factor)
    else:
        dynamic_aggression = base_aggression + momentum_factor
    
    # Wall awareness for positioning
    near_left_wall = my_x_pos < wall_threshold
    near_right_wall = my_x_pos > (1.0 - wall_threshold)
    opp_near_left_wall = opp_x_pos < wall_threshold
    opp_near_right_wall = opp_x_pos > (1.0 - wall_threshold)
    
    # Movement prediction for better timing
    predicted_distance = distance
    if abs(opp_x_vel) > 0.2:
        velocity_factor = opp_x_vel * 0.1
        if opp_x_vel * relative_pos < 0:  # Opponent moving toward us
            predicted_distance = max(0.0, distance - abs(velocity_factor))
        else:  # Opponent moving away
            predicted_distance = min(1.0, distance + abs(velocity_factor))
    
    # Cannot act while stunned
    if my_stunned > 0.5:
        return 0
    
    # Enhanced emergency defensive mode
    if my_health < critical_health and health_advantage < -0.4:
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Emergency block
        elif distance > medium_range and my_projectile_cd < 0.15:
            return 9  # Desperation projectile
        elif distance < medium_range:
            # Intelligent escape considering walls and opponent position
            if near_left_wall and relative_pos < 0:
                return 8  # Must go right
            elif near_right_wall and relative_pos > 0:
                return 7  # Must go left
            elif opp_x_vel > 0.3 and relative_pos > 0:  # Opponent chasing from left
                return 8  # Move right with block
            elif opp_x_vel < -0.3 and relative_pos < 0:  # Opponent chasing from right
                return 7  # Move left with block
            else:
                return 6  # Block if unsure
        else:
            return 6  # Default defensive stance
    
    # Enhanced stunned opponent exploitation
    if opp_stunned > 0.5:
        if distance < close_range:
            # Optimized combo based on position and health
            if health_advantage < 0:  # Need quick damage
                return 5  # Kick for maximum damage
            else:
                combo_roll = random.random()
                if combo_roll < 0.4:
                    return 5  # Kick
                elif combo_roll < 0.7:
                    return 4  # Punch
                else:
                    return 3  # Jump attack for style points
        elif distance < medium_range:
            # Smart approach considering opponent recovery time
            if abs(height_diff) > 0.3:
                return 3  # Jump to match height
            elif relative_pos > 0.15:
                return 2  # Move right
            elif relative_pos < -0.15:
                return 1  # Move left
            else:
                return 4  # Attack if close enough
        else:
            if my_projectile_cd < 0.2:
                return 9  # Free projectile
            else:
                return 1 if relative_pos < 0 else 2  # Approach quickly
    
    # Close range combat - evolved hybrid tactics
    if distance < close_range:
        # Enhanced guard break against blocking opponent
        if opp_blocking > 0.5:
            guard_break_roll = random.random()
            if guard_break_roll < 0.2:
                return 5  # Heavy kick to break guard
            elif guard_break_roll < 0.35:
                return 3  # Jump for angle change
            elif guard_break_roll < 0.55:
                # Positioning for better angle
                if not near_right_wall and relative_pos < -0.1:
                    return 2  # Flank right
                elif not near_left_wall and relative_pos > 0.1:
                    return 1  # Flank left
                else:
                    return 4  # Quick punch
            elif guard_break_roll < 0.75:
                return 4  # Quick punch to probe
            else:
                # Tactical retreat and re-engage
                if my_x_pos > 0.5:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
        
        # Counter-attack optimization against attacking opponent
        elif opp_attacking > 0.5:
            if health_advantage < losing_edge:
                return 6  # Prioritize defense when losing
            else:
                counter_roll = random.random()
                if counter_roll < 0.45:
                    return 6  # Block first
                elif counter_roll < 0.7:
                    return 4  # Quick counter