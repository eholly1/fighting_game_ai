"""
Evolutionary Agent: gen1_agent_003
==================================

Metadata:
{
  "generation": 1,
  "fitness": 275.29999999999444,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 0d717d11e44f1cd2
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
    
    # Define enhanced rushdown ranges
    touching_range = 0.05
    ultra_close_range = 0.1
    close_range = 0.18
    medium_range = 0.32
    far_range = 0.5
    
    # Advanced aggression calculation
    base_aggression = 0.85
    health_multiplier = 1.0 + (health_advantage * 0.3)
    position_multiplier = 1.1 if my_pos_x > 0.3 and my_pos_x < 0.7 else 0.9
    current_aggression = min(0.95, base_aggression * health_multiplier * position_multiplier)
    
    # Opponent behavior analysis
    opponent_retreating = False
    opponent_aggressive = False
    
    if relative_pos > 0 and opponent_velocity_x < -0.2:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_velocity_x > 0.2:
        opponent_retreating = True
    
    if opponent_attack_status > 0.5 or (distance < close_range and opponent_velocity_x > 0.1):
        opponent_aggressive = True
    
    # Critical health emergency protocols
    if my_health < 0.15 and health_advantage < -0.5:
        if opponent_attack_status > 0.6:
            return 6  # Desperate block
        if distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Desperation projectile
        # Try to escape while blocking
        if my_pos_x < 0.2:
            return 8  # Move right while blocking
        elif my_pos_x > 0.8:
            return 7  # Move left while blocking
        else:
            return 6  # Just block
    
    # Corner pressure detection and exploitation
    opponent_cornered = opponent_pos_x < 0.15 or opponent_pos_x > 0.85
    i_am_cornered = my_pos_x < 0.15 or my_pos_x > 0.85
    
    # Escape corner when cornered
    if i_am_cornered and distance < close_range:
        if opponent_attack_status > 0.4:
            # Block and move toward center
            if my_pos_x < 0.5:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
        else:
            # Jump over or dash out
            if random.random() < 0.4:
                return 3  # Jump
            else:
                if my_pos_x < 0.5:
                    return 2  # Move right
                else:
                    return 1  # Move left
    
    # Ultra-aggressive corner pressure when opponent is cornered
    if opponent_cornered and distance < medium_range:
        current_aggression = min(0.98, current_aggression + 0.15)
    
    # Enhanced distance closing logic
    if distance > ultra_close_range:
        # Long range approach
        if distance > far_range:
            # Mix projectiles with aggressive advance
            if my_projectile_cooldown < 0.3:
                if random.random() < 0.35:
                    return 9  # Projectile
            
            # Advance with occasional jump-ins
            advance_method = random.random()
            if advance_method < 0.15 and abs(height_diff) < 0.4:
                return 3  # Jump approach
            else:
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        # Medium-far range tactical approach
        elif distance > medium_range:
            # Punish opponent projectile attempts
            if opponent_projectile_cooldown > 0.7:
                # Opponent likely used projectile, rush in
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            
            # Standard advance with mixups
            if random.random() < current_aggression:
                approach_type = random.random()
                if approach_type < 0.7:
                    # Ground approach
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                elif approach_type < 0.85:
                    # Jump approach
                    return 3
                else:
                    # Projectile then advance
                    if my_projectile_cooldown < 0.4:
                        return 9
                    else:
                        return 1 if relative_pos < 0 else 2
            else:
                # Cautious advance
                if opponent_attack_status > 0.3:
                    if relative_pos > 0:
                        return 8  # Move right while blocking
                    else:
                        return 7  # Move left while blocking
                else:
                    return 1 if relative_pos < 0 else 2
        
        # Medium range preparation
        elif distance > close_range:
            # Counter opponent retreat attempts
            if opponent_retreating:
                chase_intensity = current_aggression + 0.1
                if random.random() < chase_intensity:
                    if relative_pos > 0:
                        return 2  # Aggressive chase
                    else:
                        return 1
                else:
                    return 3  # Jump chase
            
            # Handle opponent blocking
            if opponent_block_status > 0.6:
                guard_break_option = random.random()
                if guard_break_option < 0.3 and my_projectile_cooldown < 0.5:
                    return 9  # Projectile to break guard
                elif guard_break_option < 0.6:
                    return 3  # Jump for overhead
                else:
                    # Close distance for throw
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
            
            # Standard medium range rush
            rush_decision = random.random()
            if rush_decision < current_aggression:
                if relative_pos > 0:
                    return 2