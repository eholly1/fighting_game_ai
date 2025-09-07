"""
Evolutionary Agent: gen4_agent_009
==================================

Metadata:
{
  "generation": 4,
  "fitness": 313.8800000000029,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 35db36c229f73cd1
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(0.0, min(1.0, state[2] if len(state) > 2 else 0.5))
    my_velocity_x = max(-1.0, min(1.0, state[4] if len(state) > 4 else 0.0))
    my_attack_status = max(0.0, min(1.0, state[7] if len(state) > 7 else 0.0))
    my_block_status = max(0.0, min(1.0, state[8] if len(state) > 8 else 0.0))
    my_projectile_cooldown = max(0.0, min(1.0, state[10] if len(state) > 10 else 0.0))
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = max(0.0, min(1.0, state[13] if len(state) > 13 else 0.5))
    opponent_velocity_x = max(-1.0, min(1.0, state[15] if len(state) > 15 else 0.0))
    opponent_attack_status = max(0.0, min(1.0, state[18] if len(state) > 18 else 0.0))
    opponent_block_status = max(0.0, min(1.0, state[19] if len(state) > 19 else 0.0))
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21] if len(state) > 21 else 0.0))
    
    # Enhanced rushdown tactical parameters
    ultra_close_range = 0.06
    close_range = 0.12
    medium_close_range = 0.2
    medium_range = 0.3
    far_range = 0.45
    
    # Dynamic aggression system
    base_aggression = 0.85
    health_multiplier = 1.0 + (health_advantage * 0.3)
    momentum_multiplier = 1.0
    
    # Calculate momentum based on recent positioning
    if distance < close_range and my_velocity_x != 0:
        momentum_multiplier = 1.15
    elif distance > medium_range and abs(my_velocity_x) < 0.1:
        momentum_multiplier = 0.9
    
    current_aggression = min(0.95, base_aggression * health_multiplier * momentum_multiplier)
    
    # Critical health emergency protocols
    if my_health < 0.15:
        if opponent_attack_status > 0.6:
            return 6  # Desperate block
        if distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Last resort projectile
        if distance < close_range and opponent_health > 0.4:
            # Try to escape when critically low
            escape_direction = 7 if relative_pos > 0 else 8
            return escape_direction
    
    # Opponent pattern recognition
    opponent_defensive = opponent_block_status > 0.5
    opponent_aggressive = opponent_attack_status > 0.4
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.2) or (relative_pos < 0 and opponent_velocity_x > 0.2)
    opponent_stationary = abs(opponent_velocity_x) < 0.1
    
    # Corner detection and exploitation
    opponent_cornered = (opponent_pos_x < 0.15) or (opponent_pos_x > 0.85)
    im_cornered = (my_pos_x < 0.15) or (my_pos_x > 0.85)
    
    # Escape corner when pressured
    if im_cornered and distance < medium_close_range and opponent_aggressive:
        if my_pos_x < 0.15:
            return 8 if opponent_attack_status > 0.6 else 2  # Move right, block if needed
        else:
            return 7 if opponent_attack_status > 0.6 else 1  # Move left, block if needed
    
    # Enhanced distance-based rushdown strategy
    if distance > ultra_close_range:
        
        # Long range: Setup and projectile pressure
        if distance > far_range:
            if my_projectile_cooldown < 0.3:
                # Use projectiles to control space and approach
                if opponent_stationary or opponent_defensive:
                    return 9
                elif random.random() < 0.4:
                    return 9
            
            # Aggressive advance with occasional jump-ins
            advance_method = random.random()
            if advance_method < 0.15 and abs(height_diff) < 0.4:
                return 3  # Jump approach
            elif relative_pos > 0:
                return 2  # Ground advance right
            else:
                return 1  # Ground advance left
        
        # Medium-far range: Increase pressure
        elif distance > medium_range:
            if opponent_retreating:
                # Chase aggressively
                chase_speed = current_aggression + 0.1
                if random.random() < chase_speed:
                    if abs(height_diff) < 0.2 and random.random() < 0.2:
                        return 3  # Jump chase
                    elif relative_pos > 0:
                        return 2
                    else:
                        return 1
            
            # Mix projectiles with advance
            if my_projectile_cooldown < 0.4 and random.random() < 0.3:
                return 9
            elif relative_pos > 0:
                return 2
            else:
                return 1
        
        # Medium-close range: Prepare for engagement
        elif distance > medium_close_range:
            if opponent_defensive:
                # Setup for guard break
                if my_projectile_cooldown < 0.5 and random.random() < 0.25:
                    return 9  # Projectile to test guard
                elif random.random() < 0.3:
                    return 3  # Jump for overhead setup
                else:
                    # Continue advance
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
            elif opponent_aggressive:
                # Counter-approach with blocking advance
                if random.random() < 0.4:
                    return 8 if relative_pos > 0 else 7
                else:
                    return 2 if relative_pos > 0 else 1
            else:
                # Standard advance
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        # Close range: Final approach phase
        elif distance > close_range:
            if opponent_attack_status > 0.5:
                # Opponent attacking, block and advance or counter
                if my_health < opponent_health * 0.8:
                    return 8 if relative_pos > 0 else 7  # Block advance
                elif random.random() < 0.3:
                    return 6  # Pure block
                else:
                    return