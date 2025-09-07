"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_021
Rank: 55/100
Generation: 0
Fighting Style: defensive

Performance Metrics:
- Fitness: 218.43
- Win Rate: 50.0%
- Average Reward: 236.86

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
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract player state information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_vel = state[3] if len(state) > 3 else 0.0
    my_y_vel = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent state information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_vel = state[14] if len(state) > 14 else 0.0
    opp_y_vel = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    opp_stunned = state[18] if len(state) > 18 else 0.0
    
    # Define defensive strategic thresholds
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    safe_range = 0.5
    
    # Defensive parameters
    block_threshold = 0.15
    retreat_health_threshold = -0.2
    counter_attack_threshold = 0.3
    projectile_safe_distance = 0.35
    
    # Emergency defensive situations
    if my_stunned > 0.5:
        return 6  # Block while stunned
    
    # Critical health - ultra defensive
    if health_advantage < -0.6 or my_health < 0.3:
        if distance < close_range:
            if opp_attacking > 0.5:
                return 6  # Block incoming attack
            else:
                # Try to create distance while blocking
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        elif distance < medium_range:
            # Back away while ready to block
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        else:
            # At safe distance, use projectiles carefully
            if my_projectile_cooldown < 0.3:
                return 9  # Safe projectile
            else:
                return 6  # Block and wait
    
    # Opponent is attacking - defensive response
    if opp_attacking > 0.5:
        if distance < block_threshold:
            return 6  # Block close attacks
        elif distance < medium_range:
            # Maintain distance and prepare counter
            if relative_pos > 0:
                return 7  # Move away with block
            else:
                return 8  # Move away with block
        else:
            # Far enough to avoid, prepare counter
            return 6  # Stay ready to block
    
    # Opponent is blocking - respect their defense
    if opp_blocking > 0.5:
        if distance < close_range:
            # Don't attack into block, create space
            if relative_pos > 0:
                return 1  # Move left to reposition
            else:
                return 2  # Move right to reposition
        elif distance < medium_range:
            # Wait for opening or use projectile
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile against block
            else:
                return 6  # Block and wait
        else:
            # Safe projectile harassment
            return 9 if my_projectile_cooldown < 0.3 else 6
    
    # Opponent is stunned - careful counter attack
    if opp_stunned > 0.5:
        if distance < close_range:
            # Quick counter attack
            if health_advantage > 0:
                return 4  # Safe punch
            else:
                return 6  # Still be defensive
        elif distance < medium_range:
            # Move in for counter but carefully
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        else:
            # Projectile on stunned opponent
            return 9 if my_projectile_cooldown < 0.4 else 6
    
    # Range-based defensive tactics
    if distance < close_range:
        # Close range - high danger, prioritize defense
        if health_advantage < retreat_health_threshold:
            # Losing, need to escape
            if abs(my_x_pos) > 0.7:  # Near corner
                if my_x_pos > 0:  # Right corner
                    return 7  # Move left with block
                else:  # Left corner
                    return 8  # Move right with block
            else:
                # Retreat to safer distance
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        elif health_advantage > counter_attack_threshold:
            # Winning, can afford calculated risks
            if random.random() < 0.3:  # Conservative attack frequency
                return 4 if random.random() < 0.7 else 5  # Prefer quick punch
            else:
                return 6  # Block most of the time
        
        else:
            # Even match, very defensive
            if random.random() < 0.15:  # Very low attack frequency
                return 4  # Quick punch only
            else:
                return 6  # Block primarily
    
    elif distance < medium_range:
        # Medium range - positioning phase
        if health_advantage < retreat_health_threshold:
            # Losing, maintain distance
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        
        elif abs(my_x_pos) > 0.8:  # Too close to corner
            # Escape corner danger
            if my_x_pos > 0:  # Right corner
                return 7  # Move left with block
            else:  # Left corner
                return 8  # Move right with block
        
        elif opp_x_vel != 0 and abs(opp_x_vel) > 0.1:
            # Opponent moving, stay defensive
            return 6  # Block and observe
        
        else:
            # Careful positioning
            if health_advantage > 0.1:
                # Slight advantage, can advance carefully
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block