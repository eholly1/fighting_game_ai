"""
Evolutionary Agent: gen1_agent_005
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: a69ec409b046aedc
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[3] if len(state) > 3 else 1.0))
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_block_status = state[7] if len(state) > 7 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[14] if len(state) > 14 else 1.0))
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[17] if len(state) > 17 else 0.0
    opponent_block_status = state[18] if len(state) > 18 else 0.0
    opponent_projectile_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Hybrid fighter strategic parameters
    close_range = 0.13
    medium_range = 0.27
    far_range = 0.42
    critical_health = 0.25
    winning_threshold = 0.25
    losing_threshold = -0.25
    
    # Dynamic aggression based on situation
    base_aggression = 0.6
    defensive_threshold = 0.4
    offensive_threshold = 0.75
    
    # Adaptive behavior counters (simulated memory through randomness patterns)
    situation_seed = int((distance * 100) + (health_advantage * 50) + (my_health * 25))
    random.seed(situation_seed)
    adaptation_factor = random.random()
    random.seed()  # Reset to normal randomness
    
    # Critical health emergency protocols
    if my_health < critical_health:
        if distance < close_range:
            if opponent_attack_status > 0.6:
                return 6  # Emergency block
            elif health_advantage < -0.5:
                # Desperate escape
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
            else:
                # Last stand aggression
                if random.random() < 0.7:
                    return 5  # Heavy kick for maximum damage
                else:
                    return 4  # Quick punch
        elif distance < medium_range:
            if my_projectile_cooldown < 0.1:
                return 9  # Keep distance with projectile
            else:
                return 6  # Defensive block
        else:
            if my_projectile_cooldown < 0.1:
                return 9  # Long range projectile
            else:
                # Maintain distance
                if abs(relative_pos) > 0.1:
                    return 6  # Block and wait
                else:
                    return 0  # Idle to maintain position
    
    # Opponent pattern recognition and counter-adaptation
    if opponent_attack_status > 0.8:
        # Opponent is highly aggressive
        if distance < close_range:
            if my_block_status < 0.3:
                return 6  # Block the aggression
            else:
                # Counter after successful block
                if adaptation_factor < 0.6:
                    return 4  # Quick counter punch
                else:
                    return 5  # Power counter kick
        else:
            # Keep distance from aggressive opponent
            if relative_pos > 0:
                return 7  # Move away with guard
            else:
                return 8  # Move away with guard
    
    elif opponent_block_status > 0.7:
        # Opponent is very defensive
        if distance < close_range:
            # Guard break tactics
            if adaptation_factor < 0.3:
                return 5  # Heavy kick to break guard
            elif adaptation_factor < 0.6:
                return 3  # Jump for overhead
            else:
                if my_projectile_cooldown < 0.1:
                    return 9  # Point blank projectile
                else:
                    return 4  # Pressure with punches
        elif distance < medium_range:
            # Approach defensive opponent
            if my_projectile_cooldown < 0.1 and random.random() < 0.4:
                return 9  # Projectile to force movement
            else:
                if relative_pos > 0:
                    return 2  # Advance right
                else:
                    return 1  # Advance left
    
    # Range-based hybrid tactics
    if distance < close_range:
        # Close range - balanced offense and defense
        current_aggression = base_aggression
        
        # Adjust aggression based on health advantage
        if health_advantage > winning_threshold:
            current_aggression = offensive_threshold
        elif health_advantage < losing_threshold:
            current_aggression = defensive_threshold
        
        # Factor in opponent state
        if opponent_attack_status > 0.5:
            current_aggression *= 0.7  # More defensive against attacking opponent
        elif opponent_block_status > 0.5:
            current_aggression *= 1.3  # More aggressive against blocking opponent
        
        if random.random() < current_aggression:
            # Offensive actions
            if opponent_block_status > 0.6:
                # Guard break options
                guard_break_choice = random.random()
                if guard_break_choice < 0.4:
                    return 5  # Heavy kick
                elif guard_break_choice < 0.7:
                    return 3  # Jump attack
                else:
                    return 4  # Pressure punch
            else:
                # Normal attacks
                attack_choice = random.random()
                if attack_choice < 0.55:
                    return 4  # Quick punch
                else:
                    return 5  # Strong kick
        else:
            # Defensive actions
            if opponent_attack_status > 0.4:
                return 6  # Block incoming attack
            else:
                # Defensive positioning
                positioning_choice = random.random()
                if positioning_choice < 0.4:
                    return 6  # Maintain guard
                elif positioning_choice < 0.7:
                    return 3  # Jump for repositioning
                else:
                    # Create slight distance
                    if relative_pos > 0:
                        return 7  # Move left with guard
                    else:
                        return 8  # Move right with guard
    
    elif distance < medium_range:
        # Medium range - positioning and setup phase
        if health_advantage > winning_threshold:
            # Winning - controlled aggression
            if opponent_projectile_cooldown < 0.1 and random.random() < 0.3:
                # Opponent might projectile, approach with guard
                if relative_pos > 0:
                    return 8  # Guarded advance right
                else:
                    return 7  # Guarded advance left
            else:
                # Safe to advance
                advance_choice = random.random()
                if advance_choice < 0.5:
                    if relative_pos > 0:
                        return 2  # Direct advance right
                    else:
                        return 1  # Direct advance left