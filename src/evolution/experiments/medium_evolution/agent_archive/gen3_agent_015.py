"""
Evolutionary Agent: gen3_agent_015
==================================

Metadata:
{
  "generation": 3,
  "fitness": 149.35999999999254,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: acd2c749d320b6cb
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
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cd = max(0.0, state[10]) if len(state) > 10 else 1.0
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_pos = max(0.0, min(1.0, state[11]))
    opp_y_pos = state[12]
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16]
    opp_blocking = state[17]
    opp_stunned = state[18] if len(state) > 18 else 0.0
    opp_projectile_cd = max(0.0, state[21]) if len(state) > 21 else 1.0
    
    # Enhanced tactical parameters for evolved balanced style
    close_range = 0.13
    medium_range = 0.26
    far_range = 0.42
    critical_health = 0.25
    winning_edge = 0.25
    losing_edge = -0.25
    wall_threshold = 0.15
    
    # Advanced aggression calculation with multi-factor analysis
    base_aggression = 0.52
    health_ratio = my_health / max(0.1, opp_health)
    
    # Enhanced momentum tracking with velocity integration
    momentum_factor = 0.0
    if abs(my_x_vel) > 0.25:
        momentum_factor = 0.12 if my_x_vel * relative_pos > 0 else -0.08
    
    # Opponent pressure assessment
    opponent_pressure = 0.0
    if opp_attacking > 0.5 or (distance < medium_range and abs(opp_x_vel) > 0.3):
        opponent_pressure = 0.15
    
    # Dynamic aggression with pressure response
    if health_advantage > winning_edge:
        dynamic_aggression = min(0.82, base_aggression + 0.25 + momentum_factor - opponent_pressure * 0.5)
    elif health_advantage < losing_edge:
        dynamic_aggression = max(0.28, base_aggression - 0.18 + momentum_factor - opponent_pressure * 0.3)
    else:
        dynamic_aggression = base_aggression + momentum_factor - opponent_pressure * 0.2
    
    # Enhanced wall awareness and positioning
    near_left_wall = my_x_pos < wall_threshold
    near_right_wall = my_x_pos > (1.0 - wall_threshold)
    opp_near_left_wall = opp_x_pos < wall_threshold
    opp_near_right_wall = opp_x_pos > (1.0 - wall_threshold)
    
    # Advanced movement prediction with acceleration consideration
    predicted_distance = distance
    if abs(opp_x_vel) > 0.15:
        velocity_factor = opp_x_vel * 0.12
        acceleration_bonus = 0.02 if abs(opp_x_vel) > 0.4 else 0.0
        
        if opp_x_vel * relative_pos < 0:  # Opponent approaching
            predicted_distance = max(0.0, distance - abs(velocity_factor) - acceleration_bonus)
        else:  # Opponent retreating
            predicted_distance = min(1.0, distance + abs(velocity_factor) + acceleration_bonus)
    
    # Vertical positioning consideration
    height_advantage = my_y_pos - opp_y_pos
    aerial_factor = 1.0 if abs(height_advantage) > 0.2 else 0.0
    
    # Cannot act while stunned
    if my_stunned > 0.5:
        return 0
    
    # Advanced emergency protocols with escape routes
    if my_health < critical_health and health_advantage < -0.35:
        # Multi-layered emergency response
        if opp_attacking > 0.5 and distance < close_range:
            # Immediate threat response
            escape_roll = random.random()
            if escape_roll < 0.6:
                return 6  # Block incoming attack
            elif near_left_wall:
                return 8  # Block and move right
            elif near_right_wall:
                return 7  # Block and move left
            else:
                return 3 if height_advantage < -0.1 else 6  # Jump or block
        
        elif distance > medium_range and my_projectile_cd < 0.18:
            return 9  # Long range harassment
        
        elif distance < far_range:
            # Intelligent repositioning based on stage position
            if near_left_wall and relative_pos < 0:
                return 8  # Must escape right
            elif near_right_wall and relative_pos > 0:
                return 7  # Must escape left
            elif opp_x_vel > 0.25 and relative_pos > 0:
                return 8  # Opponent chasing from left
            elif opp_x_vel < -0.25 and relative_pos < 0:
                return 7  # Opponent chasing from right
            else:
                # Space control retreat
                retreat_direction = 1 if my_x_pos > 0.5 else 2
                return retreat_direction
        else:
            return 6
    
    # Enhanced stunned opponent punishment system
    if opp_stunned > 0.5:
        if distance < close_range:
            # Optimized damage dealing with combo awareness
            if health_advantage < -0.1:  # Need maximum damage
                return 5  # Heavy kick
            else:
                # Balanced combo approach
                combo_choice = random.random()
                if combo_choice < 0.45:
                    return 5  # Kick for damage
                elif combo_choice < 0.75:
                    return 4  # Punch for speed
                else:
                    # Creative follow-up
                    if abs(height_diff) > 0.2:
                        return 3  # Jump attack
                    else:
                        return 5  # Another kick
        
        elif distance < medium_range:
            # Smart approach with positioning
            if abs(height_diff) > 0.25:
                return 3  # Height adjustment
            elif relative_pos > 0.2:
                return 2  # Close distance right
            elif relative_pos < -0.2:
                return 1  # Close distance left
            else:
                # Already positioned, attack
                return 4 if distance < 0.18 else 1 if relative_pos < 0 else 2
        
        else:
            # Long range stunned opponent approach
            if my_projectile_cd < 0.15:
                return 9  # Free projectile hit
            else:
                # Quick approach
                approach_move = 1 if relative_pos < 0 else 2