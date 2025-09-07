"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_014
Rank: 40/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 249.60
- Win Rate: 50.0%
- Average Reward: 249.60

Created: 2025-06-01 02:16:30
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2] if len(state) > 2 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[7] if len(state) > 7 else 0.0
    my_attack_status = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0.0)
    
    # Extract opponent status with bounds checking
    opponent_health = max(0.0, min(1.0, state[13] if len(state) > 13 else 1.0))
    opponent_pos_x = state[11] if len(state) > 11 else 0.5
    opponent_velocity_x = state[18] if len(state) > 18 else 0.0
    opponent_attack_status = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0.0)
    
    # Strategic range definitions for hybrid approach
    touching_range = 0.08
    close_range = 0.18
    medium_close_range = 0.28
    medium_range = 0.4
    far_range = 0.55
    
    # Health-based strategy thresholds
    critical_health = 0.12
    low_health = 0.25
    moderate_health = 0.5
    good_health = 0.75
    
    # Positioning and stage control
    stage_center = abs(my_pos_x) < 0.3
    corner_danger = my_pos_x < -0.7 or my_pos_x > 0.7
    opponent_cornered = opponent_pos_x < -0.7 or opponent_pos_x > 0.7
    
    # Opponent behavior analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_stationary = abs(opponent_velocity_x) < 0.1
    
    # Projectile status
    projectile_ready = my_projectile_cooldown < 0.1
    projectile_almost_ready = my_projectile_cooldown < 0.25
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    
    # Adaptive aggression based on multiple factors
    base_aggression = 0.65
    health_factor = 1.0 + (health_advantage * 0.4)
    distance_factor = 1.2 if distance < medium_range else 0.8
    position_factor = 1.1 if stage_center else 0.9
    current_aggression = max(0.2, min(0.95, base_aggression * health_factor * distance_factor * position_factor))
    
    # Critical survival mode - absolute priority
    if my_health <= critical_health:
        # Immediate threat response
        if opponent_attack_status > 0.3 and distance < medium_close_range:
            if corner_danger:
                # Cornered and under attack - try to escape or block
                if height_diff > -0.2 and random.random() < 0.4:
                    return 3  # Desperate jump
                else:
                    return 6  # Block
            else:
                # Retreat while blocking
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        # Projectile harassment when safe
        if projectile_ready and distance > medium_close_range and opponent_attack_status < 0.2:
            return 9
        
        # Emergency spacing
        if distance < close_range and not corner_danger:
            if relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        
        # Default defensive stance
        return 6
    
    # Anti-air and aerial opponent handling
    if height_diff < -0.3:  # Opponent jumping high
        if distance < medium_range:
            if projectile_ready and distance > close_range:
                return 9  # Anti-air projectile
            elif distance < close_range:
                # Prepare for landing mix-up
                if opponent_advancing:
                    return 6  # Block potential dive attack
                else:
                    # Try to escape landing pressure
                    if relative_pos > 0 and not corner_danger:
                        return 1
                    elif not corner_danger:
                        return 2
                    else:
                        return 6
        elif projectile_ready:
            return 9  # Long range anti-air
    
    # Counter-projectile and zoning response
    if opponent_projectile_ready and distance > medium_close_range:
        if opponent_stationary and distance > medium_range:
            # Likely projectile incoming
            if projectile_ready and random.random() < 0.7:
                return 9  # Counter-projectile
            else:
                # Evasive movement
                evasion_choice = random.random()
                if evasion_choice < 0.4:
                    return 3  # Jump over
                elif evasion_choice < 0.7 and not corner_danger:
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 6  # Block if cornered
        elif distance < medium_range and opponent_attack_status < 0.2:
            # Close enough to pressure them out of projectile
            if relative_pos > 0:
                return 2  # Advance right
            else:
                return 1  # Advance left
    
    # Defensive responses to opponent attacks
    if opponent_attack_status > 0.4:
        if distance < medium_close_range:
            # Real threat - need defense
            if my_health <= low_health:
                return 6  # Priority block when low health
            else:
                # Try evasive defense
                if opponent_advancing and not corner_danger:
                    if relative_pos > 0:
                        return 7  # Retreat left with block
                    else:
                        return 8  # Retreat right with block
                else:
                    return 6  # Standard block
        elif distance < medium_range and projectile_ready:
            # Counter-attack opportunity at mid range
            return 9
    
    # Corner escape when cornered
    if corner_danger and distance < medium_close_range:
        if opponent_attack_status > 0.3:
            # Under pressure in corner
            escape_method = random.random()
            if escape_method < 0.4:
                return 3  # Jump escape