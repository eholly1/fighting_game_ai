"""
Evolutionary Agent: gen4_elite_002
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "pressure_fighter",
  "win_rate": 0.5
}

Code Hash: 9eb5bafdb4977c9a
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
    
    # Extract fighter states with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    my_velocity_x = state[2] if len(state) > 2 else 0.0
    my_velocity_y = state[3] if len(state) > 3 else 0.0
    opponent_velocity_x = state[13] if len(state) > 13 else 0.0
    opponent_velocity_y = state[14] if len(state) > 14 else 0.0
    
    # Check attack and defense states
    my_attacking = state[4] if len(state) > 4 else 0.0
    my_blocking = state[5] if len(state) > 5 else 0.0
    opponent_attacking = state[15] if len(state) > 15 else 0.0
    opponent_blocking = state[16] if len(state) > 16 else 0.0
    
    # Projectile cooldown info
    my_projectile_cooldown = state[6] if len(state) > 6 else 0.0
    opponent_projectile_cooldown = state[17] if len(state) > 17 else 0.0
    
    # Define pressure fighter parameters
    close_range = 0.12
    medium_range = 0.25
    corner_distance = 0.85
    aggression_threshold = 0.6
    critical_health = 0.3
    desperation_health = 0.15
    
    # Calculate derived strategic values
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = distance >= medium_range
    opponent_left = relative_pos < 0
    opponent_right = relative_pos > 0
    winning = health_advantage > 0.1
    losing = health_advantage < -0.1
    critical_situation = my_health < critical_health
    desperate = my_health < desperation_health
    
    # Movement direction based on opponent position
    move_toward_opponent = 2 if opponent_right else 1
    move_away_opponent = 1 if opponent_right else 2
    
    # Emergency survival mode for desperate situations
    if desperate:
        if opponent_attacking > 0.5:
            return 6  # Block incoming attack
        elif distance > 0.4 and my_projectile_cooldown < 0.3:
            return 9  # Keep distance with projectiles
        elif distance < 0.08:
            return move_away_opponent  # Create space when too close
        else:
            return 6  # Default to blocking
    
    # Critical health defensive adjustments
    if critical_situation and not winning:
        if opponent_attacking > 0.5:
            return 6  # Block attacks
        elif distance > 0.35 and my_projectile_cooldown < 0.4:
            return 9  # Use projectiles for safer damage
        elif distance < 0.1 and random.random() < 0.4:
            return 6  # Increased blocking chance
    
    # Opponent attack response - pressure fighter adapts but stays aggressive
    if opponent_attacking > 0.5:
        if distance < 0.1:
            if random.random() < 0.3:
                return 6  # Sometimes block very close attacks
            else:
                # Counter-attack mindset
                return 4 if random.random() < 0.7 else 5
        elif distance < 0.2:
            if random.random() < 0.6:
                return 6  # Block medium-close attacks more often
            else:
                return move_toward_opponent  # Keep advancing
        else:
            return move_toward_opponent  # Advance through their attack
    
    # Opponent blocking response - pressure fighter breaks through
    if opponent_blocking > 0.5 and distance < 0.2:
        if random.random() < 0.4:
            return 5  # Kicks are stronger against blocks
        elif random.random() < 0.6:
            return 4  # Fast punches to overwhelm
        else:
            # Mix in movement to find openings
            if random.random() < 0.5:
                return 7 if opponent_right else 8  # Move while blocking
            else:
                return move_toward_opponent
    
    # Core pressure fighter range-based strategy
    if is_close:
        # Close range: Maximum pressure and aggression
        if winning:
            # Press advantage with varied attacks
            attack_choice = random.random()
            if attack_choice < 0.5:
                return 4  # Fast punches
            elif attack_choice < 0.8:
                return 5  # Power kicks
            else:
                return move_toward_opponent  # Stay close
        else:
            # Maintain pressure even when not winning
            if random.random() < 0.7:
                # High attack frequency
                return 4 if random.random() < 0.6 else 5
            else:
                # Occasional defensive action
                return 6 if random.random() < 0.4 else move_toward_opponent
    
    elif is_medium:
        # Medium range: Close the distance aggressively
        if opponent_velocity_x > 0.1 and opponent_right:
            # Opponent moving right, intercept
            return 2
        elif opponent_velocity_x < -0.1 and opponent_left:
            # Opponent moving left, intercept
            return 1
        elif abs(height_diff) > 0.1 and random.random() < 0.3:
            return 3  # Jump to handle height differences
        else:
            # Direct advance toward opponent
            if random.random() < 0.8:
                return move_toward_opponent
            else:
                # Occasional projectile to disrupt opponent timing
                if my_projectile_cooldown < 0.3:
                    return 9
                else:
                    return move_toward_opponent
    
    else:
        # Far range: Close distance while using projectiles
        if my_projectile_cooldown < 0.2:
            if random.random() < 0.4:
                return 9  # Projectile attack
            else:
                return move_toward_opponent  # Advance while projectile available
        elif distance > 0.5:
            # Too far, must close distance
            if random.random() < 0.9:
                return move_toward_opponent
            else:
                return 3  # Occasional jump approach
        else:
            # Medium-far range, aggressive advance
            return move_toward_opponent
    
    # Corner pressure tactics
    if distance < 0.3:
        opponent_position_estimate = 0.5 + (relative_pos * distance * 0.5)
        if opponent_position_estimate > corner_distance or opponent_position_estimate < (1.0 - corner_distance):
            # Opponent near corner, increase pressure
            if random.random() < 0.8:
                return 4 if random.random() < 0.5 else 5
            else:
                return move_toward_opponent
    
    # Momentum and velocity considerations
    if abs(my_velocity_x) > 0.15:
        # High speed approach, prepare for attack
        if distance < 0.2:
            return 4  # Quick punch on