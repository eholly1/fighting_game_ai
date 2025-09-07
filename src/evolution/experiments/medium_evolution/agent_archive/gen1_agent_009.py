"""
Evolutionary Agent: gen1_agent_009
==================================

Metadata:
{
  "generation": 1,
  "fitness": -1.0266666666670599,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 70a1fd777e4e67f3
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
    height_diff = max(-1.0, min(1.0, state[24]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    
    # Extract combat status
    my_attack_status = state[4]
    opponent_attack_status = state[15]
    my_block_status = state[5]
    opponent_block_status = state[16]
    
    # Extract cooldowns and movement
    my_projectile_cooldown = max(0.0, state[6])
    opponent_projectile_cooldown = max(0.0, state[17])
    my_velocity_x = state[7]
    opponent_velocity_x = state[18]
    
    # Enhanced strategic constants for improved zoner play
    optimal_zone = 0.45
    safe_zone = 0.35
    danger_zone = 0.18
    critical_zone = 0.10
    escape_zone = 0.05
    
    # Health management thresholds
    critical_health = 0.15
    low_health = 0.35
    moderate_health = 0.6
    
    # Projectile management
    projectile_ready = my_projectile_cooldown < 0.08
    projectile_soon = my_projectile_cooldown < 0.25
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    
    # Enhanced position awareness
    stage_left_danger = my_position < -0.75
    stage_right_danger = my_position > 0.75
    stage_left_edge = my_position < -0.85
    stage_right_edge = my_position > 0.85
    opponent_cornered_left = opponent_position < -0.7
    opponent_cornered_right = opponent_position > 0.7
    
    # Movement pattern analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_static = abs(opponent_velocity_x) < 0.05
    
    # Time-based unpredictability factor
    chaos_factor = random.random()
    
    # Crisis management - absolute priority
    if my_health <= critical_health:
        # Survival mode with enhanced decision making
        if distance <= escape_zone:
            # Immediate danger, must block
            return 6
        
        if distance <= critical_zone:
            # Too close, emergency evasion
            if opponent_attack_status > 0:
                return 6  # Block active attacks
            
            # Smart escape routing
            if relative_pos > 0:  # Opponent right
                if stage_left_edge:
                    # Cornered, must block and wait
                    return 6
                elif opponent_attacking_soon():
                    return 7  # Block while moving
                else:
                    return 1  # Quick escape left
            else:  # Opponent left
                if stage_right_edge:
                    return 6  # Cornered
                elif opponent_attacking_soon():
                    return 8  # Block while moving
                else:
                    return 2  # Quick escape right
        
        # Desperate zoning attempts
        if projectile_ready and distance > danger_zone:
            return 9
        
        # Create space when possible
        if distance < safe_zone:
            escape_direction = get_optimal_escape_direction(relative_pos, stage_left_danger, stage_right_danger)
            if escape_direction == "left":
                return 7 if opponent_attack_status > 0 else 1
            elif escape_direction == "right":
                return 8 if opponent_attack_status > 0 else 2
        
        # Last resort blocking
        return 6
    
    # Advanced threat assessment
    immediate_threat = (opponent_attack_status > 0 and distance < danger_zone) or \
                      (opponent_approaching and distance < critical_zone)
    
    if immediate_threat:
        if my_health <= low_health:
            # Conservative response when low health
            return 6
        else:
            # Try to evade while blocking if healthier
            if relative_pos > 0 and not stage_left_danger:
                return 7
            elif relative_pos < 0 and not stage_right_danger:
                return 8
            else:
                return 6
    
    # Anti-air and vertical control
    if height_diff < -0.25:  # Opponent jumping
        if distance < safe_zone:
            if projectile_ready:
                return 9  # Anti-air projectile
            else:
                # Reposition for landing punishment
                optimal_pos = get_anti_air_position(relative_pos, stage_left_danger, stage_right_danger)
                if optimal_pos == "left":
                    return 1
                elif optimal_pos == "right":
                    return 2
                else:
                    return 6  # Block if repositioning not safe
    
    # Enhanced zoning strategy - the core of improved gameplay
    if distance >= optimal_zone:
        # Perfect zoning range
        if projectile_ready:
            # Smart projectile timing
            if opponent_static or opponent_retreating:
                # Easy target or creating more space
                return 9
            elif opponent_approaching:
                # Approaching opponent, projectile to slow advance
                if chaos_factor < 0.85:
                    return 9
                else:
                    # Occasional movement to avoid patterns
                    return get_zone_adjustment_move(relative_pos, distance, stage_left_danger, stage_right_danger)
            else:
                return 9
        else:
            # Projectile on cooldown, smart positioning
            if opponent_projectile_ready and opponent_health > 0.3:
                # Opponent might projectile back, prepare evasion
                return get_projectile_dodge_move(relative_pos, stage_left_danger, stage_right_danger)
            else:
                # Maintain optimal spacing
                return maintain_optimal_distance(distance, relative_pos, optimal_zone, stage_left_danger, stage_right_danger)
    
    elif distance >= safe_zone:
        # Good zoning range with more options
        if projectile_ready:
            # Analyze opponent behavior for better timing
            if opponent_block_status > 0:
                # Opponent blocking, mix up timing
                if chaos_factor < 0.3:
                    # Delay projectile to break block timing
                    return get_patience_move(relative_pos, distance, stage_left_danger, stage_right_danger)
                else:
                    return 9
            elif opponent_approaching:
                # Punish approach with projectile
                return 9
            else:
                # Standard zoning
                if chaos_factor < 0.9:
                    return 9
                else:
                    # Rare movement for unpredictability
                    return get_mix_up_move(relative_pos, stage_left_danger, stage_right_danger)
        else:
            # No projectile, focus on positioning
            if projectile_soon:
                # Almost ready, maintain position
                return adjust_for_projectile_timing(distance, relative_pos, safe_zone, stage_left_danger, stage_right_danger)