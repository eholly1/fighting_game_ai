"""
Evolutionary Agent: gen4_agent_004
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 5a6528dce9ac9b1e
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
    
    # Extract my fighter states
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_pos_x = state[2] if len(state) > 2 and abs(state[2]) <= 1.0 else 0.0
    my_velocity_x = state[4] if len(state) > 4 and abs(state[4]) <= 2.0 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[9] if len(state) > 9 else 0.0
    
    # Extract opponent states
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = state[13] if len(state) > 13 and abs(state[13]) <= 1.0 else 0.0
    opponent_velocity_x = state[15] if len(state) > 15 and abs(state[15]) <= 2.0 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = state[20] if len(state) > 20 else 0.0
    
    # Define hybrid fighter parameters
    close_threshold = 0.15
    medium_threshold = 0.35
    far_threshold = 0.6
    
    critical_health = 0.25
    low_health = 0.4
    healthy_threshold = 0.65
    
    corner_threshold = 0.75
    high_aggression = 0.7
    defensive_threshold = 0.4
    
    # Analyze current tactical situation
    range_close = distance < close_threshold
    range_medium = close_threshold <= distance < medium_threshold
    range_far = medium_threshold <= distance < far_threshold
    range_very_far = distance >= far_threshold
    
    health_critical = my_health < critical_health
    health_low = my_health < low_health
    health_good = my_health > healthy_threshold
    
    winning_decisively = health_advantage > 0.3
    winning_slightly = 0.1 < health_advantage <= 0.3
    losing_slightly = -0.3 <= health_advantage < -0.1
    losing_badly = health_advantage < -0.3
    
    # Opponent analysis
    opponent_attacking = opponent_attack_status > 0.1
    opponent_blocking = opponent_block_status > 0.1
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # My capabilities
    can_attack = my_attack_status < 0.05
    can_projectile = my_projectile_cooldown < 0.1
    am_cornered = abs(my_pos_x) > corner_threshold
    opponent_cornered = abs(opponent_pos_x) > corner_threshold
    
    # Movement directions
    move_toward = 2 if relative_pos > 0 else 1
    move_away = 1 if relative_pos > 0 else 2
    block_toward = 8 if relative_pos > 0 else 7
    block_away = 7 if relative_pos > 0 else 8
    
    # Emergency survival protocols
    if health_critical:
        if opponent_attacking and range_close:
            return 6  # Emergency block
        elif losing_badly and range_very_far:
            if can_projectile:
                return 9  # Desperate projectile
            else:
                return move_away  # Create more distance
        elif range_close and not can_attack:
            return block_away  # Block while retreating
    
    # Adaptive strategy based on health dynamics
    if losing_badly:
        # Defensive-focused hybrid approach
        if range_very_far:
            if can_projectile and not opponent_blocking:
                return 9  # Safe projectile damage
            elif opponent_advancing:
                return move_away  # Maintain distance
            else:
                return 6  # Defensive stance
        
        elif range_far:
            if opponent_attacking:
                return 6  # Block incoming
            elif can_projectile and random.random() < 0.6:
                return 9  # Projectile pressure
            else:
                return block_toward  # Cautious advance
        
        elif range_medium:
            if opponent_attacking:
                return 6  # Block first priority
            elif opponent_blocking:
                return block_toward  # Advance carefully
            elif can_projectile and random.random() < 0.4:
                return 9  # Medium range projectile
            else:
                return 6  # Default to defense
        
        else:  # Close range
            if opponent_attacking:
                return 6  # Must block
            elif can_attack and not opponent_blocking and random.random() < 0.5:
                return 4  # Quick counter
            else:
                return block_away  # Retreat while blocking
    
    elif losing_slightly:
        # Balanced hybrid with slight defensive bias
        if range_very_far:
            if can_projectile:
                return 9  # Projectile to chip damage
            else:
                return move_toward  # Close distance
        
        elif range_far:
            if opponent_blocking and can_projectile:
                return 9  # Pressure with projectile
            elif opponent_retreating:
                return move_toward  # Pursue
            else:
                action_choice = random.random()
                if action_choice < 0.4:
                    return move_toward
                elif action_choice < 0.7 and can_projectile:
                    return 9
                else:
                    return 6  # Defensive option
        
        elif range_medium:
            if opponent_attacking:
                return 6  # Block attacks
            elif opponent_cornered:
                return move_toward  # Press advantage
            else:
                choice = random.random()
                if choice < 0.5:
                    return move_toward  # Advance
                elif choice < 0.7 and can_projectile:
                    return 9  # Projectile
                else:
                    return 6  # Block
        
        else:  # Close range
            if opponent_attacking:
                return 6 if random.random() < 0.7 else 4  # Mostly block, some counter
            elif can_attack:
                return 4 if random.random() < 0.6 else 5  # Mixed attacks
            else:
                return 6  # Block when can't attack
    
    elif winning_slightly:
        # Balanced hybrid with slight aggressive bias
        if range_close:
            if opponent_blocking:
                # Mix attacks to break guard
                choice = random.random()
                if choice < 0.4:
                    return 5  # Kick