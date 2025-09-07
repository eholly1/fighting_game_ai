"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_010
Rank: 89/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 166.34
- Win Rate: 50.0%
- Average Reward: 237.63

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
    
    # Extract player state information with bounds checking
    my_health = max(0.0, min(1.0, state[3])) if len(state) > 3 else 1.0
    my_position = state[1] if len(state) > 1 else 0.5
    my_velocity = state[2] if len(state) > 2 else 0.0
    my_attack_state = state[7] if len(state) > 7 else 0.0
    my_block_state = state[8] if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_projectile_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent state information
    opp_health = max(0.0, min(1.0, state[14])) if len(state) > 14 else 1.0
    opp_position = state[12] if len(state) > 12 else 0.5
    opp_velocity = state[13] if len(state) > 13 else 0.0
    opp_attack_state = state[18] if len(state) > 18 else 0.0
    opp_block_state = state[19] if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_projectile_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Define hybrid tactical ranges and thresholds
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.32
    long_range = 0.55
    
    # Health-based tactical states
    critical_health = 0.2
    low_health = 0.35
    good_health = 0.65
    excellent_health = 0.85
    
    # Advantage thresholds for adaptive strategy
    desperate_threshold = -0.5
    losing_threshold = -0.2
    even_threshold = 0.1
    winning_threshold = 0.3
    dominating_threshold = 0.5
    
    # Wall proximity detection for positioning
    near_left_wall = my_position < -0.7
    near_right_wall = my_position > 0.7
    near_any_wall = near_left_wall or near_right_wall
    
    # Opponent state analysis
    opponent_attacking = opp_attack_state > 0.5
    opponent_blocking = opp_block_state > 0.5
    opponent_vulnerable = opp_attack_cooldown > 0.3
    opponent_moving_fast = abs(opp_velocity) > 0.3
    
    # My state analysis
    can_attack = my_attack_cooldown < 0.1
    can_projectile = my_projectile_cooldown < 0.1
    am_attacking = my_attack_state > 0.5
    am_blocking = my_block_state > 0.5
    
    # Immediate threat assessment and emergency responses
    immediate_threat = opponent_attacking and distance < 0.18
    projectile_incoming = distance > 0.4 and opp_projectile_cooldown > 0.7
    
    # Emergency blocking system
    if immediate_threat:
        if my_health < low_health:
            # Critical health - prioritize survival
            if near_any_wall:
                return 6  # Block in place
            elif relative_pos > 0.2:
                return 7  # Block and escape left
            else:
                return 8  # Block and escape right
        else:
            # Healthy enough for positioning while blocking
            if distance < ultra_close_range:
                return 6  # Perfect block timing
            elif relative_pos > 0:
                return 7  # Block while repositioning left
            else:
                return 8  # Block while repositioning right
    
    # Critical health survival mode
    if my_health < critical_health:
        if distance > long_range:
            # Maximum range survival
            if can_projectile and not opponent_attacking:
                return 9  # Safe projectile
            elif near_any_wall:
                # Escape from wall
                if near_left_wall:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
            else:
                return 6  # Defensive stance
        
        elif distance > medium_range:
            # Medium range survival
            if opponent_attacking:
                return 6  # Block incoming attacks
            elif can_projectile and random.random() < 0.6:
                return 9  # Harassment projectile
            else:
                # Create more distance
                if relative_pos > 0:
                    return 7  # Move away with block
                else:
                    return 8  # Move away with block
        
        else:
            # Close range survival
            if opponent_vulnerable and can_attack and random.random() < 0.3:
                return 4  # Quick desperate punch
            else:
                return 6  # Block everything
    
    # Determine primary strategy based on health advantage
    if health_advantage < desperate_threshold:
        strategy = "survival"
    elif health_advantage < losing_threshold:
        strategy = "defensive"
    elif health_advantage < even_threshold:
        strategy = "balanced_defensive"
    elif health_advantage < winning_threshold:
        strategy = "balanced_aggressive"
    elif health_advantage < dominating_threshold:
        strategy = "aggressive"
    else:
        strategy = "finish"
    
    # Ultra close range combat (touching distance)
    if distance < ultra_close_range:
        if strategy in ["survival", "defensive"]:
            if opponent_vulnerable and can_attack:
                return 4  # Quick counter punch
            else:
                return 6  # Block everything
        
        elif strategy in ["balanced_defensive", "balanced_aggressive"]:
            if opponent_attacking:
                return 6  # Block first
            elif opponent_vulnerable and can_attack:
                if random.random() < 0.7:
                    return 4  # Fast punch
                else:
                    return 5  # Power kick
            elif opponent_blocking:
                # Mix up against blocking opponent
                if random.random() < 0.4:
                    return 5  # Kick to break guard
                elif random.random() < 0.7:
                    # Reposition around block
                    if relative_pos > 0:
                        return 1  # Move left around
                    else:
                        return 2  # Move right around
                else:
                    return 6  # Block and wait
            else:
                return 4  # Default quick attack
        
        else:  # aggressive or finish
            if opponent_attacking:
                if random.random() < 0.3:
                    return 6  # Sometimes block
                else:
                    return 4  # Trade with quick punch
            elif can_attack:
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Quick punch
                elif attack_choice < 0.8:
                    return 5  # Power kick
                else:
                    return 6  # Fake defensive
            else:
                return 6  # Wait