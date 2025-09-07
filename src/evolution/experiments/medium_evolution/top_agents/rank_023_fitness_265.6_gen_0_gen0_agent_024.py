"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_024
Rank: 23/100
Generation: 0
Fighting Style: adaptive

Performance Metrics:
- Fitness: 265.58
- Win Rate: 50.0%
- Average Reward: 265.58

Created: 2025-06-01 00:36:59
Lineage: Original

Tournament Stats:
None
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract key strategic information with defensive bounds checking
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract player state information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x = state[0] if len(state) > 0 else 0.5
    my_attacking = state[4] if len(state) > 4 else 0.0
    my_blocking = state[5] if len(state) > 5 else 0.0
    my_projectile_cd = state[6] if len(state) > 6 else 0.0
    
    # Extract opponent state information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x = state[11] if len(state) > 11 else 0.5
    opp_attacking = state[15] if len(state) > 15 else 0.0
    opp_blocking = state[16] if len(state) > 16 else 0.0
    opp_projectile_cd = state[17] if len(state) > 17 else 0.0
    
    # Define tactical thresholds
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    
    # Health-based aggression levels
    desperate_threshold = -0.4
    losing_threshold = -0.15
    winning_threshold = 0.15
    dominating_threshold = 0.4
    
    # Adaptive strategy decision tree
    strategy_mode = "balanced"
    
    if health_advantage < desperate_threshold:
        strategy_mode = "desperate"
    elif health_advantage < losing_threshold:
        strategy_mode = "defensive"
    elif health_advantage > dominating_threshold:
        strategy_mode = "aggressive"
    elif health_advantage > winning_threshold:
        strategy_mode = "pressure"
    
    # Emergency blocking when opponent is attacking and close
    if opp_attacking > 0.5 and distance < 0.2:
        block_chance = 0.8 if strategy_mode in ["desperate", "defensive"] else 0.6
        if random.random() < block_chance:
            # Block while positioning
            if relative_pos > 0.3:
                return 8  # move_right_block
            elif relative_pos < -0.3:
                return 7  # move_left_block
            else:
                return 6  # block
    
    # Desperate strategy - survival focus
    if strategy_mode == "desperate":
        if distance > far_range:
            # Stay far and use projectiles
            if my_projectile_cd < 0.3:
                return 9  # projectile
            else:
                # Maintain distance
                if relative_pos > 0:
                    return 1  # move_left
                else:
                    return 2  # move_right
        
        elif distance > medium_range:
            # Medium range - careful positioning
            if opp_attacking > 0.3:
                return 6  # block
            else:
                # Try to get to projectile range
                if relative_pos > 0:
                    return 1  # move_left
                else:
                    return 2  # move_right
        
        else:
            # Close range - mostly defensive
            if opp_attacking > 0.2:
                return 6  # block
            elif random.random() < 0.3:
                # Occasional quick attack
                return 4  # punch
            else:
                # Try to escape
                if abs(my_x - 0.5) < 0.3:  # Not near wall
                    if relative_pos > 0:
                        return 1  # move_left
                    else:
                        return 2  # move_right
                else:
                    return 6  # block
    
    # Defensive strategy - cautious play
    elif strategy_mode == "defensive":
        if distance > far_range:
            # Long range harassment
            if my_projectile_cd < 0.4 and random.random() < 0.7:
                return 9  # projectile
            else:
                # Control spacing
                if distance > 0.8:
                    # Get closer for projectile accuracy
                    if relative_pos > 0:
                        return 2  # move_right
                    else:
                        return 1  # move_left
                else:
                    return 0  # idle
        
        elif distance > medium_range:
            # Medium range - careful positioning
            if opp_attacking > 0.4:
                return 6  # block
            elif my_projectile_cd < 0.3:
                return 9  # projectile
            else:
                # Maintain optimal distance
                if distance < 0.25:
                    # Back away
                    if relative_pos > 0:
                        return 1  # move_left
                    else:
                        return 2  # move_right
                else:
                    return 0  # idle
        
        else:
            # Close range - mixed defense and counter-attack
            if opp_attacking > 0.3:
                return 6  # block
            elif opp_blocking > 0.5:
                # Opponent blocking, try to reposition
                if relative_pos > 0:
                    return 1  # move_left
                else:
                    return 2  # move_right
            elif random.random() < 0.4:
                # Counter-attack opportunity
                attack_choice = random.random()
                if attack_choice < 0.6:
                    return 4  # punch
                else:
                    return 5  # kick
            else:
                # Create space
                if relative_pos > 0:
                    return 1  # move_left
                else:
                    return 2  # move_right
    
    # Balanced strategy - adaptive play
    elif strategy_mode == "balanced":
        if distance > far_range:
            # Long range - projectile game
            if my_projectile_cd < 0.5:
                projectile_chance = 0.7 if opp_projectile_cd > 0.5 else 0.5
                if random.random() < projectile_chance:
                    return 9  # projectile
            
            # Positioning for projectiles
            if distance > 0.85:
                if relative_pos > 0:
                    return 2  # move_right
                else:
                    return 1  # move_left
            else:
                positioning_choice = random.random()
                if positioning_choice < 0.4:
                    if relative_pos > 0:
                        return 2  # move_right
                    else:
                        return 1  # move_left
                else:
                    return 0  # idle
        
        elif distance > medium_range:
            # Medium range - tactical positioning
            if opp_attacking > 0.4:
                return 6  # block
            
            action_choice = random.random()
            if action_choice < 0.3 and my_projectile_cd < 0.4:
                return 9  # projectile
            elif action_choice < 0.6:
                # Advance for attack
                if relative_pos > 0:
                    return 2  # move_right
                else:
                    return 1  # move_left
            elif action_choice < 0.8:
                # Wait and observe
                return 0  # idle
            else:
                # Jump for positioning
                return 3  # jump