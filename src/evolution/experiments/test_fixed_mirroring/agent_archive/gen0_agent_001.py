"""
Evolutionary Agent: gen0_agent_001
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "defensive",
  "win_rate": 0.5
}

Code Hash: 4d77671a04dea972
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
    
    # Extract player and opponent info with bounds checking
    my_health = max(0.0, state[1]) if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opp_health = max(0.0, state[12]) if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    
    # Define tactical thresholds for defensive play
    close_range_threshold = 0.12
    medium_range_threshold = 0.28
    far_range_threshold = 0.45
    critical_health_threshold = -0.4
    safe_health_threshold = 0.2
    danger_health_threshold = -0.2
    
    # Defensive positioning parameters
    preferred_distance = 0.25
    wall_avoidance_threshold = 0.15
    counter_attack_window = 0.8
    
    # Calculate derived tactical information
    is_opponent_attacking = opp_attack_status > 0.1
    is_opponent_blocking = opp_block_status > 0.1
    is_opponent_approaching = (relative_pos > 0 and opp_velocity_x > 0.1) or (relative_pos < 0 and opp_velocity_x < -0.1)
    am_near_wall = my_x_pos < wall_avoidance_threshold or my_x_pos > (1.0 - wall_avoidance_threshold)
    opponent_projectile_ready = len(state) > 21 and state[21] < 0.1
    
    # Emergency defensive responses - highest priority
    if health_advantage < critical_health_threshold:
        # Critical health - maximum defense
        if distance < close_range_threshold:
            if is_opponent_attacking:
                return 6  # Block immediate attacks
            elif relative_pos > 0 and not am_near_wall:
                return 7  # Move left while blocking
            elif relative_pos < 0 and not am_near_wall:
                return 8  # Move right while blocking
            else:
                return 6  # Default block
        elif distance < medium_range_threshold:
            # Create distance while blocking
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        else:
            # Long range - use projectiles for safe damage
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile attack
            else:
                return 6  # Block while cooldown recovers
    
    # Wall escape - prevent being cornered
    if am_near_wall and distance < medium_range_threshold:
        if my_x_pos < 0.5:  # Near left wall
            if is_opponent_attacking:
                return 8  # Move right while blocking
            else:
                return 2  # Move right to center
        else:  # Near right wall
            if is_opponent_attacking:
                return 7  # Move left while blocking
            else:
                return 1  # Move left to center
    
    # Opponent attack response - core defensive behavior
    if is_opponent_attacking:
        if distance < close_range_threshold:
            # Immediate threat - block or evade
            if random.random() < 0.8:  # 80% block rate when attacked
                return 6  # Block attack
            else:
                # Evasive movement
                if relative_pos > 0 and my_x_pos > 0.2:
                    return 1  # Move away left
                elif relative_pos < 0 and my_x_pos < 0.8:
                    return 2  # Move away right
                else:
                    return 6  # Block if can't evade
        elif distance < medium_range_threshold:
            # Medium range attack incoming - prepare defense
            if random.random() < 0.6:
                if relative_pos > 0:
                    return 7  # Block while moving left
                else:
                    return 8  # Block while moving right
            else:
                return 6  # Static block
    
    # Range-based defensive tactics
    if distance < close_range_threshold:
        # Close range - defensive priority with counter opportunities
        if health_advantage > safe_health_threshold:
            # Healthy enough for calculated risks
            if not is_opponent_blocking and random.random() < 0.4:
                # Counter-attack opportunity
                if random.random() < 0.6:
                    return 4  # Quick punch
                else:
                    return 5  # Power kick
            else:
                # Stay defensive
                if random.random() < 0.7:
                    return 6  # Block
                else:
                    # Create space
                    if relative_pos > 0:
                        return 7  # Block and retreat left
                    else:
                        return 8  # Block and retreat right
        else:
            # Low health - maximum defense
            if is_opponent_blocking:
                # Opponent blocking - create distance
                if relative_pos > 0:
                    return 1  # Move left for space
                else:
                    return 2  # Move right for space
            else:
                return 6  # Block incoming attacks
    
    elif distance < medium_range_threshold:
        # Medium range - optimal defensive positioning
        if health_advantage < danger_health_threshold:
            # Losing - maintain distance
            if distance < preferred_distance:
                # Too close - create more space
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Good distance - hold position defensively
                if is_opponent_approaching:
                    return 6  # Block approach
                elif my_projectile_cooldown < 0.3:
                    return 9  # Safe projectile
                else:
                    return 6  # Defensive stance
        else:
            # Even or winning - controlled aggression
            if is_opponent_blocking:
                # Opponent defensive - position for advantage
                if distance > preferred_distance * 1.2:
                    # Close distance carefully
                    if relative_pos > 0:
                        return 2  # Move right towar