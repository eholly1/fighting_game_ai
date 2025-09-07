"""
Evolutionary Agent: gen1_agent_009
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 8882789f5fe9b0b4
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
    
    # Projectile and positioning info
    my_projectile_cooldown = state[6] if len(state) > 6 else 0.0
    opponent_projectile_cooldown = state[17] if len(state) > 17 else 0.0
    my_position_x = state[0] if len(state) > 0 else 0.5
    opponent_position_x = state[11] if len(state) > 11 else 0.5
    
    # Enhanced pressure fighter parameters
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.28
    far_range = 0.45
    corner_threshold = 0.15
    aggression_multiplier = 1.2
    critical_health = 0.25
    desperation_health = 0.12
    combo_distance = 0.12
    
    # Calculate strategic state variables
    is_ultra_close = distance < ultra_close_range
    is_close = ultra_close_range <= distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    opponent_left = relative_pos < -0.1
    opponent_right = relative_pos > 0.1
    winning_big = health_advantage > 0.3
    winning = health_advantage > 0.05
    losing = health_advantage < -0.05
    losing_big = health_advantage < -0.3
    critical_situation = my_health < critical_health
    desperate = my_health < desperation_health
    
    # Enhanced movement calculations
    move_toward_opponent = 2 if opponent_right else 1
    move_away_opponent = 1 if opponent_right else 2
    move_block_toward = 8 if opponent_right else 7
    move_block_away = 7 if opponent_right else 8
    
    # Opponent corner detection
    opponent_near_left_corner = opponent_position_x < corner_threshold
    opponent_near_right_corner = opponent_position_x > (1.0 - corner_threshold)
    opponent_cornered = opponent_near_left_corner or opponent_near_right_corner
    i_near_corner = my_position_x < corner_threshold or my_position_x > (1.0 - corner_threshold)
    
    # Enhanced attack pattern tracking
    frame_action_seed = int((distance * 1000 + my_health * 100 + opponent_health * 50)) % 100
    attack_pattern = frame_action_seed % 3
    
    # Desperation mode - improved survival tactics
    if desperate:
        if opponent_attacking > 0.6:
            if distance < 0.06:
                return 6  # Block very close attacks
            elif distance < 0.15:
                if random.random() < 0.7:
                    return 6
                else:
                    return move_away_opponent
            else:
                return move_toward_opponent  # Counter-attack when possible
        elif distance > 0.35 and my_projectile_cooldown < 0.25:
            return 9  # Safe projectile damage
        elif i_near_corner and distance < 0.2:
            # Escape corner situation
            if opponent_left:
                return 7  # Move right while blocking
            else:
                return 8  # Move left while blocking
        elif distance < 0.05:
            return move_away_opponent  # Create minimal space
        else:
            return 6  # Conservative blocking
    
    # Critical health with enhanced decision making
    if critical_situation and not winning:
        if opponent_attacking > 0.5:
            if distance < 0.12:
                if random.random() < 0.6:
                    return 6
                else:
                    # Risky counter-attack for pressure fighter
                    return 4
            else:
                return move_block_toward  # Advance while defending
        elif distance > 0.4 and my_projectile_cooldown < 0.3:
            return 9
        elif opponent_cornered and distance < 0.25:
            # Press advantage even when low health
            return 4 if random.random() < 0.7 else 5
        elif distance < 0.08:
            if random.random() < 0.5:
                return 6
            else:
                return 4  # Maintain pressure
    
    # Enhanced opponent attack response
    if opponent_attacking > 0.5:
        if is_ultra_close:
            if random.random() < 0.4:
                return 6  # Block ultra-close attacks
            else:
                # Aggressive counter - pressure fighter mentality
                if attack_pattern == 0:
                    return 4
                elif attack_pattern == 1:
                    return 5
                else:
                    return 3  # Jump counter
        elif is_close:
            if random.random() < 0.5:
                return 6
            elif random.random() < 0.8:
                return move_toward_opponent  # Advance through attack
            else:
                return 4  # Quick counter
        elif is_medium:
            # Medium range attack response - close distance
            if random.random() < 0.3:
                return move_block_toward
            else:
                return move_toward_opponent
        else:
            # Far attack response - aggressive advance
            return move_toward_opponent
    
    # Enhanced blocking response - pressure fighter breaks defenses
    if opponent_blocking > 0.5:
        if is_ultra_close or is_close:
            block_break_chance = 0.5 if winning else 0.4
            if random.random() < block_break_chance:
                if attack_pattern == 0:
                    return 5  # Heavy kick to break block
                elif attack_pattern == 1:
                    return 4  # Fast punch series
                else:
                    return 3  # Jump attack
            else:
                # Reposition for better angle
                if opponent_cornered:
                    return move_toward_opponent
                else:
                    return move_block_toward
        elif is_medium:
            # Close distance against blocking opponent
            if random.random() < 0.7:
                return move_toward_opponent
            else:
                return