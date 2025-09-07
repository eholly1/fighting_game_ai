"""
Evolutionary Agent: gen0_agent_006
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "counter_puncher",
  "win_rate": 0.5
}

Code Hash: 704c01c003284b3c
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
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[2] if len(state) > 2 else 0.0
    my_velocity_y = state[3] if len(state) > 3 else 0.0
    my_attack_status = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[13] if len(state) > 13 else 0.0
    opp_velocity_y = state[14] if len(state) > 14 else 0.0
    opp_attack_status = state[15] if len(state) > 15 else 0.0
    opp_block_status = state[16] if len(state) > 16 else 0.0
    
    # Define tactical ranges and thresholds
    close_range = 0.15
    medium_range = 0.35
    far_range = 0.6
    critical_health = 0.3
    dominant_health = 0.4
    
    # Counter-puncher style: patience and reaction parameters
    patience_factor = 0.7
    counter_window = 0.8
    defensive_priority = 0.6
    
    # Analyze opponent behavior patterns
    opponent_aggressive = opp_attack_status > 0.5 or (opp_velocity_x != 0 and distance < medium_range)
    opponent_retreating = (relative_pos > 0 and opp_velocity_x < -0.1) or (relative_pos < 0 and opp_velocity_x > 0.1)
    opponent_blocking = opp_block_status > 0.5
    opponent_jumping = abs(opp_velocity_y) > 0.1
    
    # Calculate positioning factors
    near_edge = my_x_pos < 0.15 or my_x_pos > 0.85
    opponent_near_edge = opp_x_pos < 0.15 or opp_x_pos > 0.85
    cornered = near_edge and ((my_x_pos < 0.15 and relative_pos > 0) or (my_x_pos > 0.85 and relative_pos < 0))
    opponent_cornered = opponent_near_edge and ((opp_x_pos < 0.15 and relative_pos < 0) or (opp_x_pos > 0.85 and relative_pos > 0))
    
    # Emergency defensive situations
    if my_health < critical_health and health_advantage < -0.5:
        if distance < close_range and opponent_aggressive:
            # Desperate escape attempt
            if cornered:
                return 3  # Jump to escape
            elif relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            return 6  # Block and wait for opening
        else:
            if my_projectile_cooldown < 0.3:
                return 9  # Long range projectile
            else:
                return 6  # Block while cooldown recovers
    
    # Dominant position exploitation
    if health_advantage > dominant_health and opp_health < critical_health:
        if opponent_cornered and distance < medium_range:
            # Aggressive finish
            if distance < close_range:
                return 5 if random.random() < 0.7 else 4  # Prefer kicks for finish
            else:
                # Close distance for final assault
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        elif distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Projectile pressure
    
    # Counter-puncher core logic: React to opponent actions
    if opponent_aggressive and distance < close_range:
        # Opponent is attacking in close range - prime counter opportunity
        if my_block_status > 0.3:
            # Already blocking, look for counter window
            if random.random() < counter_window:
                return 4  # Quick counter punch
            else:
                return 6  # Continue blocking
        else:
            # Need to defend first
            if opponent_jumping:
                return 4  # Anti-air punch
            else:
                return 6  # Block incoming attack
    
    # Opponent retreating - controlled pressure
    if opponent_retreating and distance < far_range:
        if distance > medium_range:
            # Safe to apply pressure
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        elif distance > close_range:
            # Medium range - prepare for engagement
            if my_projectile_cooldown < 0.4 and random.random() < 0.4:
                return 9  # Projectile to cut off retreat
            else:
                # Conservative advance
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Range-based tactical decisions
    if distance < close_range:
        # Close combat - counter-puncher waits for openings
        if opponent_blocking:
            # Opponent defensive, look for mix-up opportunity
            if random.random() < 0.3:
                return 5  # Kick to break guard
            elif random.random() < 0.5:
                # Create space and reset
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                return 0  # Patience - wait for opponent to act
        
        elif opp_attack_status > 0.3:
            # Opponent attacking - counter opportunity
            if my_block_status < 0.2:
                return 6  # Block first
            else:
                return 4  # Counter punch
        
        else:
            # Neutral close range
            if health_advantage > 0.2:
                # Slight advantage, can be more aggressive
                return 4 if random.random() < 0.6 else 5
            else:
                # Stay defensive
                if random.random() < patience_factor:
                    return 0  # Wait
                else:
                    return 6  # Block
    
    elif distance < medium_range:
        # Medium range - positioning and setup
        if opponent_cornered:
            # Press advantage
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        
        elif cornered:
            # Escape corner
            if relative_pos > 0:
                return 1  # Move left to escape
            else:
                return 2  # Move right to escape
        
        elif opponent_aggressive:
            # Opponent coming forward - prepare defense
            if random.random() < defensive_priority:
                return