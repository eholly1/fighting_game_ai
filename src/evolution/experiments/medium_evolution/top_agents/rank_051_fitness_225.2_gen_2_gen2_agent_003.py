"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_003
Rank: 51/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 225.16
- Win Rate: 0.0%
- Average Reward: 321.66

Created: 2025-06-01 02:16:30
Lineage: Original

Tournament Stats:
None
"""

# Agent Code:
def get_action(state):
    import random
    import math
    import numpy as np
    
    # Extract and validate key state information with bounds checking
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract my fighter information
    my_x_pos = state[0]
    my_y_pos = state[1] 
    my_health = max(0.0, min(1.0, state[2]))
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[5]
    my_blocking = state[6]
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cd = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_x_pos = state[11]
    opp_y_pos = state[12]
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16]
    opp_blocking = state[17]
    opp_stunned = state[18] if len(state) > 18 else 0.0
    
    # Enhanced strategic parameters - evolved balanced approach
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.55
    
    # Dynamic aggression system
    base_aggression = 0.68
    health_ratio = my_health / max(0.1, opp_health)
    
    # Calculate adaptive aggression
    if health_advantage > 0.4:
        aggression_level = min(0.85, base_aggression * 1.4)
    elif health_advantage > 0.1:
        aggression_level = base_aggression * 1.2
    elif health_advantage < -0.4:
        aggression_level = max(0.35, base_aggression * 0.6)
    elif health_advantage < -0.1:
        aggression_level = base_aggression * 0.8
    else:
        aggression_level = base_aggression
    
    # Position awareness - wall proximity
    near_left_wall = my_x_pos < 0.25
    near_right_wall = my_x_pos > 0.75
    in_corner = near_left_wall or near_right_wall
    
    # Velocity-based predictions
    opp_approaching = (relative_pos > 0 and opp_x_vel > 0.2) or (relative_pos < 0 and opp_x_vel < -0.2)
    opp_retreating = (relative_pos > 0 and opp_x_vel < -0.2) or (relative_pos < 0 and opp_x_vel > 0.2)
    
    # Emergency overrides
    if my_stunned > 0.5:
        return 0  # Cannot act while stunned
    
    # Critical health management with improved logic
    if my_health < 0.2:
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Emergency block
        elif distance > medium_range and my_projectile_cd < 0.1:
            return 9  # Desperate projectile
        elif distance < far_range:
            # Enhanced escape logic
            if in_corner:
                # Break out of corner
                if near_left_wall and relative_pos < 0:
                    return 8  # Move right with block
                elif near_right_wall and relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 3  # Jump to escape
            else:
                # General retreat with defense
                escape_action = 7 if relative_pos > 0 else 8
                return escape_action
    
    # Opponent stunned - enhanced punishment
    if opp_stunned > 0.5:
        if distance < close_range:
            # Maximum damage combo
            combo_selector = random.random()
            if combo_selector < 0.45:
                return 5  # Heavy kick for maximum damage
            elif combo_selector < 0.7:
                return 4  # Quick punch for consistent damage
            else:
                return 3  # Jump attack for positioning
        elif distance < medium_range:
            # Close distance quickly
            if abs(height_diff) > 0.3:
                return 3  # Jump to close height gap
            elif relative_pos > 0.05:
                return 2  # Move right
            elif relative_pos < -0.05:
                return 1  # Move left
            else:
                return 4  # Attack if close enough
        else:
            # Long range punishment
            if my_projectile_cd < 0.3:
                return 9  # Projectile
            else:
                return 2 if relative_pos > 0 else 1  # Close distance
    
    # Enhanced defensive responses to opponent attacks
    if opp_attacking > 0.5:
        if distance < close_range:
            # Close range defense with counter-attack opportunities
            if my_health > opp_health * 1.3:
                # Counter-attack when healthy
                counter_choice = random.random()
                if counter_choice < 0.4:
                    return 4  # Quick counter
                elif counter_choice < 0.6:
                    return 6  # Safe block
                else:
                    return 3  # Jump counter
            else:
                # Conservative defense
                defense_choice = random.random()
                if defense_choice < 0.7:
                    return 6  # Block primary
                else:
                    return 7 if relative_pos > 0 else 8  # Evasive movement
        elif distance < medium_range:
            # Medium range threat assessment
            if opp_approaching:
                if my_projectile_cd < 0.2:
                    return 9  # Interrupt approach
                else:
                    return 6  # Prepare defense
            else:
                # Maintain range and pressure
                if my_projectile_cd < 0.4:
                    return 9  # Ranged pressure
                else:
                    return 6  # Block preparation
    
    # CLOSE RANGE COMBAT - Enhanced hybrid approach
    if distance <= close_range:
        # Advanced guard break system
        if opp_blocking > 0.6:
            guard_break_choice = random.random()
            if guard_break_choice < 0.3:
                return 5  # Heavy kick
            elif guard_break_choice < 0.5:
                return 3  # Jump attack
            elif guard_break_choice < 0.7:
                # Reposition for better angle
                if abs(my_x_vel) < 0.1:  # Not moving
                    return 2 if my_x_pos < opp_x_pos else 1
                else:
                    return 4  # Quick jab
            else:
                # Feint with movement
                return 7 if random.random() < 0.5 else 8
        
        # Enhanced attack selection against open opponent
        elif my_attacking < 0.2:
            # Height-based attack optimization
            if abs(height_diff) > 0.25:
                if my_y_pos < opp_y_pos - 0.2:
                    return 3  # Jump up attack
                elif my_y_pos > opp_y_pos + 0.2:
                    return 5  # Downward kick
            
            #