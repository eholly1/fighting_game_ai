"""
Evolutionary Agent: gen2_agent_005
==================================

Metadata:
{
  "generation": 2,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 2f87df084f4fac56
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
    
    # Extract detailed fighter status
    my_health = state[1] if len(state) > 1 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_velocity_y = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[17] if len(state) > 17 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Enhanced range definitions for hybrid style
    ultra_close = 0.05
    very_close = 0.1
    close_range = 0.18
    mid_close = 0.25
    medium_range = 0.35
    mid_far = 0.5
    far_range = 0.7
    
    # Health thresholds for tactical adaptation
    critical_health = 0.2
    low_health = 0.35
    moderate_health = 0.55
    good_health = 0.75
    
    # Momentum and threat calculations
    opponent_closing = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    high_threat = opponent_attack_status > 0.7 or (opponent_closing and distance < close_range)
    counter_opportunity = opponent_attack_status > 0.6 and my_block_status > 0.4
    
    # Tactical awareness calculations
    projectile_advantage = my_projectile_cooldown < 0.1 and opponent_projectile_cooldown > 0.3
    stamina_advantage = my_attack_status < 0.3 and opponent_attack_status > 0.5
    positioning_advantage = (relative_pos > 0 and opponent_velocity_x > 0) or (relative_pos < 0 and opponent_velocity_x < 0)
    
    # Critical survival mode - ultra defensive when desperate
    if my_health < critical_health and health_advantage < -0.5:
        if distance < very_close and high_threat:
            return 6  # Emergency block
        elif distance < close_range:
            if relative_pos > 0:
                return 7  # Retreat with block
            else:
                return 8  # Retreat with block
        elif distance < medium_range and opponent_closing:
            # Maintain distance with projectiles if possible
            if projectile_advantage:
                return 9
            else:
                if relative_pos > 0:
                    return 7  # Defensive retreat left
                else:
                    return 8  # Defensive retreat right
        else:
            # Long range survival
            if projectile_advantage:
                return 9  # Keep distance with projectiles
            else:
                return 6  # Default defensive stance
    
    # Dominant position - aggressive when winning big
    if health_advantage > 0.6 and my_health > moderate_health:
        if distance < ultra_close:
            # Ultra close dominance
            if opponent_block_status > 0.6:
                # Break guard with power
                guard_break = random.random()
                if guard_break < 0.4:
                    return 5  # Heavy kick
                elif guard_break < 0.7:
                    return 4  # Quick punch
                else:
                    return 3  # Jump attack
            else:
                # Punish open opponent
                if random.random() < 0.7:
                    return 5  # Power attack
                else:
                    return 4  # Quick combo
        elif distance < close_range:
            # Aggressive close range
            if opponent_attack_status < 0.3:
                pressure_choice = random.random()
                if pressure_choice < 0.35:
                    return 4  # Punch pressure
                elif pressure_choice < 0.65:
                    return 5  # Kick pressure
                else:
                    # Advance for combo
                    if relative_pos > 0:
                        return 1  # Move in left
                    else:
                        return 2  # Move in right
            else:
                # Counter opponent's attack
                if counter_opportunity:
                    return 5  # Power counter
                else:
                    return 6  # Block and reset
    
    # Hybrid range management - core strategy
    if distance < ultra_close:
        # Ultra close combat
        if health_advantage > 0.3:
            # Advantage - press attack
            if opponent_block_status > 0.5:
                # Mix up against block
                mixup = random.random()
                if mixup < 0.25:
                    return 5  # Heavy attack
                elif mixup < 0.5:
                    return 4  # Quick attack
                elif mixup < 0.75:
                    return 3  # Jump mixup
                else:
                    return 6  # Reset to neutral
            else:
                # Open opponent - capitalize
                if my_attack_status < 0.4:
                    return 4 if random.random() < 0.6 else 5
                else:
                    return 6  # Avoid overcommit
        elif health_advantage < -0.2:
            # Disadvantage - defensive
            if high_threat:
                return 6  # Block
            elif counter_opportunity:
                return 4  # Safe counter
            else:
                # Create space
                if relative_pos > 0:
                    return 7  # Back up left
                else:
                    return 8  # Back up right
        else:
            # Even - cautious aggression
            if opponent_attack_status > 0.6:
                return 6  # Defend first
            elif stamina_advantage:
                return 4  # Punish tired opponent
            else:
                neutral_choice = random.random()
                if neutral_choice < 0.4:
                    return 4  # Punch
                elif neutral_choice < 0.6:
                    return 6  # Block
                else:
                    return 5  # Kick
    
    elif distance < close_range:
        # Close range - key decision zone
        if health_advantage > 0.2:
            # Slight advantage - controlled pressure
            if opponent_block_status > 0.6:
                # Patient pressure against defense
                pressure_option = random.random()
                if pressure_option < 0.3:
                    return 4  # Test with punch
                elif pressure_option < 0.5:
                    return 5  # Test with