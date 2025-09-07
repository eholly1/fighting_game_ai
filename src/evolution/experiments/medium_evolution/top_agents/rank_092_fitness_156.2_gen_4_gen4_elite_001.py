"""
Hall of Fame Agent
==================

Agent ID: gen4_elite_001
Rank: 92/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 156.23
- Win Rate: 0.0%
- Average Reward: 223.18

Created: 2025-06-01 03:58:23
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
    
    # Advanced tactical parameters
    close_range = 0.14
    medium_range = 0.32
    far_range = 0.5
    
    # Enhanced adaptive aggression system
    base_aggression = 0.65
    health_ratio = my_health / max(0.05, opp_health)
    momentum_factor = health_advantage * 0.3
    
    # Calculate dynamic aggression level
    if health_advantage > 0.5:
        aggression_level = min(0.9, base_aggression * 1.6 + momentum_factor)
    elif health_advantage > 0.2:
        aggression_level = base_aggression * 1.3 + momentum_factor
    elif health_advantage < -0.5:
        aggression_level = max(0.25, base_aggression * 0.5 + momentum_factor)
    elif health_advantage < -0.2:
        aggression_level = base_aggression * 0.7 + momentum_factor
    else:
        aggression_level = base_aggression + momentum_factor * 0.5
    
    # Enhanced positioning awareness
    near_left_wall = my_x_pos < 0.2
    near_right_wall = my_x_pos > 0.8
    in_corner = near_left_wall or near_right_wall
    center_stage = 0.3 < my_x_pos < 0.7
    
    # Advanced movement prediction
    opp_closing_fast = (relative_pos > 0 and opp_x_vel > 0.25) or (relative_pos < 0 and opp_x_vel < -0.25)
    opp_retreating_fast = (relative_pos > 0 and opp_x_vel < -0.25) or (relative_pos < 0 and opp_x_vel > 0.25)
    opp_aerial = abs(opp_y_vel) > 0.2 or abs(height_diff) > 0.3
    
    # Critical state overrides
    if my_stunned > 0.5:
        return 0
    
    # Enhanced critical health management
    if my_health < 0.25:
        if opp_attacking > 0.6 and distance < close_range:
            return 6  # Emergency defense
        elif distance > medium_range and my_projectile_cd < 0.15:
            if random.random() < 0.8:
                return 9  # Projectile harassment
        
        # Improved escape sequences
        if distance < medium_range:
            if in_corner:
                if near_left_wall and relative_pos <= 0:
                    return 8 if random.random() < 0.7 else 3
                elif near_right_wall and relative_pos >= 0:
                    return 7 if random.random() < 0.7 else 3
                else:
                    return 3  # Jump escape
            else:
                # Enhanced retreat with options
                if opp_closing_fast:
                    return 6  # Block incoming rush
                else:
                    retreat_choice = random.random()
                    if retreat_choice < 0.6:
                        return 7 if relative_pos > 0 else 8
                    elif retreat_choice < 0.8:
                        return 3  # Jump retreat
                    else:
                        return 9 if my_projectile_cd < 0.3 else 6
    
    # Enhanced opponent vulnerability exploitation
    if opp_stunned > 0.4:
        if distance <= close_range:
            # Maximum damage combinations
            if abs(height_diff) > 0.2:
                if my_y_pos < opp_y_pos:
                    return 3  # Jump strike
                else:
                    return 5  # Downward kick
            else:
                combo_roll = random.random()
                if combo_roll < 0.5:
                    return 5  # Heavy damage
                elif combo_roll < 0.75:
                    return 4  # Fast follow-up
                else:
                    return 3  # Repositioning attack
        elif distance <= medium_range:
            # Quick gap closing
            if abs(height_diff) > 0.25:
                return 3
            elif my_projectile_cd < 0.2 and random.random() < 0.4:
                return 9  # Projectile punish
            else:
                return 2 if relative_pos > 0 else 1
        else:
            # Long range punishment
            if my_projectile_cd < 0.25:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Advanced defensive responses with counter-attack options
    if opp_attacking > 0.6:
        if distance <= close_range:
            # Close range defense with calculated risks
            if aggression_level > 0.7 and my_health > opp_health * 1.2:
                # Aggressive counter system
                counter_roll = random.random()
                if counter_roll < 0.35:
                    return 4  # Quick counter
                elif counter_roll < 0.55:
                    return 3  # Jump counter
                elif counter_roll < 0.75:
                    return 6  # Safe block
                else:
                    return 5  # Risk/reward counter
            else:
                # Conservative defense with mobility
                defense_roll = random.random()
                if defense_roll < 0.6:
                    return 6  # Primary defense
                elif defense_roll < 0.8:
                    return 7 if relative_pos > 0 else 8  # Evasive movement
                else:
                    return 3  # Jump defense
        elif distance <= medium_range:
            # Medium range threat response
            if opp_closing_fast:
                if my_projectile_cd < 0.2 and random.random() < 0.6:
                    return 9  # Interrupt approach
                else:
                    return 6  # Prepare defense
            else:
                # Maintain range advantage
                if my_projectile_cd < 0.3:
                    return 9
                elif aggression_level > 0.6:
                    return 2 if relative_pos > 0 else 1