"""
Evolutionary Agent: gen2_agent_009
==================================

Metadata:
{
  "generation": 2,
  "fitness": 189.37999999999099,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 081f799a923d2c29
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information with defensive bounds
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract my fighter status
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = max(0.0, min(1.0, state[0]))
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[5]
    my_blocking = state[6]
    my_stunned = state[7]
    my_projectile_cd = max(0.0, state[10])
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_pos = max(0.0, min(1.0, state[11]))
    opp_y_pos = state[12]
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16]
    opp_blocking = state[17]
    opp_stunned = state[18]
    opp_projectile_cd = max(0.0, state[21]) if len(state) > 21 else 1.0
    
    # Define evolved tactical parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.22
    winning_threshold = 0.2
    losing_threshold = -0.2
    wall_threshold = 0.12
    
    # Advanced position analysis
    near_left_wall = my_x_pos < wall_threshold
    near_right_wall = my_x_pos > (1.0 - wall_threshold)
    opp_near_left_wall = opp_x_pos < wall_threshold
    opp_near_right_wall = opp_x_pos > (1.0 - wall_threshold)
    
    # Calculate momentum and velocity factors
    velocity_factor = abs(my_x_vel) + abs(opp_x_vel)
    approaching = (relative_pos > 0 and my_x_vel > 0) or (relative_pos < 0 and my_x_vel < 0)
    retreating = (relative_pos > 0 and my_x_vel < 0) or (relative_pos < 0 and my_x_vel > 0)
    
    # Evolved aggression calculation
    base_aggression = 0.52
    health_factor = health_advantage * 0.3
    distance_factor = (1.0 - distance) * 0.15
    position_factor = 0.0
    
    # Position advantage calculation
    if (opp_near_left_wall or opp_near_right_wall) and not (near_left_wall or near_right_wall):
        position_factor = 0.15
    elif (near_left_wall or near_right_wall) and not (opp_near_left_wall or opp_near_right_wall):
        position_factor = -0.15
    
    dynamic_aggression = base_aggression + health_factor + distance_factor + position_factor
    dynamic_aggression = max(0.1, min(0.9, dynamic_aggression))
    
    # Cannot act while stunned
    if my_stunned > 0.5:
        return 0
    
    # Exploit stunned opponent with enhanced tactics
    if opp_stunned > 0.5:
        if distance < close_range:
            # Maximize damage on stunned opponent
            damage_roll = random.random()
            if damage_roll < 0.7:
                return 5  # Kick for maximum damage
            else:
                return 4  # Mix in punches for combo potential
        elif distance < medium_range:
            # Rush to close distance
            if abs(relative_pos) > 0.05:
                return 2 if relative_pos > 0 else 1
            else:
                return 5  # Kick when in range
        else:
            # Use projectile if available, otherwise close distance
            if my_projectile_cd < 0.25:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Emergency survival tactics
    if my_health < critical_health and health_advantage < -0.35:
        # Desperate defensive mode
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Block immediate threat
        elif distance > medium_range and my_projectile_cd < 0.15:
            return 9  # Keep distance with projectile
        elif distance < medium_range:
            # Escape with blocking movement
            if near_left_wall:
                return 8
            elif near_right_wall:
                return 7
            else:
                escape_dir = 7 if relative_pos > 0 else 8
                return escape_dir
        else:
            # Default defensive stance
            return 6
    
    # Finishing mode when opponent is low
    if opp_health < critical_health and health_advantage > 0.25:
        if distance < close_range:
            # Aggressive finishing
            finish_roll = random.random()
            if finish_roll < 0.6:
                return 5  # Power attacks
            elif finish_roll < 0.85:
                return 4  # Quick attacks
            else:
                return 3  # Jump attacks for mixup
        elif distance < medium_range:
            # Close for the kill
            return 2 if relative_pos > 0 else 1
        else:
            # Projectile pressure
            if my_projectile_cd < 0.3:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Close range combat system
    if distance < close_range:
        # Handle blocking opponent
        if opp_blocking > 0.5:
            guard_break_roll = random.random()
            if guard_break_roll < 0.2:
                return 5  # Heavy attack to break guard
            elif guard_break_roll < 0.35:
                return 3  # Jump to change attack angle
            elif guard_break_roll < 0.6:
                # Attempt flanking maneuver
                if not near_right_wall and relative_pos < -0.1:
                    return 2
                elif not near_left_wall and relative_pos > 0.1:
                    return 1
                else:
                    return 5  # Power attack if can't flank
            elif guard_break_roll < 0.8:
                return 4  # Quick jab
            else:
                # Create space and reset
                if not near_left_wall and relative_pos > 0:
                    return 1
                elif not near_right_wall and relative_pos < 0:
                    return 2
                else:
                    return 3  # Jump if trapped
        
        # Counter attacking opponent
        elif opp_attacking > 0.5:
            counter_strategy = random.random()
            if health_advantage < losing_threshold:
                # Defensive counter when losing
                if counter_strategy < 0.55:
                    return 6  # Block first
                elif counter_strategy < 0.75:
                    return 4  # Quick counter
                else:
                    return 3  # Jump away
            else:
                # Aggressive counter when even or winning
                if counter_strategy < 0.25:
                    return 6