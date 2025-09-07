"""
Evolutionary Agent: gen4_agent_023
==================================

Metadata:
{
  "generation": 4,
  "fitness": 169.039999999993,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 1836712c938ba543
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
    
    # Extract my fighter state with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.5
    my_x_vel = state[3] if len(state) > 3 else 0.0
    my_y_vel = state[4] if len(state) > 4 else 0.0
    my_attacking = state[7] if len(state) > 7 else 0.0
    my_blocking = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent state with bounds checking
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_x_pos = state[11] if len(state) > 11 else 0.5
    opponent_y_pos = state[13] if len(state) > 13 else 0.5
    opponent_x_vel = state[14] if len(state) > 14 else 0.0
    opponent_y_vel = state[15] if len(state) > 15 else 0.0
    opponent_attacking = state[18] if len(state) > 18 else 0.0
    opponent_blocking = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Hybrid tactical ranges with refined thresholds
    ultra_close = 0.08
    close_range = 0.16
    medium_range = 0.35
    far_range = 0.55
    
    # Dynamic strategy parameters
    base_aggression = 0.58
    adaptation_factor = 0.0
    positioning_bonus = 0.0
    tempo_control = 0.0
    
    # Advanced health momentum calculation
    if health_advantage > 0.2:
        adaptation_factor = min(0.25, health_advantage * 0.4)
    elif health_advantage < -0.2:
        adaptation_factor = max(-0.35, health_advantage * 0.6)
    
    # Stage control assessment
    center_control = 1.0 - abs(my_x_pos * 2)  # Higher when closer to center
    edge_danger = max(0, abs(my_x_pos) - 0.75) * 4  # Penalty near edges
    positioning_bonus = (center_control * 0.08) - (edge_danger * 0.12)
    
    # Tempo control based on projectile management
    projectile_advantage = 0.0
    if my_projectile_cooldown < 0.2 and opponent_projectile_cooldown > 0.5:
        projectile_advantage = 0.15
    elif my_projectile_cooldown > 0.5 and opponent_projectile_cooldown < 0.2:
        projectile_advantage = -0.12
    tempo_control = projectile_advantage
    
    # Calculate dynamic aggression level
    current_aggression = max(0.1, min(0.85, 
        base_aggression + adaptation_factor + positioning_bonus + tempo_control))
    
    # Enhanced opponent pattern recognition
    opponent_velocity_total = abs(opponent_x_vel) + abs(opponent_y_vel)
    opponent_mobile = opponent_velocity_total > 0.05
    
    # Movement pattern analysis
    opponent_advancing = False
    opponent_retreating = False
    opponent_flanking = False
    
    movement_threshold = 0.025
    if relative_pos > 0 and opponent_x_vel > movement_threshold:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_x_vel < -movement_threshold:
        opponent_advancing = True
    elif relative_pos > 0 and opponent_x_vel < -movement_threshold:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > movement_threshold:
        opponent_retreating = True
    elif opponent_mobile and not opponent_advancing and not opponent_retreating:
        opponent_flanking = True
    
    # Opponent archetype detection
    opponent_rusher = opponent_advancing and opponent_attacking > 0.4 and distance < 0.25
    opponent_zoner = opponent_projectile_cooldown < 0.25 and distance > 0.4
    opponent_turtle = opponent_blocking > 0.65 and opponent_velocity_total < 0.02
    opponent_technical = opponent_blocking > 0.3 and opponent_attacking > 0.3
    opponent_aggressive = opponent_attacking > 0.5 and distance < 0.3
    
    # Crisis management system
    if my_health < 0.15 or health_advantage < -0.6:
        crisis_distance_threshold = 0.2
        
        if distance < crisis_distance_threshold:
            if opponent_attacking > 0.6:
                return 6  # Emergency block
            elif opponent_blocking > 0.7:
                # Try to create space from turtle
                if abs(my_x_pos) > 0.8:
                    return 3  # Jump when cornered
                else:
                    if relative_pos > 0:
                        return 7  # Retreat with block
                    else:
                        return 8
            else:
                # Desperate counter-attack
                if random.random() < 0.4:
                    return 4  # Quick punch
                else:
                    return 6  # Play safe
        else:
            # Long range crisis management
            if my_projectile_cooldown < 0.3 and distance > 0.3:
                return 9  # Zoning attempt
            elif opponent_advancing:
                return 6  # Block incoming rush
            else:
                # Try to maintain distance
                if relative_pos > 0:
                    return 1  # Move away
                else:
                    return 2
    
    # Victory condition exploitation
    if opponent_health < 0.18 and health_advantage > 0.2:
        if distance < medium_range:
            # Finishing pressure
            if opponent_blocking > 0.6:
                finish_option = random.random()
                if finish_option < 0.35:
                    return 5  # Heavy kick to break guard
                elif finish_option < 0.6:
                    return 3  # Jump attack
                elif finish_option < 0.8:
                    return 9 if my_projectile_cooldown < 0.4 else 4
                else:
                    return 4  # Safe pressure
            else:
                # Direct finishing attempts
                if random.random() < 0.6:
                    return 5  # Power finish
                else:
                    return 4  # Speed finish
        else:
            # Close distance for finish
            if distance > far_range and my_projectile_cooldown < 0.25:
                return 9  # Projectile finish attempt
            else:
                if relative_pos > 0:
                    return 2  # Advance for finish