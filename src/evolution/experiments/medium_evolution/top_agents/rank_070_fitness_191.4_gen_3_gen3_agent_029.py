"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_029
Rank: 70/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 191.42
- Win Rate: 50.0%
- Average Reward: 243.36

Created: 2025-06-01 03:09:14
Lineage: Original

Tournament Stats:
None
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
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_pos_x = max(0.0, min(1.0, state[2])) if len(state) > 2 else 0.5
    my_velocity_x = max(-1.0, min(1.0, state[4])) if len(state) > 4 else 0.0
    my_velocity_y = max(-1.0, min(1.0, state[5])) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0.0
    my_block_status = max(0.0, min(1.0, state[8])) if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opponent_velocity_x = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opponent_velocity_y = max(-1.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Define hybrid tactical ranges with improved precision
    optimal_range = 0.06
    ultra_close_range = 0.1
    very_close_range = 0.16
    close_range = 0.22
    medium_range = 0.32
    far_range = 0.48
    max_range = 0.65
    
    # Calculate positional awareness
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_proximity = min(opponent_pos_x, 1.0 - opponent_pos_x)
    corner_pressure = wall_proximity < 0.18
    opponent_cornered = opponent_wall_proximity < 0.18
    near_corner = wall_proximity < 0.3
    
    # Enhanced opponent analysis
    opponent_aggressive = opponent_attack_status > 0.4 or abs(opponent_velocity_x) > 0.25
    opponent_defensive = opponent_block_status > 0.5
    opponent_mobile = abs(opponent_velocity_x) > 0.12
    opponent_airborne = height_diff < -0.15
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2)
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    
    # Projectile readiness analysis
    my_projectile_ready = my_projectile_cooldown < 0.15
    opponent_projectile_ready = opponent_projectile_cooldown < 0.15
    my_projectile_optimal = my_projectile_cooldown < 0.05
    
    # Dynamic aggression calculation
    base_aggression = 0.6
    aggression_modifier = 0.0
    
    # Health-based aggression with nuanced scaling
    if health_advantage > 0.5:
        aggression_modifier += 0.3
    elif health_advantage > 0.2:
        aggression_modifier += 0.15
    elif health_advantage < -0.5:
        aggression_modifier -= 0.35
    elif health_advantage < -0.2:
        aggression_modifier -= 0.15
    
    # Position-based adjustment with corner control
    if opponent_cornered and not corner_pressure:
        aggression_modifier += 0.25
    elif corner_pressure and not opponent_cornered:
        aggression_modifier -= 0.2
    
    # Opponent behavior adjustment
    if opponent_defensive and not opponent_mobile:
        aggression_modifier += 0.2
    elif opponent_aggressive and my_health < opponent_health * 1.1:
        aggression_modifier -= 0.25
    
    current_aggression = max(0.15, min(0.85, base_aggression + aggression_modifier))
    
    # Critical health emergency protocols
    if my_health < 0.12:
        if opponent_attack_status > 0.6 and distance < close_range:
            return 6
        elif distance > medium_range and my_projectile_ready:
            return 9
        elif distance < very_close_range and not corner_pressure:
            escape_direction = 7 if relative_pos > 0 else 8
            return escape_direction
        elif corner_pressure and distance < very_close_range:
            if my_projectile_optimal:
                return 9
            elif random.random() < 0.4:
                return 3
            else:
                return 6
        else:
            return 6
    
    # Low health survival tactics
    if my_health < 0.25 and health_advantage < -0.3:
        if opponent_attack_status > 0.5:
            return 6
        elif distance > far_range and my_projectile_ready:
            return 9
        elif distance < close_range and not corner_pressure:
            retreat_direction = 1 if relative_pos > 0 else 2
            if opponent_projectile_ready:
                return 7 if retreat_direction == 1 else 8
            else:
                return retreat_direction
        elif distance >= close_range and distance < medium_range:
            if my_projectile_ready:
                return 9
            else:
                return 6
    
    # Corner escape with improved decision making
    if corner_pressure:
        if opponent_attack_status > 0.5 and distance < close_range:
            return 6
        elif distance < ultra_close_range:
            if opponent_airborne:
                return 4
            elif my_projectile_optimal and random.random() < 0.6:
                return 9
            elif abs(height_diff) < 0.3 and random.random() < 0.5:
                return 3
            else:
                counter_choice = random.random()
                if counter_choice < 0.6:
                    return 4
                else:
                    return 5
        elif distance < close_range:
            center_direction = 2 if my_pos_x < 0.5 else 1
            if opponent_projectile_ready and distance > ultra_close_range:
                return 7