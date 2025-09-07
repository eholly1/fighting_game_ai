"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_027
Rank: 83/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 173.54
- Win Rate: 50.0%
- Average Reward: 247.92

Created: 2025-06-01 02:16:30
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
    
    # Extract my fighter status
    my_health = state[1] if len(state) > 1 else 1.0
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent status
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define tactical ranges
    touching_range = 0.06
    ultra_close_range = 0.12
    close_range = 0.2
    medium_range = 0.35
    far_range = 0.55
    
    # Balanced aggression calculation with adaptive elements
    base_aggression = 0.65
    health_factor = 0.3 * health_advantage
    position_factor = 0.1 if 0.25 < my_pos_x < 0.75 else -0.1
    distance_factor = 0.2 if distance < close_range else -0.1
    current_aggression = max(0.2, min(0.9, base_aggression + health_factor + position_factor + distance_factor))
    
    # Opponent behavioral analysis
    opponent_retreating = False
    opponent_aggressive = False
    opponent_defensive = False
    
    if distance > ultra_close_range:
        if relative_pos > 0 and opponent_velocity_x < -0.15:
            opponent_retreating = True
        elif relative_pos < 0 and opponent_velocity_x > 0.15:
            opponent_retreating = True
    
    if opponent_attack_status > 0.4 or (distance < close_range and abs(opponent_velocity_x) > 0.1):
        opponent_aggressive = True
    
    if opponent_block_status > 0.5 or (opponent_attack_status < 0.2 and distance < medium_range):
        opponent_defensive = True
    
    # Critical health management
    if my_health < 0.2:
        if health_advantage < -0.4:
            # Defensive survival mode
            if opponent_attack_status > 0.6:
                return 6  # Block incoming attack
            if distance > medium_range and my_projectile_cooldown < 0.3:
                return 9  # Keep distance with projectiles
            # Retreat while blocking
            if my_pos_x < 0.3:
                return 8  # Move right while blocking
            elif my_pos_x > 0.7:
                return 7  # Move left while blocking
            else:
                return 6  # Block in center
        else:
            # Calculated risk taking
            if distance < close_range and opponent_health < 0.3:
                # Go for risky finisher
                attack_choice = random.random()
                if attack_choice < 0.6:
                    return 5  # Kick for higher damage
                else:
                    return 4  # Punch for speed
    
    # Corner management system
    opponent_cornered = opponent_pos_x < 0.18 or opponent_pos_x > 0.82
    i_am_cornered = my_pos_x < 0.18 or my_pos_x > 0.82
    
    # Escape corner tactics
    if i_am_cornered:
        if distance < close_range and opponent_aggressive:
            # Block and escape
            escape_direction = 8 if my_pos_x < 0.5 else 7
            if opponent_attack_status > 0.5:
                return escape_direction
            else:
                # Quick escape without blocking
                return 2 if my_pos_x < 0.5 else 1
        elif distance < medium_range:
            # Jump over opponent or dash out
            if random.random() < 0.35:
                return 3  # Jump escape
            else:
                return 2 if my_pos_x < 0.5 else 1
    
    # Corner pressure tactics
    if opponent_cornered and distance < medium_range:
        current_aggression = min(0.85, current_aggression + 0.15)
        # Mix up attacks to prevent easy escapes
        if distance < close_range:
            if opponent_block_status > 0.6:
                # Break guard with varied attacks
                guard_break = random.random()
                if guard_break < 0.25:
                    return 3  # Jump for overhead
                elif guard_break < 0.4 and my_projectile_cooldown < 0.4:
                    return 9  # Projectile pressure
                else:
                    return 5  # Strong kick
            else:
                # Standard corner pressure
                return 4 if random.random() < 0.7 else 5
    
    # Range-based tactical decisions
    if distance <= touching_range:
        # Point blank range
        if opponent_attack_status > 0.7:
            # Opponent attacking, need to block or counter
            if random.random() < 0.3:
                return 6  # Block
            else:
                # Counter attack
                return 4  # Quick punch counter
        else:
            # Free to attack
            if health_advantage > 0.2:
                # Winning, be aggressive
                return 5 if random.random() < 0.6 else 4
            else:
                # Even or losing, be careful
                if opponent_block_status > 0.5:
                    return 6  # Respect their block
                else:
                    return 4  # Quick safe attack
    
    elif distance <= ultra_close_range:
        # Ultra close combat
        if opponent_aggressive and my_health > 0.4:
            # Trade hits when healthy
            attack_type = random.random()
            if attack_type < 0.5:
                return 4  # Punch
            elif attack_type < 0.8:
                return 5  # Kick
            else:
                return 6  # Block and counter
        elif opponent_defensive:
            # Break defensive play
            if opponent_block_status > 0.6:
                pressure_option = random.random()
                if pressure_option < 0.3:
                    return 3  # Jump overhead
                elif pressure_option < 0.5 and my_projectile_cooldown < 0.5:
                    return 9  # Projectile pressure
                else:
                    return 5  # Strong attack
            else:
                return 4 if random.random() < 0.7 else 5
        else:
            # Standard close combat
            if random.random() < current_aggression:
                return