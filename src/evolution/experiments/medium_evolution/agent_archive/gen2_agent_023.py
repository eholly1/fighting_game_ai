"""
Evolutionary Agent: gen2_agent_023
==================================

Metadata:
{
  "generation": 2,
  "fitness": 21.519999999998834,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 76467ea47ab1f08f
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
    
    # Extract comprehensive fighter information
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent information
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Enhanced hybrid strategic parameters
    close_range = 0.13
    medium_range = 0.26
    far_range = 0.42
    optimal_range = 0.38
    danger_range = 0.08
    
    # Health thresholds
    critical_health = 0.2
    low_health = 0.4
    dominant_health = 0.25
    desperate_threshold = -0.4
    
    # Cooldown thresholds
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_soon = my_projectile_cooldown < 0.15
    attack_ready = my_attack_cooldown < 0.05
    block_ready = my_block_cooldown < 0.05
    
    # Opponent threat assessment
    opp_projectile_ready = opp_projectile_cooldown < 0.1
    opp_attack_ready = opp_attack_cooldown < 0.1
    
    # Movement analysis
    opponent_approaching = (relative_pos > 0 and opp_x_velocity < -0.15) or (relative_pos < 0 and opp_x_velocity > 0.15)
    opponent_retreating = (relative_pos > 0 and opp_x_velocity > 0.15) or (relative_pos < 0 and opp_x_velocity < -0.15)
    opponent_stationary = abs(opp_x_velocity) < 0.1
    
    # Stage positioning
    corner_danger_left = my_x_pos < -0.7
    corner_danger_right = my_x_pos > 0.7
    opponent_cornered = opp_x_pos < -0.7 or opp_x_pos > 0.7
    near_edge = my_x_pos < -0.5 or my_x_pos > 0.5
    
    # Adaptive aggression calculation
    base_aggression = 0.6
    aggression_factor = 1.0
    
    if health_advantage > dominant_health:
        aggression_factor = 1.3
    elif health_advantage < desperate_threshold:
        aggression_factor = 1.5
    elif health_advantage < -0.15:
        aggression_factor = 0.7
    
    if my_health < critical_health:
        aggression_factor *= 0.6
    elif opp_health < critical_health:
        aggression_factor *= 1.4
    
    current_aggression = min(1.0, base_aggression * aggression_factor)
    
    # Emergency stunned state
    if my_stunned:
        if distance < close_range:
            if opp_attacking and block_ready:
                return 6
            elif distance < danger_range:
                return 3  # Jump to escape
            else:
                return 6
        elif distance > medium_range and projectile_ready:
            return 9
        else:
            return 6
    
    # Critical health survival mode
    if my_health <= critical_health:
        if opp_attacking and distance < medium_range and block_ready:
            return 6
        
        if distance < close_range:
            if opp_stunned and attack_ready:
                return 5 if random.random() < 0.7 else 4
            elif relative_pos > 0 and not corner_danger_left:
                return 7  # Escape left with block
            elif relative_pos < 0 and not corner_danger_right:
                return 8  # Escape right with block
            else:
                return 6 if block_ready else 3
        
        if distance > far_range and projectile_ready:
            return 9
        
        # Create distance when losing badly
        if distance < optimal_range:
            if relative_pos > 0 and not corner_danger_left:
                return 1
            elif relative_pos < 0 and not corner_danger_right:
                return 2
            else:
                return 6 if block_ready else 0
    
    # Capitalize on stunned opponent
    if opp_stunned:
        if distance < close_range and attack_ready:
            combo_choice = random.random()
            if combo_choice < 0.4:
                return 5  # Heavy kick
            elif combo_choice < 0.7:
                return 4  # Quick punch
            else:
                return 5  # Another heavy
        elif distance < medium_range:
            if relative_pos > 0:
                return 2  # Close in right
            else:
                return 1  # Close in left
        elif distance > medium_range and projectile_ready:
            return 9
        else:
            if relative_pos > 0:
                return 2
            else:
                return 1