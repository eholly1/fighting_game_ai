"""
Evolutionary Agent: gen0_agent_004
==================================

Metadata:
{
  "generation": 0,
  "fitness": 71.44000000000443,
  "fighting_style": "adaptive",
  "win_rate": 0.5
}

Code Hash: 749e88d7b83b5902
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
    
    # Extract player and opponent state info
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cd = state[10] if len(state) > 10 else 0.0
    
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_attack_status = state[18] if len(state) > 18 else 0.0
    opp_block_status = state[19] if len(state) > 19 else 0.0
    
    # Define tactical ranges and thresholds
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    critical_health_diff = -0.4
    winning_health_diff = 0.3
    
    # Adaptive behavior tracking variables
    frame_randomness = random.random()
    aggression_factor = 0.5 + (health_advantage * 0.3)
    defensive_factor = max(0.1, 0.8 - health_advantage)
    
    # Emergency defensive behavior when losing badly
    if health_advantage < critical_health_diff:
        if distance < close_range:
            # In danger zone - prioritize blocking and escape
            if opp_attack_status > 0.5:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            # Try to create distance
            if my_projectile_cd < 0.3:
                return 9  # Projectile to keep distance
            elif relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        else:
            # Safe distance - use projectiles
            if my_projectile_cd < 0.5:
                return 9  # Projectile spam when losing
            else:
                return 0  # Wait for cooldown
    
    # Aggressive behavior when winning significantly
    elif health_advantage > winning_health_diff:
        if distance < close_range:
            # Go for the kill with varied attacks
            if opp_block_status > 0.5:
                # Opponent blocking - mix up timing
                if frame_randomness < 0.3:
                    return 0  # Wait then attack
                elif frame_randomness < 0.6:
                    return 5  # Heavy kick through block
                else:
                    return 4  # Quick punch
            else:
                # Opponent not blocking - aggressive assault
                if frame_randomness < 0.4:
                    return 5  # Power kick
                elif frame_randomness < 0.7:
                    return 4  # Quick punch
                else:
                    return 3  # Jump attack mix-up
        elif distance < medium_range:
            # Close the distance aggressively
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        else:
            # Long range pressure
            if my_projectile_cd < 0.4:
                return 9  # Projectile pressure
            elif relative_pos > 0:
                return 2  # Advance right
            else:
                return 1  # Advance left
    
    # Balanced adaptive strategy for even matchups
    else:
        # Close range tactical decisions
        if distance < close_range:
            # High risk/reward zone - careful decision making
            if opp_attack_status > 0.5:
                # Opponent attacking - defensive response
                if frame_randomness < defensive_factor:
                    return 6  # Block attack
                else:
                    # Counter-attack timing
                    if frame_randomness < 0.7:
                        return 4  # Quick counter punch
                    else:
                        return 5  # Heavy counter kick
            
            elif opp_block_status > 0.5:
                # Opponent blocking - break their defense
                if frame_randomness < 0.25:
                    return 0  # Wait for opening
                elif frame_randomness < 0.5:
                    return 5  # Heavy attack vs block
                elif frame_randomness < 0.75:
                    return 3  # Jump over block
                else:
                    # Reposition
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            
            else:
                # Open opponent - capitalize with attacks
                attack_choice = frame_randomness * aggression_factor
                if attack_choice < 0.2:
                    return 4  # Quick punch
                elif attack_choice < 0.35:
                    return 5  # Power kick  
                elif attack_choice < 0.45:
                    return 3  # Jump attack
                else:
                    # Mix in some defense
                    return 6  # Block to reset
        
        # Medium range positioning and tactics
        elif distance < medium_range:
            # Critical positioning zone
            if abs(height_diff) > 0.3:
                # Height advantage considerations
                if height_diff > 0:
                    # We're higher - projectile advantage
                    if my_projectile_cd < 0.6:
                        return 9  # Projectile from high ground
                    else:
                        return 0  # Wait for cooldown
                else:
                    # We're lower - close distance
                    if relative_pos > 0:
                        return 2  # Move right and up
                    else:
                        return 1  # Move left and up
            
            # Equal height medium range
            positioning_strategy = frame_randomness + (aggression_factor * 0.3)
            
            if positioning_strategy < 0.3:
                # Advance for attack
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            
            elif positioning_strategy < 0.5:
                # Projectile harassment  
                if my_projectile_cd < 0.7:
                    return 9  # Medium range projectile
                else:
                    # Can't projectile - reposition
                    if my_velocity_x > 0.1:
                        return 1  # Move left to change momentum
                    else:
                        return 2  # Move right to change momentum
            
            elif positioning_strategy < 0.7:
                # Defensive positioning
                if opp_attack_status > 0.3:
                    if relative_pos > 0:
                        return 7  # Move left while blocking
                    else:
                        return 8  # Move right while blocking
                else:
                    return 0  # Wait and observe
            
            else:
                # Jump tactics for unpredictability
                return 3  #