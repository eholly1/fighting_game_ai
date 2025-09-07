"""
Hall of Fame Agent
==================

Agent ID: gen3_agent_021
Rank: 68/100
Generation: 3
Fighting Style: evolved

Performance Metrics:
- Fitness: 194.84
- Win Rate: 0.0%
- Average Reward: 194.84

Created: 2025-06-01 03:09:14
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
    close_range = 0.12
    medium_range = 0.32
    far_range = 0.48
    critical_health_threshold = -0.45
    dominance_threshold = 0.35
    retreat_threshold = 0.16
    
    # Multi-layered aggression calculation
    base_aggression = 0.52
    health_momentum = 0.0
    position_momentum = 0.0
    tactical_momentum = 0.0
    
    # Health-based momentum with non-linear scaling
    if health_advantage > 0.15:
        health_momentum = min(0.35, health_advantage * 0.6 + 0.1)
    elif health_advantage < -0.15:
        health_momentum = max(-0.45, health_advantage * 0.8 - 0.05)
    
    # Position-based momentum considering stage control
    stage_position = my_x_pos
    if abs(stage_position) > 0.7:  # Near edge
        position_momentum -= 0.15
    elif abs(stage_position) < 0.3:  # Center control
        position_momentum += 0.1
    
    # Tactical momentum based on projectile advantage
    if my_projectile_cooldown < 0.25 and opponent_projectile_cooldown > 0.6:
        tactical_momentum += 0.2
    elif my_projectile_cooldown > 0.6 and opponent_projectile_cooldown < 0.25:
        tactical_momentum -= 0.15
    
    current_aggression = max(0.05, min(0.9, 
        base_aggression + health_momentum + position_momentum + tactical_momentum))
    
    # Enhanced opponent behavior analysis with prediction
    opponent_velocity_magnitude = abs(opponent_x_vel) + abs(opponent_y_vel)
    opponent_moving_fast = opponent_velocity_magnitude > 0.06
    
    # Directional movement analysis
    opponent_advancing = False
    opponent_retreating = False
    opponent_circling = False
    
    if relative_pos > 0 and opponent_x_vel > 0.03:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_x_vel < -0.03:
        opponent_advancing = True
    elif relative_pos > 0 and opponent_x_vel < -0.03:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > 0.03:
        opponent_retreating = True
    elif opponent_moving_fast and not opponent_advancing and not opponent_retreating:
        opponent_circling = True
    
    # Advanced opponent style classification
    opponent_aggressive = opponent_attacking > 0.45 and distance < 0.3
    opponent_defensive = opponent_blocking > 0.55 or (opponent_retreating and distance > 0.2)
    opponent_zoner = opponent_projectile_cooldown < 0.3 and distance > 0.35
    opponent_rusher = opponent_advancing and opponent_attacking > 0.3
    opponent_turtle = opponent_blocking > 0.7 and opponent_velocity_magnitude < 0.02
    
    # Emergency survival mode
    if my_health < 0.08 or health_advantage < -0.7:
        if distance < retreat_threshold:
            if opponent_attacking > 0.7:
                return 6  # Emergency block
            else:
                # Panic retreat with defensive movement
                if abs(my_x_pos) > 0.8:  # Near edge, need to fight
                    return 6
                else:
                    if relative_pos > 0:
                        return 7  # Retreat left with block
                    else:
                        return 8  # Retreat right with block
        elif my_projectile_cooldown < 0.2 and distance > 0.3:
            return 9  # Desperate projectile
        else:
            return 6  # Desperate blocking
    
    # Finishing sequence when opponent is critical
    if opponent_health < 0.12 and health_advantage > 0.25:
        if distance < close_range + 0.06:
            # Execute finishing combo
            finish_roll = random.random()
            if opponent_blocking > 0.6:
                if finish_roll < 0.4:
                    return 5  # Guard break kick
                elif finish_roll < 0.7:
                    return 3  # Jump attack
                else:
                    return 9 if my_projectile_cooldown < 0.4 else 4
            else:
                if finish_roll < 0.5:
                    return 5  # Power finish
                else:
                    return 4  # Speed finish
        elif distance < medium_range:
            # Close distance for kill
            if relative_pos > 0:
                return 2  # Approach right
            else:
                return 1  # Approach left
        else:
            # Projectile finish attempt
            if my_projectile_cooldown < 0.3:
                return 9
    
    # Close range combat with advanced tactics (0.0 - 0.12)
    if distance < close_range:
        # Counter-attack system with timing
        if opponent_attacking > 0.65:
            counter_timing = random.random()
            if health_advantage > 0:
                if counter_timing < 0.3:
                    return 6  # Safe block
                elif counter_timing < 0.6:
                    return 4  # Counter punch
                else:
                    return 5  # Counter kick
            else:
                if counter_timing < 0.7:
                    return 6  # Defensive block
                else:
                    return 4  # Desperate counter
        
        # Anti-turtle strategies
        if opponent_turtle:
            turtle_break = random.random()
            if turtle_break < 0.25:
                return 5  # Heavy kick
            elif turtle_break < 0.4:
                return 3  # Jump attack
            elif turtle_break < 0.6:
                # Create space then projectile
                if relative_pos > 0:
                    return 1  # Move away
                else:
                    return 2
            elif turtle_break < 0.8:
                return 9 if my_projectile_cooldown < 0.4 else 0
            else:
                return 6  # Reset with block
        
        # Pressure system against normal blocking
        if opponent_blocking > 0.5 and not opponent_turtle:
            pressure_