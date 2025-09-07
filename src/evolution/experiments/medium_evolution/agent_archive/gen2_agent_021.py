"""
Evolutionary Agent: gen2_agent_021
==================================

Metadata:
{
  "generation": 2,
  "fitness": 248.81999999999113,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 24ed6b9b51d01383
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
    
    # Extract velocities and status
    my_velocity_x = state[7]
    opponent_velocity_x = state[18]
    my_attack_status = state[4]
    opponent_attack_status = state[15]
    my_block_status = state[5]
    opponent_block_status = state[16]
    
    # Projectile management
    my_projectile_cooldown = max(0.0, state[6])
    opponent_projectile_cooldown = max(0.0, state[17])
    height_diff = state[24]
    
    # Enhanced strategic constants for balanced approach
    optimal_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    max_range = 0.7
    
    # Health thresholds for adaptive behavior
    critical_health = 0.2
    low_health = 0.4
    good_health = 0.7
    
    # Stage positioning
    stage_center = 0.0
    corner_threshold = 0.75
    near_corner = 0.6
    
    # Projectile readiness states
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_soon = my_projectile_cooldown < 0.15
    opponent_projectile_ready = opponent_projectile_cooldown < 0.08
    
    # Movement analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_airborne = height_diff < -0.2
    
    # Corner detection
    i_am_cornered = abs(my_position) > corner_threshold
    opponent_cornered = abs(opponent_position) > corner_threshold
    i_near_corner = abs(my_position) > near_corner
    
    # Emergency survival mode
    if my_health <= critical_health:
        # Immediate threat response
        if opponent_attack_status > 0 and distance < medium_range:
            return 6  # Block critical attacks
        
        # Escape close quarters danger
        if distance < close_range:
            if not i_am_cornered:
                # Try to escape with blocking movement
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Cornered - try desperate measures
                if opponent_airborne:
                    return 4  # Quick punch while they're vulnerable
                elif projectile_ready:
                    return 9  # Point blank projectile
                else:
                    return 6  # Block and pray
        
        # Desperate spacing attempt
        if projectile_ready and distance > close_range:
            return 9  # Try to chip damage
        
        # Create distance when not in immediate danger
        if distance < medium_range and not i_am_cornered:
            if relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        
        # Default to blocking when all else fails
        return 6
    
    # Reactive defense against opponent attacks
    if opponent_attack_status > 0:
        if distance < medium_range:
            # Real threat - prioritize defense
            if my_health <= low_health:
                return 6  # Conservative blocking
            else:
                # Try mobile defense if space allows
                if not i_near_corner:
                    if relative_pos > 0:
                        return 7  # Retreat left with block
                    else:
                        return 8  # Retreat right with block
                else:
                    return 6  # Standard block
        elif distance < far_range and projectile_ready:
            # Counter-attack opportunity at medium range
            return 9
    
    # Anti-air response
    if opponent_airborne and distance < medium_range:
        if projectile_ready:
            return 9  # Anti-air projectile
        elif distance < close_range:
            # Prepare for their landing
            if my_health > low_health:
                return 4  # Quick anti-air punch
            else:
                return 6  # Safe block
        else:
            # Reposition for better anti-air
            if relative_pos > 0 and not i_near_corner:
                return 2  # Move closer for better coverage
            elif not i_near_corner:
                return 1  # Move closer for better coverage
    
    # Opponent projectile threat management
    if opponent_projectile_ready and distance > medium_range:
        if projectile_ready and random.random() < 0.7:
            return 9  # Projectile war
        else:
            # Evasive movement
            if distance > far_range:
                # Close distance to pressure them
                if relative_pos > 0 and not i_near_corner:
                    return 2
                elif not i_near_corner:
                    return 1
            else:
                # Mid-range evasion
                if relative_pos > 0 and my_position > -near_corner:
                    return 1  # Dodge left
                elif my_position < near_corner:
                    return 2  # Dodge right
                else:
                    return 6  # Block if cornered
    
    # Balanced offensive strategy based on range and health
    
    # Optimal close combat range
    if distance <= optimal_close_range:
        if health_advantage > 0.3:
            # Winning decisively - aggressive mixups
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 4  # Fast punch
            elif attack_choice < 0.7:
                return 5  # Strong kick
            else:
                return 6  # Occasional defensive reset
        elif health_advantage > -0.2:
            # Even fight - balanced approach
            if opponent_block_status > 0:
                # They're blocking, try throws or repositioning
                if random.random() < 0.5:
                    return 5  # Kick to break guard
                else:
                    # Create space for mixup
                    if relative_pos > 0 and not i_near_corner:
                        return 1
                    elif not i_near_corner:
                        return 2
                    else:
                        return 4  # Quick punch
            else:
                # Open for attack
                if random.random() < 0.6:
                    return 4  # Reliable punch
                else:
                    return 5  # Power kick
        else:
            # Losing - defensive approach
            if random.random() < 0.7:
                return 6  # Mostly block
            else:
                return 4  # Occasional quick counter
    
    # Close combat range
    elif distance <= close_range:
        if opponent_cornered and my_health > low_health:
            # Pressure cornered opponent
            if opponent_block_status > 0:
                # They're blocking, mix up timing
                if random.random() < 0.4:
                    return 5