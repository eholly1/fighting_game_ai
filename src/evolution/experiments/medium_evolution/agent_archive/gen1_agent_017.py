"""
Evolutionary Agent: gen1_agent_017
==================================

Metadata:
{
  "generation": 1,
  "fitness": 24.49999999999834,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: f165170b8a11a5a8
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
    my_pos_x = max(0.0, min(1.0, state[2] if len(state) > 2 else 0.5))
    my_velocity_x = max(-1.0, min(1.0, state[4] if len(state) > 4 else 0.0))
    my_attack_status = max(0.0, min(1.0, state[7] if len(state) > 7 else 0.0))
    my_block_status = max(0.0, min(1.0, state[8] if len(state) > 8 else 0.0))
    my_projectile_cooldown = max(0.0, min(1.0, state[10] if len(state) > 10 else 0.0))
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = max(0.0, min(1.0, state[13] if len(state) > 13 else 0.5))
    opponent_velocity_x = max(-1.0, min(1.0, state[15] if len(state) > 15 else 0.0))
    opponent_attack_status = max(0.0, min(1.0, state[18] if len(state) > 18 else 0.0))
    opponent_block_status = max(0.0, min(1.0, state[19] if len(state) > 19 else 0.0))
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21] if len(state) > 21 else 0.0))
    
    # Define hybrid tactical parameters - balanced approach
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    critical_health = 0.2
    
    # Hybrid aggression system - adapts to situation
    base_aggression = 0.6
    defensive_threshold = -0.25
    aggressive_threshold = 0.25
    
    # Calculate adaptive aggression based on multiple factors
    situation_aggression = base_aggression
    if health_advantage > aggressive_threshold:
        situation_aggression = min(0.85, base_aggression + 0.25)
    elif health_advantage < defensive_threshold:
        situation_aggression = max(0.35, base_aggression - 0.25)
    
    # Adjust aggression based on opponent behavior
    if opponent_attack_status > 0.6:
        situation_aggression *= 0.8  # More cautious against aggressive opponent
    if opponent_block_status > 0.6:
        situation_aggression *= 1.2  # More aggressive against defensive opponent
    
    # Emergency survival mode
    if my_health < critical_health and health_advantage < -0.3:
        if opponent_attack_status > 0.5:
            return 6  # Block immediate threat
        
        if distance > medium_range:
            if my_projectile_cooldown < 0.3 and random.random() < 0.6:
                return 9  # Long range attack
            else:
                # Try to maintain distance
                if relative_pos > 0 and my_pos_x > 0.2:
                    return 7  # Move left with block
                elif relative_pos < 0 and my_pos_x < 0.8:
                    return 8  # Move right with block
                else:
                    return 6  # Block
        else:
            # Close range survival
            if random.random() < 0.7:
                return 6  # Block most of the time
            else:
                # Try to escape
                if my_pos_x < 0.3:
                    return 8  # Move right with block
                elif my_pos_x > 0.7:
                    return 7  # Move left with block
                else:
                    return 6  # Block
    
    # Opportunity recognition system
    opponent_vulnerable = False
    if opponent_attack_status < 0.2 and opponent_block_status < 0.3:
        opponent_vulnerable = True
    
    # Counter-attack opportunity
    counter_opportunity = False
    if my_attack_status < 0.3 and opponent_attack_status > 0.6:
        counter_opportunity = True
    
    # Positioning analysis
    corner_pressure = 0.0
    if my_pos_x < 0.15 or my_pos_x > 0.85:
        corner_pressure = 0.3
    
    opponent_corner_pressure = 0.0
    if opponent_pos_x < 0.15 or opponent_pos_x > 0.85:
        opponent_corner_pressure = 0.3
    
    # Movement prediction
    opponent_retreating = False
    if (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2):
        opponent_retreating = True
    
    # Ultra-close range combat (0.0 - 0.08)
    if distance <= ultra_close_range:
        # Immediate threat response
        if opponent_attack_status > 0.7:
            if counter_opportunity and random.random() < 0.4:
                return 4  # Quick counter punch
            else:
                return 6  # Block
        
        # Heavy pressure against blocking opponent
        if opponent_block_status > 0.6:
            mixup_choice = random.random()
            if mixup_choice < 0.2 and my_projectile_cooldown < 0.4:
                return 9  # Throw to break guard
            elif mixup_choice < 0.4:
                return 5  # Strong kick
            elif mixup_choice < 0.6:
                # Try to get behind
                if corner_pressure > 0:
                    return 3  # Jump out of corner
                elif relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                return 4  # Quick punch
        
        # Vulnerable opponent - capitalize
        if opponent_vulnerable:
            attack_intensity = situation_aggression + opponent_corner_pressure
            if attack_intensity > 0.7:
                combo_choice = random.random()
                if combo_choice < 0.5:
                    return 4  # Fast punch
                elif combo_choice < 0.8:
                    return 5  # Strong kick
                else:
                    return 3  # Jump attack
            else:
                return 4  # Safe punch
        
        # Neutral ultra-close
        pressure_choice = random.random()
        pressure_threshold = situation_aggression * 0.8
        
        if pressure_choice < pressure_threshold:
            # Attack pressure
            if pressure_choice < pressure_threshold * 0.6:
                return 4  # Punch
            else:
                return 5  # Kick
        else:
            # Defensive/positioning
            if corner_pressure > 0:
                return 3  # Jump to escape corner
            elif random.random() < 0.4:
                return 6  # Block