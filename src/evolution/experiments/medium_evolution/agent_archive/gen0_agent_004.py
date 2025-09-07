"""
Evolutionary Agent: gen0_agent_004
==================================

Metadata:
{
  "generation": 0,
  "fitness": 261.2399999999912,
  "fighting_style": "adaptive",
  "win_rate": 0.5
}

Code Hash: a9ab904eb2e495f9
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
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_block_status = state[6]
    opponent_block_status = state[17]
    my_attack_status = state[5]
    opponent_attack_status = state[16]
    projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    
    # Define tactical ranges and thresholds
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.25
    winning_threshold = 0.2
    losing_threshold = -0.2
    
    # Adaptive personality factors based on current situation
    aggression_base = 0.5
    if health_advantage > winning_threshold:
        aggression_base = 0.7  # More aggressive when winning
    elif health_advantage < losing_threshold:
        aggression_base = 0.3  # More defensive when losing
    
    # Emergency defensive mode - critical health
    if my_health < critical_health and health_advantage < -0.4:
        if distance < close_range and opponent_attack_status > 0:
            return 6  # Block incoming attack
        elif distance > far_range and projectile_cooldown <= 0:
            return 9  # Try projectile from safe distance
        elif distance < medium_range:
            # Try to create distance while blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            return 6  # Default to blocking
    
    # Opponent behavior analysis for adaptation
    opponent_is_aggressive = opponent_attack_status > 0
    opponent_is_blocking = opponent_block_status > 0
    opponent_has_projectile = opponent_projectile_cooldown <= 0
    
    # Close range combat tactics
    if distance < close_range:
        # If opponent is blocking, try to mix up or reposition
        if opponent_is_blocking:
            if random.random() < 0.4:
                # Try to get behind opponent
                if relative_pos > 0:
                    return 1  # Move left to get around
                else:
                    return 2  # Move right to get around
            elif random.random() < 0.3:
                return 3  # Jump to confuse
            else:
                # Try strong attack to break guard
                return 5  # Kick
        
        # If opponent is attacking, defend or counter
        elif opponent_is_aggressive:
            if health_advantage < 0:
                return 6  # Block when losing
            else:
                # Counter attack when winning
                if random.random() < 0.6:
                    return 4  # Quick punch
                else:
                    return 5  # Strong kick
        
        # Neutral close combat
        else:
            if health_advantage > winning_threshold:
                # Aggressive when winning
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Punch
                elif attack_choice < 0.8:
                    return 5  # Kick
                else:
                    return 3  # Jump attack setup
            elif health_advantage < losing_threshold:
                # More cautious when losing
                if random.random() < 0.4:
                    return 6  # Block
                elif random.random() < 0.7:
                    return 4  # Safe punch
                else:
                    return 5  # Kick
            else:
                # Balanced approach
                choice = random.random()
                if choice < 0.4:
                    return 4  # Punch
                elif choice < 0.65:
                    return 5  # Kick
                elif choice < 0.8:
                    return 6  # Block
                else:
                    return 3  # Jump
    
    # Medium range positioning and tactics
    elif distance < medium_range:
        # This is the key tactical range for positioning
        
        # If opponent has projectile ready, be more careful
        if opponent_has_projectile and distance > 0.2:
            if random.random() < 0.6:
                # Move unpredictably to avoid projectile
                if random.random() < 0.3:
                    return 3  # Jump
                elif relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                return 6  # Block projectile
        
        # Aggressive positioning when winning
        if health_advantage > winning_threshold:
            if relative_pos > 0.1:
                return 2  # Move right toward opponent
            elif relative_pos < -0.1:
                return 1  # Move left toward opponent
            else:
                # Close enough to pressure
                if random.random() < 0.4:
                    return 4  # Punch
                elif random.random() < 0.7:
                    return 5  # Kick
                else:
                    return 3  # Jump in
        
        # Defensive positioning when losing
        elif health_advantage < losing_threshold:
            if opponent_is_aggressive:
                return 6  # Block
            elif projectile_cooldown <= 0:
                return 9  # Projectile
            else:
                # Try to maintain distance
                if relative_pos > 0:
                    return 7  # Move left with guard
                else:
                    return 8  # Move right with guard
        
        # Neutral medium range
        else:
            choice = random.random()
            if choice < 0.3:
                # Close distance
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif choice < 0.5 and projectile_cooldown <= 0:
                return 9  # Projectile
            elif choice < 0.7:
                return 3  # Jump for positioning
            elif choice < 0.85:
                return 6  # Block
            else:
                return 0  # Wait and observe
    
    # Far range tactics
    elif distance < far_range:
        # Projectile range - key for ranged combat
        
        # If we can use projectile
        if projectile_cooldown <= 0:
            # Don't always use projectile - be unpredictable
            if random.random() < 0.7:
                return 9  # Projectile attack
        
        # If opponent might have projectile, be defensive
        if opponent_has_projectile:
            if random.random() < 0.4:
                return 6  # Block
            elif random.random() < 0.6:
                return 3  # Jump to avoid
            else:
                # Try to close distance safely
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
        
        # Positioning based on health advantage
        if health_advantage > winning_threshold:
            # Winning - can afford to close distance
            if relative_pos > 0.1:
                return 2  # Move right
            elif relative_pos < -0.1:
                return 1  # Move left
            else:
                return 3  # Jump in
        
        elif health_advantage < losing_threshold:
            # Losing - try to keep distance and poke
            if projectile_cooldown <= 0:
                return