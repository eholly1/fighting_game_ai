"""
Evolutionary Agent: gen1_agent_020
==================================

Metadata:
{
  "generation": 1,
  "fitness": 24.70066666666662,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 374fc7756cd3b79f
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
    
    # Extract my fighter information
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_combo_counter = state[9] if len(state) > 9 else 0.0
    my_special_meter = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    opp_stunned = state[18] if len(state) > 18 else 0.0
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_combo_counter = state[20] if len(state) > 20 else 0.0
    opp_special_meter = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid fighter strategic parameters
    danger_zone = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    max_range = 0.8
    
    # Health thresholds
    critical_health = 0.2
    low_health = 0.4
    moderate_health = 0.6
    good_health = 0.8
    
    # Tactical parameters
    projectile_ready = my_projectile_cooldown < 0.2
    opp_projectile_ready = opp_projectile_cooldown < 0.2
    aggression_threshold = 0.15
    defensive_threshold = -0.25
    
    # Stage positioning
    stage_center = 0.5
    left_corner_zone = 0.2
    right_corner_zone = 0.8
    
    my_near_left = my_x_pos < left_corner_zone
    my_near_right = my_x_pos > right_corner_zone
    opp_near_left = opp_x_pos < left_corner_zone
    opp_near_right = opp_x_pos > right_corner_zone
    
    # Movement prediction
    predicted_opp_x = opp_x_pos + (opp_velocity_x * 0.1)
    future_distance = abs(my_x_pos - predicted_opp_x)
    
    # Adaptation tracking variables
    time_factor = random.random() * 0.3  # Add unpredictability
    
    # CRITICAL SURVIVAL MODE
    if my_health <= critical_health:
        if distance < danger_zone and opp_attacking > 0.5:
            return 6  # Emergency block
        
        if distance < close_range:
            # Escape dangerous close range
            if opp_stunned > 0.5:
                # Punish stunned opponent even at low health
                return 5 if random.random() < 0.7 else 4
            elif relative_pos > 0 and not my_near_left:
                return 7  # Move left with block
            elif relative_pos < 0 and not my_near_right:
                return 8  # Move right with block
            else:
                return 6  # Block if cornered
        
        # Try to zone from safe distance
        if projectile_ready and distance > medium_range:
            return 9
        
        # Create space when possible
        if distance < far_range:
            if relative_pos > 0 and not my_near_left:
                return 1  # Retreat left
            elif relative_pos < 0 and not my_near_right:
                return 2  # Retreat right
            
        return 6  # Default to blocking when desperate
    
    # OPPONENT STUNNED - MAXIMUM OPPORTUNITY
    if opp_stunned > 0.5:
        if distance < close_range:
            # Close range punishment
            combo_choice = random.random()
            if combo_choice < 0.5:
                return 5  # Heavy kick for damage
            elif combo_choice < 0.8:
                return 4  # Fast punch to extend combo
            else:
                return 5  # Another heavy attack
        elif distance < medium_range:
            # Rush in for punishment
            if relative_pos > 0:
                return 2  # Move right toward stunned opponent
            else:
                return 1  # Move left toward stunned opponent
        else:
            # Long range - projectile while closing
            if projectile_ready:
                return 9
            else:
                # Close distance quickly
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # SELF STUNNED - DEFENSIVE RECOVERY
    if my_stunned > 0.5:
        if distance < close_range and opp_attacking > 0.3:
            return 6  # Block to minimize damage
        elif distance < medium_range:
            # Create space while recovering
            if relative_pos > 0 and not my_near_left:
                return 7  # Move left with block
            elif relative_pos < 0 and not my_near_right:
                return 8  # Move right with block
            else:
                return 6  # Block and wait
        else:
            return 6  # Safe distance, just block
    
    # ANTI-AIR AND AERIAL CONTROL
    if height_diff < -0.4:  # Opponent jumping above
        if distance < medium_range:
            if projectile_ready:
                return 9  # Anti-air projectile
            else:
                # Position for landing punishment
                predicted_landing = opp_x_pos + (opp_velocity_x * 0.2)
                if predicted_landing > my_x_pos and not my_near_right:
                    return 2  # Move toward landing spot
                elif predicted_landing < my_x_pos and not my_near_left:
                    return 1  # Move towar