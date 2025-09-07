"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_023
Rank: 47/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 236.44
- Win Rate: 50.0%
- Average Reward: 236.44

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
    
    # Extract attack and movement status
    my_attack_status = state[4] if len(state) > 4 else 0
    opponent_attack_status = state[15] if len(state) > 15 else 0
    my_block_status = state[5] if len(state) > 5 else 0
    opponent_block_status = state[16] if len(state) > 16 else 0
    
    # Extract projectile cooldowns
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0)
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0)
    
    # Extract velocities for prediction
    my_velocity_x = state[7] if len(state) > 7 else 0
    opponent_velocity_x = state[18] if len(state) > 18 else 0
    
    # Height difference for anti-air
    height_diff = state[24] if len(state) > 24 else 0
    
    # Define hybrid tactical ranges
    danger_zone = 0.08
    close_range = 0.15
    medium_range = 0.30
    projectile_range = 0.45
    max_range = 0.65
    
    # Health-based thresholds
    critical_health = 0.15
    low_health = 0.35
    good_health = 0.65
    
    # Cooldown and status checks
    projectile_ready = my_projectile_cooldown < 0.08
    opponent_projectile_ready = opponent_projectile_cooldown < 0.08
    
    # Position analysis for corner awareness
    stage_left = -0.8
    stage_right = 0.8
    near_left_wall = my_position < stage_left
    near_right_wall = my_position > stage_right
    opponent_cornered = opponent_position < stage_left or opponent_position > stage_right
    
    # Frame advantage calculation
    frame_advantage = 0
    if my_attack_status > 0 and opponent_attack_status == 0:
        frame_advantage = 1
    elif opponent_attack_status > 0 and my_attack_status == 0:
        frame_advantage = -1
    
    # Movement prediction
    opponent_approaching = False
    if relative_pos > 0 and opponent_velocity_x > 0.1:
        opponent_approaching = True
    elif relative_pos < 0 and opponent_velocity_x < -0.1:
        opponent_approaching = True
    
    # Critical health emergency protocol
    if my_health <= critical_health:
        if distance < danger_zone and opponent_attack_status > 0:
            return 6  # Emergency block
        
        if distance < close_range:
            # Escape with blocking movement
            if relative_pos > 0 and not near_left_wall:
                return 7  # Block left retreat
            elif relative_pos < 0 and not near_right_wall:
                return 8  # Block right retreat
            else:
                return 6  # Block in place if cornered
        
        # Desperate projectile zoning
        if projectile_ready and distance > close_range:
            return 9
        
        # Create distance when possible
        if distance < medium_range:
            if relative_pos > 0 and not near_left_wall:
                return 1  # Move away left
            elif not near_right_wall:
                return 2  # Move away right
        
        return 6  # Default block when desperate
    
    # Opponent attack response system
    if opponent_attack_status > 0:
        if distance < medium_range:
            # Incoming attack likely to connect
            if frame_advantage >= 0 and distance < close_range:
                # Counter-attack opportunity
                counter_choice = random.random()
                if counter_choice < 0.4:
                    return 4  # Quick counter punch
                elif counter_choice < 0.65:
                    return 5  # Counter kick
                else:
                    return 6  # Safe block
            else:
                # Defensive response
                if my_health <= low_health:
                    return 6  # Block when low health
                else:
                    # Evasive blocking
                    if relative_pos > 0 and not near_left_wall:
                        return 7  # Block left
                    elif not near_right_wall:
                        return 8  # Block right
                    else:
                        return 6  # Block
        else:
            # Far enough to counter with projectile
            if projectile_ready and random.random() < 0.6:
                return 9
    
    # Anti-air system for jumping opponents
    if height_diff < -0.2:
        if distance < medium_range:
            if projectile_ready:
                return 9  # Projectile anti-air
            elif distance < close_range:
                return 4  # Quick anti-air punch
            else:
                # Reposition for better anti-air
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
    
    # Hybrid combat strategy by range
    if distance <= danger_zone:
        # Extreme close range - high risk/reward
        if opponent_block_status > 0:
            # Opponent blocking, mix up or retreat
            mix_choice = random.random()
            if mix_choice < 0.3:
                return 5  # Strong kick to break guard
            elif mix_choice < 0.5:
                # Quick retreat
                if relative_pos > 0:
                    return 1
                else:
                    return 2
            else:
                return 4  # Quick punch
        else:
            # Opponent not blocking, aggressive options
            if health_advantage > 0 or my_health > good_health:
                aggro_choice = random.random()
                if aggro_choice < 0.45:
                    return 4  # Fast punch
                elif aggro_choice < 0.75:
                    return 5  # Strong kick
                else:
                    return 6  # Block for safety
            else:
                # Health disadvantage, safer approach
                safe_choice = random.random()
                if safe_choice < 0.4:
                    return 4  # Quick punch
                else:
                    return 6  # Block
    
    elif distance <= close_range:
        # Close range - primary engagement zone
        if opponent_approaching and frame_advantage >= 0:
            # Counter approaching opponent
            return 5 if random.random() < 0.6 else 4
        
        if health_advantage > 0.2:
            # Winning, maintain pressure
            if opponent_block_status > 0:
                pressure_choice = random.random()
                if pressure_choice < 0.4:
                    return 5  # Strong attack vs block
                elif pressure_choice < 0.6:
                    return 4  # Quick attack
                else:
                    # Reposition for better angle
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
            else:
                # Opponent not blocking, attack
                attack_choice