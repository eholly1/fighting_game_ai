"""
Evolutionary Agent: gen2_agent_008
==================================

Metadata:
{
  "generation": 2,
  "fitness": 250.759999999993,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 4c64d1f9b69338c8
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_velocity_y = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_stunned = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_velocity_y = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_stunned = state[20] if len(state) > 20 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid tactical ranges
    point_blank_range = 0.06
    ultra_close_range = 0.12
    close_range = 0.18
    medium_close_range = 0.28
    medium_range = 0.42
    far_range = 0.65
    
    # Calculate dynamic aggression based on multiple factors
    base_aggression = 0.75
    health_factor = 1.0
    distance_factor = 1.0
    momentum_factor = 1.0
    
    # Health-based aggression adjustment
    if health_advantage > 0.4:
        health_factor = 1.3  # Dominant position
    elif health_advantage > 0.2:
        health_factor = 1.15  # Winning
    elif health_advantage > -0.1:
        health_factor = 1.0  # Even
    elif health_advantage > -0.3:
        health_factor = 0.8  # Losing
    else:
        health_factor = 0.6  # Desperate
    
    # Distance-based aggression
    if distance < close_range:
        distance_factor = 1.2  # More aggressive up close
    elif distance > medium_range:
        distance_factor = 0.9  # More cautious at range
    
    # Momentum consideration
    opponent_approaching = False
    if relative_pos > 0 and opponent_velocity_x > 0.2:
        opponent_approaching = True
    elif relative_pos < 0 and opponent_velocity_x < -0.2:
        opponent_approaching = True
    
    if opponent_approaching:
        momentum_factor = 1.1  # Counter-aggressive
    
    current_aggression = min(1.0, base_aggression * health_factor * distance_factor * momentum_factor)
    
    # Emergency defensive protocols
    if my_stunned > 0.5:
        if distance < close_range and opponent_attack_status > 0.5:
            return 6  # Block while stunned
        elif distance > medium_range and my_projectile_cooldown < 0.3:
            return 9  # Projectile to reset
        else:
            return 6  # Default block when stunned
    
    # Critical health situations
    if my_health < 0.18:
        if opponent_stunned > 0.5 and distance < close_range:
            # Last chance offensive
            if random.random() < 0.7:
                return 5  # Strong attack
            else:
                return 4  # Quick attack
        elif distance > far_range:
            if my_projectile_cooldown < 0.2:
                return 9  # Long range safety
            else:
                return 6  # Defensive
        elif distance < ultra_close_range and opponent_attack_status < 0.3:
            # Desperate close range gamble
            return 5 if random.random() < 0.6 else 4
        else:
            # Survival mode
            if opponent_attack_status > 0.6:
                return 6  # Block incoming
            elif distance < medium_close_range:
                # Try to create space while blocking
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
            else:
                return 6
    
    # Exploit stunned opponent
    if opponent_stunned > 0.5:
        if distance < medium_close_range:
            if distance > ultra_close_range:
                # Close the gap quickly
                return 2 if relative_pos > 0 else 1
            else:
                # Maximize damage on stunned target
                punish_choice = random.random()
                if punish_choice < 0.7:
                    return 5  # Heavy punish
                elif punish_choice < 0.9:
                    return 4  # Quick punish
                else:
                    return 9 if my_projectile_cooldown < 0.1 else 5
        else:
            # Rush in while they're helpless
            return 2 if relative_pos > 0 else 1
    
    # Opponent attack responses - hybrid defensive approach
    if opponent_attack_status > 0.6:
        if distance < close_range:
            # Close range defense with counter potential
            defense_choice = random.random()
            if my_health < opponent_health * 0.8:
                # Prioritize blocking when behind
                if defense_choice < 0.8:
                    return 6
                else:
                    return 8 if relative_pos > 0 else 7
            else:
                # Mix blocks and counters when ahead
                if defense_choice < 0.5:
                    return 6  # Pure block
                elif defense_choice < 0.7:
                    return 4  # Counter punch
                else:
                    return 8 if relative_pos > 0 else 7  # Block and reposition
        elif distance < medium_range:
            # Medium range - advance with block
            return 8 if relative_pos > 0 else 7
        else:
            # Far range - projectile counter or block
            if my_projectile_cooldown < 0.2 and random.random() < 0.4:
                return 9
            else:
                return 6
    
    # Range-based hybrid tactics
    if distance < point_blank_range:
        # Point blank - maximum pressure
        if opponent_block_status > 0.7:
            # Guard break mixups
            mixup_roll = random.random()
            if mixup_roll < 0.3:
                return 9 if my_projectile_cooldown < 0.1 else 5