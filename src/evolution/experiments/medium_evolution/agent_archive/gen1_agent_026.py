"""
Evolutionary Agent: gen1_agent_026
==================================

Metadata:
{
  "generation": 1,
  "fitness": -5.0800000000003145,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 32238b1375301a48
Serialization Version: 1.0
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
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cooldown = max(0.0, state[8])
    my_attack_cooldown = max(0.0, state[9])
    my_block_cooldown = max(0.0, state[10])
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cooldown = max(0.0, state[19])
    opp_attack_cooldown = max(0.0, state[20])
    opp_block_cooldown = max(0.0, state[21])
    
    # Define hybrid fighter strategic ranges
    close_range = 0.14
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_health_advantage = 0.25
    losing_health_advantage = -0.25
    
    # Calculate adaptive aggression based on multiple factors
    base_aggression = 0.7
    aggression_modifier = 1.0
    
    # Health-based aggression adjustment
    if health_advantage > winning_health_advantage:
        aggression_modifier = 1.4  # More aggressive when winning
    elif health_advantage < losing_health_advantage:
        aggression_modifier = 0.5  # More defensive when losing
    elif my_health < critical_health:
        aggression_modifier = 0.3  # Very defensive when low health
    
    # Distance-based aggression
    if distance < close_range:
        aggression_modifier *= 1.2  # More aggressive up close
    elif distance > far_range:
        aggression_modifier *= 0.8  # More cautious at range
    
    current_aggression = base_aggression * aggression_modifier
    
    # Calculate stage positioning
    stage_left_edge = 0.15
    stage_right_edge = 0.85
    my_near_left_corner = my_x_pos < stage_left_edge
    my_near_right_corner = my_x_pos > stage_right_edge
    opp_near_left_corner = opp_x_pos < stage_left_edge
    opp_near_right_corner = opp_x_pos > stage_right_edge
    
    # Emergency situations - highest priority
    if my_stunned:
        if distance < close_range and opp_attacking:
            return 6  # Block when stunned and under attack
        elif distance < medium_range:
            # Try to create space while stunned
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            return 6  # Block and recover
    
    # Critical health survival mode
    if my_health < critical_health and health_advantage < -0.3:
        if distance < close_range and opp_attacking:
            return 6  # Defensive blocking
        elif distance > medium_range:
            if my_projectile_cooldown < 0.2:
                return 9  # Safe projectile attacks
            else:
                # Maintain distance defensively
                if relative_pos > 0:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
        else:
            # Medium range - careful positioning
            if my_near_left_corner:
                return 8  # Escape left corner
            elif my_near_right_corner:
                return 7  # Escape right corner
            else:
                return 6  # Cautious blocking
    
    # Opponent stunned - maximum opportunity
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                # Mix heavy and light attacks on stunned opponent
                if random.random() < 0.7:
                    return 5  # Heavy kick for maximum damage
                else:
                    return 4  # Quick punch
            else:
                # Position for follow-up attack
                if abs(relative_pos) > 0.2:
                    if relative_pos > 0:
                        return 2  # Close distance
                    else:
                        return 1
                else:
                    return 0  # Wait for attack cooldown
        elif distance < medium_range:
            # Rush in to capitalize
            if relative_pos > 0:
                return 2  # Aggressive advance
            else:
                return 1
        else:
            # Too far - close distance quickly
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile while advancing
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Corner escape when I'm trapped
    if (my_near_left_corner or my_near_right_corner) and distance < medium_range:
        if opp_attacking:
            # Under pressure in corner - block and move
            if my_near_left_corner:
                return 8  # Block and move right
            else:
                return 7  # Block and move left
        else:
            # Try to escape corner
            escape_method = random.random()
            if escape_method < 0.4:
                return 3  # Jump to escape
            elif my_near_left_corner:
                return 2  # Move right out of corner
            else:
                return 1  # Move left out of corner
    
    # Corner pressure when opponent is trapped
    if (opp_near_left_corner or opp_near_right_corner) and distance < medium_range:
        if distance < close_range:
            if my_attack_cooldown < 0.1:
                if opp_blocking:
                    # Break guard with varied attacks
                    mixup = random.random()
                    if mixup < 0.4:
                        return 5  # Heavy attack to break block
                    elif mixup < 0.7:
                        return 4  # Quick attack
                    else:
                        return 3  # Jump attack for confusion
                else:
                    # Punish unguarded opponent in corner
                    return 5 if random.random() < 0.8 else 4
            else:
                # Maintain corner pressure
                return 0  # Stay ready
        else:
            # Move in to maintain corner pressure
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    # Opponent attacking - hybrid defensive response
    if opp_attacking:
        if distance < close_range:
            # Close range opponent attack
            if my_block_cooldown < 0.1:
                block_