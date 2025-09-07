"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_018
Rank: 52/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 225.08
- Win Rate: 0.0%
- Average Reward: 225.08

Created: 2025-06-01 03:58:23
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
    
    # Extract my fighter state
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = state[0]
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[7]
    my_blocking = state[8]
    my_projectile_cooldown = max(0.0, state[9])
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_x_pos = state[11]
    opponent_y_pos = state[12]
    opponent_x_vel = state[14]
    opponent_y_vel = state[15]
    opponent_attacking = state[18]
    opponent_blocking = state[19]
    opponent_projectile_cooldown = max(0.0, state[20])
    
    # Advanced tactical parameters for evolved balanced fighter
    close_range = 0.13
    medium_range = 0.34
    far_range = 0.52
    critical_health = 0.15
    dominance_threshold = 0.4
    
    # Multi-dimensional aggression calculation
    base_aggression = 0.55
    health_factor = 0.0
    momentum_factor = 0.0
    position_factor = 0.0
    opportunity_factor = 0.0
    
    # Health-based adjustment with smoother transitions
    if health_advantage > 0.2:
        health_factor = min(0.3, health_advantage * 0.5 + 0.08)
    elif health_advantage < -0.2:
        health_factor = max(-0.4, health_advantage * 0.7 - 0.05)
    else:
        health_factor = health_advantage * 0.15
    
    # Momentum calculation based on velocity and positioning
    my_speed = abs(my_x_vel) + abs(my_y_vel)
    opponent_speed = abs(opponent_x_vel) + abs(opponent_y_vel)
    
    if my_speed > opponent_speed + 0.02:
        momentum_factor += 0.12
    elif opponent_speed > my_speed + 0.02:
        momentum_factor -= 0.08
    
    # Stage position awareness
    if abs(my_x_pos) > 0.75:  # Near edge danger
        position_factor -= 0.2
    elif abs(my_x_pos) < 0.25:  # Center control
        position_factor += 0.15
    
    # Opportunity detection
    if opponent_projectile_cooldown > 0.7 and my_projectile_cooldown < 0.3:
        opportunity_factor += 0.18
    if opponent_attacking > 0.6 and distance < 0.2:
        opportunity_factor += 0.1  # Counter opportunity
    
    current_aggression = max(0.1, min(0.85, 
        base_aggression + health_factor + momentum_factor + position_factor + opportunity_factor))
    
    # Enhanced opponent analysis with pattern recognition
    opponent_velocity_total = abs(opponent_x_vel) + abs(opponent_y_vel)
    opponent_is_mobile = opponent_velocity_total > 0.05
    
    # Movement pattern detection
    opponent_approaching = False
    opponent_retreating = False
    opponent_flanking = False
    
    if distance > 0.1:  # Only analyze at meaningful distances
        if relative_pos > 0.05 and opponent_x_vel > 0.025:
            opponent_approaching = True
        elif relative_pos < -0.05 and opponent_x_vel < -0.025:
            opponent_approaching = True
        elif relative_pos > 0.05 and opponent_x_vel < -0.03:
            opponent_retreating = True
        elif relative_pos < -0.05 and opponent_x_vel > 0.03:
            opponent_retreating = True
        elif opponent_is_mobile and abs(opponent_y_vel) > 0.03:
            opponent_flanking = True
    
    # Fighting style classification with improved detection
    opponent_rushdown = opponent_approaching and opponent_attacking > 0.4
    opponent_zoner = opponent_projectile_cooldown < 0.4 and distance > 0.3
    opponent_turtle = opponent_blocking > 0.6 and opponent_velocity_total < 0.025
    opponent_hit_and_run = opponent_is_mobile and opponent_attacking > 0.3 and opponent_blocking < 0.4
    opponent_balanced = not (opponent_rushdown or opponent_zoner or opponent_turtle or opponent_hit_and_run)
    
    # Critical health emergency protocols
    if my_health < critical_health or health_advantage < -0.6:
        if distance < 0.18:
            if opponent_attacking > 0.7:
                return 6  # Emergency block
            elif abs(my_x_pos) > 0.8:  # Cornered
                if opponent_blocking > 0.5:
                    return 3  # Jump escape
                else:
                    desperation_roll = random.random()
                    if desperation_roll < 0.6:
                        return 6  # Block
                    else:
                        return 5  # Desperation kick
            else:
                # Retreat with cover
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        elif distance > 0.35 and my_projectile_cooldown < 0.35:
            return 9  # Desperation projectile
        else:
            return 6  # Defensive block
    
    # Finishing combinations when opponent is low
    if opponent_health < critical_health and health_advantage > 0.2:
        if distance < close_range + 0.05:
            finish_choice = random.random()
            if opponent_blocking > 0.5:
                if finish_choice < 0.35:
                    return 5  # Guard break
                elif finish_choice < 0.6:
                    return 3  # Overhead jump
                else:
                    return 9 if my_projectile_cooldown < 0.5 else 4
            else:
                if finish_choice < 0.55:
                    return 5  # Power finish
                else:
                    return 4  # Quick finish
        elif distance < medium_range + 0.1:
            # Approach for finish
            if relative_pos > 0:
                return 2
            else:
                return 1
        elif my_projectile_cooldown < 0.4:
            return 9  # Finish with projectile
    
    # Close range tactical combat (0-0.13)
    if distance < close_range:
        # Advanced counter-attack system
        if opponent_attacking > 0.6:
            counter_decision = random.random()
            counter_confidence = current_aggression
            
            if counter_confidence > 0.65:
                if counter_decision < 0.25:
                    return 6  # Safe block
                elif counter_decision < 0.55:
                    return 4  # Counter punch
                else:
                    return 5  # Counter kick
            else:
                if counter_decision < 0.6:
                    return 6  # Defensive block
                elif counter_decision < 0.8:
                    return