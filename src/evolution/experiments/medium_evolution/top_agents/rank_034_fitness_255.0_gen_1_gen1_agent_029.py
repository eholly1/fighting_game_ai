"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_029
Rank: 34/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 255.02
- Win Rate: 50.0%
- Average Reward: 255.02

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
    my_stunned = state[7]
    my_projectile_cd = max(0.0, state[10])
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_pos = max(0.0, min(1.0, state[11]))
    opp_y_pos = state[12]
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16]
    opp_blocking = state[17]
    opp_stunned = state[18]
    opp_projectile_cd = max(0.0, state[21]) if len(state) > 21 else 1.0
    
    # Define tactical parameters for hybrid style
    close_range = 0.13
    medium_range = 0.32
    far_range = 0.48
    critical_health = 0.25
    winning_edge = 0.15
    losing_edge = -0.15
    wall_distance = 0.15
    
    # Calculate dynamic aggression based on situation
    base_aggression = 0.5  # Hybrid baseline
    if health_advantage > winning_edge:
        base_aggression = 0.65  # More aggressive when ahead
    elif health_advantage < losing_edge:
        base_aggression = 0.35  # More defensive when behind
    
    # Edge position awareness
    near_left_wall = my_x_pos < wall_distance
    near_right_wall = my_x_pos > (1.0 - wall_distance)
    opp_near_left_wall = opp_x_pos < wall_distance
    opp_near_right_wall = opp_x_pos > (1.0 - wall_distance)
    
    # Cannot act while stunned
    if my_stunned > 0.5:
        return 0
    
    # Emergency defensive mode - critical health
    if my_health < critical_health and health_advantage < -0.3:
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Block incoming attack
        elif distance > medium_range and my_projectile_cd < 0.2:
            return 9  # Keep distance with projectile
        elif distance < medium_range:
            # Escape while blocking
            if near_left_wall:
                return 8  # Can only go right
            elif near_right_wall:
                return 7  # Can only go left
            else:
                return 7 if relative_pos > 0 else 8  # Move away from opponent
        else:
            return 6  # Default block
    
    # Capitalize on stunned opponent
    if opp_stunned > 0.5:
        if distance < close_range:
            # Mix attacks for unpredictability
            if random.random() < 0.6:
                return 5  # Kick for more damage
            else:
                return 4  # Punch for speed
        elif distance < medium_range:
            # Close distance quickly
            if relative_pos > 0.1:
                return 2  # Move right
            elif relative_pos < -0.1:
                return 1  # Move left
            else:
                return 4  # Attack if close enough
        else:
            return 9 if my_projectile_cd < 0.3 else 1  # Projectile or approach
    
    # Close range tactics (primary engagement range)
    if distance < close_range:
        # Opponent is blocking - need to break guard or reposition
        if opp_blocking > 0.5:
            action_roll = random.random()
            if action_roll < 0.25:
                return 5  # Strong kick to break guard
            elif action_roll < 0.45:
                return 3  # Jump to change angle
            elif action_roll < 0.7:
                # Try to flank
                if not near_right_wall and relative_pos < 0:
                    return 2  # Move right around them
                elif not near_left_wall and relative_pos > 0:
                    return 1  # Move left around them
                else:
                    return 5  # Kick if can't flank
            else:
                return 4  # Quick punch
        
        # Opponent is attacking - defend or counter
        elif opp_attacking > 0.5:
            if health_advantage < losing_edge:
                return 6  # Block when losing
            elif my_blocking < 0.3:  # Not already blocking
                counter_roll = random.random()
                if counter_roll < 0.4:
                    return 6  # Block first
                elif counter_roll < 0.7:
                    return 4  # Quick counter
                else:
                    return 5  # Strong counter
            else:
                return 4  # Quick counter if already blocking
        
        # Neutral close combat
        else:
            if health_advantage > winning_edge:
                # Aggressive when winning
                attack_roll = random.random()
                if attack_roll < 0.45:
                    return 4  # Punch
                elif attack_roll < 0.75:
                    return 5  # Kick
                elif attack_roll < 0.9:
                    return 3  # Jump attack setup
                else:
                    return 6  # Occasional block
            elif health_advantage < losing_edge:
                # Cautious when losing
                caution_roll = random.random()
                if caution_roll < 0.35:
                    return 6  # Block more often
                elif caution_roll < 0.65:
                    return 4  # Safe punch
                elif caution_roll < 0.85:
                    return 5  # Kick
                else:
                    return 3  # Jump
            else:
                # Balanced hybrid approach
                balance_roll = random.random()
                if balance_roll < 0.35:
                    return 4  # Punch
                elif balance_roll < 0.6:
                    return 5  # Kick
                elif balance_roll < 0.8:
                    return 6  # Block
                else:
                    return 3  # Jump
    
    # Medium range tactics (positioning and transition range)
    elif distance < medium_range:
        # Handle opponent projectile threat
        if opp_projectile_cd < 0.3 and distance > 0.2:
            evasion_roll = random.random()
            if evasion_roll < 0.3:
                return 3  # Jump to avoid
            elif evasion_roll < 0.6:
                # Move with block
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                return 6  # Block projectile
        
        # Corner opponent if they're near wall
        if opp_near_left_wall and relative_pos < 0:
            return 1  # Press the advantage