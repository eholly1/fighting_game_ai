"""
Evolutionary Agent: gen0_agent_020
==================================

Metadata:
{
  "generation": 0,
  "fitness": -7.051333333333625,
  "fighting_style": "aggressive",
  "win_rate": 0.0
}

Code Hash: b50f4886226c029c
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22])) if len(state) > 22 else 0.5
    relative_pos = max(-1.0, min(1.0, state[23])) if len(state) > 23 else 0.0
    health_advantage = max(-1.0, min(1.0, state[25])) if len(state) > 25 else 0.0
    
    # Extract player and opponent states
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_is_attacking = state[5] if len(state) > 5 else 0.0
    my_is_blocking = state[6] if len(state) > 6 else 0.0
    my_attack_cooldown = state[7] if len(state) > 7 else 0.0
    my_block_cooldown = state[8] if len(state) > 8 else 0.0
    my_stun_time = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_x_pos = state[11] if len(state) > 11 else 0.5
    opponent_y_pos = state[13] if len(state) > 13 else 0.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_velocity_y = state[15] if len(state) > 15 else 0.0
    opponent_is_attacking = state[16] if len(state) > 16 else 0.0
    opponent_is_blocking = state[17] if len(state) > 17 else 0.0
    opponent_attack_cooldown = state[18] if len(state) > 18 else 0.0
    opponent_block_cooldown = state[19] if len(state) > 19 else 0.0
    opponent_stun_time = state[20] if len(state) > 20 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    height_difference = state[24] if len(state) > 24 else 0.0
    
    # Define aggressive strategy parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    max_aggression_health = 0.8
    min_aggression_health = 0.2
    attack_mix_randomness = 0.4
    pressure_threshold = 0.35
    
    # Calculate aggression level based on health advantage
    base_aggression = 0.85  # High base aggression for aggressive style
    if health_advantage > 0.1:
        aggression_multiplier = 1.2
    elif health_advantage < -0.2:
        aggression_multiplier = 0.7
    else:
        aggression_multiplier = 1.0
    
    current_aggression = min(1.0, base_aggression * aggression_multiplier)
    
    # Emergency defensive measures when critically low health
    if my_health < 0.15 and health_advantage < -0.4:
        if distance < close_range and opponent_is_attacking > 0.5:
            return 6  # Emergency block
        elif distance > medium_range:
            if my_projectile_cooldown < 0.1 and random.random() < 0.7:
                return 9  # Desperate projectile
            else:
                return 6  # Block and wait
    
    # Stunned - can only block or idle
    if my_stun_time > 0.1:
        if opponent_is_attacking > 0.5 and distance < medium_range:
            return 6  # Block while stunned
        return 0  # Idle to recover
    
    # Opponent is stunned - maximum aggression opportunity
    if opponent_stun_time > 0.2:
        if distance < close_range:
            # Mix heavy attacks when opponent is stunned
            if random.random() < 0.6:
                return 5  # Kick for heavy damage
            else:
                return 4  # Punch for speed
        elif distance < medium_range:
            # Close distance quickly to capitalize
            if relative_pos > 0:
                return 2  # Move right toward stunned opponent
            else:
                return 1  # Move left toward stunned opponent
        else:
            # Long range projectile on stunned opponent
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                # Move closer while projectile cools down
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Aggressive close-range combat
    if distance < close_range:
        # Check if opponent is blocking heavily
        opponent_blocking_heavily = opponent_is_blocking > 0.6
        
        # If opponent is attacking, decide whether to trade or block
        if opponent_is_attacking > 0.5:
            if health_advantage > 0.2 and random.random() < current_aggression:
                # Trade hits when ahead
                if my_attack_cooldown < 0.1:
                    return 4 if random.random() < 0.7 else 5
                else:
                    return 6  # Block if can't attack
            else:
                # Block when behind or playing safer
                return 6
        
        # Opponent not attacking - full aggression
        if my_attack_cooldown < 0.1:
            if opponent_blocking_heavily:
                # Mix kicks to break blocks, some punches for speed
                if random.random() < 0.7:
                    return 5  # Kick to break block
                else:
                    return 4  # Fast punch
            else:
                # Open opponent - mix attacks unpredictably
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Quick punch
                elif attack_choice < 0.8:
                    return 5  # Power kick
                else:
                    return 9 if my_projectile_cooldown < 0.1 else 4  # Surprise projectile
        else:
            # Attack on cooldown - apply pressure through positioning
            if opponent_velocity_x > 0.1:  # Opponent moving right
                return 2  # Chase right
            elif opponent_velocity_x < -0.1:  # Opponent moving left
                return 1  # Chase left
            else:
                return 6  # Block briefly while waiting for cooldown
    
    # Medium range - aggressive positioning and setup
    elif distance < medium_range:
        # Try to close distance for attacks
        closing_distance = True
        
        # Check if opponent is preparing projectile
        if opponent_projectile_cooldown < 0.1 and distance > 0.2:
            if random.random() < 0.6:
                closing_distance = True  # Aggressive approach through projectiles
            else:
                # Occasionally respect projectile threat
                if my_projectile_cooldown < 0.1:
                    return 9  # Counter-projectile
        
        # Opponent