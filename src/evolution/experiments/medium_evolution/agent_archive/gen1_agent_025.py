"""
Evolutionary Agent: gen1_agent_025
==================================

Metadata:
{
  "generation": 1,
  "fitness": 263.6399999999932,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 40f201268748a61b
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Define hybrid tactical ranges
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    
    # Hybrid fighting parameters - balanced approach
    base_aggression = 0.65
    defensive_threshold = 0.75
    counter_attack_window = 0.25
    spacing_preference = 0.2
    
    # Adaptive aggression based on health advantage
    if health_advantage > 0.4:
        current_aggression = min(0.85, base_aggression + 0.2)
        defense_priority = 0.3
    elif health_advantage < -0.4:
        current_aggression = max(0.4, base_aggression - 0.25)
        defense_priority = 0.8
    else:
        current_aggression = base_aggression
        defense_priority = 0.5
    
    # Critical health emergency responses
    if my_health < 0.15:
        if opponent_attack_status > 0.6 and distance < 0.25:
            return 6  # Emergency block
        if distance > 0.4 and my_projectile_cooldown < 0.2:
            return 9  # Desperate projectile
        # Escape with blocking movement
        if relative_pos > 0:
            return 7
        else:
            return 8
    
    # Opponent behavior analysis for hybrid adaptation
    opponent_is_aggressive = opponent_velocity_x != 0 and abs(opponent_velocity_x) > 0.2
    opponent_is_retreating = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    opponent_is_attacking = opponent_attack_status > 0.5
    opponent_is_blocking = opponent_block_status > 0.6
    
    # Wall awareness for positioning
    near_left_wall = my_pos_x < 0.2
    near_right_wall = my_pos_x > 0.8
    opponent_near_wall = opponent_pos_x < 0.2 or opponent_pos_x > 0.8
    
    # Range-based hybrid strategy
    if distance <= ultra_close_range:
        # Ultra-close: Mix offense and defense
        if opponent_is_attacking:
            # Defensive response with counter opportunities
            if my_health < opponent_health * 0.8:
                return 6  # Block when at disadvantage
            elif random.random() < defense_priority:
                return 6  # Block based on defensive priority
            else:
                # Counter attack - quick punch for speed
                return 4
        
        elif opponent_is_blocking:
            # Guard break mixups
            mixup_choice = random.random()
            if mixup_choice < 0.3 and my_projectile_cooldown < 0.4:
                return 9  # Projectile to break guard
            elif mixup_choice < 0.55:
                return 5  # Strong kick
            elif mixup_choice < 0.75:
                # Reposition for angle change
                if not near_left_wall and (near_right_wall or random.random() < 0.5):
                    return 1
                else:
                    return 2
            else:
                return 4  # Quick punch
        
        else:
            # Neutral ultra-close - hybrid pressure
            attack_choice = random.random()
            aggression_modifier = current_aggression + 0.1
            
            if attack_choice < aggression_modifier * 0.4:
                return 4  # Quick punch
            elif attack_choice < aggression_modifier * 0.7:
                return 5  # Power kick
            elif attack_choice < aggression_modifier * 0.85:
                return 6  # Defensive stance
            else:
                # Movement for positioning
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    elif distance <= close_range:
        # Close range: Balanced approach with spacing control
        if opponent_is_attacking:
            # Defensive options with spacing
            if distance < 0.12:
                return 6  # Block close attacks
            else:
                # Create space while defending
                if relative_pos > 0:
                    return 7  # Block and move left
                else:
                    return 8  # Block and move right
        
        # Counter attack window after opponent attack
        if opponent_attack_status < 0.1 and my_attack_status < 0.1:
            counter_chance = current_aggression + 0.15
            if random.random() < counter_chance:
                if health_advantage > 0.2:
                    return 5  # Power attack when ahead
                else:
                    return 4  # Safe quick attack
        
        # Standard close range tactics
        if opponent_is_blocking:
            # Patient approach against defense
            if my_projectile_cooldown < 0.3 and random.random() < 0.25:
                return 9  # Occasional projectile
            elif random.random() < 0.4:
                return 5  # Strong attack vs block
            else:
                return 6  # Wait for opening
        
        else:
            # Mixed approach in close range
            action_choice = random.random()
            if action_choice < current_aggression * 0.5:
                return 4  # Quick attack
            elif action_choice < current_aggression * 0.75:
                return 5  # Power attack
            elif action_choice < current_aggression:
                # Spacing movement
                if relative_pos > spacing_preference:
                    return 1  # Move left for spacing
                else:
                    return 2  # Move right for spacing
            else:
                return 6  # Defensive stance
    
    elif distance <= medium_range:
        # Medium range: Hybrid positioning and engagement
        if opponent_is_attacking and distance < 0.25:
            return 6  # Block incoming attacks