"""
Evolutionary Agent: gen0_agent_001
==================================

Metadata:
{
  "generation": 0,
  "fitness": 167.22533333332805,
  "fighting_style": "defensive",
  "win_rate": 0.5
}

Code Hash: 35cb63d01f6de5b7
Serialization Version: 1.0
"""

# Agent Code:
import random
import numpy as np
import math

def get_action(state):
    # Defensive programming - validate state input
    if state is None or len(state) < 26:
        return 6  # Default to block if invalid state
    
    # Extract key strategic information with bounds checking
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract player and opponent status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_position_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[2] if len(state) > 2 else 0.0
    my_velocity_y = state[3] if len(state) > 3 else 0.0
    my_attack_status = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_position_x = state[11] if len(state) > 11 else 0.5
    opponent_velocity_x = state[13] if len(state) > 13 else 0.0
    opponent_attack_status = state[15] if len(state) > 15 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define strategic thresholds for defensive play
    close_combat_range = 0.12
    medium_range = 0.25
    safe_range = 0.45
    critical_health = 0.3
    comfortable_health_lead = 0.2
    
    # Defensive style parameters
    block_probability_base = 0.4
    counter_attack_window = 0.3
    retreat_threshold = 0.15
    projectile_spam_distance = 0.5
    
    # Emergency defensive actions when health is critical
    if my_health < critical_health:
        # Prioritize survival over aggression
        if distance < close_combat_range:
            # Very close - high chance to block or retreat
            if opponent_attack_status > 0.5:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking (retreat)
            else:
                return 8  # Move right while blocking (retreat)
        elif distance < medium_range:
            # Medium range - create distance
            if relative_pos > 0:
                return 7  # Retreat left with block
            else:
                return 8  # Retreat right with block
        else:
            # Far range - use projectiles to chip damage
            if my_projectile_cooldown < 0.1:
                return 9  # Safe projectile
            else:
                return 6  # Block while waiting for cooldown
    
    # Comfortable health lead - maintain distance and control
    if health_advantage > comfortable_health_lead:
        if distance > safe_range:
            # Very safe - projectile spam
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile attack
            else:
                # Move to maintain optimal projectile distance
                if relative_pos > 0:
                    return 2  # Move right to maintain distance
                else:
                    return 1  # Move left to maintain distance
        elif distance > medium_range:
            # Medium-far range - control space
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile
            elif random.random() < 0.3:
                return 6  # Occasional block to stay defensive
            else:
                # Maintain spacing
                if opponent_velocity_x > 0.1 and relative_pos < 0:
                    return 1  # Move away from approaching opponent
                elif opponent_velocity_x < -0.1 and relative_pos > 0:
                    return 2  # Move away from approaching opponent
                else:
                    return 0  # Idle and observe
        else:
            # Close range with health advantage - careful aggression
            if opponent_attack_status > 0.5:
                return 6  # Block opponent's attack
            elif random.random() < 0.6:
                return 6  # Stay defensive even with advantage
            else:
                # Controlled counter-attack
                if random.random() < 0.7:
                    return 4  # Quick punch
                else:
                    return 5  # Stronger kick
    
    # Standard defensive play - balanced approach
    if distance < close_combat_range:
        # Close combat - high blocking priority
        if opponent_attack_status > 0.3:
            # Opponent is attacking - definitely block
            return 6
        elif my_block_status > 0.5:
            # Already blocking - look for counter opportunity
            if random.random() < counter_attack_window:
                if random.random() < 0.8:
                    return 4  # Quick counter punch
                else:
                    return 5  # Counter kick
            else:
                return 6  # Continue blocking
        else:
            # Not currently blocking - decide based on situation
            block_chance = block_probability_base
            
            # Increase block chance based on opponent aggression
            if opponent_velocity_x != 0:
                block_chance += 0.2
            if distance < 0.08:
                block_chance += 0.3
            
            if random.random() < block_chance:
                return 6  # Block
            else:
                # Counter-attack opportunity
                if health_advantage > 0:
                    # Slight advantage - more aggressive counter
                    if random.random() < 0.6:
                        return 4  # Punch
                    else:
                        return 5  # Kick
                else:
                    # No advantage - quick counter only
                    return 4  # Safe punch
    
    elif distance < medium_range:
        # Medium range - positioning and spacing
        if opponent_attack_status > 0.5:
            # Opponent attacking - block while moving
            if relative_pos > 0:
                return 7  # Block and move left
            else:
                return 8  # Block and move right
        elif opponent_velocity_x > 0.2:
            # Opponent rushing - prepare defense
            if relative_pos < 0:  # Opponent coming from left
                if random.random() < 0.7:
                    return 8  # Block and move right (away)
                else:
                    return 6  # Stand and block
            else:  # Opponent coming from right
                if random.random() < 0.7:
                    return 7  # Block and move left (away)
                else:
                    return 6  # Stand and block
        else:
            # Neutral medium range - control space
            if my_projectile_cooldown < 0.3:
                if random.random() < 0.4:
                    return 9  # Projectile attack
                else:
                    return 6  # Block (stay defensive)
            else:
                # No projectile available - positioning
                if random.random() < 0.5:
                    return 6  # Block and wait
                else:
                    # Adjust position slightly
                    if my_position_x < 0.3:  # Near left edge
                        return 2  # Move right
                    elif my_position_x > 0.7:  # Near right edge
                        return 1  # Move left