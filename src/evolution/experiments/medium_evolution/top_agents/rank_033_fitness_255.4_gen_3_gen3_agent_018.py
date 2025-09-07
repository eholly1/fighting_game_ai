"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_018
Rank: 33/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 255.40
- Win Rate: 50.0%
- Average Reward: 255.40

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
    
    # Define evolved tactical ranges with more granular control
    point_blank_range = 0.03
    ultra_close_range = 0.08
    very_close_range = 0.15
    close_range = 0.22
    mid_close_range = 0.32
    medium_range = 0.45
    mid_far_range = 0.60
    far_range = 0.80
    
    # Enhanced situational awareness
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_proximity = min(opponent_pos_x, 1.0 - opponent_pos_x)
    corner_pressure = wall_proximity < 0.12
    opponent_cornered = opponent_wall_proximity < 0.12
    near_corner = wall_proximity < 0.25
    opponent_near_corner = opponent_wall_proximity < 0.25
    
    # Advanced opponent analysis
    opponent_aggressive = opponent_attack_status > 0.3 or abs(opponent_velocity_x) > 0.15
    opponent_very_aggressive = opponent_attack_status > 0.6 or abs(opponent_velocity_x) > 0.3
    opponent_defensive = opponent_block_status > 0.4
    opponent_very_defensive = opponent_block_status > 0.7
    opponent_mobile = abs(opponent_velocity_x) > 0.08
    opponent_highly_mobile = abs(opponent_velocity_x) > 0.2
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    opponent_projectile_ready = opponent_projectile_cooldown < 0.25
    my_projectile_ready = my_projectile_cooldown < 0.3
    
    # Calculate momentum and pressure states
    momentum_factor = 0.0
    if health_advantage > 0.2:
        momentum_factor += 0.3
    elif health_advantage < -0.2:
        momentum_factor -= 0.3
    
    if opponent_cornered and not corner_pressure:
        momentum_factor += 0.4
    elif corner_pressure and not opponent_cornered:
        momentum_factor -= 0.4
    
    if opponent_defensive and not opponent_mobile:
        momentum_factor += 0.2
    elif opponent_very_aggressive and my_health < opponent_health:
        momentum_factor -= 0.3
    
    # Advanced aggression calculation with momentum
    base_aggression = 0.55  # Balanced evolved baseline
    aggression_modifier = momentum_factor * 0.6
    
    # Health differential fine-tuning
    health_ratio = my_health / max(0.1, opponent_health)
    if health_ratio > 1.5:
        aggression_modifier += 0.2
    elif health_ratio < 0.6:
        aggression_modifier -= 0.25
    
    # Distance-based aggression adjustment
    if distance < close_range:
        aggression_modifier += 0.1  # Slightly more aggressive up close
    elif distance > medium_range:
        aggression_modifier -= 0.05  # Slightly more cautious at range
    
    current_aggression = max(0.15, min(0.85, base_aggression + aggression_modifier))
    
    # Critical health emergency protocols
    if my_health < 0.12 and health_advantage < -0.5:
        if opponent_attack_status > 0.6:
            return 6  # Emergency block
        elif distance > mid_far_range and my_projectile_ready:
            return 9  # Desperate projectile
        elif distance < very_close_range and corner_pressure:
            # Last ditch escape attempt
            if abs(height_diff) < 0.3:
                return 3  # Jump escape
            else:
                return 4 if random.random() < 0.6 else 5  # Fight back
        elif corner_pressure:
            escape_direction = 2 if my_pos_x < 0.5 else 1
            return 7 if escape_direction == 1 else 8  # Defensive movement
        else:
            return 6  # Block and pray
    
    # Enhanced corner management
    if corner_pressure:
        if opponent_very_aggressive and distance < close_range:
            if opponent_attack_status > 0.7:
                return 6  # Block immediate threat
            elif distance < ultra_close_range and my_health > opponent_health * 0.8:
                return 4 if random.random() < 0.6 else 5  # Counter-pressure
            else:
                # Escape sequence based on opponent position
                if abs(height_diff) < 0.2 and random.random() < 0.5:
                    return 3  # Jump out
                else:
                    center_direction = 2 if my_pos_x < 0.5 else 1
                    return 7 if center_direction == 1 else 8  #