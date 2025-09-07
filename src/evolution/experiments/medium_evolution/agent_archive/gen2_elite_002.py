"""
Evolutionary Agent: gen2_elite_002
==================================

Metadata:
{
  "generation": 2,
  "fitness": 211.00333333333333,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 27b228654484ec45
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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity = state[3]
    opponent_velocity = state[14]
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    projectile_cooldown = max(0.0, state[9])
    opponent_projectile_cooldown = max(0.0, state[20])
    height_difference = state[24]
    
    # Enhanced tactical parameters for improved hit-and-run
    strike_range = 0.14
    danger_zone = 0.20
    medium_range = 0.35
    safe_projectile_range = 0.50
    critical_health = 0.25
    winning_margin = 0.25
    retreat_health_threshold = -0.35
    
    # Track momentum and create unpredictability
    momentum_factor = abs(my_velocity) + abs(opponent_velocity)
    unpredictability = random.random()
    
    # Critical health emergency protocol
    if my_health < critical_health or health_advantage < retreat_health_threshold:
        if distance < danger_zone:
            # Emergency retreat with maximum protection
            if opponent_attack_status > 0.3:
                # Opponent attacking - defensive retreat
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Quick escape
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
        elif distance < safe_projectile_range and projectile_cooldown < 0.15:
            return 9  # Keep distance with projectile
        else:
            # Defensive positioning
            if unpredictability < 0.4:
                return 6  # Block
            elif unpredictability < 0.7:
                return 3  # Jump for evasion
            else:
                return 0  # Wait for opportunity
    
    # Aggressive finishing when opponent is vulnerable
    if health_advantage > winning_margin and opponent_health < 0.35:
        if distance < strike_range:
            # Finishing combinations
            if opponent_block_status < 0.2:
                finish_choice = unpredictability
                if finish_choice < 0.5:
                    return 5  # Powerful kick
                elif finish_choice < 0.8:
                    return 4  # Quick punch
                else:
                    # Feint retreat then counter
                    if relative_pos > 0:
                        return 1  # Move away briefly
                    else:
                        return 2  # Move away briefly
            else:
                # Opponent blocking - reposition
                if relative_pos > 0:
                    return 2  # Circle right
                else:
                    return 1  # Circle left
        elif distance < medium_range:
            # Aggressive approach for finish
            if opponent_projectile_cooldown > 0.4:
                if relative_pos > 0:
                    return 2  # Move in
                else:
                    return 1  # Move in
            elif projectile_cooldown < 0.1:
                return 9  # Projectile pressure
    
    # Core hit-and-run strategy - refined
    if distance < strike_range:
        # In striking range - hit or run decision
        if my_attack_status > 0.3:
            # Currently attacking - prepare immediate retreat
            retreat_direction = random.random()
            if retreat_direction < 0.6:
                # Direct retreat
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
        
        # Evaluate strike opportunity
        if opponent_block_status > 0.4:
            # Opponent blocking - avoid engagement
            evasion_choice = unpredictability
            if evasion_choice < 0.4:
                # Quick retreat
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            elif evasion_choice < 0.7:
                # Jump over/away
                return 3  # Jump
            else:
                # Protected withdrawal
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        # Strike opportunity available
        if opponent_attack_status > 0.5:
            # Opponent attacking - counter or evade
            if health_advantage > 0 and unpredictability < 0.4:
                # Counter attack
                return 4  # Quick punch counter
            else:
                # Evasive maneuver
                if unpredictability < 0.5:
                    return 3  # Jump
                else:
                    if relative_pos > 0:
                        return 7  # Move left with block
                    else:
                        return 8  # Move right with block
        
        # Clean strike opportunity
        strike_decision = unpredictability
        if strike_decision < 0.45:
            return 4  # Fast punch for hit-and-run
        elif strike_decision < 0.7:
            return 5  # Kick for damage
        elif strike_decision < 0.85:
            # Feint - no strike, immediate retreat
            if relative_pos > 0:
                return 1  # Move away
            else:
                return 2  # Move away
        else:
            # Mix up with jump
            return 3  # Jump attack/evasion
    
    elif distance < danger_zone:
        # Danger zone - prioritize repositioning
        threat_assessment = opponent_attack_status + (1.0 - opponent_projectile_cooldown)
        
        if threat_assessment > 0.6:
            # High threat - defensive movement
            if relative_pos > 0:
                return 7  # Move left with block
            else:
                return 8  # Move right with block
        
        # Standard retreat from danger zone
        retreat_style = unpredictability
        if retreat_style < 0.5:
            # Direct retreat
            if relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
        elif retreat_style < 0.75:
            # Jump retreat
            return 3  # Jump away
        else:
            # Protected retreat
            if relative_pos > 0:
                return 7  # Move left with block
            else:
                return 8  # Move right with block
    
    elif distance < medium_range:
        # Medium range - tactical positioning
        # Assess opponent patterns and vulnerabilities
        opponent_vulnerable = (opponent_attack_status > 0.4 or 
                             opponent_projectile_cooldown > 0.4 or
                             momentum_factor > 0.5)
        
        if opponent_vulnerable and health_advantage > -0.15:
            # Setup for hit-and-run approach
            approach_style = unpredictability
            if approach_style < 0.3:
                # Direct approach
                if relative_pos > 0:
                    return 2  # Move right