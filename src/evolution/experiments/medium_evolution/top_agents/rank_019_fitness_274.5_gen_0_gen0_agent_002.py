"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_002
Rank: 19/100
Generation: 0
Fighting Style: zoner

Performance Metrics:
- Fitness: 274.52
- Win Rate: 50.0%
- Average Reward: 274.52

Created: 2025-06-01 00:36:59
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
    
    # Extract projectile cooldown
    my_projectile_cooldown = max(0.0, state[6])
    opponent_projectile_cooldown = max(0.0, state[17])
    
    # Extract velocities for movement prediction
    my_velocity_x = state[7]
    opponent_velocity_x = state[18]
    
    # Height difference
    height_diff = state[24]
    
    # Define strategic constants for zoner playstyle
    safe_distance = 0.4
    medium_distance = 0.25
    close_distance = 0.15
    danger_distance = 0.08
    
    # Health thresholds
    critical_health = 0.2
    low_health = 0.4
    good_health = 0.7
    
    # Projectile cooldown threshold
    projectile_ready = my_projectile_cooldown < 0.1
    
    # Corner detection (assuming stage boundaries at -1.0 and 1.0)
    near_left_corner = my_position < -0.7
    near_right_corner = my_position > 0.7
    opponent_near_left = opponent_position < -0.7
    opponent_near_right = opponent_position > 0.7
    
    # Emergency situations - highest priority
    if my_health <= critical_health:
        # Desperate survival mode
        if distance < danger_distance and opponent_attack_status > 0:
            return 6  # Block incoming attack
        
        if distance < close_distance:
            # Too close, need to escape
            if relative_pos > 0:  # Opponent to right
                if not near_left_corner:
                    return 7  # Move left while blocking
                else:
                    return 6  # Block if cornered
            else:  # Opponent to left
                if not near_right_corner:
                    return 8  # Move right while blocking
                else:
                    return 6  # Block if cornered
        
        # Try to create distance with projectiles
        if projectile_ready and distance > close_distance:
            return 9
        
        # Maintain safe distance
        if distance < safe_distance:
            if relative_pos > 0 and not near_left_corner:
                return 1  # Move left away from opponent
            elif relative_pos < 0 and not near_right_corner:
                return 2  # Move right away from opponent
            else:
                return 6  # Block if can't escape
    
    # Opponent is attacking - defensive response
    if opponent_attack_status > 0:
        if distance < medium_distance:
            # Close enough that attack might hit
            if my_health <= low_health:
                return 6  # Block when low health
            else:
                # Try to evade while blocking
                if relative_pos > 0 and not near_left_corner:
                    return 7  # Move left block
                elif relative_pos < 0 and not near_right_corner:
                    return 8  # Move right block
                else:
                    return 6  # Just block
        else:
            # Far enough to potentially counter with projectile
            if projectile_ready:
                return 9
    
    # Anti-air response if opponent is jumping
    if height_diff < -0.3:  # Opponent is significantly higher
        if distance < medium_distance:
            if projectile_ready:
                return 9  # Projectile anti-air
            else:
                # Move away and prepare
                if relative_pos > 0 and not near_left_corner:
                    return 1
                elif not near_right_corner:
                    return 2
                else:
                    return 6  # Block if cornered
    
    # Zoner main strategy - range control
    if distance > safe_distance:
        # Optimal zoning range
        if projectile_ready:
            # Add some timing variation to avoid predictability
            if random.random() < 0.8:
                return 9  # Primary zoning tool
            else:
                # Occasional movement to avoid being too static
                if relative_pos > 0 and random.random() < 0.5:
                    return 1  # Move left occasionally
                elif relative_pos < 0:
                    return 2  # Move right occasionally
                else:
                    return 9  # Default to projectile
        else:
            # Projectile on cooldown, maintain position
            if opponent_velocity_x != 0:
                # Opponent is moving, adjust position
                if opponent_velocity_x > 0:  # Opponent moving right
                    if not near_left_corner:
                        return 1  # Move left to maintain distance
                elif opponent_velocity_x < 0:  # Opponent moving left
                    if not near_right_corner:
                        return 2  # Move right to maintain distance
            
            # Default positioning
            return 0  # Wait for projectile cooldown
    
    elif distance > medium_distance:
        # Good zoning range but need to be ready
        if projectile_ready:
            # Check opponent's movement pattern
            if opponent_velocity_x == 0:
                # Stationary opponent, good projectile target
                return 9
            else:
                # Moving opponent, predict and adjust
                if abs(opponent_velocity_x) > 0.5:
                    # Fast moving opponent, prepare for defense
                    if distance < 0.35:
                        return 6  # Block as they approach
                    else:
                        return 9  # Projectile while still safe
                else:
                    return 9  # Standard projectile
        else:
            # Maintain optimal spacing while cooldown recovers
            if relative_pos > 0:  # Opponent to right
                if distance < 0.3 and not near_left_corner:
                    return 1  # Create more space
                elif distance > 0.35 and not near_right_corner:
                    return 2  # Close gap slightly
            else:  # Opponent to left
                if distance < 0.3 and not near_right_corner:
                    return 2  # Create more space
                elif distance > 0.35 and not near_left_corner:
                    return 1  # Close gap slightly
            
            return 0  # Hold position
    
    elif distance > close_distance:
        # Medium range - transition zone
        if health_advantage > 0.3:
            # Winning significantly, can afford some risks
            if projectile_ready:
                return 9
            else:
                # Maybe pressure slightly
                if opponent_block_status > 0:
                    # Opponent blocking, maintain pressure
                    if relative_pos > 0 and not near_right_corner:
                        return 2  # Move closer
                    elif relative_pos < 0 and not near_left_corner:
                        return 1  # Move closer
                else:
                    # Opponent not blocking but we're in danger zone
                    if not near_left_corner and relative_pos > 0:
                        return 1  # Back away
                    elif not near_right_corner and relative_pos < 0:
                        return 2  # Back away