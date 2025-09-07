"""
Evolutionary Agent: gen3_agent_017
==================================

Metadata:
{
  "generation": 3,
  "fitness": 269.3599999999937,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 9e77455a20d88a20
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_position = state[0]
    my_velocity_x = state[7]
    my_velocity_y = state[8]
    my_attack_status = max(0.0, state[4])
    my_block_status = max(0.0, state[5])
    my_projectile_cooldown = max(0.0, state[6])
    
    # Extract opponent status
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_position = state[11]
    opponent_velocity_x = state[18]
    opponent_velocity_y = state[19]
    opponent_attack_status = max(0.0, state[15])
    opponent_block_status = max(0.0, state[16])
    opponent_projectile_cooldown = max(0.0, state[17])
    
    # Strategic range definitions for hybrid approach
    ultra_close_range = 0.05
    close_range = 0.12
    mid_range = 0.25
    far_range = 0.4
    ultra_far_range = 0.6
    
    # Health thresholds
    critical_health = 0.15
    low_health = 0.35
    good_health = 0.65
    
    # Positioning thresholds
    corner_threshold = 0.8
    near_corner_threshold = 0.65
    center_zone = 0.3
    
    # Status checks
    projectile_ready = my_projectile_cooldown < 0.08
    projectile_charging = my_projectile_cooldown < 0.15
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    
    # Movement analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > -0.2) or (relative_pos < 0 and opponent_velocity_x < 0.2)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.3) or (relative_pos < 0 and opponent_velocity_x > 0.3)
    opponent_airborne = abs(height_diff) > 0.25
    
    # Positioning awareness
    am_cornered = abs(my_position) > corner_threshold
    am_near_corner = abs(my_position) > near_corner_threshold
    opponent_cornered = abs(opponent_position) > corner_threshold
    in_center = abs(my_position) < center_zone
    
    # Adaptive aggression calculation
    base_aggression = 0.65
    health_modifier = health_advantage * 0.35
    distance_modifier = (mid_range - distance) * 0.4
    position_modifier = 0.15 if opponent_cornered else (-0.1 if am_cornered else 0)
    current_aggression = max(0.25, min(0.9, base_aggression + health_modifier + distance_modifier + position_modifier))
    
    # Defense priority system
    defense_urgency = 0.4
    if my_health < critical_health:
        defense_urgency = 0.85
    elif my_health < low_health:
        defense_urgency = 0.65
    elif health_advantage < -0.4:
        defense_urgency = 0.7
    
    # Emergency survival mode - critical health
    if my_health <= critical_health:
        if opponent_attack_status > 0 and distance < mid_range:
            return 6  # Priority block
        
        if distance < close_range:
            if am_cornered:
                # Cornered and desperate
                if projectile_ready and random.random() < 0.4:
                    return 9  # Point blank projectile gamble
                elif opponent_airborne:
                    return 4  # Anti-air attempt
                else:
                    return 6  # Block and hope
            else:
                # Escape with blocking movement
                escape_direction = 7 if relative_pos > 0 else 8
                return escape_direction
        
        # Create space when possible
        if distance < mid_range and not am_cornered:
            retreat_direction = 1 if relative_pos > 0 else 2
            return retreat_direction
        
        # Long range chip damage attempt
        if projectile_ready and distance > mid_range:
            return 9
        
        return 6  # Default to blocking
    
    # Opponent attack response system
    if opponent_attack_status > 0:
        threat_level = 1.0 - distance
        
        if distance < ultra_close_range:
            return 6  # Must block at point blank
        elif distance < close_range:
            if my_health > low_health and not am_near_corner:
                # Mobile defense
                defensive_move = 7 if relative_pos > 0 else 8
                return defensive_move if random.random() < 0.7 else 6
            else:
                return 6  # Safe block
        elif distance < mid_range:
            # Medium range threat
            if projectile_ready and random.random() < 0.5:
                return 9  # Counter projectile
            else:
                return 6  # Block incoming
        else:
            # Long range attack - advance or counter
            if projectile_ready:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Anti-air system
    if opponent_airborne:
        if distance < mid_range:
            if projectile_ready:
                return 9  # Projectile anti-air
            elif distance < close_range:
                return 4  # Quick anti-air punch
            else:
                # Position for landing punish
                return 2 if relative_pos > 0 else 1
        elif distance < far_range and projectile_ready:
            return 9  # Long range anti-air
    
    # Projectile warfare management
    if opponent_projectile_ready and distance > mid_range:
        if projectile_ready:
            if random.random() < 0.6:
                return 9  # Projectile duel
            else:
                # Evasive approach
                return 2 if relative_pos > 0 else 1
        else:
            # Dodge or advance
            if distance > far_range:
                return 2 if relative_pos > 0 else 1
            else:
                return 3 if random.random() < 0.3 else 6
    
    # Range-based hybrid combat system
    
    # Ultra close range - explosive mixups
    if distance <= ultra_close_range:
        if current_aggression > 0.6:
            if opponent_block_status > 0:
                # Guard pressure sequence
                choice = random.random()
                if choice < 0.35 and projectile_ready:
                    return 9  # Point blank projectile mixup
                elif choice < 0.7:
                    return 5  # Power kick guard break
                else:
                    # Micro spacing
                    return 1 if relative_pos > 0.2 else 2
            else:
                # Open opponent - damage maximize
                return 5 if random.random() < 0.65 else 4
        else:
            # Defensive reset
            if random.random() < defense_urgency:
                return 6
            else:
                return 4  # Quick