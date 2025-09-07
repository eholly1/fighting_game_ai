"""
Evolutionary Agent: gen2_agent_006
==================================

Metadata:
{
  "generation": 2,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 74d21b2a48140e19
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
    
    # Extract my fighter state
    my_health = max(0.0, min(1.0, state[1] if state[1] >= 0 else 0.5))
    my_pos_x = max(-1.0, min(1.0, state[2] if abs(state[2]) <= 1.0 else 0.0))
    my_velocity_x = max(-2.0, min(2.0, state[4] if abs(state[4]) <= 2.0 else 0.0))
    my_attack_cooldown = max(0.0, state[7] if state[7] >= 0 else 0.0)
    my_block_status = max(0.0, state[8] if state[8] >= 0 else 0.0)
    my_projectile_cooldown = max(0.0, state[9] if state[9] >= 0 else 0.0)
    
    # Extract opponent fighter state
    opponent_health = max(0.0, min(1.0, state[12] if state[12] >= 0 else 0.5))
    opponent_pos_x = max(-1.0, min(1.0, state[13] if abs(state[13]) <= 1.0 else 0.0))
    opponent_velocity_x = max(-2.0, min(2.0, state[15] if abs(state[15]) <= 2.0 else 0.0))
    opponent_attack_cooldown = max(0.0, state[18] if state[18] >= 0 else 0.0)
    opponent_block_status = max(0.0, state[19] if state[19] >= 0 else 0.0)
    
    # Behavioral pattern tracking variables
    frame_time = 0.016  # Assume ~60fps
    
    # Define strategic ranges and thresholds
    close_range = 0.1
    medium_close_range = 0.2
    medium_range = 0.35
    far_range = 0.55
    
    critical_health = 0.2
    low_health = 0.35
    good_health = 0.65
    dominant_health = 0.8
    
    # Analyze tactical situation
    is_very_close = distance < close_range
    is_close = distance < medium_close_range
    is_medium = medium_close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health analysis
    am_critical = my_health < critical_health
    am_low_health = my_health < low_health
    am_healthy = my_health > good_health
    am_dominant = my_health > dominant_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    
    # Combat state analysis
    can_attack = my_attack_cooldown < 0.03
    can_projectile = my_projectile_cooldown < 0.03
    am_blocking = my_block_status > 0.05
    
    opponent_attacking = opponent_attack_cooldown > 0.05
    opponent_blocking = opponent_block_status > 0.05
    opponent_vulnerable = opponent_attack_cooldown < 0.02 and opponent_block_status < 0.02
    
    # Movement analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.05) or (relative_pos < 0 and opponent_velocity_x < -0.05)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.05) or (relative_pos < 0 and opponent_velocity_x > 0.05)
    opponent_stationary = abs(opponent_velocity_x) < 0.05
    
    # Positional analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    stage_center = abs(my_pos_x) < 0.3
    
    # Winning/losing state
    am_winning_big = health_advantage > 0.3
    am_winning = health_advantage > 0.1
    am_losing = health_advantage < -0.1
    am_losing_big = health_advantage < -0.3
    close_match = abs(health_advantage) < 0.1
    
    # Emergency survival mode
    if am_critical:
        if opponent_attacking and is_close:
            # Immediate block or escape
            if random.random() < 0.85:
                return 6  # Block
            else:
                if am_cornered:
                    if relative_pos > 0:
                        return 8  # Move right block
                    else:
                        return 7  # Move left block
                else:
                    if relative_pos > 0:
                        return 7  # Move left block
                    else:
                        return 8  # Move right block
        
        elif is_very_far and can_projectile:
            return 9  # Safe projectile
        
        elif is_far:
            if opponent_approaching:
                if can_projectile and not opponent_blocking:
                    return 9  # Projectile to slow approach
                else:
                    return 6  # Defensive block
            else:
                if can_projectile:
                    return 9
                else:
                    return 6
        
        elif is_medium:
            if opponent_attacking:
                return 6  # Block incoming
            elif opponent_approaching:
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
            else:
                if can_projectile and not opponent_blocking:
                    return 9
                else:
                    return 6
        
        else:  # Close range
            if opponent_attacking:
                return 6  # Block
            elif can_attack and opponent_vulnerable:
                return 4  # Quick counter
            else:
                if relative_pos > 0:
                    return 7  # Escape left
                else:
                    return 8  # Escape right
    
    # Aggressive domination when winning big
    if am_winning_big and am_healthy:
        if opponent_critical:
            # Finish them off
            if is_very_close:
                if can_attack:
                    if opponent_blocking:
                        return 5  # Power through with kick
                    else:
                        return 4 if random.random() < 0.6 else 5  # Mix attacks
                else:
                    return 0  # Wait for cooldown
            
            elif is_close:
                if opponent_retreating:
                    if relative_pos > 0:
                        return 2  # Chase right
                    else:
                        return 1  # Chase left
                elif can_attack:
                    return 5  # Strong attack
                else:
                    if relative_pos > 0:
                        return 2  # Close distance
                    else:
                        return 1  # Close distance
            
            elif is_medium:
                if opponent_blocking:
                    if relative_pos > 0:
                        return 2  # Flank right
                    else:
                        return 1  # Flank left
                else:
                    if relative_pos > 0:
                        return 2  #