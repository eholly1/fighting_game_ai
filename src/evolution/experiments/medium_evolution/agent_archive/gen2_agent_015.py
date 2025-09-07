"""
Evolutionary Agent: gen2_agent_015
==================================

Metadata:
{
  "generation": 2,
  "fitness": 249.45999999999066,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 035f954da426c081
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
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    
    # Extract velocities and movement data
    my_velocity_x = state[7]
    my_velocity_y = state[8]
    opponent_velocity_x = state[18]
    opponent_velocity_y = state[19]
    
    # Extract attack and defensive status
    my_attack_status = state[4]
    opponent_attack_status = state[15]
    my_block_status = state[5]
    opponent_block_status = state[16]
    
    # Projectile information
    my_projectile_cooldown = max(0.0, state[6])
    opponent_projectile_cooldown = max(0.0, state[17])
    
    # Height and positioning
    height_diff = state[24]
    
    # Enhanced strategic constants
    danger_zone = 0.08
    close_range = 0.15
    medium_range = 0.28
    optimal_range = 0.42
    max_range = 0.65
    
    # Health thresholds
    critical_health = 0.18
    low_health = 0.35
    good_health = 0.65
    
    # Projectile timing
    projectile_ready = my_projectile_cooldown < 0.1
    projectile_almost_ready = my_projectile_cooldown < 0.25
    opponent_projectile_ready = opponent_projectile_cooldown < 0.12
    
    # Enhanced stage awareness
    left_corner_danger = my_position < -0.7
    right_corner_danger = my_position > 0.7
    opponent_left_corner = opponent_position < -0.7
    opponent_right_corner = opponent_position > 0.7
    center_stage = abs(my_position) < 0.3
    
    # Movement analysis
    opponent_rushing = abs(opponent_velocity_x) > 0.25 and (
        (relative_pos > 0 and opponent_velocity_x < -0.2) or 
        (relative_pos < 0 and opponent_velocity_x > 0.2)
    )
    opponent_retreating = abs(opponent_velocity_x) > 0.15 and (
        (relative_pos > 0 and opponent_velocity_x > 0.15) or 
        (relative_pos < 0 and opponent_velocity_x < -0.15)
    )
    opponent_airborne = abs(opponent_velocity_y) > 0.1 or height_diff < -0.2
    my_airborne = abs(my_velocity_y) > 0.1
    
    # Adaptive aggression based on health and position
    base_aggression = 0.5
    if health_advantage > 0.3:
        base_aggression = 0.7  # More aggressive when winning
    elif health_advantage < -0.3:
        base_aggression = 0.3  # More defensive when losing
    
    # Critical survival mode
    if my_health <= critical_health:
        # Immediate threat response
        if opponent_attack_status > 0 and distance < medium_range:
            if distance < close_range:
                # Try to escape with blocking movement
                if relative_pos > 0 and not left_corner_danger:
                    return 7  # Block retreat left
                elif relative_pos < 0 and not right_corner_danger:
                    return 8  # Block retreat right
                else:
                    return 6  # Pure block if cornered
            else:
                return 6  # Block at medium range
        
        # Desperate escape from close quarters
        if distance < close_range:
            if left_corner_danger and relative_pos < 0:
                # Cornered on left, opponent on left
                if opponent_airborne or height_diff > 0.1:
                    return 3  # Jump escape attempt
                else:
                    return 2  # Try to move past opponent
            elif right_corner_danger and relative_pos > 0:
                # Cornered on right, opponent on right
                if opponent_airborne or height_diff > 0.1:
                    return 3  # Jump escape attempt
                else:
                    return 1  # Try to move past opponent
            else:
                # Standard retreat
                if relative_pos > 0 and not left_corner_danger:
                    return 7  # Retreat left with block
                elif not right_corner_danger:
                    return 8  # Retreat right with block
                else:
                    return 6  # Block
        
        # Long-range survival tactics
        if projectile_ready and distance > medium_range:
            return 9  # Desperate projectile
        
        # Create distance when possible
        if distance < optimal_range:
            if relative_pos > 0 and not left_corner_danger:
                return 1  # Move away
            elif not right_corner_danger:
                return 2  # Move away
            else:
                return 6  # Block if trapped
    
    # Enhanced defensive reactions
    if opponent_attack_status > 0:
        if distance < medium_range:
            # Real threat detected
            if opponent_rushing and distance < close_range:
                # They're rushing with attack, counter-strategy
                if my_health > low_health and projectile_ready and distance > danger_zone:
                    return 9  # Counter-attack
                else:
                    # Defensive movement
                    if relative_pos > 0 and not left_corner_danger:
                        return 7  # Block retreat
                    elif not right_corner_danger:
                        return 8  # Block retreat
                    else:
                        return 6  # Pure block
            else:
                # Standard defensive response
                if my_health <= low_health:
                    return 6  # Prioritize blocking when low health
                else:
                    # Mix defense with positioning
                    if random.random() < 0.75:
                        return 6  # Block
                    else:
                        # Occasional evasion
                        if relative_pos > 0 and not left_corner_danger:
                            return 1
                        elif not right_corner_danger:
                            return 2
                        else:
                            return 6
        elif distance < optimal_range and projectile_ready:
            # Medium range counter-attack opportunity
            if random.random() < 0.8:
                return 9  # High probability counter
            else:
                return 6  # Occasional block
    
    # Anti-air and aerial combat
    if opponent_airborne:
        if distance < optimal_range:
            if projectile_ready:
                # Anti-air projectile timing
                if distance > close_range:
                    return 9  # Good anti-air position
                else:
                    # Too close, prepare for landing
                    return 6  # Block potential dive attack
            else:
                # No projectile, positioning response
                if distance < medium_range:
                    # Get ready for their landing
                    if opponent_velocity_y > 0:  # They're falling
                        if relative_pos > 0 and not left_corner_danger:
                            return 1  # Position for landing punish
                        elif not right_corner_danger:
                            return 2  # Position for landing punish
                        else:
                            return 6  # Block landing attack
                    else:
                        return 6  # Block while they're in air