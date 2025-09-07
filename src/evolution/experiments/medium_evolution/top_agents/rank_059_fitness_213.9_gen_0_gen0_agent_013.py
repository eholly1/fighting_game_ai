"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_013
Rank: 59/100
Generation: 0
Fighting Style: balanced

Performance Metrics:
- Fitness: 213.91
- Win Rate: 50.0%
- Average Reward: 305.59

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
    
    # Extract fighter status information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    
    # Define strategic thresholds
    close_range = 0.15
    medium_range = 0.35
    critical_health = 0.25
    winning_threshold = 0.2
    losing_threshold = -0.2
    
    # Calculate dynamic factors
    is_airborne = abs(my_y_pos) > 0.1 or abs(my_velocity_y) > 0.1
    opponent_attacking = opp_attack_status > 0.5
    opponent_blocking = opp_block_status > 0.5
    opponent_airborne = abs(height_diff) > 0.2
    
    # Emergency defensive actions
    if my_health < critical_health and health_advantage < -0.4:
        if opponent_attacking and distance < 0.25:
            return 6  # Block incoming attack
        if distance > 0.6 and my_projectile_cooldown < 0.3:
            return 9  # Keep distance with projectile
        if relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Aggressive winning strategy
    if health_advantage > winning_threshold and my_health > 0.4:
        if distance < close_range:
            if opponent_blocking:
                # Mix up attacks to break guard
                attack_choice = random.random()
                if attack_choice < 0.4:
                    return 5  # Strong kick
                elif attack_choice < 0.7:
                    return 4  # Fast punch
                else:
                    return 3  # Jump to mix timing
            else:
                # Go for damage
                if random.random() < 0.65:
                    return 4  # Fast punch combo
                else:
                    return 5  # Power kick
        
        elif distance < medium_range:
            # Aggressive positioning
            if opponent_airborne:
                return 4  # Punish landing
            if relative_pos > 0.1:
                return 2  # Chase right
            elif relative_pos < -0.1:
                return 1  # Chase left
            else:
                return 4  # Quick attack
        
        else:
            # Long range pressure
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile pressure
            else:
                if relative_pos > 0:
                    return 2  # Close distance
                else:
                    return 1  # Close distance
    
    # Defensive/cautious strategy when losing
    elif health_advantage < losing_threshold:
        if distance < close_range:
            if opponent_attacking:
                return 6  # Block attack
            elif opponent_blocking:
                # Try to reset neutral
                if abs(my_x_pos) > 0.7:  # Near corner
                    if my_x_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
                else:
                    return 3  # Jump to reset
            else:
                # Quick counterattack
                if random.random() < 0.4:
                    return 4  # Safe punch
                else:
                    return 6  # Play defensive
        
        elif distance < medium_range:
            # Careful spacing
            if opponent_attacking or opp_velocity_x > 0.3:
                return 6  # Block approaching attack
            
            # Zone control
            if my_projectile_cooldown < 0.4:
                return 9  # Projectile for space
            
            # Positioning
            if abs(my_x_pos) > 0.6:  # Avoid corner
                if my_x_pos > 0:
                    return 1  # Move toward center
                else:
                    return 2  # Move toward center
            else:
                if distance > 0.25:
                    return 6  # Patient blocking
                else:
                    return 4  # Quick poke
        
        else:
            # Long range defensive
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile to control space
            else:
                return 6  # Block and wait
    
    # Balanced neutral game strategy
    else:
        if distance < close_range:
            # Close range mix-ups
            if opponent_blocking:
                action_roll = random.random()
                if action_roll < 0.25:
                    return 5  # Kick to break guard
                elif action_roll < 0.45:
                    return 3  # Jump for timing mix
                elif action_roll < 0.7:
                    return 4  # Fast punch
                else:
                    return 6  # Block and reset
            
            elif opponent_attacking:
                counter_roll = random.random()
                if counter_roll < 0.6:
                    return 6  # Block then counter
                elif counter_roll < 0.8:
                    return 4  # Trade with punch
                else:
                    return 3  # Jump over attack
            
            else:
                # Neutral close game
                if random.random() < 0.5:
                    return 4  # Punch pressure
                else:
                    return 5  # Kick threat
        
        elif distance < medium_range:
            # Medium range footsies
            if opponent_airborne:
                return 4  # Anti-air punch
            
            if my_projectile_cooldown < 0.4 and random.random() < 0.3:
                return 9  # Occasional projectile
            
            # Movement game
            movement_decision = random.random()
            if movement_decision < 0.3:
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif movement_decision < 0.5:
                return 4  # Poke with punch
            elif movement_decision < 0.7:
                return 6  # Block and observe
            else:
                return 3