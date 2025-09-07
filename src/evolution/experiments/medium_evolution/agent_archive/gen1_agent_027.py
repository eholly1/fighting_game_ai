"""
Evolutionary Agent: gen1_agent_027
==================================

Metadata:
{
  "generation": 1,
  "fitness": 263.139999999993,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 9c89d3f2de647d8a
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
    height_diff = state[24]
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity_x = state[3]
    my_velocity_y = state[4]
    my_attack_status = state[5]
    my_block_status = state[6]
    opponent_velocity_x = state[14]
    opponent_velocity_y = state[15]
    opponent_attack_status = state[16]
    opponent_block_status = state[17]
    projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    
    # Advanced tactical ranges and thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.5
    critical_health = 0.2
    low_health = 0.35
    winning_threshold = 0.25
    losing_threshold = -0.25
    
    # Adaptive strategy parameters based on current situation
    base_aggression = 0.5
    situation_modifier = 0.0
    
    # Calculate dynamic aggression based on multiple factors
    if health_advantage > winning_threshold:
        situation_modifier += 0.3
    elif health_advantage < losing_threshold:
        situation_modifier -= 0.4
    
    if my_health < critical_health:
        situation_modifier -= 0.3
    elif my_health > 0.8:
        situation_modifier += 0.2
    
    current_aggression = max(0.1, min(0.9, base_aggression + situation_modifier))
    
    # Pattern tracking for adaptation
    opponent_seems_aggressive = opponent_attack_status > 0 or abs(opponent_velocity_x) > 0.1
    opponent_is_blocking = opponent_block_status > 0
    opponent_is_mobile = abs(opponent_velocity_x) > 0.05
    opponent_can_projectile = opponent_projectile_cooldown <= 0
    i_can_projectile = projectile_cooldown <= 0
    
    # Emergency survival mode
    if my_health < critical_health and health_advantage < -0.5:
        if distance < very_close_range and opponent_attack_status > 0:
            return 6  # Block immediate threat
        elif distance > far_range and i_can_projectile and not opponent_is_blocking:
            return 9  # Safe projectile
        elif distance < medium_range:
            # Create distance with defensive movement
            if relative_pos > 0:
                return 7 if random.random() < 0.7 else 1
            else:
                return 8 if random.random() < 0.7 else 2
        else:
            return 6  # Default defensive block
    
    # Very close range combat - high intensity
    if distance < very_close_range:
        # Counter-attack opportunities
        if opponent_attack_status > 0 and not my_attack_status:
            if health_advantage > 0 and random.random() < 0.6:
                return 5  # Counter with strong kick
            else:
                return 6  # Block first
        
        # Break through opponent's guard
        if opponent_is_blocking:
            choice = random.random()
            if choice < 0.25:
                return 5  # Strong kick to break guard
            elif choice < 0.4:
                return 3  # Jump over guard
            elif choice < 0.6:
                # Try to get around guard
                return 1 if relative_pos > 0 else 2
            else:
                return 4  # Quick punch
        
        # Aggressive very close combat
        if current_aggression > 0.6:
            attack_roll = random.random()
            if attack_roll < 0.4:
                return 4  # Fast punch
            elif attack_roll < 0.7:
                return 5  # Strong kick
            elif attack_roll < 0.85:
                return 3  # Jump attack setup
            else:
                return 6  # Defensive block
        
        # Defensive very close combat
        else:
            if random.random() < 0.5:
                return 6  # Block
            elif random.random() < 0.75:
                return 4  # Safe punch
            else:
                # Try to create space
                return 1 if relative_pos > 0 else 2
    
    # Close range combat tactics
    elif distance < close_range:
        # Adaptive responses to opponent behavior
        if opponent_is_blocking and opponent_is_mobile:
            # Opponent is mobile guard - predict movement
            if opponent_velocity_x > 0.05:  # Moving right
                return 2 if random.random() < 0.6 else 5  # Follow or kick
            elif opponent_velocity_x < -0.05:  # Moving left
                return 1 if random.random() < 0.6 else 5  # Follow or kick
            else:
                return 3  # Jump over stationary guard
        
        elif opponent_seems_aggressive and not opponent_is_blocking:
            # Counter aggressive opponent
            if health_advantage > 0:
                # Trade blows when winning
                return 5 if random.random() < 0.6 else 4
            else:
                # Defend when losing
                if random.random() < 0.6:
                    return 6
                else:
                    return 4  # Quick counter
        
        # Standard close combat based on health advantage
        if health_advantage > winning_threshold:
            # Aggressive pressure when winning
            combat_choice = random.random()
            if combat_choice < 0.35:
                return 4  # Punch
            elif combat_choice < 0.6:
                return 5  # Kick
            elif combat_choice < 0.75:
                return 3  # Jump attack
            elif combat_choice < 0.9:
                return 6  # Block
            else:
                return 1 if relative_pos > 0 else 2  # Reposition
        
        elif health_advantage < losing_threshold:
            # Cautious approach when losing
            if random.random() < 0.45:
                return 6  # Block more often
            elif random.random() < 0.7:
                return 4  # Safe punch
            elif random.random() < 0.85:
                return 5  # Kick
            else:
                return 3  # Jump
        
        # Balanced close combat
        else:
            balanced_choice = random.random()
            if balanced_choice < 0.3:
                return 4  # Punch
            elif balanced_choice < 0.55:
                return 5  # Kick
            elif balanced_choice < 0.75:
                return 6  # Block
            elif balanced_choice < 0.9:
                return 3  # Jump
            else:
                return 0  # Wait and observe
    
    # Medium range - critical positioning zone
    elif distance < medium_range:
        # Handle opponent projectile threat
        if opponent_can_projectile and distance > 0.25:
            evasion_choice = random.random()
            if evasion_choice < 0.3:
                return 3  # Jump over projectile
            elif evasion_choice < 0.6:
                return 6  # Block projectile
            else:
                # Approach with blocking movement
                if relative_pos > 0:
                    return 8