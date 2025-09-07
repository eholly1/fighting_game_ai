"""
Evolutionary Agent: gen2_agent_004
==================================

Metadata:
{
  "generation": 2,
  "fitness": -4.120666666666981,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 13098c4d2d7d922a
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
    
    # Enhanced range definitions for hybrid strategy
    ultra_close_range = 0.08
    strike_range = 0.16
    control_range = 0.28
    transition_range = 0.42
    projectile_range = 0.65
    
    # Dynamic aggression system based on multiple factors
    base_aggression = 0.6
    health_modifier = health_advantage * 0.3
    distance_modifier = (1.0 - distance) * 0.2
    momentum_factor = abs(my_velocity_x) + abs(opponent_velocity_x)
    
    current_aggression = max(0.2, min(0.9, base_aggression + health_modifier + distance_modifier))
    
    # Tactical awareness variables
    opponent_is_aggressive = opponent_velocity_x != 0 and abs(opponent_velocity_x) > 0.15
    opponent_approaching = ((relative_pos > 0 and opponent_velocity_x < -0.1) or 
                           (relative_pos < 0 and opponent_velocity_x > 0.1))
    opponent_retreating = ((relative_pos > 0 and opponent_velocity_x > 0.1) or 
                          (relative_pos < 0 and opponent_velocity_x < -0.1))
    opponent_attacking = opponent_attack_status > 0.4
    opponent_blocking = opponent_block_status > 0.5
    
    # Wall and positioning awareness
    near_left_wall = my_pos_x < 0.25
    near_right_wall = my_pos_x > 0.75
    opponent_cornered = opponent_pos_x < 0.2 or opponent_pos_x > 0.8
    i_am_cornered = near_left_wall or near_right_wall
    
    # Critical health management
    critical_health_threshold = 0.2
    desperate_health_threshold = 0.12
    
    if my_health < desperate_health_threshold:
        # Survival mode - maximum defensive play
        if opponent_attacking and distance < control_range:
            return 6  # Emergency block
        elif distance > projectile_range * 0.7 and my_projectile_cooldown < 0.2:
            return 9  # Desperate projectile for space
        elif distance < strike_range:
            # Defensive movement away from opponent
            if i_am_cornered:
                # Must move toward center even if toward opponent
                if my_pos_x < 0.5:
                    return 8 if opponent_blocking else 2
                else:
                    return 7 if opponent_blocking else 1
            else:
                # Move away from opponent
                if relative_pos > 0:
                    return 7  # Left with block
                else:
                    return 8  # Right with block
        else:
            # Maintain distance
            return 6  # Block and wait
    
    elif my_health < critical_health_threshold:
        # Cautious mode - defensive with calculated risks
        defense_priority = 0.75
        
        if opponent_attacking:
            if distance < control_range:
                return 6  # Block incoming attacks
            else:
                # Create more space
                if relative_pos > 0:
                    return 7
                else:
                    return 8
        
        # Limited offensive opportunities
        if distance < strike_range and not opponent_blocking:
            if random.random() < (1.0 - defense_priority):
                return 4  # Quick safe attack
        
        # Spacing and projectile game
        if distance > control_range and my_projectile_cooldown < 0.3:
            return 9  # Projectile for chip damage
    
    # Finishing mode when opponent is vulnerable
    if health_advantage > 0.3 and opponent_health < 0.3:
        finishing_aggression = min(0.95, current_aggression + 0.2)
        
        if distance < strike_range:
            if opponent_blocking:
                # Mix up against blocking opponent
                mixup_choice = random.random()
                if mixup_choice < 0.25 and my_projectile_cooldown < 0.3:
                    return 9  # Projectile mixup
                elif mixup_choice < 0.5:
                    return 5  # Strong kick
                elif mixup_choice < 0.75:
                    # Reposition for angle
                    if not near_right_wall and (near_left_wall or random.random() < 0.5):
                        return 2
                    else:
                        return 1
                else:
                    return 4  # Quick punch
            else:
                # Go for finish
                if random.random() < finishing_aggression:
                    return 5 if random.random() < 0.6 else 4
        
        elif distance < control_range:
            # Aggressive approach for finish
            if relative_pos > 0:
                return 2  # Move in
            else:
                return 1  # Move in
    
    # Ultra close range combat (0.0 - 0.08)
    if distance <= ultra_close_range:
        if opponent_attacking:
            # React to opponent attacks
            if my_health <= opponent_health * 0.8:
                return 6  # Defensive when at health disadvantage
            elif random.random() < 0.4:
                return 6  # Sometimes block anyway
            else:
                # Counter attack
                return 4  # Quick counter
        
        elif opponent_blocking:
            # Break guard tactics
            guard_break_choice = random.random()
            if guard_break_choice < 0.2 and my_projectile_cooldown < 0.4:
                return 9  # Point blank projectile
            elif guard_break_choice < 0.45:
                return 5  # Strong attack
            elif guard_break_choice < 0.7:
                # Create angle
                if not near_left_wall and (near_right_wall or random.random() < 0.5):
                    return 1
                else:
                    return