"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_023
Rank: 67/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 195.18
- Win Rate: 0.0%
- Average Reward: 195.18

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
    
    # Extract fighter status information with defensive bounds checking
    my_health = max(0.0, min(1.0, state[2] if len(state) > 2 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.0
    my_velocity_x = state[7] if len(state) > 7 else 0.0
    my_velocity_y = state[8] if len(state) > 8 else 0.0
    my_attack_status = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[13] if len(state) > 13 else 1.0))
    opponent_pos_x = state[11] if len(state) > 11 else 0.0
    opponent_velocity_x = state[18] if len(state) > 18 else 0.0
    opponent_velocity_y = state[19] if len(state) > 19 else 0.0
    opponent_attack_status = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0.0)
    
    # Enhanced tactical range definitions
    danger_zone = 0.05
    point_blank = 0.08
    ultra_close = 0.12
    close_range = 0.18
    medium_close = 0.26
    medium_range = 0.38
    medium_far = 0.55
    far_range = 0.75
    
    # Advanced positioning analysis
    left_corner_trap = my_pos_x < -0.75
    right_corner_trap = my_pos_x > 0.75
    opponent_cornered_left = opponent_pos_x < -0.75
    opponent_cornered_right = opponent_pos_x > 0.75
    center_control = abs(my_pos_x) < 0.25
    
    # Movement pattern recognition
    opponent_rushing = False
    opponent_retreating = False
    opponent_circling = False
    
    if abs(opponent_velocity_x) > 0.2:
        if (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2):
            opponent_rushing = True
        elif (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2):
            opponent_retreating = True
        else:
            opponent_circling = True
    
    # Aerial status assessment
    opponent_airborne = abs(opponent_velocity_y) > 0.08 or height_diff < -0.15
    my_airborne = abs(my_velocity_y) > 0.08
    opponent_landing = opponent_airborne and opponent_velocity_y > 0.05
    
    # Projectile timing analysis
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_charging = my_projectile_cooldown < 0.2
    opponent_projectile_threat = opponent_projectile_cooldown < 0.1
    
    # Dynamic aggression calculation
    base_aggression = 0.68
    situation_modifier = 1.0
    
    # Health-based modifier
    if health_advantage > 0.5:
        situation_modifier *= 1.4  # Dominating
    elif health_advantage > 0.25:
        situation_modifier *= 1.2  # Winning solidly
    elif health_advantage > 0.0:
        situation_modifier *= 1.05  # Slight advantage
    elif health_advantage > -0.25:
        situation_modifier *= 0.85  # Slight disadvantage
    elif health_advantage > -0.5:
        situation_modifier *= 0.65  # Losing
    else:
        situation_modifier *= 0.45  # Desperate
    
    # Distance modifier
    if distance < close_range:
        situation_modifier *= 1.15
    elif distance > medium_far:
        situation_modifier *= 0.9
    
    current_aggression = min(1.0, max(0.2, base_aggression * situation_modifier))
    
    # Critical health emergency protocols
    if my_health < 0.15:
        # Survival mode with calculated risks
        if opponent_attack_status > 0.6 and distance < medium_range:
            if distance < close_range:
                # Escape with blocking movement
                if left_corner_trap:
                    if relative_pos < 0:
                        return 3 if random.random() < 0.3 else 8
                    else:
                        return 6
                elif right_corner_trap:
                    if relative_pos > 0:
                        return 3 if random.random() < 0.3 else 7
                    else:
                        return 6
                else:
                    # Standard defensive retreat
                    return 7 if relative_pos > 0 else 8
            else:
                return 6  # Block at medium range
        
        # Desperate offense opportunity
        if opponent_health < 0.2 and distance < close_range and opponent_attack_status < 0.3:
            # Both critical - go for it
            return 5 if random.random() < 0.7 else 4
        
        # Create space when possible
        if distance < medium_range and not (left_corner_trap or right_corner_trap):
            if projectile_ready and distance > ultra_close:
                return 9
            else:
                return 7 if relative_pos > 0 else 8
        
        # Long range survival
        if distance > medium_range:
            if projectile_ready:
                return 9
            elif opponent_projectile_threat:
                return 6
            else:
                return 0  # Stay at safe distance
    
    # Opponent vulnerability exploitation
    if opponent_landing and distance < medium_close:
        # Anti-air timing
        if distance > ultra_close:
            if projectile_ready:
                return 9  # Projectile anti-air
            else:
                return 2 if relative_pos > 0 else 1  # Position for landing punish
        else:
            # Close range landing punish
            return 5 if random.random() < 0.8 else 4
    
    # Enhanced opponent attack response system
    if opponent_attack_status > 0.5:
        threat_level = opponent_attack_status * (1.0 - distance)
        
        if threat_level > 0.4:  # High threat
            if my_health < opponent_health * 0.75:
                # Defensive priority when behind
                if distance < ultra_close:
                    return 6  # Pure block in danger zone
                else:
                    return 7 if relative_pos > 0 else 8  # Block retreat
            else:
                # Counter opportunities when ahead
                counter_chance = random.random()