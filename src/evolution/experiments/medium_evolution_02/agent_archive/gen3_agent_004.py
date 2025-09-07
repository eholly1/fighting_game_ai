"""
Evolutionary Agent: gen3_agent_004
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: b1b8a7a30e50c92d
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
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_pos_x = state[2] if len(state) > 2 and abs(state[2]) <= 1.0 else 0.0
    my_velocity_x = state[4] if len(state) > 4 and abs(state[4]) <= 2.0 else 0.0
    my_block_status = max(0.0, state[5]) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, state[6]) if len(state) > 6 else 0.0
    my_attack_cooldown = max(0.0, state[7]) if len(state) > 7 else 0.0
    my_block_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opponent_pos_x = state[13] if len(state) > 13 and abs(state[13]) <= 1.0 else 0.0
    opponent_velocity_x = state[15] if len(state) > 15 and abs(state[15]) <= 2.0 else 0.0
    opponent_block_status = max(0.0, state[16]) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, state[17]) if len(state) > 17 else 0.0
    opponent_attack_cooldown = max(0.0, state[18]) if len(state) > 18 else 0.0
    opponent_projectile_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    
    # Define strategic ranges and thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.55
    
    critical_health = 0.2
    low_health = 0.35
    good_health = 0.65
    excellent_health = 0.85
    
    # Analyze tactical situation
    is_very_close = distance < very_close_range
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health analysis
    am_critical = my_health < critical_health
    am_low = my_health < low_health
    am_healthy = my_health > good_health
    am_excellent = my_health > excellent_health
    
    opponent_critical = opponent_health < critical_health
    opponent_low = opponent_health < low_health
    
    # Combat state analysis
    can_attack = my_attack_cooldown < 0.05
    can_block = my_block_cooldown < 0.05
    can_projectile = my_projectile_cooldown < 0.05
    
    opponent_attacking = opponent_attack_status > 0.3 or opponent_attack_cooldown > 0.1
    opponent_blocking = opponent_block_status > 0.2
    opponent_can_projectile = opponent_projectile_cooldown < 0.1
    
    # Movement analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # Positioning analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    center_control = abs(my_pos_x) < 0.3
    
    # Hybrid fighting logic - balance aggression and defense
    aggression_factor = 0.5  # Base hybrid balance
    
    # Adjust aggression based on health advantage
    if health_advantage > 0.3:
        aggression_factor = 0.7  # More aggressive when winning
    elif health_advantage < -0.3:
        aggression_factor = 0.3  # More defensive when losing
    
    # Emergency survival mode
    if am_critical and health_advantage < -0.4:
        if opponent_attacking and is_close:
            if can_block:
                return 6  # Emergency block
            else:
                # Desperate escape
                if am_cornered:
                    return 3  # Jump to escape corner
                elif relative_pos > 0:
                    return 7  # Block retreat left
                else:
                    return 8  # Block retreat right
        
        elif is_very_far and can_projectile:
            return 9  # Safe projectile at distance
        
        else:
            # Create distance while defending
            if relative_pos > 0:
                return 7  # Move left blocking
            else:
                return 8  # Move right blocking
    
    # Opportunity recognition - counter attacking
    if opponent_attacking and can_attack and is_close:
        if my_block_status > 0.5:  # Successfully blocking
            # Counter attack after block
            counter_roll = random.random()
            if counter_roll < 0.4:
                return 4  # Quick punch counter
            elif counter_roll < 0.7:
                return 5  # Power kick counter
            else:
                return 6  # Continue blocking
    
    # Finishing opportunities when opponent is critical
    if opponent_critical and am_healthy:
        aggression_factor = 0.9  # Maximum aggression for finish
        
        if is_close and can_attack:
            if opponent_blocking:
                # Mix up to break guard
                if random.random() < 0.6:
                    return 5  # Strong kick
                else:
                    return 4  # Fast punch
            else:
                # Go for finish
                return 5 if random.random() < 0.8 else 4
        
        elif is_medium:
            if opponent_retreating:
                # Chase for finish
                if relative_pos > 0:
                    return 2  # Chase right
                else:
                    return 1  # Chase left
            else:
                # Close distance
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
    
    # Range-specific hybrid tactics
    if is_very_close:
        # Very close range - high intensity
        if opponent_blocking:
            # Guard breaking mixups
            mixup_choice = random.random()
            if mixup_choice < 0.3:
                return 5  # Strong kick to break guard
            elif mixup_choice < 0.5:
                # Create space for projectile
                if relative_pos > 0:
                    return 1  # Step back left
                else:
                    return 2  # Step