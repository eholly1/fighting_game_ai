"""
Evolutionary Agent: gen0_agent_026
==================================

Metadata:
{
  "generation": 0,
  "fitness": 164.93093333332843,
  "fighting_style": "counter_puncher",
  "win_rate": 0.3333333333333333
}

Code Hash: c3130490b9df99f1
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
    
    # Extract player and opponent state information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_pos_x = state[0]
    my_velocity_x = state[2]
    my_velocity_y = state[3]
    my_is_attacking = state[4] > 0.5
    my_is_blocking = state[5] > 0.5
    my_projectile_cooldown = state[6]
    my_stun_timer = state[7] if len(state) > 7 else 0.0
    my_combo_count = state[8] if len(state) > 8 else 0.0
    my_energy = state[9] if len(state) > 9 else 1.0
    my_is_grounded = state[10] > 0.5 if len(state) > 10 else True
    
    opp_health = state[12] if state[12] >= 0 else 0.5
    opp_pos_x = state[11]
    opp_velocity_x = state[13]
    opp_velocity_y = state[14]
    opp_is_attacking = state[15] > 0.5
    opp_is_blocking = state[16] > 0.5
    opp_projectile_cooldown = state[17]
    opp_stun_timer = state[18] if len(state) > 18 else 0.0
    opp_combo_count = state[19] if len(state) > 19 else 0.0
    opp_energy = state[20] if len(state) > 20 else 1.0
    opp_is_grounded = state[21] > 0.5 if len(state) > 21 else True
    
    # Define tactical ranges and thresholds
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_threshold = 0.2
    losing_threshold = -0.3
    
    # Counter-puncher strategic parameters
    patience_factor = 0.75  # Higher means more patient
    counter_window = 0.8    # Reaction time to opponent attacks
    defensive_bonus = 0.6   # Extra defensive behavior
    punish_aggression = 0.85 # How much to punish opponent mistakes
    
    # Emergency defensive mode when critically low health
    if my_health < critical_health and health_advantage < -0.4:
        if distance < close_range:
            if opp_is_attacking:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            # Create distance when low health
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        else:
            # Long range harassment
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile attack
            else:
                return 6  # Block while cooldown recovers
    
    # Counter-attack when opponent is vulnerable
    if opp_stun_timer > 0.3 or (opp_is_attacking and distance < close_range):
        if distance < close_range:
            # Punish with strong attacks
            if random.random() < punish_aggression:
                return 5 if my_energy > 0.4 else 4  # Kick or punch based on energy
            else:
                return 4  # Quick punch counter
        elif distance < medium_range:
            # Close in for counter-attack
            if relative_pos > 0:
                return 2  # Move right to close distance
            else:
                return 1  # Move left to close distance
    
    # Opponent is attacking - defensive counter-puncher response
    if opp_is_attacking:
        if distance < close_range:
            # In danger zone - prioritize defense
            if random.random() < defensive_bonus:
                return 6  # Block the attack
            else:
                # Counter-attack opportunity
                if my_velocity_x * relative_pos < 0:  # Moving toward opponent
                    return 4  # Quick counter punch
                else:
                    return 6  # Play it safe with block
        elif distance < medium_range:
            # Medium range - position for counter
            if opp_velocity_x * relative_pos > 0:  # Opponent advancing
                return 6  # Prepare to block
            else:
                # Opponent retreating - pursue carefully
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        else:
            # Long range - wait and projectile
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile while they attack air
            else:
                return 0  # Wait patiently
    
    # Opponent is blocking - probe for openings
    if opp_is_blocking:
        if distance < close_range:
            # Try to break guard or reposition
            if random.random() < 0.4:
                return 5  # Strong kick to break block
            elif random.random() < 0.3:
                # Try to get behind them
                if relative_pos > 0:
                    return 1  # Move left to get around
                else:
                    return 2  # Move right to get around
            else:
                return 0  # Wait for them to drop guard
        elif distance < medium_range:
            # Maintain pressure but stay safe
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile pressure
            else:
                # Slight positioning adjustment
                if abs(relative_pos) > 0.1:
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    return 0  # Wait for opening
        else:
            # Long range against blocker
            if my_projectile_cooldown < 0.4:
                return 9  # Projectile harassment
            else:
                return 0  # Patient waiting
    
    # Health-based strategic adjustments
    if health_advantage > winning_threshold:
        # Winning - controlled aggression
        if distance < close_range:
            if random.random() < 0.6:
                return 5 if my_energy > 0.5 else 4  # Strong attacks when winning
            else:
                return 6  # Still defensive but less so
        elif distance < medium_range:
            # Press advantage by closing distance
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        else:
            # Long range control
            if my_projectile_cooldown < 0.5:
                return 9  # Projectile
            else:
                # Close to medium range
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
    
    elif health_advantage < losing_threshold:
        # Losing - extra defensive
        if distance < close_range:
            if random.random() < 0.8:
                return 6  # Heavy blocking when losing
            else:
                # Desperate counter
                return