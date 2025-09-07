"""
Evolutionary Agent: gen2_agent_018
==================================

Metadata:
{
  "generation": 2,
  "fitness": 91.5399999999971,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 36a6ea70d01cd5c2
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
    
    # Extract detailed fighter status
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
    ultra_close_range = 0.07
    close_range = 0.14
    medium_range = 0.28
    far_range = 0.45
    max_range = 0.65
    
    # Dynamic aggression system
    base_aggression = 0.85
    health_modifier = health_advantage * 0.2
    distance_modifier = (1.0 - distance) * 0.15
    current_aggression = min(0.95, max(0.4, base_aggression + health_modifier + distance_modifier))
    
    # Pressure momentum tracking (simulated)
    pressure_momentum = 0.0
    if my_attack_status > 0.5:
        pressure_momentum += 0.3
    if opponent_block_status > 0.5:
        pressure_momentum += 0.2
    if distance < close_range:
        pressure_momentum += 0.25
    
    # Critical health emergency protocols
    if my_health < 0.15 and health_advantage < -0.5:
        if opponent_attack_status > 0.6:
            return 6  # Desperate block
        if distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Last resort projectile
        if opponent_velocity_x > 0.4 and relative_pos < 0:
            return 7  # Escape left with block
        elif opponent_velocity_x < -0.4 and relative_pos > 0:
            return 8  # Escape right with block
    
    # Advanced opponent behavior detection
    opponent_defensive = opponent_block_status > 0.4 or (opponent_velocity_x * relative_pos < -0.2)
    opponent_aggressive = opponent_attack_status > 0.4 or (opponent_velocity_x * relative_pos > 0.2)
    opponent_zoning = distance > medium_range and opponent_projectile_cooldown < 0.3
    
    # Corner awareness and exploitation
    stage_edge_threshold = 0.15
    near_left_edge = my_pos_x < stage_edge_threshold
    near_right_edge = my_pos_x > (1.0 - stage_edge_threshold)
    opponent_near_left = opponent_pos_x < stage_edge_threshold
    opponent_near_right = opponent_pos_x > (1.0 - stage_edge_threshold)
    
    # Opponent cornered - increase pressure
    opponent_cornered = opponent_near_left or opponent_near_right
    if opponent_cornered and distance < medium_range:
        current_aggression = min(0.98, current_aggression + 0.2)
    
    # Self cornered - escape priority
    self_cornered = near_left_edge or near_right_edge
    if self_cornered and distance < close_range and health_advantage < 0:
        if near_left_edge and relative_pos < 0:
            return 8  # Escape right with block
        elif near_right_edge and relative_pos > 0:
            return 7  # Escape left with block
    
    # Ultra-close range combat (prime rushdown zone)
    if distance <= ultra_close_range:
        # Immediate threat response
        if opponent_attack_status > 0.8:
            if my_health < opponent_health * 0.6:
                return 6  # Block when significantly behind
            elif random.random() < 0.25:
                return 6  # Occasional defensive block
            else:
                # Counter with fast attack
                return 4 if random.random() < 0.7 else 5
        
        # Guard break sequences against defensive opponents
        elif opponent_block_status > 0.7:
            guard_break_option = random.random()
            if guard_break_option < 0.2 and my_projectile_cooldown < 0.4:
                return 9  # Point blank projectile
            elif guard_break_option < 0.4:
                return 5  # Strong kick to break guard
            elif guard_break_option < 0.6:
                if abs(height_diff) < 0.4:
                    return 3  # Jump for overhead
                else:
                    return 4  # Quick punch
            elif guard_break_option < 0.8:
                # Micro-movement for repositioning
                if my_pos_x > opponent_pos_x:
                    return 1 if random.random() < 0.5 else 4
                else:
                    return 2 if random.random() < 0.5 else 4
            else:
                return 4  # Fast punch to maintain pressure
        
        # Maximum pressure offense
        else:
            offense_choice = random.random()
            aggression_bonus = current_aggression - 0.5
            
            if offense_choice < (0.6 + aggression_bonus):
                # Primary pressure: fast punches
                return 4
            elif offense_choice < (0.85 + aggression_bonus * 0.5):
                # Secondary pressure: strong kicks
                return 5
            elif offense_choice < 0.92:
                # Mixup: jump attack
                return 3
            else:
                # Maintain position and pressure
                return 4
    
    # Close range engagement
    elif distance <= close_range:
        # React to opponent's immediate actions
        if opponent_attack_status > 0.65:
            if health_advantage < -0.2:
                # Defensive approach when behind
                return 6
            else:
                # Trade or counter when ahead
                counter_choice = random.random()
                if counter_choice < 0.4:
                    return 4  # Fast counter
                elif counter_choice < 0.7:
                    return 6  # Block then counter next frame
                else:
                    return 5  # Heavy counter
        
        # Approach blocking opponent
        elif opponent_block_status > 0.5:
            approach_option = random.random()
            if approach_option < 0.3:
                # Close final gap
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif approach_option < 0.5:
                return 3