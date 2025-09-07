"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_014
Rank: 85/100
Generation: 0
Fighting Style: adaptive

Performance Metrics:
- Fitness: 168.77
- Win Rate: 50.0%
- Average Reward: 241.10

Created: 2025-06-01 00:36:59
Lineage: Original

Tournament Stats:
None
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
    
    # Extract fighter states
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[2]
    my_y_pos = state[3]
    my_x_vel = state[4]
    my_y_vel = state[5]
    my_attacking = state[6]
    my_blocking = state[7]
    my_stunned = state[8]
    my_projectile_cooldown = state[10]
    
    opponent_health = state[12] if state[12] >= 0 else 0.5
    opponent_x_pos = state[13]
    opponent_y_pos = state[14]
    opponent_x_vel = state[15]
    opponent_y_vel = state[16]
    opponent_attacking = state[17]
    opponent_blocking = state[18]
    opponent_stunned = state[19]
    
    # Define tactical ranges and thresholds
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    critical_health = -0.4
    winning_health = 0.3
    
    # Adaptive strategy parameters based on health advantage
    if health_advantage < critical_health:
        # Defensive survival mode
        aggression_level = 0.2
        block_tendency = 0.8
        projectile_preference = 0.7
    elif health_advantage < -0.1:
        # Cautious disadvantage mode
        aggression_level = 0.4
        block_tendency = 0.6
        projectile_preference = 0.5
    elif health_advantage > winning_health:
        # Aggressive winning mode
        aggression_level = 0.8
        block_tendency = 0.2
        projectile_preference = 0.3
    else:
        # Balanced neutral mode
        aggression_level = 0.6
        block_tendency = 0.4
        projectile_preference = 0.4
    
    # Emergency defensive responses
    if my_stunned > 0.5:
        return 6  # Block while stunned
    
    if opponent_attacking > 0.5 and distance < close_range:
        if random.random() < block_tendency:
            return 6  # Block incoming attack
    
    # Opponent behavior analysis for adaptation
    opponent_moving_toward = False
    if relative_pos > 0 and opponent_x_vel > 0.1:
        opponent_moving_toward = True
    elif relative_pos < 0 and opponent_x_vel < -0.1:
        opponent_moving_toward = True
    
    opponent_retreating = False
    if relative_pos > 0 and opponent_x_vel < -0.1:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > 0.1:
        opponent_retreating = True
    
    # Range-based tactical decisions
    if distance < close_range:
        # Close combat zone
        if health_advantage < critical_health:
            # Survival mode in close range
            if opponent_attacking > 0.5:
                return 6  # Block
            elif opponent_blocking > 0.5:
                # Try to create distance
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
            else:
                # Quick escape attempt
                if abs(relative_pos) > 0.5:
                    return 3  # Jump to create distance
                else:
                    return 6  # Block
        
        elif health_advantage > winning_health:
            # Aggressive close combat when winning
            if opponent_blocking > 0.5:
                # Mix up attacks against blocking opponent
                attack_choice = random.random()
                if attack_choice < 0.4:
                    return 5  # Kick to break block
                elif attack_choice < 0.7:
                    return 4  # Fast punch
                else:
                    return 3  # Jump attack
            else:
                # Normal aggressive attacks
                if random.random() < 0.6:
                    return 4  # Fast punch
                else:
                    return 5  # Strong kick
        
        else:
            # Balanced close combat
            if opponent_blocking > 0.5:
                # Counter blocking opponent
                if random.random() < 0.5:
                    return 5  # Kick
                else:
                    return 3  # Jump
            elif opponent_attacking > 0.5:
                if random.random() < block_tendency:
                    return 6  # Block
                else:
                    return 4  # Counter attack
            else:
                # Normal close combat
                combat_choice = random.random()
                if combat_choice < 0.5:
                    return 4  # Punch
                elif combat_choice < 0.8:
                    return 5  # Kick
                else:
                    return 6  # Block
    
    elif distance < medium_range:
        # Medium range positioning zone
        if health_advantage < critical_health:
            # Maintain distance when losing
            if opponent_moving_toward:
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
            else:
                # Use projectiles if available
                if my_projectile_cooldown < 0.3:
                    return 9  # Projectile
                else:
                    return 6  # Block
        
        elif health_advantage > winning_health:
            # Aggressive positioning when winning
            if opponent_retreating:
                # Chase retreating opponent
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                # Close distance for attack
                positioning_choice = random.random()
                if positioning_choice < 0.6:
                    if relative_pos > 0:
                        return 2  # Move right toward opponent
                    else:
                        return 1  # Move left toward opponent
                elif positioning_choice < 0.8:
                    return 3  # Jump approach
                else:
                    return 9  # Projectile
        
        else:
            # Balanced medium range tactics
            if opponent_attacking > 0.5:
                # Defensive positioning
                if random.random() < 0.6:
                    return 6  # Block
                else:
                    if relative_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
            
            elif opponent_blocking > 0.5:
                # Attack blocking opponent
                if my_projectile_cooldown < 0.3:
                    return 9  # Projectile
                else:
                    if relative_pos > 0:
                        return 2  # Move right to close
                    else:
                        return 1  # Move left to close
            
            else:
                # Normal medium range tactics
                medium_choice = random.random()
                if medium_choice < 0.3:
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                elif medium_choice < 0.6:
                    return 9  # Projectile
                elif medium_choice < 0.8:
                    return 3  # Jump
                else:
                    return 6  # Block