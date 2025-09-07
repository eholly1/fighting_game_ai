"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_020
Rank: 95/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 142.70
- Win Rate: 0.0%
- Average Reward: 142.70

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
    my_health = max(0.0, min(1.0, state[2] if len(state) > 2 else 1.0))
    opponent_health = max(0.0, min(1.0, state[13] if len(state) > 13 else 1.0))
    my_position = state[0] if len(state) > 0 else 0.0
    opponent_position = state[11] if len(state) > 11 else 0.0
    
    # Velocity and movement data
    my_velocity_x = state[7] if len(state) > 7 else 0.0
    my_velocity_y = state[8] if len(state) > 8 else 0.0
    opponent_velocity_x = state[18] if len(state) > 18 else 0.0
    opponent_velocity_y = state[19] if len(state) > 19 else 0.0
    
    # Combat status information
    my_attack_status = state[4] if len(state) > 4 else 0.0
    opponent_attack_status = state[15] if len(state) > 15 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    
    # Projectile cooldowns
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0.0)
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0.0)
    
    # Hybrid fighting tactical ranges
    danger_zone = 0.06
    ultra_close = 0.12
    close_range = 0.18
    medium_close = 0.28
    medium_range = 0.42
    far_range = 0.58
    max_range = 0.75
    
    # Health management thresholds
    critical_health = 0.15
    low_health = 0.32
    good_health = 0.68
    dominant_health = 0.85
    
    # Projectile readiness states
    projectile_ready = my_projectile_cooldown < 0.08
    projectile_soon = my_projectile_cooldown < 0.2
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    opponent_projectile_threat = opponent_projectile_cooldown < 0.25
    
    # Enhanced positioning awareness
    stage_left_edge = my_position < -0.75
    stage_right_edge = my_position > 0.75
    opponent_cornered_left = opponent_position < -0.7
    opponent_cornered_right = opponent_position > 0.7
    center_control = abs(my_position) < 0.25
    
    # Advanced movement pattern detection
    opponent_rushing = (abs(opponent_velocity_x) > 0.3 and 
                      ((relative_pos > 0 and opponent_velocity_x < -0.25) or 
                       (relative_pos < 0 and opponent_velocity_x > 0.25)))
    
    opponent_retreating = (abs(opponent_velocity_x) > 0.2 and 
                          ((relative_pos > 0 and opponent_velocity_x > 0.2) or 
                           (relative_pos < 0 and opponent_velocity_x < -0.2)))
    
    opponent_airborne = abs(opponent_velocity_y) > 0.12 or height_diff < -0.15
    my_airborne = abs(my_velocity_y) > 0.1
    opponent_landing = opponent_velocity_y > 0.15 and height_diff < -0.1
    
    # Hybrid strategy adaptation parameters
    base_aggression = 0.55
    defensive_threshold = 0.4
    aggressive_threshold = 0.75
    
    # Dynamic aggression calculation
    current_aggression = base_aggression
    if health_advantage > 0.4:
        current_aggression = min(0.85, base_aggression + 0.25)
    elif health_advantage > 0.15:
        current_aggression = min(0.7, base_aggression + 0.1)
    elif health_advantage < -0.4:
        current_aggression = max(0.25, base_aggression - 0.3)
    elif health_advantage < -0.15:
        current_aggression = max(0.4, base_aggression - 0.15)
    
    # Critical survival protocol
    if my_health <= critical_health:
        # Immediate threat assessment
        if opponent_attack_status > 0.5 and distance < medium_range:
            if distance < close_range and not my_airborne:
                # Emergency evasion with blocking
                if stage_left_edge and relative_pos < 0:
                    if opponent_airborne:
                        return 3  # Jump escape
                    else:
                        return 8  # Block right movement
                elif stage_right_edge and relative_pos > 0:
                    if opponent_airborne:
                        return 3  # Jump escape
                    else:
                        return 7  # Block left movement
                else:
                    # Standard blocking retreat
                    if relative_pos > 0 and not stage_left_edge:
                        return 7  # Block retreat left
                    elif not stage_right_edge:
                        return 8  # Block retreat right
                    else:
                        return 6  # Pure block
            else:
                return 6  # Block at medium range
        
        # Desperate spacing when cornered
        if distance < close_range and (stage_left_edge or stage_right_edge):
            if opponent_rushing:
                # Counter-attack attempt with projectile
                if projectile_ready and distance > danger_zone:
                    return 9
                else:
                    return 6  # Block rush
            else:
                # Try to create space
                if stage_left_edge and relative_pos > 0:
                    return 2  # Move away from corner
                elif stage_right_edge and relative_pos < 0:
                    return 1  # Move away from corner
                else:
                    return 3  # Jump attempt
        
        # Long-range survival tactics
        if distance > medium_range:
            if projectile_ready:
                return 9  # Projectile for damage/space
            else:
                # Maintain distance
                if opponent_rushing:
                    if relative_pos > 0 and not stage_left_edge:
                        return 1  # Retreat
                    elif not stage_right_edge:
                        return 2  # Retreat
                    else:
                        return 6  # Block if trapped
    
    # Enhanced threat response system
    if opponent_attack_status > 0.6:
        threat_level = opponent_attack_status * (1.0 / max(distance, 0.1))
        
        if threat_level > 3.0:  # High immediate threat
            if my_health <= low_health:
                return 6  # Priority block when low health
            else:
                # Counter-attack opportunity assessment
                if projectile_ready and distance > ultra_close and distance < medium_close:
                    if random.random() < 0.65:
                        return