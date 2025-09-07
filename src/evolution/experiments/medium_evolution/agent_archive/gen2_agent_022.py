"""
Evolutionary Agent: gen2_agent_022
==================================

Metadata:
{
  "generation": 2,
  "fitness": 281.42000000000684,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 061fb82a400b9e20
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
    
    # Extract my fighter information with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_block_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information with bounds checking
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_block_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Enhanced hybrid fighter parameters
    close_range = 0.12
    medium_range = 0.26
    far_range = 0.42
    optimal_range = 0.38
    critical_health = 0.2
    low_health = 0.4
    winning_threshold = 0.2
    losing_threshold = -0.2
    
    # Advanced positioning analysis
    stage_center = 0.5
    left_edge = 0.15
    right_edge = 0.85
    is_near_left_edge = my_x_pos < left_edge
    is_near_right_edge = my_x_pos > right_edge
    is_cornered = is_near_left_edge or is_near_right_edge
    opp_cornered = opp_x_pos < left_edge or opp_x_pos > right_edge
    
    # Movement and timing analysis
    opponent_closing = abs(opp_x_velocity) > 0.25 and distance < medium_range
    opponent_retreating = (relative_pos > 0 and opp_x_velocity > 0.2) or (relative_pos < 0 and opp_x_velocity < -0.2)
    projectile_ready = my_projectile_cooldown < 0.1
    attack_ready = my_attack_cooldown < 0.1
    block_ready = my_block_cooldown < 0.15
    
    # Opponent threat assessment
    opp_projectile_threat = opp_projectile_cooldown < 0.12
    opp_attack_threat = opp_attack_cooldown < 0.15
    immediate_danger = opp_attacking and distance < close_range
    
    # Emergency defensive responses
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health - pure survival mode
    if my_health <= critical_health:
        if immediate_danger:
            if block_ready:
                return 6  # Emergency block
            else:
                return 0  # Wait for block recovery
        
        if distance < close_range:
            # Escape from danger zone
            if is_cornered:
                if height_diff > -0.15:
                    return 3  # Jump escape
                else:
                    return 6  # Block in corner
            else:
                # Mobile escape
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        elif distance < medium_range:
            # Create safe distance
            if relative_pos > 0 and not is_near_left_edge:
                return 1  # Move away left
            elif relative_pos < 0 and not is_near_right_edge:
                return 2  # Move away right
            else:
                if projectile_ready:
                    return 9  # Desperation projectile
                else:
                    return 6  # Block
        
        else:
            # Safe distance - try to chip
            if projectile_ready:
                return 9
            else:
                return 0  # Wait safely
    
    # Opponent stunned - maximum punishment combo
    if opp_stunned:
        if distance < close_range:
            if attack_ready:
                # Optimized damage combo
                stun_timer = random.random()
                if stun_timer < 0.3:
                    return 4  # Quick punch to extend
                elif stun_timer < 0.8:
                    return 5  # Heavy kick for damage
                else:
                    return 4  # Quick finisher
            else:
                # Position for next attack
                if distance > 0.05:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 0  # Perfect distance
        elif distance < medium_range:
            # Rush in for combo
            return 2 if relative_pos > 0 else 1
        else:
            # Too far for melee
            if projectile_ready:
                return 9  # Projectile while closing
            else:
                return 2 if relative_pos > 0 else 1
    
    # Counter opponent attacks with improved timing
    if opp_attacking:
        if distance < close_range:
            if block_ready:
                # Intelligent blocking based on situation
                if is_cornered:
                    return 6  # Pure block when cornered
                elif opponent_closing:
                    # Mobile defense
                    if relative_pos > 0 and not is_near_left_edge:
                        return 7  # Block retreat left
                    elif not is_near_right_edge:
                        return 8  # Block retreat right
                    else:
                        return 6  # Standard block
                else:
                    return 6  # Standar