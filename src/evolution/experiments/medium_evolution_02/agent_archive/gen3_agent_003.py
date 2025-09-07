"""
Evolutionary Agent: gen3_agent_003
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 2553e566ce9dc4fc
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
    my_pos_x = state[0] if len(state) > 0 else 0.0
    my_health = state[1] if len(state) > 1 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_attack_cooldown = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_pos_x = state[11] if len(state) > 11 else 0.0
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_velocity_y = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[17] if len(state) > 17 else 0.0
    opponent_attack_cooldown = state[20] if len(state) > 20 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define enhanced defensive thresholds
    ultra_close = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.50
    critical_health = 0.25
    low_health = 0.45
    safe_health = 0.75
    
    # Calculate threat assessment
    incoming_threat = 0.0
    if opponent_attack_status > 0.6:
        incoming_threat += 0.4
    if abs(opponent_velocity_x) > 0.4 and distance < medium_range:
        incoming_threat += 0.3
    if opponent_attack_cooldown < 0.1 and distance < close_range:
        incoming_threat += 0.3
    
    # Opponent pattern analysis
    opponent_aggressive = (opponent_attack_status > 0.5 or 
                          abs(opponent_velocity_x) > 0.3 or 
                          opponent_attack_cooldown < 0.2)
    
    opponent_defensive = (opponent_block_status > 0.4 or 
                         (distance > medium_range and abs(opponent_velocity_x) < 0.2))
    
    # Adaptive defensive intensity based on situation
    base_defensive_chance = 0.6
    if health_advantage < -0.4:
        base_defensive_chance = 0.8
    elif health_advantage < -0.2:
        base_defensive_chance = 0.7
    elif health_advantage > 0.3:
        base_defensive_chance = 0.4
    elif health_advantage > 0.1:
        base_defensive_chance = 0.5
    
    # Crisis management - ultimate defensive priority
    if my_health < critical_health and health_advantage < -0.5:
        if distance < ultra_close and incoming_threat > 0.6:
            return 6  # Emergency block
        elif distance < close_range:
            if opponent_velocity_x > 0.3 and relative_pos < 0:
                return 7  # Escape left while blocking
            elif opponent_velocity_x < -0.3 and relative_pos > 0:
                return 8  # Escape right while blocking
            else:
                return 6  # Default crisis block
        elif distance < medium_range:
            # Create maximum distance while guarded
            if my_pos_x < 0.3:
                return 8  # Move right with block
            elif my_pos_x > 0.7:
                return 7  # Move left with block
            else:
                if relative_pos > 0:
                    return 7  # Move away left
                else:
                    return 8  # Move away right
        else:
            if my_projectile_cooldown < 0.1:
                return 9  # Desperate projectile
            else:
                return 6  # Wait defensively
    
    # Advanced threat response system
    if incoming_threat > 0.7:
        if distance < close_range:
            if my_block_status < 0.3:
                return 6  # Immediate block
            else:
                # Already blocking - consider counter
                if opponent_attack_status > 0.8 and random.random() < 0.3:
                    return 4  # Quick counter punch
                else:
                    return 6  # Continue blocking
        else:
            # Medium range threat - evasive blocking
            evasion_roll = random.random()
            if evasion_roll < 0.5:
                if relative_pos > 0:
                    return 7  # Defensive left movement
                else:
                    return 8  # Defensive right movement
            elif evasion_roll < 0.8:
                return 3  # Jump to avoid
            else:
                return 6  # Stand and block
    
    # Counter-attack opportunity detection
    if (opponent_attack_status > 0.7 and my_block_status > 0.5 and 
        distance < close_range and my_attack_cooldown < 0.1):
        counter_chance = 0.4
        if health_advantage > 0:
            counter_chance = 0.6
        elif health_advantage < -0.2:
            counter_chance = 0.25
        
        if random.random() < counter_chance:
            if opponent_health < 0.3:
                return 5  # Finishing kick
            else:
                return 4  # Safe counter punch
    
    # Range-specific defensive strategies
    if distance < ultra_close:
        # Ultra close - highest risk zone
        if health_advantage > 0.4:
            # Strong advantage - can be more aggressive
            if opponent_block_status > 0.6:
                # Opponent blocking - mix up attacks
                mix_roll = random.random()
                if mix_roll < 0.3:
                    return 4  # Quick punch
                elif mix_roll < 0.5:
                    return 5  # Power kick
                else:
                    return 6  # Reset with block
            else:
                attack_roll = random.random()
                if attack_roll < 0.6:
                    return 4  # Punch
                elif attack_roll < 0.8:
                    return 5  # Kick
                else:
                    return 6  # Stay defensive
        elif health_advantage > 0.1:
            # Slight advantage - measured aggression
            if opponent_attack_status < 0.3:
                action_roll = random.random()
                if action_roll < 0.4:
                    return 4  # Careful punch
                elif action_roll < 0.6:
                    return 5  # Careful kick
                else:
                    return 6  # Defensive block
            else:
                return 6  # Block opponent's attack