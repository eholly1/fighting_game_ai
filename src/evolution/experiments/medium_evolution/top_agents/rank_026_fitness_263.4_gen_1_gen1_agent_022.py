"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_022
Rank: 26/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 263.40
- Win Rate: 50.0%
- Average Reward: 263.40

Created: 2025-06-01 01:24:51
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
    
    # Hybrid strategic parameters - balanced approach
    close_range = 0.14
    medium_range = 0.32
    far_range = 0.50
    
    # Adaptive aggression based on situation
    base_aggression = 0.65
    defensive_threshold = 0.4
    aggressive_threshold = 0.8
    
    # Health-based strategic adjustment
    health_ratio = my_health / max(0.1, opp_health)
    critical_health = 0.25
    winning_health = 0.7
    
    # Calculate dynamic aggression level
    if health_advantage > 0.3:
        aggression_level = min(aggressive_threshold, base_aggression * 1.3)
    elif health_advantage < -0.3:
        aggression_level = max(defensive_threshold, base_aggression * 0.7)
    else:
        aggression_level = base_aggression
    
    # Emergency situations - override normal strategy
    if my_stunned > 0.5:
        return 0  # Cannot act while stunned
    
    # Critical health management
    if my_health < critical_health:
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Emergency block
        elif distance > medium_range and my_projectile_cd < 0.2:
            return 9  # Keep away with projectiles
        elif distance < medium_range:
            # Escape while blocking
            if my_x_pos < 0.2:  # Near left wall
                return 8  # Move right with block
            elif my_x_pos > 0.8:  # Near right wall  
                return 7  # Move left with block
            else:
                return 7 if relative_pos > 0 else 8  # Move away with block
    
    # Opponent stunned - capitalize with balanced approach
    if opp_stunned > 0.5:
        if distance < close_range:
            combo_choice = random.random()
            if combo_choice < 0.4:
                return 5  # Heavy kick for damage
            elif combo_choice < 0.7:
                return 4  # Quick punch
            else:
                return 3  # Jump attack for mix-up
        elif distance < medium_range:
            # Close distance efficiently
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        else:
            return 9  # Projectile if too far
    
    # Opponent attacking - balanced defensive response
    if opp_attacking > 0.5:
        if distance < close_range:
            defensive_choice = random.random()
            if defensive_choice < 0.6:
                return 6  # Block primary option
            elif defensive_choice < 0.8:
                return 4  # Counter attack
            else:
                return 7 if relative_pos > 0 else 8  # Evasive movement
        elif distance < medium_range:
            # Prepare for approach
            if abs(opp_x_vel) > 0.4:  # Opponent rushing
                return 6  # Block preparation
            else:
                return 9 if my_projectile_cd < 0.3 else 6  # Projectile or block
    
    # CLOSE RANGE COMBAT - Hybrid approach
    if distance <= close_range:
        # Opponent blocking - mix-up strategy
        if opp_blocking > 0.5:
            mixup_choice = random.random()
            if mixup_choice < 0.25:
                return 5  # Strong kick to break guard
            elif mixup_choice < 0.45:
                return 3  # Jump to change angle
            elif mixup_choice < 0.65:
                return 4  # Quick punch
            else:
                # Reposition for better angle
                side_choice = random.random()
                if side_choice < 0.5:
                    return 1 if my_x_pos > 0.3 else 2  # Move to open side
                else:
                    return 2 if my_x_pos < 0.7 else 1  # Move to open side
        
        # Open opponent - attack based on aggression level
        elif my_attacking < 0.3:  # Not currently attacking
            if random.random() < aggression_level:
                # Height-based attack selection
                if abs(height_diff) > 0.3:
                    if my_y_pos < opp_y_pos:
                        return 3  # Jump to reach
                    else:
                        return 5  # Kick from above
                
                # Standard attack selection
                attack_choice = random.random()
                if attack_choice < 0.55:
                    return 4  # Punch - faster
                else:
                    return 5  # Kick - stronger
            else:
                # More defensive approach
                if health_advantage < 0:
                    return 6  # Block when losing
                else:
                    return 4  # Safe punch
        
        # Currently attacking or cooling down
        else:
            # Maintain position and pressure
            if abs(relative_pos) > 0.2:
                return 2 if relative_pos > 0 else 1  # Stay close
            else:
                return 0  # Wait for attack cooldown
    
    # MEDIUM RANGE COMBAT - Positioning and control
    elif distance <= medium_range:
        # Projectile opportunity
        if my_projectile_cd < 0.2 and random.random() < 0.4:
            return 9
        
        # Approach vs. maintain distance decision
        approach_decision = random.random()
        
        if approach_decision < aggression_level:
            # Aggressive approach
            if abs(height_diff) > 0.4:
                return 3  # Jump to close height gap
            
            # Smart approach based on opponent state
            if opp_blocking > 0.3:
                # Cautious approach against blocking opponent
                if relative_pos > 0.1:
                    return 8  # Move right with block
                elif relative_pos < -0.1:
                    return 7  # Move left with block
                else:
                    return 6  # Block and wait
            else:
                # Direct approach against open opponent
                if relative_pos > 0.1:
                    return