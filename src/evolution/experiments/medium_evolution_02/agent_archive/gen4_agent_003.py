"""
Evolutionary Agent: gen4_agent_003
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 0a33cd6fd9a62cf6
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
    
    # Extract fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(-1.0, min(1.0, state[2] if len(state) > 2 else 0.0))
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_block_status = max(0.0, state[5] if len(state) > 5 else 0.0)
    my_attack_status = max(0.0, state[6] if len(state) > 6 else 0.0)
    my_attack_cooldown = max(0.0, state[7] if len(state) > 7 else 0.0)
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = max(-1.0, min(1.0, state[13] if len(state) > 13 else 0.0))
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_block_status = max(0.0, state[16] if len(state) > 16 else 0.0)
    opponent_attack_status = max(0.0, state[17] if len(state) > 17 else 0.0)
    opponent_attack_cooldown = max(0.0, state[18] if len(state) > 18 else 0.0)
    
    # Strategic range definitions
    ultra_close = 0.08
    close_range = 0.15
    medium_range = 0.35
    far_range = 0.6
    
    # Health thresholds
    critical_health = 0.15
    low_health = 0.3
    good_health = 0.7
    
    # Situation analysis
    is_ultra_close = distance < ultra_close
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    # Health states
    am_critical = my_health < critical_health
    am_low = my_health < low_health
    am_healthy = my_health > good_health
    
    # Advantage evaluation
    major_advantage = health_advantage > 0.35
    slight_advantage = health_advantage > 0.1
    balanced = abs(health_advantage) <= 0.1
    slight_disadvantage = health_advantage < -0.1
    major_disadvantage = health_advantage < -0.35
    
    # Opponent behavior patterns
    opponent_aggressive = opponent_attack_status > 0.5 or opponent_attack_cooldown > 0.2
    opponent_defensive = opponent_block_status > 0.4
    opponent_moving_toward = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # Ability states
    can_attack = my_attack_cooldown < 0.05
    can_projectile = my_projectile_cooldown < 0.05
    am_attacking = my_attack_status > 0.2
    am_blocking = my_block_status > 0.2
    
    # Position analysis
    am_cornered = abs(my_pos_x) > 0.8
    opponent_cornered = abs(opponent_pos_x) > 0.8
    have_center = abs(my_pos_x) < 0.2
    
    # Crisis management - highest priority
    if am_critical:
        if opponent_aggressive and is_close:
            # Immediate blocking priority
            if opponent_attack_status > 0.8:
                return 6
            # Escape with block
            if am_cornered:
                escape_dir = 7 if my_pos_x > 0 else 8
                return escape_dir
            # Retreat while blocking
            retreat_dir = 7 if relative_pos > 0 else 8
            return retreat_dir
        elif is_medium and can_projectile:
            return 9  # Desperation projectile
        elif is_far and can_projectile:
            return 9  # Maintain distance with projectile
        else:
            return 6  # Block and survive
    
    # Opportunity recognition and counter-attacks
    if opponent_attack_cooldown > 0.4 and distance < medium_range:
        # Opponent recovering from attack
        if is_ultra_close and can_attack:
            # Punish with strong attack
            return 5 if random.random() < 0.7 else 4
        elif is_close:
            if can_attack:
                return 4  # Quick punish
            elif can_projectile:
                return 9  # Point blank projectile
        elif can_projectile:
            return 9  # Ranged punish
    
    # Defensive counter-attack setup
    if opponent_aggressive and am_blocking and my_block_status > 0.6:
        # Successfully blocking - prepare counter
        if is_ultra_close and can_attack:
            counter_choice = random.random()
            if counter_choice < 0.5:
                return 5  # Heavy counter
            elif counter_choice < 0.8:
                return 4  # Fast counter
            else:
                return 6  # Continue block
        elif is_close and can_projectile:
            return 9  # Projectile counter
    
    # Range-based tactical system
    if is_ultra_close:
        # Maximum intensity close combat
        if major_advantage or am_healthy:
            # Dominant offense
            if opponent_defensive:
                # Guard breaking sequence
                break_guard = random.random()
                if break_guard < 0.4:
                    return 5  # Power kick
                elif break_guard < 0.65:
                    return 4  # Fast punch
                else:
                    # Reposition for better angle
                    if random.random() < 0.5:
                        return 1 if relative_pos > 0 else 2
                    else:
                        return 3  # Jump mix-up
            elif can_attack:
                # Pure aggression
                if random.random() < 0.65:
                    return 5  # Favor kicks for damage
                else:
                    return 4  # Mix punches
            else:
                # Maintain pressure while cooling down
                return 0
        
        elif slight_advantage or balanced:
            # Calculated aggression
            if opponent_defensive:
                # Patient pressure
                if can_attack and random.random() < 0.6:
                    return 4 if random.random() < 0.7 else 5
                else:
                    # Smart positioning
                    position_choice = random.random()
                    if position_choice < 0.3:
                        return 1 if relative_pos > 0 else 2