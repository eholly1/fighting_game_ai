"""
Evolutionary Agent: gen1_agent_019
==================================

Metadata:
{
  "generation": 1,
  "fitness": 238.45999999999373,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 923ff3cbe9054008
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
    
    # Extract my fighter status
    my_health = max(0.0, min(1.0, state[2])) if len(state) > 2 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[1] if len(state) > 1 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_stamina = state[5] if len(state) > 5 else 1.0
    my_attacking = state[7] if len(state) > 7 else 0.0
    my_blocking = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[9] if len(state) > 9 else 0.0
    my_recovery_frames = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent status
    opp_health = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[12] if len(state) > 12 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_stamina = state[16] if len(state) > 16 else 1.0
    opp_attacking = state[18] if len(state) > 18 else 0.0
    opp_blocking = state[19] if len(state) > 19 else 0.0
    opp_projectile_cooldown = state[20] if len(state) > 20 else 0.0
    opp_recovery_frames = state[21] if len(state) > 21 else 0.0
    
    # Hybrid fighter tactical parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_health_advantage = 0.25
    losing_health_advantage = -0.25
    corner_threshold = 0.15
    aggressive_distance = 0.35
    defensive_distance = 0.4
    
    # Calculate dynamic aggression level based on multiple factors
    base_aggression = 0.5
    health_aggression_bonus = health_advantage * 0.3
    stamina_aggression_bonus = (my_stamina - 0.5) * 0.2
    opponent_vulnerable_bonus = 0.0
    
    if opp_recovery_frames > 0.3 or opp_attacking > 0.5:
        opponent_vulnerable_bonus = 0.3
    
    current_aggression = base_aggression + health_aggression_bonus + stamina_aggression_bonus + opponent_vulnerable_bonus
    current_aggression = max(0.1, min(0.9, current_aggression))
    
    # Stage positioning analysis
    my_near_left_wall = my_x_pos < corner_threshold
    my_near_right_wall = my_x_pos > (1.0 - corner_threshold)
    opp_near_left_wall = opp_x_pos < corner_threshold
    opp_near_right_wall = opp_x_pos > (1.0 - corner_threshold)
    i_am_cornered = my_near_left_wall or my_near_right_wall
    opponent_cornered = opp_near_left_wall or opp_near_right_wall
    
    # Critical health emergency protocols
    if my_health < critical_health and health_advantage < -0.3:
        if distance < close_range and opp_attacking > 0.4:
            return 6  # Emergency block
        elif distance < medium_range:
            # Desperate escape with blocking movement
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif my_projectile_cooldown < 0.2:
            return 9  # Desperate projectile
        else:
            return 6  # Default to blocking
    
    # Opponent critical health - aggressive finishing
    if opp_health < critical_health and health_advantage > 0.2:
        if distance < close_range:
            # Finish with strong attacks
            if opp_blocking > 0.5:
                return 5  # Kick to break guard
            else:
                finishing_attack = random.random()
                if finishing_attack < 0.7:
                    return 5  # Strong kick
                else:
                    return 4  # Fast punch
        elif distance < medium_range:
            # Aggressive approach for finish
            if relative_pos > 0:
                return 2  # Move right aggressively
            else:
                return 1  # Move left aggressively
        elif my_projectile_cooldown < 0.1:
            return 9  # Projectile to finish
    
    # Corner escape when I'm trapped
    if i_am_cornered and distance < medium_range:
        if opp_attacking > 0.4:
            # Under pressure in corner
            escape_method = random.random()
            if escape_method < 0.4:
                return 6  # Block first
            elif escape_method < 0.7:
                return 3  # Jump out of corner
            else:
                # Move out with blocking
                if my_near_left_wall:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
        else:
            # Not under immediate pressure, create space
            if my_near_left_wall:
                return 2  # Move right
            else:
                return 1  # Move left
    
    # Corner pressure when opponent is trapped
    if opponent_cornered and distance < aggressive_distance:
        if distance < close_range:
            # Maximum corner pressure
            if opp_blocking > 0.6:
                # Break guard with varied attacks
                guard_break_choice = random.random()
                if guard_break_choice < 0.4:
                    return 5  # Heavy kick
                elif guard_break_choice < 0.7:
                    return 4  # Fast punch
                else:
                    return 3  # Jump attack mixup
            else:
                # Opponent not blocking - attack aggressively
                corner_attack_choice = random.random()
                if corner_attack_choice < 0.6:
                    return 5  # Strong kick
                else:
                    return 4  # Quick punch
        elif distance < medium_range:
            # Maintain corner pressure
            pressure_choice = random.random()
            if pressure_choice < 0.6:
                # Close distance for pressure
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif pressure_choice < 0.8 and my_projectile_cooldown < 0.1:
                return 9  # Projectile pressure
            else:
                return 3