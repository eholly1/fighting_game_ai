"""
Evolutionary Agent: gen4_agent_003
==================================

Metadata:
{
  "generation": 4,
  "fitness": -9.954000000000281,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 5d97b16bfa0dffa9
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
    
    # Define adaptive tactical ranges
    micro_range = 0.05
    optimal_range = 0.08
    ultra_close_range = 0.12
    very_close_range = 0.18
    close_range = 0.25
    medium_close_range = 0.32
    medium_range = 0.42
    far_range = 0.55
    max_range = 0.7
    
    # Enhanced positional analysis
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_proximity = min(opponent_pos_x, 1.0 - opponent_pos_x)
    corner_pressure = wall_proximity < 0.15
    opponent_cornered = opponent_wall_proximity < 0.15
    near_corner = wall_proximity < 0.25
    center_control = abs(my_pos_x - 0.5) < 0.3
    
    # Advanced opponent analysis with timing patterns
    opponent_aggressive = opponent_attack_status > 0.3 or abs(opponent_velocity_x) > 0.2
    opponent_defensive = opponent_block_status > 0.4
    opponent_mobile = abs(opponent_velocity_x) > 0.1
    opponent_airborne = abs(height_diff) > 0.12
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_stationary = abs(opponent_velocity_x) < 0.08
    
    # Projectile management with cooldown prediction
    my_projectile_ready = my_projectile_cooldown < 0.2
    opponent_projectile_ready = opponent_projectile_cooldown < 0.2
    my_projectile_optimal = my_projectile_cooldown < 0.08
    projectile_advantage = my_projectile_cooldown < opponent_projectile_cooldown
    
    # Dynamic aggression with momentum consideration
    base_aggression = 0.55
    aggression_modifier = 0.0
    
    # Health-based aggression with momentum scaling
    health_ratio = my_health / max(0.1, opponent_health)
    if health_advantage > 0.4:
        aggression_modifier += 0.25 + (health_advantage * 0.3)
    elif health_advantage > 0.15:
        aggression_modifier += 0.12
    elif health_advantage < -0.4:
        aggression_modifier -= 0.3 - (abs(health_advantage) * 0.2)
    elif health_advantage < -0.15:
        aggression_modifier -= 0.18
    
    # Position-based strategic adjustment
    if opponent_cornered and not corner_pressure:
        aggression_modifier += 0.3
    elif corner_pressure and not opponent_cornered:
        aggression_modifier -= 0.25
    elif center_control and not opponent_cornered:
        aggression_modifier += 0.1
    
    # Opponent behavior adaptive response
    if opponent_defensive and opponent_stationary:
        aggression_modifier += 0.2
    elif opponent_aggressive and distance < close_range:
        aggression_modifier += 0.15 if health_advantage > 0 else -0.2
    elif opponent_retreating:
        aggression_modifier += 0.18
    
    current_aggression = max(0.2, min(0.9, base_aggression + aggression_modifier))
    
    # Critical health emergency with enhanced survival
    if my_health < 0.1:
        if opponent_attack_status > 0.5 and distance < very_close_range:
            return 6
        elif distance > medium_range and my_projectile_optimal:
            return 9
        elif corner_pressure and distance < close_range:
            if my_projectile_ready and random.random() < 0.5:
                return 9
            elif opponent_airborne:
                return 5
            else:
                return 6
        elif distance < ultra_close_range and not corner_pressure:
            escape_direction = 7 if relative_pos > 0 else 8
            return escape_direction
        else:
            return 6
    
    # Low health tactical survival
    if my_health < 0.22 and health_advantage < -0.25:
        if opponent_attack_status > 0.4 and distance < close_range:
            return 6
        elif distance > far_range and my_projectile_ready:
            return 9
        elif distance > medium_range and my_projectile_optimal:
            return 9
        elif distance < close_range and not corner_pressure:
            retreat_direction = 1 if relative_pos > 0 else 2
            if opponent_projectile_ready and distance > ultra_close_range:
                return 7 if retreat_direction == 1 else 8
            else:
                return retreat_direction
        elif opponent_defensive and distance > very_close_range:
            if my_projectile_ready:
                return