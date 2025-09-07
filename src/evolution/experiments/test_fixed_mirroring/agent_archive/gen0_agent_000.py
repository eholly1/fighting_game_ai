"""
Evolutionary Agent: gen0_agent_000
==================================

Metadata:
{
  "generation": 0,
  "fitness": 96.86666666666183,
  "fighting_style": "aggressive",
  "win_rate": 0.0
}

Code Hash: 966ccde86e4afeb0
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22])) if len(state) > 22 else 0.5
    relative_pos = max(-1.0, min(1.0, state[23])) if len(state) > 23 else 0.0
    health_advantage = max(-1.0, min(1.0, state[25])) if len(state) > 25 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    opponent_health = state[12] if len(state) > 12 else 1.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    opponent_block_status = state[17] if len(state) > 17 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    opponent_attack_status = state[16] if len(state) > 16 else 0.0
    projectile_cooldown = state[10] if len(state) > 10 else 0.0
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Define aggressive tactical parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    aggression_base = 0.8
    health_panic_threshold = -0.4
    winning_threshold = 0.2
    pressure_distance = 0.35
    
    # Calculate dynamic aggression level based on health
    aggression_modifier = 1.0
    if health_advantage > winning_threshold:
        aggression_modifier = 1.3  # Even more aggressive when winning
    elif health_advantage < health_panic_threshold:
        aggression_modifier = 0.6  # Slightly less reckless when desperate
    
    final_aggression = aggression_base * aggression_modifier
    
    # Emergency defensive actions when critically low health
    if my_health < 0.2 and opponent_attack_status > 0.5:
        if distance < close_range:
            return 6  # Block immediate threat
        elif relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Aggressive pressure tactics - chase relentlessly
    chase_urgency = 1.0
    if distance > pressure_distance:
        chase_urgency = 1.5  # Increase urgency when opponent is far
    
    # Close range combat - maximize damage output
    if distance < close_range:
        # Counter opponent blocks with varied attacks
        if opponent_block_status > 0.5:
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 5  # Kick to break blocks
            elif attack_choice < 0.7:
                return 4  # Quick punch
            else:
                # Reposition for better attack angle
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        # When opponent is vulnerable, attack aggressively
        if opponent_attack_status < 0.3:
            if random.random() < 0.65:
                return 4  # Fast punch for pressure
            else:
                return 5  # Strong kick for damage
        
        # Mixed offense when trading blows
        combat_roll = random.random()
        if combat_roll < 0.45:
            return 4  # Punch
        elif combat_roll < 0.75:
            return 5  # Kick
        elif combat_roll < 0.85:
            return 6  # Brief block
        else:
            # Aggressive repositioning
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    # Medium range - aggressive positioning and setup
    elif distance < medium_range:
        # Height advantage considerations
        if abs(height_diff) > 0.3:
            if height_diff < -0.3:  # Opponent is higher
                return 3  # Jump to equalize
            
        # Aggressive approach based on opponent state
        if opponent_block_status > 0.6:
            # Opponent is defensive, charge in aggressively
            if relative_pos > 0:
                return 2  # Chase right
            else:
                return 1  # Chase left
        
        # Mix attacks and movement for unpredictable pressure
        medium_action = random.random()
        if medium_action < 0.35:
            # Direct approach
            if relative_pos > 0:
                return 2
            else:
                return 1
        elif medium_action < 0.55:
            return 4  # Aggressive punch approach
        elif medium_action < 0.7:
            # Projectile to force opponent action
            if projectile_cooldown < 0.3:
                return 9
            else:
                # Keep pressuring with movement
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        else:
            return 3  # Jump for position change
    
    # Far range - close distance while applying pressure
    else:
        # Projectile pressure when available
        if projectile_cooldown < 0.4 and random.random() < 0.6:
            return 9  # Ranged pressure
        
        # Aggressive advancement
        advance_method = random.random()
        if advance_method < 0.7:
            # Direct chase
            if relative_pos > 0:
                return 2
            else:
                return 1
        elif advance_method < 0.85:
            return 3  # Jump approach
        else:
            # Projectile if available, otherwise advance
            if projectile_cooldown < 0.5:
                return 9
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Fallback aggressive action
    if relative_pos > 0:
        return 2
    else:
        return 1