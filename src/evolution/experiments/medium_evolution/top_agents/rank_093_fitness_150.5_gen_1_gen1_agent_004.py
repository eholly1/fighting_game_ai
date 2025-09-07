"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_004
Rank: 93/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 150.45
- Win Rate: 0.0%
- Average Reward: 214.93

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
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid tactical parameters
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.45
    zoner_range = 0.6
    
    # Calculate stage positioning
    stage_center = 0.5
    my_corner_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_corner_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    near_corner = my_corner_distance < 0.2
    opponent_cornered = opponent_corner_distance < 0.15
    
    # Dynamic strategy selection based on game state
    health_ratio = my_health / max(opponent_health, 0.1)
    momentum_factor = health_advantage + (my_health - opponent_health)
    
    # Determine current fighting mode
    crisis_mode = my_health < 0.25 or health_advantage < -0.5
    dominating_mode = health_advantage > 0.4 and my_health > 0.6
    zoner_mode = distance > medium_range and my_projectile_cooldown < 0.3
    rushdown_mode = health_ratio > 1.2 or (opponent_health < 0.4 and my_health > 0.5)
    
    # Opponent behavior analysis
    opponent_aggressive = opponent_attack_status > 0.6
    opponent_defensive = opponent_block_status > 0.7
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.2) or (relative_pos < 0 and opponent_velocity_x < -0.2)
    
    # Crisis management - survival first
    if crisis_mode:
        if distance < ultra_close_range and opponent_aggressive:
            return 6  # Block critical hits
        
        if distance < close_range:
            if near_corner:
                # Escape corner with blocking movement
                if my_pos_x < stage_center:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
            else:
                # Create space defensively
                if opponent_aggressive:
                    return 6  # Block first
                else:
                    if relative_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
        
        elif distance < medium_range:
            # Try to get to projectile range
            if my_projectile_cooldown < 0.2:
                return 9  # Use projectile to create space
            else:
                if relative_pos > 0:
                    return 1  # Move left to create distance
                else:
                    return 2  # Move right to create distance
        
        else:
            # At safe distance, use projectiles
            if my_projectile_cooldown < 0.4:
                return 9  # Projectile zoning
            else:
                return 0  # Wait for cooldown
    
    # Dominating mode - controlled aggression
    elif dominating_mode:
        if opponent_cornered and distance < medium_range:
            # Corner pressure
            if opponent_defensive:
                # Mix up against blocking
                mixup = random.random()
                if mixup < 0.3:
                    return 9 if my_projectile_cooldown < 0.3 else 5  # Throw or kick
                elif mixup < 0.6:
                    return 3  # Jump for overhead
                else:
                    return 4  # Quick punch
            else:
                # Apply pressure
                if distance < close_range:
                    return 4 if random.random() < 0.6 else 5  # Attack mix
                else:
                    if relative_pos > 0:
                        return 2  # Move in
                    else:
                        return 1  # Move in
        
        elif distance < close_range:
            # Close range dominance
            if opponent_aggressive:
                # Counter attack
                if random.random() < 0.4:
                    return 6  # Block then counter
                else:
                    return 4  # Quick counter punch
            else:
                # Offensive pressure
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Punch
                elif attack_choice < 0.8:
                    return 5  # Kick
                else:
                    return 9 if my_projectile_cooldown < 0.2 else 4  # Throw or punch
        
        elif distance < medium_range:
            # Control medium range
            if opponent_retreating:
                # Chase retreating opponent
                if relative_pos > 0:
                    return 2  # Chase right
                else:
                    return 1  # Chase left
            else:
                # Advance with purpose
                if my_projectile_cooldown < 0.3 and random.random() < 0.3:
                    return 9  # Projectile approach
                else:
                    if relative_pos > 0:
                        return 2  # Move in
                    else:
                        return 1  # Move in
        
        else:
            # Long range control
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile pressure
            else:
                if distance > zoner_range:
                    # Close distance slightly
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                else:
                    return 0  # Wait at good distance
    
    # Rushdown mode - aggressive close combat
    elif rushdown_mode:
        if distance > medium_range:
            # Approach aggressively
            if opponent_projectile_cooldown < 0.2:
                # Opponent might shoot, approach with blocking
                if relative_pos > 0:
                    return 8  # Move right blocking
                else:
                    return 7  #