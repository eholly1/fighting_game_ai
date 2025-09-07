"""
Evolutionary Agent: gen2_elite_000
==================================

Metadata:
{
  "generation": 2,
  "fitness": 340.32000000001113,
  "fighting_style": "rushdown",
  "win_rate": 0.0
}

Code Hash: 64475fb329eba968
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
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define rushdown tactical parameters
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    
    # Rushdown aggression levels
    base_aggression = 0.8
    winning_aggression = 0.9
    losing_aggression = 0.6
    
    # Determine current aggression level based on health
    if health_advantage > 0.3:
        current_aggression = winning_aggression
    elif health_advantage < -0.3:
        current_aggression = losing_aggression
    else:
        current_aggression = base_aggression
    
    # Emergency defensive actions when very low health
    if my_health < 0.2 and health_advantage < -0.4:
        if opponent_attack_status > 0.5:
            return 6  # Block incoming attack
        if distance > medium_range and my_projectile_cooldown < 0.3:
            return 9  # Projectile to create space
        if distance < close_range:
            # Try to escape close range when critically low
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
    
    # Rushdown core: Always try to close distance when not in ultra-close range
    if distance > ultra_close_range:
        # Detect opponent trying to create distance
        opponent_retreating = False
        if relative_pos > 0 and opponent_velocity_x < -0.3:
            opponent_retreating = True
        elif relative_pos < 0 and opponent_velocity_x > 0.3:
            opponent_retreating = True
        
        # Chase retreating opponent aggressively
        if opponent_retreating and distance < medium_range:
            if relative_pos > 0:
                return 2  # Chase right
            else:
                return 1  # Chase left
        
        # Standard approach when not ultra-close
        if distance > far_range:
            # At long range, mix projectiles with advancing
            if my_projectile_cooldown < 0.2 and random.random() < 0.4:
                return 9  # Projectile while advancing
            else:
                # Move toward opponent
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        elif distance > medium_range:
            # Medium-far range: aggressive advance
            approach_chance = current_aggression + 0.1
            if random.random() < approach_chance:
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                # Occasional projectile to mix up approach
                if my_projectile_cooldown < 0.3:
                    return 9
                else:
                    return 1 if relative_pos < 0 else 2
        
        elif distance > close_range:
            # Medium range: prepare for rush
            # Check if opponent is blocking heavily
            if opponent_block_status > 0.7:
                # Throw to break guard or reposition
                if my_projectile_cooldown < 0.4 and random.random() < 0.3:
                    return 9
                else:
                    # Close distance to grab/throw range
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
            else:
                # Advance aggressively
                rush_chance = current_aggression
                if random.random() < rush_chance:
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                else:
                    # Jump in for aerial approach
                    if abs(height_diff) < 0.3:
                        return 3
                    else:
                        return 1 if relative_pos < 0 else 2
        
        else:
            # Close range but not ultra-close: final approach
            if opponent_attack_status > 0.6:
                # Opponent is attacking, block and advance
                if relative_pos > 0:
                    return 8  # Move right while blocking
                else:
                    return 7  # Move left while blocking
            else:
                # Rush in for attack
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Ultra-close range combat (rushdown pressure)
    else:
        # Detect if opponent is attacking
        if opponent_attack_status > 0.7:
            # Opponent is attacking, decide whether to block or counter
            if my_health < opponent_health * 0.7:
                return 6  # Block when at health disadvantage
            elif random.random() < 0.3:
                return 6  # Sometimes block even when winning
            else:
                # Counter attack - favor faster punch
                return 4
        
        # Detect if opponent is blocking heavily
        elif opponent_block_status > 0.6:
            # Mix up against blocking opponent
            mixup_option = random.random()
            if mixup_option < 0.25:
                # Throw/projectile to break guard
                if my_projectile_cooldown < 0.5:
                    return 9
                else:
                    return 5  # Strong kick
            elif mixup_option < 0.5:
                # Reposition for different angle
                if my_pos_x < 0.3:
                    return 2  # Move right
                elif my_pos_x > 0.7:
                    return 1  # Move left
                else:
                    return 3  # Jump for overhead
            elif mixup_option < 0.75:
                return 5  # Kick to break guard
            else:
                return 4  # Quick punch
        
        # Opponent not attacking or blocking heavily - rushdown pressure
        else:
            # Apply continuous pressure with attack mixups
            pressure_option = random.random()
            
            # Weight attacks based on current aggression
            punch_threshold = 0.5 + (current_aggression - 0.5) * 0.3
            kick_threshold = punch_threshold + 0