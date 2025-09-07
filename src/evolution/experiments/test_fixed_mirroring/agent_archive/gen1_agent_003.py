"""
Evolutionary Agent: gen1_agent_003
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: e9cb5ef830789f20
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22])) if len(state) > 22 else 0.5
    relative_pos = max(-1.0, min(1.0, state[23])) if len(state) > 23 else 0.0
    health_advantage = max(-1.0, min(1.0, state[25])) if len(state) > 25 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    opponent_health = state[12] if len(state) > 12 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_velocity_y = state[15] if len(state) > 15 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    opponent_block_status = state[17] if len(state) > 17 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    opponent_attack_status = state[16] if len(state) > 16 else 0.0
    projectile_cooldown = state[10] if len(state) > 10 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Define enhanced aggressive tactical parameters
    close_range = 0.10
    medium_range = 0.25
    far_range = 0.40
    max_range = 0.6
    base_aggression = 0.85
    health_critical = 0.15
    health_panic_threshold = -0.5
    winning_threshold = 0.25
    pressure_distance = 0.32
    
    # Calculate opponent movement prediction
    opponent_moving_away = False
    if relative_pos > 0 and opponent_velocity_x < -0.1:
        opponent_moving_away = True
    elif relative_pos < 0 and opponent_velocity_x > 0.1:
        opponent_moving_away = True
    
    # Calculate dynamic aggression based on multiple factors
    aggression_modifier = 1.0
    if health_advantage > winning_threshold:
        aggression_modifier = 1.4  # Maximum aggression when winning
    elif health_advantage < health_panic_threshold:
        aggression_modifier = 0.7  # Controlled aggression when desperate
    
    # Increase aggression if opponent is retreating
    if opponent_moving_away:
        aggression_modifier *= 1.2
    
    # Boost aggression if opponent is blocking defensively
    if opponent_block_status > 0.6:
        aggression_modifier *= 1.3
    
    final_aggression = min(1.5, base_aggression * aggression_modifier)
    
    # Critical health emergency responses
    if my_health < health_critical:
        if opponent_attack_status > 0.6 and distance < close_range:
            return 6  # Emergency block
        elif distance > far_range and projectile_cooldown < 0.3:
            return 9  # Desperate projectile
        elif opponent_moving_away and distance < medium_range:
            # Chase desperately when low health
            if relative_pos > 0:
                return 2
            else:
                return 1
    
    # Counter-attack opportunities when opponent is attacking
    if opponent_attack_status > 0.5 and distance < close_range:
        counter_chance = random.random()
        if counter_chance < 0.4:
            return 5  # Counter with kick
        elif counter_chance < 0.65:
            return 4  # Counter with punch
        else:
            return 6  # Block and reset
    
    # Close range combat - enhanced aggression and mix-ups
    if distance < close_range:
        # Anti-block pressure tactics
        if opponent_block_status > 0.5:
            pressure_tactic = random.random()
            if pressure_tactic < 0.35:
                return 5  # Heavy kick to break guard
            elif pressure_tactic < 0.55:
                # Reposition for throw/grab simulation
                if abs(relative_pos) < 0.1:
                    return 3  # Jump for position change
                else:
                    return 4  # Quick punch
            elif pressure_tactic < 0.75:
                # Aggressive repositioning
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                return 4  # Persistent punch pressure
        
        # Exploit vulnerable opponent
        if opponent_attack_status < 0.2 and opponent_block_status < 0.3:
            # Maximum punishment
            punishment_roll = random.random()
            if punishment_roll < 0.6:
                return 5  # Strong kick for damage
            else:
                return 4  # Fast punch for combo potential
        
        # Standard close combat mix-up
        close_combat_choice = random.random()
        if close_combat_choice < 0.4:
            return 4  # Punch pressure
        elif close_combat_choice < 0.7:
            return 5  # Kick damage
        elif close_combat_choice < 0.85:
            # Brief defensive moment
            if opponent_attack_status > 0.4:
                return 6
            else:
                return 4
        else:
            # Mobility in close range
            return 3
    
    # Medium range - aggressive setup and pressure
    elif distance < medium_range:
        # Height differential tactics
        if abs(height_diff) > 0.25:
            if height_diff < -0.25:  # Opponent higher
                return 3  # Jump to close gap
            elif height_diff > 0.25 and opponent_velocity_y < 0:  # Opponent falling
                # Rush in for ground attack
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        # Punish defensive opponents
        if opponent_block_status > 0.6:
            rush_tactic = random.random()
            if rush_tactic < 0.6:
                # Direct aggressive advance
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif rush_tactic < 0.8:
                return 3  # Jump approach
            else:
                return 4  # Advancing punch
        
        # Pressure retreating opponents
        if opponent_moving_away:
            chase_method = random.random()
            if chase_method < 0.7:
                # Direct pursuit
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            elif chase_method < 0.85:
                return 3  # Jump chase
            else:
                # Projectile to cut off retreat
                if projectile_cooldown < 0.4:
                    return 9
                else:
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
        
        # Standard medium range aggression
        medium_aggression = random.random()
        if medium_aggression < 0.45:
            # Close distance
            if relative_pos > 0:
                return 2
            else:
                return 1
        elif medium_aggression < 0.65:
            return