"""
Evolutionary Agent: gen1_agent_006
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: d8e9dc61686342c8
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
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract detailed fighter status
    my_health = state[1] if len(state) > 1 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_velocity_y = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[17] if len(state) > 17 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Enhanced defensive thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.5
    critical_health = 0.25
    low_health = 0.4
    good_health = 0.7
    
    # Threat assessment for defensive positioning
    incoming_threat = opponent_attack_status > 0.6 or abs(opponent_velocity_x) > 0.4
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    safe_to_counter = opponent_attack_status < 0.2 and my_block_status > 0.5
    
    # Critical defensive situations - maximum priority
    if my_health < critical_health or health_advantage < -0.7:
        # Survival mode - ultra defensive
        if distance < very_close_range and incoming_threat:
            return 6  # Emergency block
        elif distance < close_range:
            # Escape while defending
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        elif distance < medium_range and opponent_approaching:
            # Maintain distance defensively
            if relative_pos > 0:
                return 7  # Defensive movement left
            else:
                return 8  # Defensive movement right
        else:
            # Long range survival tactics
            if my_projectile_cooldown < 0.05:
                return 9  # Projectile to keep distance
            else:
                return 6  # Default defensive stance
    
    # Opponent prediction and counter-defense
    if opponent_attack_status > 0.8:
        # Opponent committed to attack - defensive response
        if distance < close_range:
            if my_block_status < 0.4:
                return 6  # Block the incoming attack
            elif safe_to_counter:
                # Perfect counter opportunity
                counter_type = random.random()
                if counter_type < 0.7:
                    return 4  # Quick counter punch
                else:
                    return 5  # Power counter kick
            else:
                return 6  # Stay blocking
        else:
            # Opponent attacking from range - prepare defense
            if opponent_projectile_cooldown < 0.1:
                return 6  # Block potential projectile
            else:
                # Position defensively
                if relative_pos > 0:
                    return 7  # Move with guard
                else:
                    return 8  # Move with guard
    
    # Adaptive range-based defensive tactics
    if distance < very_close_range:
        # Extreme close range - dangerous for defensive style
        if health_advantage > 0.4:
            # Significant lead - can afford calculated risks
            if opponent_block_status > 0.6:
                # Opponent blocking - try to break guard
                guard_break_attempt = random.random()
                if guard_break_attempt < 0.3:
                    return 5  # Heavy kick to break block
                elif guard_break_attempt < 0.6:
                    return 4  # Quick punch combination
                else:
                    return 6  # Stay defensive
            else:
                # Opponent not blocking - safe offense
                if my_attack_status < 0.3:
                    return 4  # Quick punch
                else:
                    return 6  # Return to defense
        else:
            # Even or losing - prioritize defense
            if incoming_threat:
                return 6  # Block
            elif safe_to_counter and random.random() < 0.4:
                return 4  # Careful counter
            else:
                return 6  # Default block
    
    elif distance < close_range:
        # Close range - key defensive decision zone
        if health_advantage > 0.2:
            # Slight advantage - controlled aggression
            if opponent_block_status > 0.5:
                # Opponent defending - probe carefully
                probe_action = random.random()
                if probe_action < 0.25:
                    return 4  # Test with punch
                elif probe_action < 0.4:
                    return 5  # Test with kick
                elif probe_action < 0.6:
                    # Reposition for better angle
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 6  # Stay defensive
            else:
                # Opponent open - calculated attack
                if my_attack_status < 0.4:
                    attack_choice = random.random()
                    if attack_choice < 0.6:
                        return 4  # Punch attack
                    else:
                        return 5  # Kick attack
                else:
                    return 6  # Recover to defense
        else:
            # Losing or even - defensive priority
            if opponent_approaching and incoming_threat:
                return 6  # Block approach
            elif safe_to_counter:
                # Defensive counter opportunity
                if random.random() < 0.5:
                    return 4  # Safe counter punch
                else:
                    return 6  # Stay defensive
            else:
                # Defensive positioning
                defensive_move = random.random()
                if defensive_move < 0.4:
                    return 6  # Block
                elif defensive_move < 0.7:
                    # Defensive repositioning
                    if abs(height_diff) > 0.2:
                        return 3  # Jump for position
                    elif relative_pos > 0:
                        return 7  # Move left with guard
                    else:
                        return 8  # Move right with guard
                else:
                    return 6  # Default block
    
    elif distance < medium_range:
        # Medium range - positioning and setup phase
        if health_advantage < -0.3:
            # Losing - defensive positioning
            if opponent_approaching:
                # Opponent closing in - defensive movement
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8