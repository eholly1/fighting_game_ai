"""
Evolutionary Agent: gen0_agent_000
==================================

Metadata:
{
  "generation": 0,
  "fitness": 293.99999999999835,
  "fighting_style": "aggressive",
  "win_rate": 0.5
}

Code Hash: a67c957e017e3aa0
Serialization Version: 1.0
"""

# Agent Code:
import random
import numpy as np
import math

def get_action(state):
    # Extract and validate key game state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract player status information
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = state[0]
    my_y_pos = state[1]
    my_x_velocity = state[3]
    my_y_velocity = state[4]
    my_attack_cooldown = max(0.0, state[5])
    my_block_status = state[6]
    my_projectile_cooldown = max(0.0, state[10])
    
    # Extract opponent status information
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_pos = state[11]
    opp_y_pos = state[12]
    opp_x_velocity = state[14]
    opp_y_velocity = state[15]
    opp_attack_cooldown = max(0.0, state[16])
    opp_block_status = state[17]
    opp_projectile_cooldown = max(0.0, state[21])
    
    # Height difference for aerial tactics
    height_diff = state[24]
    
    # Aggressive fighting style parameters
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    aggression_base = 0.85
    chase_threshold = 0.6
    attack_mix_chance = 0.75
    
    # Dynamic aggression based on health advantage
    current_aggression = aggression_base
    if health_advantage > 0.2:
        current_aggression = min(0.95, aggression_base + 0.1)
    elif health_advantage < -0.4:
        current_aggression = max(0.6, aggression_base - 0.25)
    
    # Emergency defensive behavior when critically low health
    if my_health < 0.15 and health_advantage < -0.5:
        if distance < close_range and opp_attack_cooldown < 0.1:
            return 6  # Block incoming attack
        elif distance > medium_range:
            return 9  # Desperate projectile attempt
        else:
            # Try to create distance while blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
    
    # Opponent is attacking or about to attack - aggressive counter
    if opp_attack_cooldown < 0.15 and distance < close_range:
        if random.random() < 0.3:
            return 6  # Occasional block
        else:
            # Aggressive counter-attack
            if random.random() < 0.6:
                return 4  # Quick punch counter
            else:
                return 5  # Power kick counter
    
    # Close range aggressive combat
    if distance < close_range:
        # Can't attack due to cooldown
        if my_attack_cooldown > 0.2:
            if opp_attack_cooldown < 0.1:
                return 6  # Block while cooling down
            else:
                # Aggressive positioning while cooling down
                if abs(relative_pos) > 0.1:
                    if relative_pos > 0:
                        return 2  # Chase right
                    else:
                        return 1  # Chase left
                else:
                    return 0  # Wait briefly
        
        # Opponent is blocking - mix up attacks aggressively
        if opp_block_status > 0.5:
            attack_choice = random.random()
            if attack_choice < 0.35:
                return 5  # Heavy kick to break guard
            elif attack_choice < 0.65:
                return 4  # Quick punch
            else:
                # Try to reposition for attack angle
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        # Normal close combat - aggressive attack patterns
        if random.random() < attack_mix_chance:
            punch_vs_kick = random.random()
            if punch_vs_kick < 0.55:
                return 4  # Favor punches for speed
            else:
                return 5  # Kicks for power
        else:
            # Aggressive movement to maintain pressure
            if abs(relative_pos) > 0.2:
                if relative_pos > 0:
                    return 2  # Pursue right
                else:
                    return 1  # Pursue left
            else:
                return 4  # Default to quick punch
    
    # Medium range - aggressive positioning and timing
    elif distance < medium_range:
        # Projectile available and opponent far enough
        if my_projectile_cooldown < 0.1 and distance > 0.18:
            if random.random() < 0.4:
                return 9  # Projectile to pressure
        
        # Opponent is vulnerable - press the attack
        if opp_attack_cooldown > 0.3 or opp_block_status < 0.1:
            if relative_pos > 0.1:
                return 2  # Aggressive advance right
            elif relative_pos < -0.1:
                return 1  # Aggressive advance left
            else:
                # Close enough to attack
                if distance < 0.2:
                    if random.random() < 0.7:
                        return 4  # Quick punch
                    else:
                        return 5  # Power kick
                else:
                    # Continue closing distance
                    if relative_pos >= 0:
                        return 2
                    else:
                        return 1
        
        # Opponent might counter-attack
        if opp_attack_cooldown < 0.2:
            # Aggressive but cautious approach
            if distance < 0.2:
                if random.random() < 0.25:
                    return 6  # Brief block
                else:
                    return 4  # Punch first
            else:
                # Continue pressure
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        # Default medium range aggression
        chase_roll = random.random()
        if chase_roll < chase_threshold:
            if relative_pos > 0:
                return 2  # Chase right
            else:
                return 1  # Chase left
        else:
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile pressure
            else:
                # Keep advancing
                if relative_pos >= 0:
                    return 2
                else:
                    return 1
    
    # Far range - projectile pressure and aggressive advancement
    else:
        # Prioritize projectiles for constant pressure
        if my_projectile_cooldown < 0.1:
            return 9  # Projectile attack
        
        # No projectile available - aggressive approach
        approach_style = random.random()
        if approach_style < 0.8:
            # Direct aggressive approach
            if relative_pos > 0.1:
                return 2  # Move right toward opponent
            elif relative_pos < -0.1:
                return 1  # Move left toward opponent
            else:
                # Opponent directly ahead - charge forward
                if random.random() < 0.6:
                    if relative_pos >= 0:
                        return 2
                    else:
                        return 1
                else:
                    return 0  # Brief pause before assault
        else:
            # Aerial approach for unpredictability
            if abs(height_diff) < 0.1:
                return