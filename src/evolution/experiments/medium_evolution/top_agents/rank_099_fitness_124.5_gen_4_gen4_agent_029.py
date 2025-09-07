"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_029
Rank: 99/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 124.52
- Win Rate: 0.0%
- Average Reward: 124.52

Created: 2025-06-01 03:58:23
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_position = state[0]
    my_velocity_x = state[7]
    my_velocity_y = state[8]
    my_attack_status = max(0.0, state[4])
    my_block_status = max(0.0, state[5])
    my_projectile_cooldown = max(0.0, state[6])
    
    # Extract opponent status
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_position = state[11]
    opponent_velocity_x = state[18]
    opponent_velocity_y = state[19]
    opponent_attack_status = max(0.0, state[15])
    opponent_block_status = max(0.0, state[16])
    opponent_projectile_cooldown = max(0.0, state[17])
    
    # Enhanced tactical range definitions
    touch_range = 0.02
    ultra_close_range = 0.06
    very_close_range = 0.12
    close_range = 0.18
    mid_close_range = 0.28
    medium_range = 0.42
    mid_far_range = 0.58
    far_range = 0.75
    
    # Health and positioning thresholds
    critical_health = 0.08
    very_low_health = 0.18
    low_health = 0.35
    good_health = 0.65
    excellent_health = 0.85
    
    # Position analysis
    wall_distance = min(abs(my_position), abs(1.0 - my_position))
    opponent_wall_distance = min(abs(opponent_position), abs(1.0 - opponent_position))
    corner_trapped = wall_distance < 0.08
    near_corner = wall_distance < 0.2
    opponent_cornered = opponent_wall_distance < 0.08
    opponent_near_corner = opponent_wall_distance < 0.2
    center_control = abs(my_position - 0.5) < 0.15
    
    # Advanced status analysis
    projectile_ready = my_projectile_cooldown < 0.12
    projectile_charging = my_projectile_cooldown < 0.25
    opponent_projectile_ready = opponent_projectile_cooldown < 0.15
    opponent_projectile_threat = opponent_projectile_cooldown < 0.3
    
    # Movement and behavior patterns
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.05) or (relative_pos < 0 and opponent_velocity_x < -0.05)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    opponent_aggressive = opponent_attack_status > 0.4 or abs(opponent_velocity_x) > 0.2
    opponent_very_aggressive = opponent_attack_status > 0.7 or abs(opponent_velocity_x) > 0.35
    opponent_defensive = opponent_block_status > 0.3
    opponent_very_defensive = opponent_block_status > 0.6
    opponent_airborne = abs(height_diff) > 0.2
    opponent_high_airborne = abs(height_diff) > 0.4
    
    # Enhanced momentum calculation
    momentum_score = 0.0
    
    # Health momentum
    health_ratio = my_health / max(0.01, opponent_health)
    if health_ratio > 1.8:
        momentum_score += 0.4
    elif health_ratio > 1.3:
        momentum_score += 0.2
    elif health_ratio < 0.5:
        momentum_score -= 0.4
    elif health_ratio < 0.8:
        momentum_score -= 0.2
    
    # Position momentum
    if opponent_cornered and not corner_trapped:
        momentum_score += 0.35
    elif corner_trapped and not opponent_cornered:
        momentum_score -= 0.35
    elif center_control and not opponent_near_corner:
        momentum_score += 0.15
    
    # Tactical momentum
    if opponent_very_defensive and distance < medium_range:
        momentum_score += 0.25
    elif opponent_very_aggressive and my_health < low_health:
        momentum_score -= 0.3
    
    # Calculate adaptive aggression with momentum
    base_aggression = 0.58
    momentum_modifier = momentum_score * 0.5
    health_modifier = health_advantage * 0.3
    
    # Distance-based aggression tuning
    distance_modifier = 0.0
    if distance < close_range:
        distance_modifier = 0.15
    elif distance > medium_range:
        distance_modifier = -0.1
    
    current_aggression = max(0.2, min(0.9, base_aggression + momentum_modifier + health_modifier + distance_modifier))
    
    # Enhanced defense priority calculation
    defense_priority = 0.35
    if my_health < critical_health:
        defense_priority = 0.9
    elif my_health < very_low_health:
        defense_priority = 0.75
    elif my_health < low_health and health_advantage < -0.3:
        defense_priority = 0.65
    elif corner_trapped and opponent_aggressive:
        defense_priority = 0.7
    
    # Emergency survival protocols
    if my_health <= critical_health:
        if opponent_attack_status > 0.6 and distance < medium_range:
            return 6  # Priority defensive block
        
        if corner_trapped:
            if distance < ultra_close_range and projectile_ready:
                return 9  # Desperate point-blank projectile
            elif opponent_airborne and distance < close_range:
                return 4  # Anti-air attempt
            elif abs(height_diff) < 0.25:
                return 3  # Jump escape
            else:
                escape_dir = 2 if my_position < 0.5 else 1
                return 7 if escape_dir == 1 else 8
        
        if distance > medium_range and projectile_ready:
            return 9  # Safe projectile
        elif distance < close_range and not corner_trapped:
            retreat_dir = 1 if relative_pos > 0 else 2
            return retreat_dir
        
        return 6  # Default emergency block
    
    # Advanced threat response system
    if opponent_attack_status > 0.5:
        threat_intensity = opponent_attack_status * (1.0 - distance)
        
        if distance < touch_range:
            return 6  # Mandatory block at touch range
        elif distance < ultra_close_range:
            if my_health > low_health and not near_corner:
                evasive_move = 7 if relative_pos > 0 else 8
                return evasive_move if random.random() < 0.75 else 6
            else:
                return 6
        elif distance < very_close_range:
            if threat_intensity > 0.4:
                if projectile_ready and random.random() < 0.45:
                    return 9  # Counter projectile
                else:
                    return 6  # Defensive block