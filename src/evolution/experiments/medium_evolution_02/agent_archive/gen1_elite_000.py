"""
Evolutionary Agent: gen1_elite_000
==================================

Metadata:
{
  "generation": 1,
  "fitness": 188.9441666666672,
  "fighting_style": "adaptive",
  "win_rate": 0.0
}

Code Hash: 74226a44e227d76d
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
    
    # Extract fighter states
    my_health = state[1] if state[1] >= 0 else 0.5
    my_pos_x = state[2] if abs(state[2]) <= 1.0 else 0.0
    my_velocity_x = state[4] if abs(state[4]) <= 2.0 else 0.0
    my_attack_cooldown = state[7] if state[7] >= 0 else 0.0
    my_block_status = state[8] if state[8] >= 0 else 0.0
    my_projectile_cooldown = state[9] if state[9] >= 0 else 0.0
    
    opponent_health = state[12] if state[12] >= 0 else 0.5
    opponent_pos_x = state[13] if abs(state[13]) <= 1.0 else 0.0
    opponent_velocity_x = state[15] if abs(state[15]) <= 2.0 else 0.0
    opponent_attack_cooldown = state[18] if state[18] >= 0 else 0.0
    opponent_block_status = state[19] if state[19] >= 0 else 0.0
    
    # Define strategic thresholds
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    
    critical_health = 0.25
    low_health = 0.4
    good_health = 0.7
    
    # Analyze current situation
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = distance >= medium_range
    is_very_far = distance > far_range
    
    am_winning = health_advantage > 0.2
    am_losing = health_advantage < -0.2
    am_critical = my_health < critical_health
    am_low_health = my_health < low_health
    
    opponent_attacking = opponent_attack_cooldown > 0.1
    opponent_blocking = opponent_block_status > 0.1
    opponent_moving_toward = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_moving_away = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    can_attack = my_attack_cooldown < 0.05
    can_projectile = my_projectile_cooldown < 0.05
    am_cornered = abs(my_pos_x) > 0.8
    opponent_cornered = abs(opponent_pos_x) > 0.8
    
    # Emergency defensive measures
    if am_critical and opponent_attacking and is_close:
        if random.random() < 0.8:
            return 6  # Block to survive
        else:
            # Desperate escape
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
    
    # Adaptive strategy based on health situation
    if am_losing and my_health < low_health:
        # Defensive/cautious play when losing
        if is_very_far:
            if can_projectile and not opponent_blocking:
                return 9  # Safe projectile
            else:
                # Position for better angle
                if abs(relative_pos) < 0.3:
                    return 1 if random.random() < 0.5 else 2
                else:
                    return 0  # Wait
        
        elif is_far:
            if opponent_moving_toward and can_projectile:
                return 9  # Projectile to slow approach
            elif opponent_blocking:
                # Try to flank
                if relative_pos > 0:
                    return 1  # Move left to flank
                else:
                    return 2  # Move right to flank
            else:
                if can_projectile:
                    return 9
                else:
                    return 6  # Block while waiting
        
        elif is_medium:
            if opponent_attacking:
                return 6  # Block incoming attack
            elif opponent_moving_toward:
                # Maintain distance while blocking
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
            else:
                if can_projectile and not opponent_blocking:
                    return 9
                else:
                    return 6  # Defensive stance
        
        else:  # Close range
            if opponent_attacking:
                return 6  # Block
            elif can_attack and not opponent_blocking:
                # Quick counter-attack
                return 4  # Fast punch
            else:
                # Try to create space
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
    
    elif am_winning or my_health > good_health:
        # Aggressive play when winning
        if is_close:
            if opponent_blocking:
                # Mix up attacks to break guard
                if random.random() < 0.4:
                    return 5  # Strong kick
                elif random.random() < 0.6:
                    return 4  # Fast punch
                else:
                    # Create space for projectile
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            elif can_attack:
                # Aggressive combo
                if random.random() < 0.7:
                    return 5  # Kick for damage
                else:
                    return 4  # Punch for speed
            else:
                # Position for next attack
                if opponent_moving_away:
                    if relative_pos > 0:
                        return 2  # Chase right
                    else:
                        return 1  # Chase left
                else:
                    return 0  # Wait for cooldown
        
        elif is_medium:
            if opponent_blocking:
                # Move to better position
                if random.random() < 0.5:
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    if can_projectile:
                        return 9  # Projectile to pressure
                    else:
                        return 0
            elif opponent_moving_away:
                # Pursue aggressively
                if relative_pos > 0:
                    return 2  # Chase right
                else:
                    return 1  # Chase left
            else:
                # Close distance for attack
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        else:  # Far range
            if can_projectile and not opponent_blocking:
                return 9  # Projectile pressure
            elif opponent_blocking:
                # Advance while they block
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                # Maintain pressure
                if can_projectile:
                    return 9
                else:
                    if relative_pos > 0:
                        return 2  # Move right