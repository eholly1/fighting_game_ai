"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_008
Rank: 100/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 122.59
- Win Rate: 0.0%
- Average Reward: 175.13

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
    my_health = max(0.0, state[1] if len(state) > 1 else 0.5)
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent status
    opp_health = max(0.0, state[12] if len(state) > 12 else 0.5)
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    opp_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid strategic parameters
    close_threshold = 0.16
    medium_threshold = 0.32
    far_threshold = 0.55
    critical_health = 0.22
    winning_threshold = 0.25
    losing_threshold = -0.25
    corner_threshold = 0.75
    
    # Calculate situational awareness
    is_airborne = abs(my_velocity_y) > 0.15 or abs(my_y_pos) > 0.1
    opponent_airborne = abs(height_diff) > 0.25
    opponent_attacking = opp_attack_status > 0.6
    opponent_blocking = opp_block_status > 0.6
    near_corner = abs(my_x_pos) > corner_threshold
    opponent_near_corner = abs(opp_x_pos) > corner_threshold
    can_projectile = my_projectile_cooldown < 0.2
    opponent_can_projectile = opp_projectile_cooldown < 0.3
    
    # Calculate momentum and positioning factors
    closing_speed = abs(my_velocity_x) if (my_velocity_x > 0 and relative_pos > 0) or (my_velocity_x < 0 and relative_pos < 0) else 0
    retreating = (my_velocity_x < 0 and relative_pos > 0) or (my_velocity_x > 0 and relative_pos < 0)
    opponent_approaching = (opp_velocity_x > 0 and relative_pos < 0) or (opp_velocity_x < 0 and relative_pos > 0)
    
    # Emergency survival tactics
    if my_health < critical_health and health_advantage < -0.5:
        if opponent_attacking and distance < 0.25:
            return 6  # Emergency block
        if distance > 0.7 and can_projectile:
            return 9  # Desperate projectile
        if near_corner:
            if my_x_pos > 0:
                return 7  # Escape corner left with block
            else:
                return 8  # Escape corner right with block
        if distance < close_threshold:
            # Last ditch attack
            return 5 if random.random() < 0.7 else 4
        else:
            # Defensive movement
            if relative_pos > 0:
                return 7
            else:
                return 8
    
    # Aggressive winning strategy
    if health_advantage > winning_threshold and my_health > 0.35:
        if distance < close_threshold:
            if opponent_blocking:
                # Break guard tactics
                guard_break = random.random()
                if guard_break < 0.35:
                    return 5  # Heavy kick
                elif guard_break < 0.6:
                    return 3  # Jump mix-up
                elif guard_break < 0.8:
                    return 4  # Fast punch
                else:
                    return 9 if can_projectile else 4  # Point blank projectile or punch
            elif opponent_attacking:
                # Counter attack aggressively
                if random.random() < 0.6:
                    return 4  # Quick counter
                else:
                    return 5  # Power counter
            else:
                # Pure aggression
                if opponent_airborne:
                    return 4  # Anti-air
                elif random.random() < 0.55:
                    return 4  # Fast pressure
                else:
                    return 5  # Power attack
        
        elif distance < medium_threshold:
            # Aggressive approach
            if opponent_near_corner:
                # Corner pressure
                if relative_pos > 0:
                    return 2  # Chase to corner
                else:
                    return 1  # Chase to corner
            elif opponent_attacking or opponent_approaching:
                # Meet aggression with aggression
                if relative_pos > 0:
                    return 2  # Advance right
                else:
                    return 1  # Advance left
            else:
                # Standard aggressive positioning
                approach_choice = random.random()
                if approach_choice < 0.4:
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                elif approach_choice < 0.6:
                    return 3  # Jump approach
                elif approach_choice < 0.8:
                    return 4  # Advancing punch
                else:
                    return 9 if can_projectile else 2 if relative_pos > 0 else 1
        
        else:
            # Long range dominance
            if can_projectile and random.random() < 0.65:
                return 9  # Projectile pressure
            else:
                # Close distance for kill
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Defensive strategy when losing
    elif health_advantage < losing_threshold:
        if distance < close_threshold:
            if opponent_attacking:
                return 6  # Defensive block
            elif opponent_blocking:
                # Try to create space
                if near_corner:
                    if my_x_pos > 0:
                        return 7  # Escape left
                    else:
                        return 8  # Escape right
                else:
                    # Reset with jump or careful attack
                    if random.random() < 0.6:
                        return 3  # Jump reset
                    else:
                        return 4  # Safe poke
            else:
                # Careful counterattack
                if my_attack_status < 0.3:
                    if random.random() < 0.45:
                        return 4  # Safe punch
                    elif random.random() < 0.7:
                        return 6  # Block and wait