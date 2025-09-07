"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_017
Rank: 80/100
Generation: 0
Fighting Style: hit_and_run

Performance Metrics:
- Fitness: 180.42
- Win Rate: 0.0%
- Average Reward: 180.42

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
    my_velocity_x = state[3]
    my_velocity_y = state[4]
    my_attack_cooldown = state[7]
    my_block_status = state[8]
    my_projectile_cooldown = state[9]
    
    # Extract opponent information
    opp_health = state[12] if state[12] >= 0 else 0.5
    opp_velocity_x = state[14]
    opp_velocity_y = state[15]
    opp_attack_status = state[16]
    opp_block_status = state[19]
    opp_projectile_cooldown = state[20]
    
    # Define tactical parameters for hit-and-run style
    close_range = 0.12
    strike_range = 0.18
    medium_range = 0.35
    safe_range = 0.45
    
    # Hit-and-run aggression factors
    retreat_threshold = 0.2
    strike_confidence = 0.3
    health_panic_level = -0.4
    
    # Emergency defensive behavior when health is critical
    if health_advantage < health_panic_level or my_health < 0.2:
        if distance < retreat_threshold:
            # Immediate retreat with blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            # Keep retreating to safe distance
            if relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
        else:
            # Use projectiles from safe distance
            if my_projectile_cooldown <= 0:
                return 9  # Projectile
            else:
                return 6  # Block while waiting
    
    # Detect if opponent is attacking or about to attack
    opponent_threatening = (opp_attack_status > 0.5 or 
                          (distance < strike_range and opp_velocity_x != 0))
    
    # Hit-and-run strike opportunities
    if distance <= strike_range and not opponent_threatening:
        # Perfect striking distance and opponent seems vulnerable
        if my_attack_cooldown <= 0:
            # Quick strike decision based on positioning
            if distance <= close_range:
                # Very close - mix up attacks
                if random.random() < 0.4:
                    return 4  # Quick punch
                elif random.random() < 0.7:
                    return 5  # Stronger kick
                else:
                    # Immediate retreat after considering attack
                    if relative_pos > 0:
                        return 1  # Move left to retreat
                    else:
                        return 2  # Move right to retreat
            else:
                # At strike range - favor quick attacks
                if random.random() < 0.6:
                    return 4  # Quick punch for hit-and-run
                else:
                    return 5  # Kick when confident
        else:
            # Attack on cooldown - retreat immediately
            if relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
    
    # Immediate threat response - opponent is attacking
    if opponent_threatening and distance < medium_range:
        if distance < close_range:
            # Very close threat - block or retreat with block
            if random.random() < 0.6:
                return 6  # Pure block
            else:
                # Retreat while blocking
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
        else:
            # Medium threat - evasive movement
            if relative_pos > 0:
                return 1  # Move left to evade
            else:
                return 2  # Move right to evade
    
    # Hit-and-run positioning logic
    if distance > safe_range:
        # Too far - need to close in for strike opportunity
        if my_projectile_cooldown <= 0 and random.random() < 0.4:
            return 9  # Projectile while closing
        else:
            # Move toward opponent
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
    
    elif distance > medium_range:
        # Good medium range for projectiles and positioning
        if my_projectile_cooldown <= 0 and random.random() < 0.6:
            return 9  # Projectile attack
        elif health_advantage > strike_confidence:
            # Winning - can afford to be more aggressive
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        else:
            # Maintain distance while looking for opportunities
            if random.random() < 0.3:
                if relative_pos > 0:
                    return 2  # Slight advance
                else:
                    return 1  # Slight advance
            else:
                return 0  # Wait for better opportunity
    
    elif distance > strike_range:
        # Approaching strike range - prepare for hit-and-run
        if opp_block_status > 0.5:
            # Opponent is blocking - wait or reposition
            if random.random() < 0.4:
                return 0  # Wait for opening
            else:
                # Try to get better angle
                if relative_pos > 0:
                    return 1  # Move left for angle
                else:
                    return 2  # Move right for angle
        elif health_advantage > 0:
            # Winning and in good position - advance for strike
            if relative_pos > 0:
                return 2  # Move right for attack
            else:
                return 1  # Move left for attack
        else:
            # Even or losing - be more cautious
            if my_projectile_cooldown <= 0:
                return 9  # Projectile
            else:
                return 0  # Wait
    
    else:
        # Within strike range - hit-and-run execution
        if my_attack_cooldown <= 0 and not opp_block_status > 0.5:
            # Can attack and opponent not blocking
            if random.random() < 0.7:
                return 4  # Quick punch for hit-and-run
            else:
                return 5  # Kick when feeling confident
        else:
            # Can't attack effectively - retreat
            if distance < close_range:
                # Too close - retreat with urgency
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                # Maintain distance
                if random.random() < 0.5:
                    return 6  # Block while repositioning
                else:
                    return 0  # Wait for cooldown
    
    # Adaptive behavior based on opponent patterns
    if opp_velocity_x == 0 and distance < medium_range:
        # Opponent is stationary - good strike opportunity
        if my_attack_cooldown <= 0 and distance <= strike_range:
            return 4  # Quick strike
        elif distance > strike_range:
            # Close in for strike
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
    
    # Height advantage