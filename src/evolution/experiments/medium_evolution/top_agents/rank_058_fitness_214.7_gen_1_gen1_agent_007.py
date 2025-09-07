"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_007
Rank: 58/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 214.71
- Win Rate: 50.0%
- Average Reward: 306.73

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
    # Validate input and extract core strategic information
    if len(state) < 26:
        return 0  # Safety fallback
    
    # Core strategic metrics with bounds checking
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # My fighter comprehensive status
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.1 if len(state) > 5 else False
    my_blocking = state[6] > 0.1 if len(state) > 6 else False
    my_stunned = state[7] > 0.1 if len(state) > 7 else False
    my_projectile_cooldown = state[8] if len(state) > 8 else 1.0
    my_attack_cooldown = state[9] if len(state) > 9 else 1.0
    my_block_cooldown = state[10] if len(state) > 10 else 1.0
    
    # Opponent comprehensive status
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = state[11]
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.1 if len(state) > 16 else False
    opp_blocking = state[17] > 0.1 if len(state) > 17 else False
    opp_stunned = state[18] > 0.1 if len(state) > 18 else False
    opp_projectile_cooldown = state[19] if len(state) > 19 else 1.0
    opp_attack_cooldown = state[20] if len(state) > 20 else 1.0
    opp_block_cooldown = state[21] if len(state) > 21 else 1.0
    
    # Hybrid fighter tactical ranges
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.30
    far_range = 0.45
    max_range = 0.65
    
    # Dynamic aggression calculation for hybrid approach
    base_aggression = 0.65  # Balanced baseline
    health_modifier = health_advantage * 0.25
    range_modifier = 0.0
    
    # Range-based aggression adjustments
    if distance < close_range:
        range_modifier = 0.15  # More aggressive up close
    elif distance > far_range:
        range_modifier = -0.1  # More cautious at range
    
    current_aggression = max(0.2, min(0.9, base_aggression + health_modifier + range_modifier))
    
    # Tactical state analysis
    can_attack = my_attack_cooldown < 0.15
    can_projectile = my_projectile_cooldown < 0.15
    can_block = my_block_cooldown < 0.15
    
    # Opponent threat assessment
    opp_can_attack = opp_attack_cooldown < 0.15
    opp_can_projectile = opp_projectile_cooldown < 0.15
    opp_threatening = opp_attacking or (opp_can_attack and distance < 0.2)
    
    # Critical health emergency protocols
    if my_stunned and opp_threatening:
        if can_block:
            return 6  # Desperate block
        else:
            # Try to escape
            if relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
    
    # Extremely low health survival mode
    if my_health < 0.15 and health_advantage < -0.5:
        if distance > 0.4:
            # Safe projectile range
            if can_projectile:
                return 9
            else:
                return 6  # Block and wait
        elif distance > 0.2:
            # Create more distance
            if relative_pos > 0:
                return 1  # Move away
            else:
                return 2  # Move away
        else:
            # Too close - block or escape
            if can_block and random.random() < 0.7:
                return 6
            else:
                if relative_pos > 0:
                    return 1
                else:
                    return 2
    
    # Opponent stunned - maximum opportunity exploitation
    if opp_stunned:
        if distance < close_range:
            if can_attack:
                # Choose attack based on opponent health
                if opp_health < 0.3:
                    return 5  # Kick for potential finish
                else:
                    return 4 if random.random() < 0.6 else 5  # Mix attacks
            else:
                # Position for next attack
                if distance > very_close_range:
                    if relative_pos > 0:
                        return 2  # Move closer
                    else:
                        return 1  # Move closer
                else:
                    return 0  # Wait for attack cooldown
        else:
            # Move in to capitalize
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    # Opponent attacking - hybrid defensive response
    if opp_attacking:
        if distance < 0.12:
            # Very close threat
            if can_block and random.random() < 0.8:
                return 6  # Block most of the time
            else:
                # Try to escape
                if relative_pos > 0:
                    return 1
                else:
                    return 2
        elif distance < 0.25:
            # Medium threat range
            defensive_choice = random.random()
            if defensive_choice < 0.4 and can_block:
                # Block with movement
                if relative_pos > 0:
                    return 7  # Block left
                else:
                    return 8  # Block right
            elif defensive_choice < 0.7:
                # Pure movement
                if relative_pos > 0:
                    return 1
                else:
                    return 2
            else:
                # Counter-attack if winning
                if health_advantage > 0.1 and can_attack:
                    return 4  # Quick counter
                else:
                    return 6  # Block
        else:
            # Far enough to projectile
            if can_projectile:
                return 9
            else:
                return 0  # Wait
    
    # Core hybrid combat strategy by range
    if distance < very_close_range:
        # Extreme close quarters - high intensity
        if health_advantage > 0.2:
            # Winning - maintain pressure
            if can_attack:
                attack_roll = random.random()
                if attack_roll < 0.5:
                    return 4  # Quick punch
                elif attack_roll < 0.85:
                    return 5  # Strong kick