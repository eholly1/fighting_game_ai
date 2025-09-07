"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_025
Rank: 97/100
Generation: 0
Fighting Style: rushdown

Performance Metrics:
- Fitness: 127.94
- Win Rate: 0.0%
- Average Reward: 127.94

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
    # Validate and extract key state information
    if len(state) < 26:
        return 4  # Default to punch if invalid state
    
    # Core state variables with bounds checking
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Player state information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[2] if len(state) > 2 else 0.0
    my_velocity_y = state[3] if len(state) > 3 else 0.0
    my_attack_cooldown = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = state[6] if len(state) > 6 else 0.0
    my_stun_timer = state[7] if len(state) > 7 else 0.0
    
    # Opponent state information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[13] if len(state) > 13 else 0.0
    opp_velocity_y = state[14] if len(state) > 14 else 0.0
    opp_attack_cooldown = state[15] if len(state) > 15 else 0.0
    opp_block_status = state[16] if len(state) > 16 else 0.0
    opp_projectile_cooldown = state[17] if len(state) > 17 else 0.0
    opp_stun_timer = state[18] if len(state) > 18 else 0.0
    
    # RUSHDOWN STYLE: Define aggressive tactical ranges
    ultra_close_range = 0.08  # Immediate attack range
    close_range = 0.15        # Primary engagement zone
    rush_range = 0.25         # Distance to start rushing in
    max_engage_range = 0.4    # Maximum distance to engage
    
    # Aggression parameters for rushdown style
    base_aggression = 0.8     # High base aggression
    winning_aggression = 0.95 # Even more aggressive when winning
    losing_aggression = 0.6   # Still aggressive when losing
    
    # Calculate current aggression level
    if health_advantage > 0.2:
        current_aggression = winning_aggression
    elif health_advantage < -0.2:
        current_aggression = losing_aggression
    else:
        current_aggression = base_aggression
    
    # Check if we're stunned or in cooldown
    if my_stun_timer > 0:
        return 6  # Block while stunned
    
    # Emergency defensive measures - even rushdown needs some defense
    if my_health < 0.2 and opp_attack_cooldown < 0.3 and distance < close_range:
        if random.random() < 0.4:  # Still sometimes attack even when low
            return 6  # Block when critically low and opponent can attack
    
    # ULTRA CLOSE RANGE - Maximum aggression
    if distance < ultra_close_range:
        # Opponent is stunned or in cooldown - go for kill
        if opp_stun_timer > 0 or opp_attack_cooldown > 0.5:
            if my_attack_cooldown < 0.2:
                # Mix up attacks for unpredictability
                attack_choice = random.random()
                if attack_choice < 0.6:
                    return 4  # Punch - faster
                else:
                    return 5  # Kick - stronger
        
        # Opponent can counter-attack
        if opp_attack_cooldown < 0.3 and opp_block_status < 0.5:
            # High risk, high reward - trade blows
            if random.random() < current_aggression:
                return 4  # Quick punch to interrupt
            else:
                return 6  # Brief block then continue pressure
        
        # Default ultra-close behavior
        if my_attack_cooldown < 0.3:
            return 4 if random.random() < 0.7 else 5
        else:
            return 6  # Block while in cooldown
    
    # CLOSE RANGE - Primary rushdown zone
    elif distance < close_range:
        # Check if opponent is blocking - mix up approach
        if opp_block_status > 0.5:
            # Opponent blocking - grab or throw timing mix-up
            if random.random() < 0.4:
                return 5  # Kick can sometimes break guard
            elif random.random() < 0.3:
                # Back off slightly then re-engage
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                return 4  # Keep pressure with punches
        
        # Opponent not blocking - aggressive attack
        if my_attack_cooldown < 0.4:
            # Height advantage consideration
            if abs(height_diff) > 0.3:
                return 3  # Jump to adjust height
            
            # Choose attack based on situation
            if opp_velocity_x != 0:  # Opponent moving
                return 4  # Quick punch to catch them
            else:  # Opponent stationary
                attack_roll = random.random()
                if attack_roll < 0.5:
                    return 4  # Punch
                elif attack_roll < 0.8:
                    return 5  # Kick
                else:
                    return 3  # Jump attack mix-up
        else:
            # In attack cooldown - maintain pressure with movement
            if relative_pos > 0.1:
                return 2  # Move right to stay close
            elif relative_pos < -0.1:
                return 1  # Move left to stay close
            else:
                return 6  # Block briefly
    
    # RUSH RANGE - Close the distance aggressively
    elif distance < rush_range:
        # This is prime rushdown territory - get in fast
        
        # Check if opponent is preparing projectile
        if opp_projectile_cooldown < 0.3 and distance > 0.2:
            # Rush in with block
            if relative_pos > 0:
                return 8  # Move right with block
            else:
                return 7  # Move left with block
        
        # Opponent is backing away - chase aggressively
        if (relative_pos > 0 and opp_velocity_x > 0) or (relative_pos < 0 and opp_velocity_x < 0):
            # Jump in to close distance faster
            if random.random() < 0.6:
                return 3  # Jump toward opponent
            else:
                # Direct rush
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        # Standard rush approach
        rush_method = random.random()
        if rush_method < 0.6:
            # Direct approach
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        elif rush_method < 0.8:
            # Jump approach
            return 3