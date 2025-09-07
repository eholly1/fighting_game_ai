"""
Evolutionary Agent: gen2_agent_005
==================================

Metadata:
{
  "generation": 2,
  "fitness": 189.81666666666305,
  "fighting_style": "evolved",
  "win_rate": 0.6666666666666666
}

Code Hash: 469693d1e89ec719
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
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cooldown = max(0.0, state[8])
    my_attack_cooldown = max(0.0, state[9])
    my_block_cooldown = max(0.0, state[10])
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cooldown = max(0.0, state[19])
    opp_attack_cooldown = max(0.0, state[20])
    opp_block_cooldown = max(0.0, state[21])
    
    # Define tactical ranges optimized for hybrid fighting
    very_close_range = 0.09
    close_range = 0.16
    medium_range = 0.30
    far_range = 0.48
    
    # Calculate dynamic aggression based on multiple factors
    base_aggression = 0.70
    health_multiplier = 1.0
    momentum_factor = 1.0
    positioning_factor = 1.0
    
    # Health-based strategy adjustments
    if health_advantage > 0.4:
        health_multiplier = 1.3  # Press advantage hard
    elif health_advantage > 0.1:
        health_multiplier = 1.1  # Slight aggression boost
    elif health_advantage < -0.4:
        health_multiplier = 0.6  # Focus on survival
    elif health_advantage < -0.1:
        health_multiplier = 0.8  # Cautious approach
    
    # Momentum calculation based on recent actions
    if my_attacking and not opp_blocking:
        momentum_factor = 1.2  # Continue pressure
    elif opp_attacking and my_blocking:
        momentum_factor = 0.9  # Stay defensive momentarily
    
    # Positioning advantage factor
    wall_distance_left = my_x_pos
    wall_distance_right = 1.0 - my_x_pos
    if wall_distance_left < 0.15 or wall_distance_right < 0.15:
        positioning_factor = 0.8  # More cautious near walls
    elif 0.3 < my_x_pos < 0.7:
        positioning_factor = 1.1  # Center stage advantage
    
    # Calculate final tactical intensity
    tactical_intensity = base_aggression * health_multiplier * momentum_factor * positioning_factor
    tactical_intensity = max(0.3, min(1.0, tactical_intensity))
    
    # Emergency override conditions
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health emergency protocols
    if my_health < 0.12:
        if opp_attacking and distance < close_range:
            return 6 if my_block_cooldown < 0.2 else 0
        elif distance > medium_range and my_projectile_cooldown < 0.15:
            return 9  # Desperate projectile
        elif distance < very_close_range and not opp_blocking:
            # Last chance all-in
            return 5 if my_attack_cooldown < 0.1 else 4
        else:
            # Survival mode - escape with blocking
            if wall_distance_left < wall_distance_right:
                return 8  # Move right with block
            else:
                return 7  # Move left with block
    
    # Capitalize on stunned opponent with improved timing
    if opp_stunned:
        if distance < close_range:
            if my_attack_cooldown < 0.08:
                # Optimal punishment combo
                punishment_choice = random.random()
                if distance < very_close_range:
                    return 5 if punishment_choice < 0.75 else 4  # Heavy emphasis on kicks
                else:
                    return 4 if punishment_choice < 0.6 else 5  # Mix based on range
            else:
                # Position for guaranteed follow-up
                if distance > very_close_range:
                    return 2 if relative_pos > 0 else 1
                else:
                    return 0  # Wait for attack window
        else:
            # Rush in efficiently
            if distance > medium_range and my_projectile_cooldown < 0.1:
                return 9  # Quick projectile before closing
            else:
                return 2 if relative_pos > 0 else 1
    
    # Advanced counter-attack system
    if opp_attacking:
        if distance < very_close_range:
            # Point blank defense
            if my_block_cooldown < 0.1:
                return 6  # Pure block at closest range
            else:
                # Cannot block - emergency evasion
                if abs(my_y_velocity) < 0.2:
                    return 3  # Jump away
                else:
                    return 2 if relative_pos < 0 else 1  # Lateral escape
        elif distance < close_range:
            # Close range counter opportunities
            if my_block_cooldown < 0.15:
                counter_strategy = random.random()
                if counter_strategy < 0.5:
                    return 6  # Standard block
                elif counter_strategy < 0.8:
                    # Counter with movement
                    return 8 if relative_pos > 0 else 7
                else:
                    # Risky counter-attack
                    return 4 if my_attack_cooldown < 0.1 else 6
            else:
                # No block available - evasive action
                return 1 if relative_pos > 0 else 2
        elif distance < medium_range:
            # Medium range preparation
            if my_projectile_cooldown < 0.2 and random.random() < 0.4:
                return 9  # Interrupt with projectile
            else:
                return 8 if relative_pos > 0 else 7  # Advance with block
    
    # VERY CLOSE RANGE - Point blank combat
    if distance < very_close_range:
        if my_attack_cooldown < 0.06:
            if opp_blocking:
                # Guard breaking at point blank
                guard_break_intensity = 0.7 + (health_advantage * 0.15)
                if random.random() < guard_break_intensity:
                    # Varied guard break attempts
                    break_method = random.random()
                    if break_method < 0.4:
                        return 5  # Heavy kick
                    elif break_method < 0.7:
                        return 4  # Quick punch
                    else:
                        return