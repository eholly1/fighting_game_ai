"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_008
Rank: 87/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 167.90
- Win Rate: 50.0%
- Average Reward: 239.85

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
    point_blank = 0.04
    ultra_close = 0.08
    close_range = 0.15
    mid_close = 0.24
    medium_range = 0.38
    mid_far = 0.52
    far_range = 0.68
    max_range = 0.85
    
    # Refined health thresholds
    critical_hp = 0.12
    low_hp = 0.28
    mid_hp = 0.5
    good_hp = 0.72
    excellent_hp = 0.88
    
    # Advanced positioning analysis
    left_corner = my_position < -0.8
    right_corner = my_position > 0.8
    near_left_edge = my_position < -0.65
    near_right_edge = my_position > 0.65
    center_stage = abs(my_position) < 0.3
    opponent_left_corner = opponent_position < -0.75
    opponent_right_corner = opponent_position > 0.75
    
    # Enhanced status tracking
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_charging = my_projectile_cooldown < 0.12
    projectile_soon = my_projectile_cooldown < 0.25
    opponent_proj_ready = opponent_projectile_cooldown < 0.08
    opponent_proj_charging = opponent_projectile_cooldown < 0.18
    
    # Advanced movement pattern recognition
    opponent_advancing_fast = (relative_pos > 0 and opponent_velocity_x < -0.35) or (relative_pos < 0 and opponent_velocity_x > 0.35)
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2)
    opponent_airborne = abs(height_diff) > 0.2 or abs(opponent_velocity_y) > 0.15
    opponent_falling = opponent_velocity_y > 0.12 and height_diff < -0.08
    my_airborne = abs(my_velocity_y) > 0.12
    
    # Hybrid aggression system with momentum tracking
    base_aggression = 0.58
    momentum_factor = 0.0
    
    # Health-based aggression adjustment
    if health_advantage > 0.5:
        momentum_factor += 0.25
    elif health_advantage > 0.2:
        momentum_factor += 0.12
    elif health_advantage < -0.5:
        momentum_factor -= 0.35
    elif health_advantage < -0.2:
        momentum_factor -= 0.18
    
    # Distance-based aggression modifier
    if distance < close_range:
        momentum_factor += 0.15
    elif distance > far_range:
        momentum_factor -= 0.1
    
    # Position advantage modifier
    if opponent_left_corner or opponent_right_corner:
        momentum_factor += 0.2
    elif left_corner or right_corner:
        momentum_factor -= 0.25
    
    current_aggression = max(0.2, min(0.9, base_aggression + momentum_factor))
    
    # Critical health emergency protocols
    if my_health <= critical_hp:
        # Immediate survival mode
        if opponent_attack_status > 0.4 and distance < medium_range:
            if distance <= ultra_close:
                # Point blank defense
                if left_corner and relative_pos < 0:
                    return 8 if random.random() < 0.7 else 3
                elif right_corner and relative_pos > 0:
                    return 7 if random.random() < 0.7 else 3
                else:
                    return 6
            elif distance < close_range:
                # Close range evasive blocking
                if not left_corner and relative_pos > 0:
                    return 7
                elif not right_corner and relative_pos < 0:
                    return 8
                else:
                    return 6
            else:
                # Medium range blocking
                return 6
        
        # Desperate spacing management
        if distance < close_range:
            if left_corner or right_corner:
                # Cornered - try to escape
                if projectile_ready and distance > ultra_close:
                    return 9  # Desperation projectile
                elif opponent_airborne:
                    return 4  # Anti-air attempt
                else:
                    # Try to escape corner
                    if left_corner and relative_pos > -0.5:
                        return 2
                    elif right_corner and relative_pos < 0.5:
                        return 1
                    else:
                        return 6
            else:
                # Create distance when possible
                if relative_pos > 0 and not near_left_edge:
                    return 1
                elif relative_pos < 0 and not near_right_edge:
                    return 2
                else:
                    return 6
        
        # Long range survival tactics
        if distance > medium_range and projectile_ready:
            return 9
        
        # Default survival block
        return 6
    
    # Enhanced threat response system
    if opponent_attack_status > 0.5:
        threat_intensity = opponent_attack_status / max(distance, 0.05)
        
        if threat_intensity > 4.0:  # Extreme threat
            if my_health <= low_hp:
                return 6  # Prioritize survival
            else:
                # Calculated counter-risk
                if projectile_ready and distance > ultra_close and random.random() < 0.4:
                    return 9  # Counter projectile
                else:
                    return 6
        elif threat_intensity > 2.5:  # High threat
            if distance <= ultra_close:
                return 6  # Must block
            elif distance < close_range:
                # Mobile defense consideration
                if my_health > mid_hp and not (left_corner or right_corner):
                    return 7 if relative_pos > 0 else 8
                else:
                    return 6
            else:
                # Medium range threat assessment
                if projectile_ready and random.random() < 0.6:
                    return 9