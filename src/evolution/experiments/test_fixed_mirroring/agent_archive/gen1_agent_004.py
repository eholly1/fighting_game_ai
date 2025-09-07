"""
Evolutionary Agent: gen1_agent_004
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 238de3c70a5e18e3
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
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cd = state[10] if len(state) > 10 else 0.0
    
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_attack_status = state[18] if len(state) > 18 else 0.0
    opp_block_status = state[19] if len(state) > 19 else 0.0
    opp_projectile_cd = state[21] if len(state) > 21 else 0.0
    
    # Define hybrid tactical parameters
    close_range = 0.11
    medium_range = 0.32
    far_range = 0.55
    critical_health = -0.5
    winning_health = 0.25
    momentum_threshold = 0.15
    
    # Calculate adaptive factors
    frame_rand = random.random()
    health_ratio = my_health / max(0.1, opp_health)
    momentum_factor = abs(my_velocity_x) + abs(opp_velocity_x)
    defensive_need = max(0.2, 1.0 - health_advantage)
    aggressive_opportunity = max(0.2, 0.8 + health_advantage)
    
    # Critical survival mode
    if health_advantage < critical_health or my_health < 0.15:
        if distance < close_range:
            if opp_attack_status > 0.6:
                return 6  # Emergency block
            elif opp_block_status < 0.3 and frame_rand < 0.4:
                return 4  # Desperate counter-attack
            elif relative_pos > 0:
                return 7  # Escape left with block
            else:
                return 8  # Escape right with block
        elif distance < medium_range:
            if my_projectile_cd < 0.4 and frame_rand < 0.7:
                return 9  # Projectile for space
            elif abs(height_diff) > 0.2:
                return 3  # Jump for positioning
            elif relative_pos > 0:
                return 1  # Create distance
            else:
                return 2  # Create distance
        else:
            if my_projectile_cd < 0.6:
                return 9  # Long range safety
            else:
                return 0  # Wait for cooldown
    
    # Opportunistic finishing mode
    elif health_advantage > winning_health and opp_health < 0.3:
        if distance < close_range:
            if opp_block_status > 0.5:
                finish_choice = frame_rand
                if finish_choice < 0.3:
                    return 5  # Heavy kick through block
                elif finish_choice < 0.5:
                    return 3  # Jump over block
                elif finish_choice < 0.7:
                    return 0  # Wait for opening
                else:
                    if relative_pos > 0:
                        return 2  # Reposition right
                    else:
                        return 1  # Reposition left
            else:
                if frame_rand < 0.5:
                    return 5  # Finishing kick
                else:
                    return 4  # Quick finisher
        elif distance < medium_range:
            if relative_pos > 0:
                return 2  # Close for kill
            else:
                return 1  # Close for kill
        else:
            if my_projectile_cd < 0.5:
                return 9  # Projectile pressure
            elif relative_pos > 0:
                return 2  # Advance
            else:
                return 1  # Advance
    
    # Hybrid balanced combat
    else:
        # Close range hybrid tactics
        if distance < close_range:
            # Opponent behavior analysis
            if opp_attack_status > 0.6:
                counter_choice = frame_rand * defensive_need
                if counter_choice < 0.4:
                    return 6  # Block and counter
                elif counter_choice < 0.6:
                    return 4  # Quick counter
                elif counter_choice < 0.75:
                    if relative_pos > 0:
                        return 7  # Block and move
                    else:
                        return 8  # Block and move
                else:
                    return 5  # Heavy counter
            
            elif opp_block_status > 0.5:
                block_break_choice = frame_rand * aggressive_opportunity
                if block_break_choice < 0.25:
                    return 0  # Wait for opening
                elif block_break_choice < 0.45:
                    return 5  # Heavy attack vs block
                elif block_break_choice < 0.65:
                    return 3  # Jump attack
                elif block_break_choice < 0.8:
                    if relative_pos > 0:
                        return 2  # Move for angle
                    else:
                        return 1  # Move for angle
                else:
                    return 4  # Quick poke
            
            else:
                # Open combat situation
                attack_pattern = frame_rand + (momentum_factor * 0.2)
                if attack_pattern < 0.35:
                    return 4  # Quick punch
                elif attack_pattern < 0.6:
                    return 5  # Power kick
                elif attack_pattern < 0.75:
                    return 6  # Defensive mix
                elif attack_pattern < 0.85:
                    return 3  # Jump mix
                else:
                    if my_velocity_x > 0.1:
                        return 1  # Counter momentum
                    else:
                        return 2  # Counter momentum
        
        # Medium range hybrid positioning
        elif distance < medium_range:
            # Height positioning consideration
            if abs(height_diff) > 0.35:
                if height_diff > 0.35:
                    # We have height advantage
                    if my_projectile_cd < 0.5 and frame_rand < 0.6:
                        return 9  # Projectile from above
                    elif frame_rand < 0.8:
                        if relative_pos > 0:
                            return 2  # Maintain position
                        else:
                            return 1  # Maintain position
                    else:
                        return 0  #