"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_010
Rank: 43/100
Generation: 0
Fighting Style: aggressive

Performance Metrics:
- Fitness: 240.32
- Win Rate: 50.0%
- Average Reward: 240.32

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
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attack_cooldown = state[5]
    my_block_status = state[6]
    my_projectile_cooldown = state[9]
    my_stamina = state[10] if len(state) > 10 else 1.0
    
    # Extract opponent information
    opp_health = state[12] if state[12] >= 0 else 0.5
    opp_x_pos = state[11]
    opp_y_pos = state[13]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attack_cooldown = state[16]
    opp_block_status = state[17]
    opp_projectile_cooldown = state[20]
    
    # Define aggressive strategy parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    aggression_multiplier = 1.2
    chase_threshold = 0.8
    pressure_distance = 0.2
    
    # Aggressive style: Always prefer forward movement and attacks
    base_aggression = 0.85
    current_aggression = base_aggression * aggression_multiplier
    
    # Health-based aggression adjustment (still aggressive when losing)
    if health_advantage < -0.4:
        current_aggression = max(0.6, current_aggression * 0.8)
    elif health_advantage > 0.3:
        current_aggression = min(1.0, current_aggression * 1.3)
    
    # Critical health emergency (only time to be defensive)
    if my_health < 0.15 and health_advantage < -0.6:
        if distance < close_range and opp_attack_cooldown <= 0.1:
            return 6  # Block when in immediate danger
        elif distance > medium_range:
            return 9  # Projectile to chip damage
    
    # Opponent vulnerability detection (aggressive exploitation)
    opponent_vulnerable = (opp_attack_cooldown > 0.3 or 
                          opp_block_status < 0.1 or
                          abs(opp_x_velocity) > 0.5)
    
    # Stamina management for sustained aggression
    low_stamina = my_stamina < 0.3
    critical_stamina = my_stamina < 0.15
    
    # CLOSE RANGE COMBAT (Primary aggressive zone)
    if distance <= close_range:
        # Maximum aggression in close range
        if critical_stamina and opp_attack_cooldown <= 0.1:
            return 6  # Brief defensive moment
        
        # Opponent is blocking - break through with variety
        if opp_block_status > 0.5:
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 5  # Heavy kick to break blocks
            elif attack_choice < 0.7:
                return 4  # Quick punch combo
            else:
                # Reposition for better angle
                if relative_pos > 0:
                    return 2  # Move right for angle
                else:
                    return 1  # Move left for angle
        
        # Opponent vulnerable - unleash maximum offense
        if opponent_vulnerable:
            if my_attack_cooldown <= 0.1:
                combo_choice = random.random()
                if combo_choice < 0.5:
                    return 4  # Fast punch
                else:
                    return 5  # Power kick
        
        # Standard close combat aggression
        if my_attack_cooldown <= 0.2:
            if not low_stamina:
                attack_pattern = random.random()
                if attack_pattern < 0.6:
                    return 4  # Punch (primary close attack)
                else:
                    return 5  # Kick (power follow-up)
            else:
                return 4  # Conserve stamina with punches
        
        # Can't attack but stay aggressive with positioning
        if abs(height_diff) > 0.3:
            return 3  # Jump to match height
        
        # Maintain pressure even during cooldown
        if relative_pos > 0.1:
            return 2  # Stay close, move right
        elif relative_pos < -0.1:
            return 1  # Stay close, move left
        else:
            return 4  # Attempt attack
    
    # MEDIUM RANGE COMBAT (Aggressive positioning)
    elif distance <= medium_range:
        # Rush in for close combat (core aggressive strategy)
        rush_probability = current_aggression * 0.9
        
        if random.random() < rush_probability:
            # Determine best approach angle
            if abs(height_diff) > 0.4:
                return 3  # Jump to close height gap
            
            # Direct aggressive approach
            if relative_pos > 0.05:
                if opp_block_status > 0.3:
                    return 8  # Move right with block (cautious aggression)
                else:
                    return 2  # Pure aggressive advance right
            elif relative_pos < -0.05:
                if opp_block_status > 0.3:
                    return 7  # Move left with block (cautious aggression)
                else:
                    return 1  # Pure aggressive advance left
            else:
                # Direct frontal approach
                if my_attack_cooldown <= 0.3:
                    return 4  # Punch while advancing
                else:
                    return 2 if random.random() < 0.5 else 1
        
        # Projectile to force opponent reaction (aggressive zoning)
        if my_projectile_cooldown <= 0.1 and not low_stamina:
            if opp_x_velocity < 0.2:  # Opponent not moving much
                return 9  # Force them to react
        
        # Jump-in attack approach
        if abs(height_diff) < 0.2 and my_attack_cooldown <= 0.2:
            jump_attack = random.random()
            if jump_attack < 0.3:
                return 3  # Jump toward opponent
        
        # Default: close the distance aggressively
        if relative_pos > 0:
            return 2  # Move right
        else:
            return 1  # Move left
    
    # FAR RANGE COMBAT (Aggressive approach/projectile game)
    elif distance <= far_range:
        # Projectile pressure while advancing
        if my_projectile_cooldown <= 0.1:
            projectile_aggression = random.random()
            if projectile_aggression < current_aggression:
                return 9  # Projectile attack
        
        # Aggressive approach - close distance quickly
        approach_roll = random.random()
        if approach_roll < current_aggression * 0.8:
            if abs(height_diff) > 0.5:
                return 3  # Jump to close gap
            
            # Sprint toward opponent
            if relative_pos > 0.1:
                return 2  # Move right aggressively
            elif relative_pos < -0.1:
                return 1  # Move left aggressively