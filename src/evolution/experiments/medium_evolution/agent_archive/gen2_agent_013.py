"""
Evolutionary Agent: gen2_agent_013
==================================

Metadata:
{
  "generation": 2,
  "fitness": -3.360000000000948,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: dd290d885b47dbb5
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[1]))
    my_x_pos = max(0.0, min(1.0, state[0]))
    my_y_pos = state[2]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[5] > 0.5
    my_blocking = state[6] > 0.5
    my_stunned = state[7] > 0.5
    my_projectile_cd = max(0.0, state[8])
    my_attack_cd = max(0.0, state[9])
    my_block_cd = max(0.0, state[10])
    
    # Extract opponent status with bounds checking
    opp_health = max(0.0, min(1.0, state[12]))
    opp_x_pos = max(0.0, min(1.0, state[11]))
    opp_y_pos = state[13]
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = state[16] > 0.5
    opp_blocking = state[17] > 0.5
    opp_stunned = state[18] > 0.5
    opp_projectile_cd = max(0.0, state[19])
    opp_attack_cd = max(0.0, state[20])
    opp_block_cd = max(0.0, state[21])
    
    # Define hybrid tactical ranges and thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.30
    far_range = 0.50
    critical_health = 0.20
    low_health = 0.35
    winning_threshold = 0.20
    losing_threshold = -0.20
    wall_proximity = 0.12
    
    # Calculate position awareness
    near_left_edge = my_x_pos < wall_proximity
    near_right_edge = my_x_pos > (1.0 - wall_proximity)
    opp_near_left_edge = opp_x_pos < wall_proximity
    opp_near_right_edge = opp_x_pos > (1.0 - wall_proximity)
    cornered = (near_left_edge or near_right_edge) and distance < close_range
    opponent_cornered = (opp_near_left_edge or opp_near_right_edge) and distance < close_range
    
    # Dynamic aggression calculation for hybrid style
    base_aggression = 0.55  # Slightly aggressive hybrid baseline
    
    # Adjust aggression based on health situation
    if health_advantage > winning_threshold:
        aggression_factor = 0.75  # More aggressive when winning
    elif health_advantage < losing_threshold:
        aggression_factor = 0.35  # More defensive when losing
    else:
        aggression_factor = base_aggression
    
    # Modify based on health levels
    if my_health < critical_health:
        aggression_factor *= 0.6  # Much more cautious at critical health
    elif my_health < low_health:
        aggression_factor *= 0.8  # Somewhat more cautious at low health
    
    # Cannot act effectively while stunned
    if my_stunned:
        return 6 if my_block_cd < 0.3 else 0
    
    # Crisis mode - extremely low health and losing
    if my_health < critical_health and health_advantage < -0.3:
        if opp_attacking and distance < close_range:
            return 6  # Block desperately
        elif distance > medium_range:
            if my_projectile_cd < 0.2:
                return 9  # Projectile to maintain distance
            else:
                return 6  # Block while waiting for cooldown
        else:
            # Try to escape while defending
            if cornered:
                if near_left_edge:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
            else:
                # Move away from opponent
                if relative_pos > 0:
                    return 7  # Move left away
                else:
                    return 8  # Move right away
    
    # Capitalize on stunned opponent aggressively
    if opp_stunned:
        if distance < very_close_range:
            # Maximum damage at very close range
            return 5 if random.random() < 0.8 else 4
        elif distance < close_range:
            # Mix of attacks and positioning
            action_choice = random.random()
            if action_choice < 0.5:
                return 5  # Strong kick
            elif action_choice < 0.8:
                return 4  # Quick punch
            else:
                return 9 if my_projectile_cd < 0.3 else 5  # Surprise projectile
        elif distance < medium_range:
            # Close distance quickly
            if abs(relative_pos) > 0.2:
                return 2 if relative_pos > 0 else 1
            else:
                return 4  # Attack if close enough
        else:
            # Long range - projectile or advance
            return 9 if my_projectile_cd < 0.2 else (2 if relative_pos > 0 else 1)
    
    # Very close range combat (0-0.08)
    if distance < very_close_range:
        # Opponent is blocking - need guard break tactics
        if opp_blocking:
            guard_break_roll = random.random()
            if guard_break_roll < 0.3:
                return 5  # Strong kick to break guard
            elif guard_break_roll < 0.5:
                return 3  # Jump to change attack angle
            elif guard_break_roll < 0.7:
                # Try to reposition around guard
                if not near_right_edge and relative_pos < 0.3:
                    return 2  # Move right
                elif not near_left_edge and relative_pos > -0.3:
                    return 1  # Move left
                else:
                    return 5  # Default to kick
            else:
                return 4  # Quick punch
        
        # Opponent attacking - counter or defend
        elif opp_attacking:
            if health_advantage < losing_threshold:
                return 6  # Prioritize defense when losing
            else:
                counter_choice = random.random()
                if counter_choice < 0.4:
                    return 6  # Block first
                elif counter_choice < 0.7:
                    return 4  # Quick counter
                else:
                    return 5  # Strong counter
        
        # Neutral very close combat
        else:
            if aggression_factor > 0.6:
                # High aggression close combat
                attack_roll = random.random()
                if attack_roll < 0.4:
                    return 4  # Fast punch
                elif attack_roll < 0.7:
                    return 5  # Strong kick
                elif attack_roll < 0.85:
                    return 3  # Jump attack setup
                else:
                    return 6  # Mix in defense
            else:
                # Cautious close combat
                careful_roll = random.random()
                if careful_roll < 0.3:
                    return 6  # Block more