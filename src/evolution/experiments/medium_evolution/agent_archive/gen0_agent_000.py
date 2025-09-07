"""
Evolutionary Agent: gen0_agent_000
==================================

Metadata:
{
  "generation": 0,
  "fitness": 216.57133333333016,
  "fighting_style": "aggressive",
  "win_rate": 0.6666666666666666
}

Code Hash: 3a1814c740a866d7
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
    opponent_health = state[12] if len(state) > 12 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    opponent_attack_status = state[16] if len(state) > 16 else 0.0
    opponent_block_status = state[17] if len(state) > 17 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define aggressive strategic parameters
    close_threshold = 0.18
    medium_threshold = 0.35
    far_threshold = 0.6
    aggression_base = 0.8
    rush_threshold = 0.25
    desperate_threshold = -0.4
    dominant_threshold = 0.3
    
    # Calculate dynamic aggression level based on health and situation
    aggression_modifier = 1.0
    if health_advantage > dominant_threshold:
        aggression_modifier = 1.3  # Extra aggressive when winning
    elif health_advantage < desperate_threshold:
        aggression_modifier = 1.5  # All-out attack when desperate
    else:
        aggression_modifier = 1.1  # Always above baseline aggression
    
    final_aggression = min(1.0, aggression_base * aggression_modifier)
    
    # Emergency survival mode when critically low health
    if my_health < 0.15 and health_advantage < -0.6:
        if distance < close_threshold and opponent_attack_status > 0.5:
            return 6  # Block incoming attack
        elif distance > medium_threshold:
            return 9 if my_projectile_cooldown < 0.1 else 6
        else:
            # Desperate close-range all-out attack
            return 5 if random.random() < 0.7 else 4
    
    # Opponent is attacking - aggressive counter or block
    if opponent_attack_status > 0.5:
        if distance < close_threshold:
            if health_advantage > 0.2:
                # Counter-attack when strong
                return 4 if random.random() < 0.6 else 5
            else:
                # Block then counter
                if my_block_status < 0.3:
                    return 6
                else:
                    return 5  # Heavy counter after blocking
        elif distance < medium_threshold:
            # Rush in for counter attack
            if relative_pos > 0:
                return 2  # Move right to close distance
            else:
                return 1  # Move left to close distance
    
    # Opponent is blocking - aggressive pressure tactics
    if opponent_block_status > 0.5:
        if distance < close_threshold:
            # Mix up attacks to break guard
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 5  # Heavy kick to break block
            elif attack_choice < 0.7:
                return 4  # Quick punch
            else:
                return 3  # Jump attack to confuse
        elif distance < medium_threshold:
            # Close distance while they're blocking
            if relative_pos > 0:
                return 2
            else:
                return 1
        else:
            # Projectile pressure from range
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                # Close distance for pressure
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Close range aggressive combat
    if distance < close_threshold:
        # Height advantage considerations
        if abs(height_diff) > 0.3:
            if height_diff < -0.3:  # Opponent is above
                return 3  # Jump to match height
            else:  # We are above
                return 5  # Kick down at opponent
        
        # Aggressive close combat mixing
        if health_advantage > 0.1:
            # Winning - maintain pressure
            combat_roll = random.random()
            if combat_roll < 0.45:
                return 4  # Quick punch
            elif combat_roll < 0.75:
                return 5  # Power kick
            elif combat_roll < 0.9:
                return 3  # Jump attack for mix-up
            else:
                return 6  # Brief defensive moment
        else:
            # Even or losing - more calculated aggression
            combat_roll = random.random()
            if combat_roll < 0.35:
                return 4  # Punch
            elif combat_roll < 0.6:
                return 5  # Kick
            elif combat_roll < 0.8:
                return 6  # Block briefly
            else:
                return 3  # Jump mix-up
    
    # Medium range - aggressive positioning and setup
    elif distance < medium_threshold:
        # Check if we should rush in or use projectile
        if my_projectile_cooldown < 0.1 and random.random() < 0.3:
            return 9  # Occasional projectile to mix up approach
        
        # Aggressive approach with some tactical blocking
        if opponent_attack_status > 0.3:
            # Opponent might attack - approach with guard
            if relative_pos > 0:
                return 8  # Move right with block
            else:
                return 7  # Move left with block
        else:
            # Standard aggressive approach
            approach_style = random.random()
            if approach_style < 0.7:
                # Direct approach
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif approach_style < 0.85:
                # Jump approach for unpredictability
                return 3
            else:
                # Guarded approach
                if relative_pos > 0:
                    return 8
                else:
                    return 7
    
    # Far range - projectile pressure and aggressive closing
    elif distance < far_threshold:
        # Projectile available - use for pressure
        if my_projectile_cooldown < 0.1:
            projectile_chance = 0.6 if health_advantage > 0 else 0.4
            if random.random() < projectile_chance:
                return 9
        
        # Close distance aggressively
        movement_choice = random.random()
        if movement_choice < 0.6:
            # Direct approach
            if relative_pos > 0:
                return 2
            else:
                return 1
        elif movement_choice < 0.8:
            # Jump approach
            return 3
        else:
            # Cautious approach if opponent might have projectile ready
            if opponent_projectile_cooldown < 0.2:
                if relative_pos > 0:
                    return 8  # Approach with block
                else:
                    return 7
            else:
                if relative_pos > 0:
                    return 2
                else:
                    return 1