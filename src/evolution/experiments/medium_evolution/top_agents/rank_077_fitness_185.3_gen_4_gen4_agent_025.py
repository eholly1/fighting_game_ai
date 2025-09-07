"""
Hall of Fame Agent
==================

Agent ID: gen4_agent_025
Rank: 77/100
Generation: 4
Fighting Style: evolved

Performance Metrics:
- Fitness: 185.32
- Win Rate: 0.0%
- Average Reward: 185.32

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
    
    # Extract my fighter state with bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = state[0]
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = max(0.0, state[5])
    my_blocking = max(0.0, state[6])
    my_stunned = max(0.0, state[7]) if len(state) > 7 else 0.0
    my_projectile_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    
    # Extract opponent state with bounds checking
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_x_pos = state[11]
    opponent_y_pos = state[12]
    opponent_x_vel = state[14]
    opponent_y_vel = state[15]
    opponent_attacking = max(0.0, state[16])
    opponent_blocking = max(0.0, state[17])
    opponent_stunned = max(0.0, state[18]) if len(state) > 18 else 0.0
    opponent_projectile_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    
    # Enhanced tactical parameters for hybrid evolution
    close_range = 0.13
    medium_range = 0.31
    far_range = 0.47
    critical_health = 0.20
    dominance_health = 0.65
    
    # Advanced multi-dimensional aggression calculation
    base_aggression = 0.58
    health_factor = 0.0
    position_factor = 0.0
    momentum_factor = 0.0
    tactical_factor = 0.0
    
    # Health-based aggression with exponential scaling
    health_ratio = my_health / max(0.05, opponent_health)
    if health_advantage > 0.3:
        health_factor = min(0.4, health_advantage * 0.75 + 0.15)
    elif health_advantage > 0.1:
        health_factor = health_advantage * 0.5
    elif health_advantage < -0.3:
        health_factor = max(-0.5, health_advantage * 0.9 - 0.1)
    elif health_advantage < -0.1:
        health_factor = health_advantage * 0.6
    
    # Position-based tactical awareness
    stage_center = abs(my_x_pos) < 0.35
    stage_edge = abs(my_x_pos) > 0.75
    opponent_cornered = abs(opponent_x_pos) > 0.8
    i_am_cornered = abs(my_x_pos) > 0.8
    
    if stage_center:
        position_factor += 0.12
    elif stage_edge:
        position_factor -= 0.18
    
    if opponent_cornered:
        position_factor += 0.15
    elif i_am_cornered:
        position_factor -= 0.2
    
    # Momentum calculation based on velocities and recent actions
    velocity_advantage = (abs(my_x_vel) + abs(my_y_vel)) - (abs(opponent_x_vel) + abs(opponent_y_vel))
    momentum_factor = velocity_advantage * 0.2
    
    # Tactical advantage from cooldowns and states
    if my_projectile_cooldown < 0.2 and opponent_projectile_cooldown > 0.5:
        tactical_factor += 0.18
    elif my_projectile_cooldown > 0.5 and opponent_projectile_cooldown < 0.2:
        tactical_factor -= 0.15
    
    if my_stunned > 0.3:
        tactical_factor -= 0.4
    elif opponent_stunned > 0.3:
        tactical_factor += 0.35
    
    # Calculate final aggression level
    current_aggression = max(0.1, min(0.95, 
        base_aggression + health_factor + position_factor + momentum_factor + tactical_factor))
    
    # Enhanced opponent behavior analysis and prediction
    opponent_velocity_total = abs(opponent_x_vel) + abs(opponent_y_vel)
    opponent_mobile = opponent_velocity_total > 0.08
    opponent_stationary = opponent_velocity_total < 0.03
    
    # Directional movement prediction with timing
    opponent_advancing = False
    opponent_retreating = False
    opponent_flanking = False
    
    if distance > 0.05:  # Only analyze if not touching
        if relative_pos > 0.1 and opponent_x_vel > 0.04:
            opponent_advancing = True
        elif relative_pos < -0.1 and opponent_x_vel < -0.04:
            opponent_advancing = True
        elif relative_pos > 0.1 and opponent_x_vel < -0.04:
            opponent_retreating = True
        elif relative_pos < -0.1 and opponent_x_vel > 0.04:
            opponent_retreating = True
        elif opponent_mobile and abs(opponent_y_vel) > 0.05:
            opponent_flanking = True
    
    # Advanced fighting style recognition
    opponent_rusher = opponent_advancing and opponent_attacking > 0.4 and distance < 0.25
    opponent_zoner = opponent_projectile_cooldown < 0.3 and distance > 0.35 and opponent_retreating
    opponent_turtle = opponent_blocking > 0.6 and opponent_stationary
    opponent_jumper = abs(opponent_y_vel) > 0.15 or abs(height_diff) > 0.25
    opponent_counter_fighter = opponent_blocking > 0.4 and opponent_attacking > 0.3
    
    # Emergency survival protocols
    if my_stunned > 0.4:
        return 0  # Can't act while stunned
    
    if my_health < critical_health or health_advantage < -0.6:
        # Critical health survival mode
        if distance < close_range and opponent_attacking > 0.7:
            return 6  # Emergency block
        elif distance < medium_range:
            if i_am_cornered:
                # Corner escape sequences
                if opponent_advancing:
                    escape_roll = random.random()
                    if escape_roll < 0.4:
                        return 3  # Jump escape
                    elif escape_roll < 0.7:
                        return 6  # Block and wait
                    else:
                        return 4 if random.random() < 0.6 else 5  # Desperate attack
                else:
                    # Safe corner play
                    if my_projectile_cooldown < 0.25:
                        return 9
                    else:
                        return 6
            else:
                # Mid-stage retreat
                retreat_choice = random.random()
                if retreat_choice < 0.5:
                    return 7 if relative_pos > 0 else 8  # Defensive movement
                elif retreat_choice < 0.75:
                    return 6  # Block
                else:
                    return 3  # Jump retreat
        else:
            # Long range survival
            if my_projectile_cooldown < 0.3:
                return 9