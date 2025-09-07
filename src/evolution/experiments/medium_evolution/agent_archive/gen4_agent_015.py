"""
Evolutionary Agent: gen4_agent_015
==================================

Metadata:
{
  "generation": 4,
  "fitness": 73.7468000000026,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: daf55a4d221c9b51
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
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Enhanced rushdown tactical parameters
    ultra_close_range = 0.06
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.45
    max_range = 0.7
    
    # Adaptive aggression system
    base_aggression = 0.85
    health_multiplier = health_advantage * 0.3
    distance_multiplier = (1.0 - distance) * 0.2
    current_aggression = min(0.95, max(0.4, base_aggression + health_multiplier + distance_multiplier))
    
    # Movement prediction and interception
    opponent_movement_speed = abs(opponent_velocity_x)
    opponent_approaching = False
    if relative_pos > 0 and opponent_velocity_x > 0.2:
        opponent_approaching = True
    elif relative_pos < 0 and opponent_velocity_x < -0.2:
        opponent_approaching = True
    
    # Corner detection and management
    near_left_corner = my_pos_x < 0.15
    near_right_corner = my_pos_x > 0.85
    opponent_near_corner = opponent_pos_x < 0.15 or opponent_pos_x > 0.85
    
    # Critical health emergency actions
    if my_health < 0.15 and health_advantage < -0.5:
        if opponent_attack_status > 0.6:
            return 6  # Desperate block
        if distance < close_range and not (near_left_corner or near_right_corner):
            # Escape with blocking movement
            if relative_pos > 0:
                return 7  # Block and retreat left
            else:
                return 8  # Block and retreat right
        if distance > medium_range and my_projectile_cooldown < 0.4:
            return 9  # Projectile to buy time
    
    # Enhanced corner pressure system
    if opponent_near_corner and distance < medium_range:
        # Opponent is cornered - maximize pressure
        if distance > close_range:
            # Close the gap quickly
            if relative_pos > 0:
                return 2  # Rush right
            else:
                return 1  # Rush left
        else:
            # Apply corner pressure with varied attacks
            if opponent_block_status > 0.5:
                corner_mixup = random.random()
                if corner_mixup < 0.4:
                    return 5  # Heavy kick to break guard
                elif corner_mixup < 0.7:
                    return 3  # Jump for overhead
                else:
                    return 9 if my_projectile_cooldown < 0.6 else 4
            else:
                # Unleash corner combo
                return 4 if random.random() < 0.7 else 5
    
    # Avoid being cornered yourself
    if (near_left_corner or near_right_corner) and distance > ultra_close_range:
        if near_left_corner and relative_pos < 0:
            return 2  # Move away from corner
        elif near_right_corner and relative_pos > 0:
            return 1  # Move away from corner
    
    # Long range approach optimization
    if distance > max_range:
        # Mix projectiles with aggressive advancement
        if my_projectile_cooldown < 0.3 and random.random() < 0.35:
            return 9  # Projectile approach
        else:
            # Sprint toward opponent
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    elif distance > far_range:
        # Far range: Controlled aggression with projectile mix
        projectile_chance = 0.25 if my_projectile_cooldown < 0.4 else 0.0
        if random.random() < projectile_chance:
            return 9
        else:
            # Advance with purpose
            advance_roll = random.random()
            if advance_roll < current_aggression:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                # Jump advance for aerial approach
                return 3 if abs(height_diff) < 0.4 else (1 if relative_pos < 0 else 2)
    
    elif distance > medium_range:
        # Medium-far range: Setup for rush
        if opponent_block_status > 0.7:
            # Opponent defending heavily
            if my_projectile_cooldown < 0.5 and random.random() < 0.4:
                return 9  # Projectile to chip
            else:
                # Close distance for throw/mixup
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        # Detect opponent's projectile patterns
        if opponent_projectile_cooldown > 0.7 and distance > 0.35:
            # Opponent can't projectile, rush in
            rush_approach = random.random()
            if rush_approach < 0.7:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                return 3  # Jump approach
        
        # Standard medium range approach
        if random.random() < current_aggression + 0.1:
            if relative_pos > 0:
                return 2
            else:
                return 1
        else:
            # Mix with jump or projectile
            if my_projectile_cooldown < 0.4 and random.random() < 0.3:
                return 9
            else:
                return 3
    
    elif distance > close_range:
        # Close-medium range: Final approach phase
        if opponent_attack_status > 0.5:
            # Opponent attacking, block and advance or counter
            if my_health < opponent_health * 0.8:
                # Defensive approach
                if relative_pos > 0:
                    return 8  # Block advance right
                else:
                    return 7  # Block advance left
            else:
                # Counter attack opportunity
                counter_choice = random.random()
                if counter_choice < 0.4:
                    return 4  # Quick counter