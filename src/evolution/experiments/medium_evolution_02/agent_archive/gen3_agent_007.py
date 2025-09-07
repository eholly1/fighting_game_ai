"""
Evolutionary Agent: gen3_agent_007
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 0cc2fe2569314114
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
    
    # Extract fighter status information with validation
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(-1.0, min(1.0, state[2] if len(state) > 2 else 0.0))
    my_velocity_x = max(-2.0, min(2.0, state[4] if len(state) > 4 else 0.0))
    my_block_status = max(0.0, state[5] if len(state) > 5 else 0.0)
    my_attack_status = max(0.0, state[6] if len(state) > 6 else 0.0)
    my_attack_cooldown = max(0.0, state[7] if len(state) > 7 else 0.0)
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = max(-1.0, min(1.0, state[13] if len(state) > 13 else 0.0))
    opponent_velocity_x = max(-2.0, min(2.0, state[15] if len(state) > 15 else 0.0))
    opponent_block_status = max(0.0, state[16] if len(state) > 16 else 0.0)
    opponent_attack_status = max(0.0, state[17] if len(state) > 17 else 0.0)
    opponent_attack_cooldown = max(0.0, state[18] if len(state) > 18 else 0.0)
    
    # Define strategic thresholds for hybrid style
    close_range = 0.10
    medium_range = 0.32
    far_range = 0.55
    
    critical_health = 0.20
    low_health = 0.35
    good_health = 0.65
    excellent_health = 0.85
    
    # Analyze current tactical situation
    is_very_close = distance < close_range * 0.7
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health analysis
    am_critical = my_health < critical_health
    am_low = my_health < low_health
    am_healthy = my_health > good_health
    am_excellent = my_health > excellent_health
    
    # Advantage analysis
    major_advantage = health_advantage > 0.4
    minor_advantage = health_advantage > 0.15
    even_fight = abs(health_advantage) <= 0.15
    minor_disadvantage = health_advantage < -0.15
    major_disadvantage = health_advantage < -0.4
    
    # Opponent behavior analysis
    opponent_aggressive = opponent_attack_status > 0.6 or opponent_attack_cooldown > 0.3
    opponent_defensive = opponent_block_status > 0.5
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    
    # Cooldown and ability checks
    can_attack = my_attack_cooldown < 0.1
    can_projectile = my_projectile_cooldown < 0.1
    am_attacking = my_attack_status > 0.3
    am_blocking = my_block_status > 0.3
    
    # Positional analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    center_control = abs(my_pos_x) < 0.3
    
    # Emergency survival mode - highest priority
    if am_critical and (opponent_aggressive or opponent_approaching):
        if is_very_close and opponent_attack_status > 0.7:
            return 6  # Block critical incoming damage
        elif is_close:
            # Escape while blocking
            if am_cornered:
                # Must escape corner
                if my_pos_x > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Create distance defensively
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        elif is_medium and can_projectile:
            return 9  # Desperate projectile to create space
        else:
            return 6  # Block and survive
    
    # Counter-attack opportunities for hybrid style
    if opponent_attack_status > 0.8 and distance < medium_range:
        if my_block_status > 0.5:
            # Successfully blocking - counter attack
            if is_very_close and can_attack:
                counter_roll = random.random()
                if counter_roll < 0.45:
                    return 4  # Quick punch counter
                elif counter_roll < 0.75:
                    return 5  # Power kick counter
                else:
                    return 6  # Continue blocking
            elif is_close and can_projectile:
                return 9  # Point-blank projectile
        else:
            # Need to block first
            return 6
    
    # Hybrid range-based strategy
    if is_very_close:
        # Ultra close combat - high intensity
        if major_advantage or am_excellent:
            # Dominant position - aggressive offense
            if opponent_defensive:
                # Break guard with varied attacks
                guard_break = random.random()
                if guard_break < 0.35:
                    return 5  # Heavy kick to break block
                elif guard_break < 0.6:
                    return 4  # Fast punch combo
                else:
                    # Create space for projectile
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            elif can_attack:
                # Full aggression
                if random.random() < 0.6:
                    return 5  # Prioritize kicks for damage
                else:
                    return 4  # Mix in punches
            else:
                # Wait for attack cooldown
                return 0
        
        elif minor_advantage or even_fight:
            # Balanced approach
            if opponent_defensive:
                # Patient pressure
                if can_attack and random.random() < 0.5:
                    return 4 if random.random() < 0.6 else 5
                else:
                    # Reposition
                    if random.random() < 0.4:
                        return 1 if relative_pos > 0 else 2
                    else:
                        return 6  # Block and wait
            elif opponent_aggressive:
                # Defensive counter
                if random.random() < 0.7:
                    return 6  #