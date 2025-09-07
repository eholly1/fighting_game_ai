"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_018
Rank: 32/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 255.76
- Win Rate: 50.0%
- Average Reward: 255.76

Created: 2025-06-01 01:24:51
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
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    
    # Extract attack and block status
    my_attack_status = state[4]
    opponent_attack_status = state[15]
    my_block_status = state[5]
    opponent_block_status = state[16]
    
    # Extract projectile cooldown and velocities
    my_projectile_cooldown = max(0.0, state[6])
    opponent_projectile_cooldown = max(0.0, state[17])
    my_velocity_x = state[7]
    opponent_velocity_x = state[18]
    
    # Height difference for jump detection
    height_diff = state[24]
    
    # Enhanced strategic constants for improved zoner play
    optimal_range = 0.45
    safe_distance = 0.35
    medium_distance = 0.22
    close_distance = 0.12
    danger_distance = 0.06
    
    # Health management thresholds
    critical_health = 0.15
    low_health = 0.35
    moderate_health = 0.6
    
    # Projectile management
    projectile_ready = my_projectile_cooldown < 0.08
    projectile_almost_ready = my_projectile_cooldown < 0.2
    opponent_projectile_threat = opponent_projectile_cooldown < 0.1
    
    # Enhanced corner detection and stage control
    stage_left = -0.8
    stage_right = 0.8
    corner_danger_left = my_position < -0.65
    corner_danger_right = my_position > 0.65
    opponent_cornered_left = opponent_position < -0.65
    opponent_cornered_right = opponent_position > 0.65
    
    # Movement prediction and opponent analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2)
    opponent_stationary = abs(opponent_velocity_x) < 0.1
    
    # Critical survival mode - highest priority
    if my_health <= critical_health:
        # Immediate attack defense
        if opponent_attack_status > 0 and distance < medium_distance:
            return 6  # Block incoming damage
        
        # Escape from close quarters
        if distance < close_distance:
            if relative_pos > 0:  # Opponent to right
                if not corner_danger_left:
                    return 7  # Move left with block
                else:
                    # Cornered, try to jump over or block
                    if height_diff > -0.1:
                        return 3  # Jump to escape
                    else:
                        return 6  # Block
            else:  # Opponent to left
                if not corner_danger_right:
                    return 8  # Move right with block
                else:
                    if height_diff > -0.1:
                        return 3  # Jump to escape
                    else:
                        return 6  # Block
        
        # Desperate zoning attempts
        if projectile_ready and distance > close_distance:
            return 9
        
        # Create distance when possible
        if distance < safe_distance:
            if relative_pos > 0 and not corner_danger_left:
                return 1  # Move away left
            elif relative_pos < 0 and not corner_danger_right:
                return 2  # Move away right
            else:
                return 6  # Block if can't escape
    
    # Enhanced defensive responses
    if opponent_attack_status > 0:
        if distance < medium_distance:
            # Threat is real, need defense
            if my_health <= low_health:
                return 6  # Priority block when low health
            else:
                # Try evasive blocking
                if opponent_approaching:
                    if relative_pos > 0 and not corner_danger_left:
                        return 7  # Retreat left with block
                    elif relative_pos < 0 and not corner_danger_right:
                        return 8  # Retreat right with block
                    else:
                        return 6  # Pure block
                else:
                    return 6  # Standard block
        elif distance < safe_distance and projectile_ready:
            # Counter-attack opportunity
            return 9
    
    # Anti-air and jump defense
    if height_diff < -0.25:  # Opponent jumping
        if distance < safe_distance:
            if projectile_ready:
                return 9  # Anti-air projectile
            else:
                # Prepare for landing mixup
                if distance < medium_distance:
                    return 6  # Block potential dive attack
                else:
                    # Create space
                    if relative_pos > 0 and not corner_danger_left:
                        return 1
                    elif not corner_danger_right:
                        return 2
                    else:
                        return 6
    
    # Opponent projectile threat response
    if opponent_projectile_threat and distance > medium_distance:
        # They might throw projectile, prepare to deal with it
        if opponent_stationary and distance > safe_distance:
            # Likely projectile incoming, prepare movement or our own
            if projectile_ready and random.random() < 0.6:
                return 9  # Counter-projectile
            else:
                # Prepare to evade
                if relative_pos > 0 and not corner_danger_left:
                    return 1  # Move left to avoid
                elif not corner_danger_right:
                    return 2  # Move right to avoid
        elif distance < safe_distance:
            # Close enough to pressure them out of projectile
            if relative_pos > 0 and not corner_danger_right:
                return 2  # Close distance
            elif not corner_danger_left:
                return 1  # Close distance
    
    # Core zoning strategy - optimal range control
    if distance >= optimal_range:
        # Perfect zoning distance
        if projectile_ready:
            # Check for optimal firing conditions
            if opponent_stationary or opponent_approaching:
                return 9  # High-probability hit
            elif opponent_retreating:
                # They're backing away, maintain pressure but consider spacing
                if distance > 0.6:
                    # Too far, let them retreat and reset
                    if relative_pos > 0 and not corner_danger_right:
                        return 2  # Close gap slightly
                    elif not corner_danger_left:
                        return 1  # Close gap slightly
                    else:
                        return 0  # Wait
                else:
                    return 9  # Continue pressure
            else:
                # Uncertain movement, throw projectile with slight delay
                if random.random() < 0.75:
                    return 9
                else:
                    return 0  # Occasional pause for unpredictability
        else:
            # Projectile cooling down, maintain optimal position
            if opponent_approaching and distance < 0.55:
                # They're getting too close, back up
                if relative_pos > 0 and not corner_danger_left:
                    return 1
                elif not corner_danger_right:
                    return 2
                else:
                    return