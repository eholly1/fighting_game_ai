"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_011
Rank: 18/100
Generation: 0
Fighting Style: defensive

Performance Metrics:
- Fitness: 275.28
- Win Rate: 50.0%
- Average Reward: 275.28

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
    # Extract and validate key game state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    my_velocity = state[3]
    opponent_velocity = state[14]
    
    # Extract attack and defense status
    my_attacking = state[6] > 0.5
    opponent_attacking = state[17] > 0.5
    my_blocking = state[7] > 0.5
    opponent_blocking = state[18] > 0.5
    
    # Projectile cooldown information
    my_projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    
    # Height difference
    height_diff = state[24]
    
    # Define strategic thresholds for defensive play
    close_range = 0.12
    medium_range = 0.35
    danger_health = 0.3
    critical_health = 0.15
    safe_distance = 0.45
    
    # Emergency survival mode when critically low health
    if my_health < critical_health:
        if opponent_attacking and distance < close_range:
            return 6  # Block incoming attack
        elif distance < safe_distance:
            # Retreat while blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            # Use projectile from safe distance
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                return 6  # Block while waiting for cooldown
    
    # Defensive positioning when health is low
    if my_health < danger_health:
        # Prioritize blocking and safe distance
        if opponent_attacking:
            if distance < medium_range:
                return 6  # Block incoming attacks
            elif distance < safe_distance:
                # Maintain defensive distance
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
        
        # Counter-attack opportunities when opponent is vulnerable
        if not opponent_blocking and distance < close_range:
            if opponent_velocity > 0.3:  # Opponent moving fast, risky
                return 6  # Stay defensive
            else:
                # Quick counter-attack
                return 4 if random.random() < 0.7 else 5
        
        # Long-range harassment
        if distance > safe_distance and my_projectile_cooldown < 0.2:
            return 9
        
        # Default defensive stance
        return 6
    
    # Standard defensive play when health is moderate
    if health_advantage < 0:
        # We're behind, play more defensively
        if opponent_attacking and distance < medium_range:
            if distance < close_range:
                return 6  # Block close attacks
            else:
                # Defensive movement
                if relative_pos > 0:
                    return 7  # Move away with block
                else:
                    return 8  # Move away with block
        
        # Look for counter-attack windows
        if distance < close_range and not opponent_blocking:
            if my_attacking:  # Already in attack sequence
                return 0  # Let attack complete
            else:
                # Conservative counter-attack
                if random.random() < 0.6:
                    return 4  # Quick punch
                else:
                    return 6  # Stay defensive
        
        # Medium range positioning
        if distance >= close_range and distance < medium_range:
            if opponent_attacking:
                return 6  # Block at medium range
            else:
                # Careful positioning
                if abs(relative_pos) > 0.5:
                    # Move to better position
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 6  # Maintain guard
        
        # Long range defensive tactics
        if distance >= medium_range:
            if my_projectile_cooldown < 0.3 and not opponent_blocking:
                return 9  # Safe projectile
            else:
                # Maintain safe distance
                if distance < safe_distance:
                    if relative_pos > 0:
                        return 1  # Move away
                    else:
                        return 2  # Move away
                else:
                    return 6  # Guard up
    
    # Balanced play when health is even
    elif abs(health_advantage) < 0.2:
        # Focus on defensive positioning with selective aggression
        if opponent_attacking:
            if distance < close_range:
                return 6  # Block close attacks
            elif distance < medium_range:
                # Defensive movement at medium range
                if random.random() < 0.7:
                    return 6  # Block
                else:
                    # Occasional evasive movement
                    if relative_pos > 0:
                        return 7
                    else:
                        return 8
        
        # Controlled aggression opportunities
        if distance < close_range and not opponent_blocking:
            if opponent_velocity < 0.2:  # Opponent relatively still
                # Measured attack
                if random.random() < 0.5:
                    return 4  # Quick punch
                elif random.random() < 0.3:
                    return 5  # Stronger kick
                else:
                    return 6  # Stay defensive
            else:
                return 6  # Opponent moving, stay defensive
        
        # Medium range control
        if distance >= close_range and distance < medium_range:
            if opponent_projectile_cooldown > 0.5:  # Safe from projectiles
                # Move to optimal range
                if distance > 0.25:
                    # Close distance slightly
                    if relative_pos > 0:
                        return 2  # Move right toward opponent
                    else:
                        return 1  # Move left toward opponent
                else:
                    return 6  # Maintain guard
            else:
                return 6  # Guard against potential projectile
        
        # Long range tactics
        if distance >= medium_range:
            if my_projectile_cooldown < 0.4 and opponent_projectile_cooldown > 0.3:
                return 9  # Safe projectile opportunity
            elif distance > 0.6:
                # Close distance gradually
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                return 6  # Maintain defensive stance
    
    # Cautious offense when ahead
    else:
        # We have health advantage, but maintain defensive principles
        if opponent_attacking:
            # Still prioritize defense even when winning
            if distance < medium_range:
                return 6  # Block attacks
            else:
                # Can be slightly more mobile when ahead
                if relative_pos > 0:
                    return 7  # Move with block
                else:
                    return 8  # Move with block
        
        # Selective pressure when winning
        if distance < close_range:
            if not opponent_blocking and opponent_velocity < 0.3:
                # Apply controlled pressure
                if random.random() < 0.6:
                    return 4  # Punch
                elif random.random() < 0.4:
                    return 5  # Kick
                else:
                    return 6  # Stay guarded
            else:
                return 6  # Maintain defense