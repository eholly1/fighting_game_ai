"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_024
Rank: 66/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 195.96
- Win Rate: 0.0%
- Average Reward: 195.96

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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity_x = state[4]
    opponent_velocity_x = state[15]
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    projectile_cooldown = max(0.0, state[9])
    opponent_projectile_cooldown = max(0.0, state[20])
    height_difference = state[24]
    
    # Enhanced tactical parameters for evolved hit-and-run
    ultra_close_range = 0.08
    close_range = 0.14
    medium_range = 0.32
    safe_range = 0.50
    long_range = 0.70
    
    # Dynamic thresholds based on health state
    critical_health = 0.15
    low_health = 0.30
    retreat_urgency_distance = 0.20
    winning_aggression_threshold = 0.25
    desperation_threshold = -0.5
    
    # Adaptive behavior state tracking
    opponent_blocking_frequently = opponent_block_status > 0.4
    opponent_attacking = opponent_attack_status > 0.3
    safe_to_projectile = projectile_cooldown < 0.05
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    
    # Emergency survival mode - critical health
    if my_health < critical_health or health_advantage < desperation_threshold:
        if distance < retreat_urgency_distance:
            # Panic retreat with maximum protection
            if opponent_attacking:
                # Opponent is attacking, block while retreating
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Fast retreat without blocking for speed
                if relative_pos > 0:
                    return 1  # Move left fast
                else:
                    return 2  # Move right fast
        
        elif distance < safe_range:
            if safe_to_projectile and not opponent_projectile_ready:
                return 9  # Desperate projectile
            else:
                return 6  # Full defensive block
        
        else:
            # Long range survival - projectile spam
            if safe_to_projectile:
                return 9  # Projectile attack
            else:
                # Maintain maximum distance
                if relative_pos > 0:
                    return 1  # Move away left
                else:
                    return 2  # Move away right
    
    # Aggressive finishing mode - significant health advantage
    if health_advantage > winning_aggression_threshold and opponent_health < low_health:
        if distance < ultra_close_range:
            # Ultra close finishing moves
            if opponent_blocking_frequently:
                # Try to break guard or reposition
                if random.random() < 0.4:
                    return 5  # Strong kick to break block
                else:
                    # Quick repositioning strike
                    return 4  # Fast punch
            else:
                # Go for knockout
                finish_choice = random.random()
                if finish_choice < 0.6:
                    return 5  # Power kick
                else:
                    return 4  # Quick punch combo
        
        elif distance < close_range:
            # Close in for finish
            if opponent_attacking:
                # Counter-attack opportunity
                return 4  # Fast counter punch
            else:
                # Aggressive approach
                if relative_pos > 0:
                    return 2  # Move right aggressively
                else:
                    return 1  # Move left aggressively
    
    # Core hit-and-run strategy - ultra close range
    if distance < ultra_close_range:
        # Maximum danger zone - immediate action required
        if opponent_blocking_frequently:
            # Opponent blocking - immediate retreat
            retreat_method = random.random()
            if retreat_method < 0.6:
                # Fast retreat
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
            else:
                # Protected retreat
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        elif opponent_attacking:
            # Opponent attacking - defensive counter or retreat
            if my_attack_status < 0.1 and random.random() < 0.4:
                return 4  # Quick counter punch
            else:
                # Defensive retreat
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        else:
            # Open opponent - hit and run opportunity
            if my_attack_status < 0.1:
                # Can attack
                strike_decision = random.random()
                if strike_decision < 0.5:
                    return 4  # Quick punch - fastest option
                elif strike_decision < 0.75:
                    return 5  # Kick for damage
                else:
                    # Fake out - retreat instead
                    if relative_pos > 0:
                        return 1  # Move left away
                    else:
                        return 2  # Move right away
            else:
                # Already attacked - must retreat
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
    
    # Close range hit-and-run tactics
    elif distance < close_range:
        if opponent_attacking:
            # Opponent attacking - evasive maneuvers
            evasion_choice = random.random()
            if evasion_choice < 0.3:
                return 3  # Jump over attack
            elif evasion_choice < 0.6:
                # Retreat with block
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Fast retreat
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        elif opponent_blocking_frequently:
            # Opponent defensive - maintain distance or reposition
            if random.random() < 0.7:
                # Retreat to better range
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
            else:
                # Try jump attack approach
                return 3  # Jump
        
        else:
            # Neutral close range - hit and run decision
            if my_attack_status < 0.1 and health_advantage > -0.3:
                # Safe to attack
                attack_choice = random.random()
                if attack_choice < 0.55:
                    return 4  # Quick punch
                elif attack_choice < 0.75:
                    return 5  # Kick
                else:
                    # Retreat instead for unpredictability
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            else:
                # Retreat to safer distance
                retreat_choice = random.random()
                if retreat_choice < 0.8:
                    if relative_pos > 0:
                        return 1