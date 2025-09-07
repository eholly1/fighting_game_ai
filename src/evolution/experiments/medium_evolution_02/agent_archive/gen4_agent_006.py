"""
Evolutionary Agent: gen4_agent_006
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: c6fa43fc0df4d8e7
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
    my_health = max(0.0, min(1.0, state[1]))
    my_pos_x = max(-1.0, min(1.0, state[2]))
    my_velocity_x = max(-2.0, min(2.0, state[4]))
    my_attack_cooldown = max(0.0, state[7])
    my_block_status = max(0.0, state[8])
    my_projectile_cooldown = max(0.0, state[9])
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[12]))
    opponent_pos_x = max(-1.0, min(1.0, state[13]))
    opponent_velocity_x = max(-2.0, min(2.0, state[15]))
    opponent_attack_cooldown = max(0.0, state[18])
    opponent_block_status = max(0.0, state[19])
    
    # Define enhanced strategic thresholds
    ultra_close = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.55
    ultra_far = 0.75
    
    # Health thresholds
    critical_health = 0.2
    low_health = 0.35
    medium_health = 0.6
    high_health = 0.8
    
    # Behavioral analysis
    opponent_attacking = opponent_attack_cooldown > 0.05
    opponent_blocking = opponent_block_status > 0.05
    opponent_vulnerable = not opponent_attacking and not opponent_blocking
    opponent_moving_toward = (relative_pos > 0 and opponent_velocity_x > 0.08) or (relative_pos < 0 and opponent_velocity_x < -0.08)
    opponent_moving_away = (relative_pos > 0 and opponent_velocity_x < -0.08) or (relative_pos < 0 and opponent_velocity_x > 0.08)
    opponent_stationary = abs(opponent_velocity_x) < 0.05
    
    # My capabilities
    can_attack = my_attack_cooldown < 0.03
    can_projectile = my_projectile_cooldown < 0.03
    am_moving = abs(my_velocity_x) > 0.05
    am_cornered = abs(my_pos_x) > 0.85
    opponent_cornered = abs(opponent_pos_x) > 0.85
    
    # Range classifications
    is_ultra_close = distance < ultra_close
    is_close = ultra_close <= distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_ultra_far = distance >= far_range
    
    # Health situation analysis
    am_critical = my_health < critical_health
    am_low = my_health < low_health
    am_healthy = my_health > medium_health
    am_dominant = my_health > high_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    
    # Dynamic aggression levels
    base_aggression = 0.5
    if health_advantage > 0.3:
        aggression_level = 0.8
    elif health_advantage > 0.1:
        aggression_level = 0.65
    elif health_advantage < -0.3:
        aggression_level = 0.2
    elif health_advantage < -0.1:
        aggression_level = 0.35
    else:
        aggression_level = base_aggression
    
    # Adaptive pattern recognition counter
    pattern_counter = int(distance * 100 + my_health * 50 + opponent_health * 25) % 4
    
    # Emergency situations - highest priority
    if am_critical and opponent_attacking:
        if is_ultra_close or is_close:
            if random.random() < 0.9:
                return 6  # Block desperately
            else:
                # Panic escape
                if am_cornered:
                    return 3  # Jump over
                else:
                    return 7 if relative_pos > 0 else 8
        else:
            return 6  # Block at range
    
    # Cornered situations
    if am_cornered and opponent_moving_toward:
        if is_close:
            if can_attack and opponent_vulnerable:
                return 5  # Desperate counter-kick
            else:
                return 3  # Jump escape
        else:
            # Move toward center
            if my_pos_x > 0:
                return 7  # Move left block
            else:
                return 8  # Move right block
    
    # Opponent cornered - pressure tactics
    if opponent_cornered and aggression_level > 0.4:
        if is_ultra_close:
            if can_attack:
                return 5 if random.random() < 0.7 else 4  # Heavy pressure
            else:
                return 6  # Block counter-attacks
        elif is_close:
            if opponent_blocking:
                # Mix up attacks
                if can_attack:
                    return 4 if pattern_counter % 2 else 5
                else:
                    return 0  # Wait for opening
            else:
                # Close in for kill
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        else:
            # Advance with projectiles
            if can_projectile and not opponent_blocking:
                return 9
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Adaptive strategy based on health advantage
    if health_advantage > 0.4:  # Winning decisively
        if is_ultra_close:
            if opponent_blocking:
                # Break guard with varied attacks
                if can_attack:
                    attack_choice = pattern_counter % 3
                    if attack_choice == 0:
                        return 4  # Punch
                    elif attack_choice == 1:
                        return 5  # Kick
                    else:
                        # Create space for projectile
                        return 1 if relative_pos > 0 else 2
                else:
                    return 0
            elif can_attack:
                return 5 if random.random() < 0.8 else 4  # Favor kicks
            else:
                return 0
        
        elif is_close:
            if opponent_moving_away:
                # Chase aggressively
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif opponent_blocking:
                if can_projectile:
                    return 9  # Projectile pressure
                else:
                    # Reposition
                    return 1 if pattern_counter % 2 else 2
            else:
                # Close for attack
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        elif is_medium:
            if opponent_blocking:
                # Advance while they're defensive
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif can_projectile:
                return 9  # Maintain pressure
            else:
                # Close distance
                if relative_pos > 0:
                    return