"""
Evolutionary Agent: gen3_agent_006
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 5c3a80d309cdfdbd
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
    
    # Adaptive strategy thresholds
    close_range = 0.10
    medium_range = 0.30
    far_range = 0.55
    
    critical_health = 0.20
    low_health = 0.35
    good_health = 0.65
    excellent_health = 0.85
    
    # Situational analysis
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health-based strategy states
    am_critical = my_health < critical_health
    am_low = my_health < low_health
    am_healthy = my_health > good_health
    am_excellent = my_health > excellent_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    
    # Advantage states
    significant_advantage = health_advantage > 0.3
    slight_advantage = 0.1 < health_advantage <= 0.3
    even_match = abs(health_advantage) <= 0.1
    slight_disadvantage = -0.3 <= health_advantage < -0.1
    significant_disadvantage = health_advantage < -0.3
    
    # Combat readiness
    can_attack = my_attack_cooldown < 0.08
    can_projectile = my_projectile_cooldown < 0.08
    opponent_attacking = opponent_attack_cooldown > 0.15
    opponent_blocking = opponent_block_status > 0.12
    
    # Movement analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_stationary = abs(opponent_velocity_x) < 0.1
    
    # Positioning analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    center_control = abs(my_pos_x) < 0.3
    
    # Emergency survival mode - critical health with immediate threat
    if am_critical and is_close and opponent_attacking:
        escape_probability = 0.85 if significant_disadvantage else 0.7
        if random.random() < escape_probability:
            if am_cornered:
                # Desperate counter if cornered
                if can_attack and random.random() < 0.3:
                    return 5  # Desperate kick
                else:
                    return 6  # Block and hope
            else:
                # Escape with blocking movement
                if relative_pos > 0:
                    return 7  # Block left
                else:
                    return 8  # Block right
        else:
            return 6  # Pure block
    
    # Adaptive strategy selection based on health advantage
    if significant_disadvantage or (am_low and not opponent_critical):
        # Defensive/Survival Strategy
        if is_very_far:
            if can_projectile and not opponent_blocking:
                # Safe long-range harassment
                charge_projectile = random.random() < 0.4
                return 9
            else:
                # Positioning for better shots or wait
                if opponent_advancing:
                    # Maintain distance
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 0  # Wait and observe
        
        elif is_far:
            if opponent_blocking and can_projectile:
                return 9  # Pressure with projectile
            elif opponent_advancing and can_projectile:
                return 9  # Slow their advance
            elif opponent_retreating:
                # Don't chase, maintain safe distance
                return 0
            else:
                if can_projectile and random.random() < 0.6:
                    return 9
                else:
                    return 6  # Defensive stance
        
        elif is_medium:
            if opponent_attacking:
                return 6  # Block incoming
            elif opponent_advancing:
                # Maintain distance with blocking movement
                if am_cornered:
                    # Must advance to escape corner
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    if relative_pos > 0:
                        return 7  # Block left
                    else:
                        return 8  # Block right
            else:
                if can_projectile and not opponent_blocking:
                    return 9
                else:
                    return 6  # Block and wait
        
        else:  # Close range
            if opponent_attacking:
                return 6  # Block
            elif opponent_blocking:
                # Try to create space
                if am_cornered:
                    # Quick attack to create opening
                    if can_attack:
                        return 4  # Fast punch
                    else:
                        return 6  # Block
                else:
                    if relative_pos > 0:
                        return 7  # Block left
                    else:
                        return 8  # Block right
            else:
                if can_attack and random.random() < 0.5:
                    return 4  # Quick counter
                else:
                    # Create distance
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right