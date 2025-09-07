"""
Evolutionary Agent: gen0_agent_029
==================================

Metadata:
{
  "generation": 0,
  "fitness": 257.23999999999035,
  "fighting_style": "patient_defender",
  "win_rate": 0.5
}

Code Hash: 88cefdd3cc81b43c
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key game state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[3]))
    opponent_health = max(0.0, min(1.0, state[14]))
    my_position = state[1]
    opponent_position = state[12]
    
    # Extract attack and defense states
    my_attack_cooldown = max(0.0, state[8])
    opponent_attack_cooldown = max(0.0, state[19])
    my_projectile_cooldown = max(0.0, state[10])
    opponent_is_attacking = state[18] > 0.5
    
    # Define strategic thresholds for patient defender style
    close_range = 0.12
    medium_range = 0.28
    critical_health = 0.25
    safe_health = 0.6
    perfect_block_distance = 0.18
    
    # Emergency defensive actions when health is critical
    if my_health < critical_health:
        if opponent_is_attacking and distance < perfect_block_distance:
            return 6  # Block incoming attack
        
        if distance > 0.4 and my_projectile_cooldown < 0.1:
            return 9  # Safe projectile from distance
        
        # Defensive movement when critically low
        if relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Patient defense - wait for opponent mistakes
    if opponent_is_attacking:
        if distance < 0.2:
            return 6  # Perfect block timing
        elif distance < 0.35:
            # Create space while blocking
            if relative_pos > 0:
                return 7  # Block and move left
            else:
                return 8  # Block and move right
    
    # Counter-attack opportunities after successful defense
    if opponent_attack_cooldown > 0.3 and distance < close_range:
        # Opponent is vulnerable after attack
        if health_advantage > 0.2:
            return 5  # Power kick when ahead
        else:
            return 4  # Quick punch to stay safe
    
    # Health advantage adaptations
    if health_advantage > 0.4:
        # Winning decisively - more aggressive patient style
        if distance < close_range and my_attack_cooldown < 0.1:
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 4  # Quick punch
            elif attack_choice < 0.7:
                return 5  # Power kick
            else:
                return 6  # Maintain defensive stance
        
        elif distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Projectile pressure
    
    # Losing situation - ultra defensive
    elif health_advantage < -0.3:
        if distance < 0.15:
            return 6  # Block close attacks
        elif distance > 0.45:
            if my_projectile_cooldown < 0.1:
                return 9  # Long range harassment
            else:
                return 6  # Defensive stance
        else:
            # Medium range defensive movement
            if abs(my_position) > 0.7:  # Near wall
                if my_position > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                return 6  # Hold defensive position
    
    # Core patient defender logic by range
    if distance < close_range:
        # Close range - prioritize defense with calculated offense
        if opponent_attack_cooldown > 0.2:
            # Safe window to attack
            if random.random() < 0.6:
                return 4  # Quick punch
            else:
                return 5  # Power kick
        else:
            # Default to blocking in close range
            return 6
    
    elif distance < medium_range:
        # Medium range - positioning and timing
        if opponent_is_attacking:
            return 6  # Block incoming attacks
        
        # Controlled approach when safe
        if opponent_attack_cooldown > 0.4:
            if relative_pos > 0.1:
                return 2  # Move right toward opponent
            elif relative_pos < -0.1:
                return 1  # Move left toward opponent
            else:
                return 6  # Hold position defensively
        else:
            return 6  # Stay defensive
    
    else:
        # Long range - patient projectile game
        if my_projectile_cooldown < 0.1:
            return 9  # Projectile attack
        
        # Position for projectiles while staying defensive
        if abs(my_position) > 0.8:  # Too close to wall
            if my_position > 0:
                return 7  # Move away from right wall with block
            else:
                return 8  # Move away from left wall with block
        
        # Maintain distance advantage
        if distance < 0.4:
            if relative_pos > 0:
                return 7  # Back away left with defense
            else:
                return 8  # Back away right with defense
        else:
            return 6  # Patient defensive stance
    
    # Fallback to defensive stance
    return 6