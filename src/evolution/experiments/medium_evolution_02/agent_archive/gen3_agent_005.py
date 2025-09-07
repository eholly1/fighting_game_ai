"""
Evolutionary Agent: gen3_agent_005
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 7bb190ebb9a442b0
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
    
    # Extract detailed fighter states with validation
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
    
    # Advanced strategic thresholds for hybrid combat
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.55
    ultra_far_range = 0.75
    
    critical_health_threshold = 0.2
    low_health_threshold = 0.35
    good_health_threshold = 0.65
    excellent_health_threshold = 0.85
    
    # Analyze tactical situation
    is_ultra_close = distance < ultra_close_range
    is_close = ultra_close_range <= distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_ultra_far = distance >= far_range
    
    # Health assessments
    am_critical = my_health < critical_health_threshold
    am_low_health = my_health < low_health_threshold
    am_good_health = my_health > good_health_threshold
    am_excellent_health = my_health > excellent_health_threshold
    
    opponent_critical = opponent_health < critical_health_threshold
    opponent_low_health = opponent_health < low_health_threshold
    
    # Combat state analysis
    can_attack = my_attack_cooldown < 0.05
    can_projectile = my_projectile_cooldown < 0.08
    am_blocking = my_block_status > 0.3
    am_attacking = my_attack_status > 0.3
    
    opponent_attacking = opponent_attack_status > 0.4
    opponent_blocking = opponent_block_status > 0.3
    opponent_can_attack = opponent_attack_cooldown < 0.05
    
    # Movement analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    am_moving_fast = abs(my_velocity_x) > 0.2
    
    # Position analysis
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    both_centered = abs(my_pos_x) < 0.3 and abs(opponent_pos_x) < 0.3
    
    # Calculate aggression level based on multiple factors
    base_aggression = 0.5  # Hybrid baseline
    
    # Health-based aggression modifiers
    if am_excellent_health and opponent_low_health:
        base_aggression += 0.4
    elif am_good_health and health_advantage > 0.3:
        base_aggression += 0.25
    elif am_critical and health_advantage < -0.4:
        base_aggression -= 0.45
    elif am_low_health:
        base_aggression -= 0.2
    
    # Situational aggression modifiers
    if opponent_cornered and not am_cornered:
        base_aggression += 0.2
    elif am_cornered and not opponent_cornered:
        base_aggression -= 0.25
    
    if opponent_critical:
        base_aggression += 0.3
    
    current_aggression = max(0.1, min(0.9, base_aggression))
    
    # Emergency survival protocols
    if am_critical and opponent_attacking and (is_ultra_close or is_close):
        emergency_action = random.random()
        if emergency_action < 0.6:
            return 6  # Block to survive
        elif emergency_action < 0.8:
            # Escape with blocking movement
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            # Desperate counter-attack
            return 4  # Quick punch
    
    # Corner escape protocols
    if am_cornered and opponent_advancing:
        if is_ultra_close or is_close:
            if opponent_attacking:
                return 6  # Block then escape next turn
            else:
                # Active escape
                if my_pos_x > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        else:
            # Jump over or projectile to create space
            escape_choice = random.random()
            if escape_choice < 0.4 and can_projectile:
                return 9  # Projectile to slow advance
            elif escape_choice < 0.7:
                return 3  # Jump escape
            else:
                if my_pos_x > 0:
                    return 7  # Move left with guard
                else:
                    return 8  # Move right with guard
    
    # Finishing moves when opponent is critical
    if opponent_critical and current_aggression > 0.6:
        if is_ultra_close:
            if can_attack and not opponent_blocking:
                return 5  # Powerful finishing kick
            elif can_attack:
                return 4  # Fast punch to break guard
            else:
                return 0  # Wait for attack cooldown
        elif is_close:
            if opponent_blocking:
                # Move for better angle
                if relative_pos > 0:
                    return 2  # Move right for better position
                else:
                    return 1