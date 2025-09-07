"""
Evolutionary Agent: gen3_agent_022
==================================

Metadata:
{
  "generation": 3,
  "fitness": 190.01999999999174,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 5579f7eeff844f7e
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information with enhanced bounds checking
    distance = max(0.0, min(1.0, state[22] if len(state) > 22 else 0.5))
    relative_pos = max(-1.0, min(1.0, state[23] if len(state) > 23 else 0.0))
    health_advantage = max(-1.0, min(1.0, state[25] if len(state) > 25 else 0.0))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract comprehensive fighter status
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 0.5))
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.4 if len(state) > 5 else False
    my_blocking = state[6] > 0.4 if len(state) > 6 else False
    my_stunned = state[7] > 0.4 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Opponent comprehensive status
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 0.5))
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.4 if len(state) > 16 else False
    opp_blocking = state[17] > 0.4 if len(state) > 17 else False
    opp_stunned = state[18] > 0.4 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Enhanced hybrid strategy parameters
    strike_range = 0.10
    close_range = 0.16
    medium_range = 0.32
    far_range = 0.48
    optimal_range = 0.24
    critical_health = 0.18
    low_health = 0.35
    winning_threshold = 0.15
    losing_threshold = -0.20
    
    # Advanced stage positioning analysis
    stage_center = 0.5
    left_wall = 0.12
    right_wall = 0.88
    corner_zone = 0.18
    my_near_left_wall = my_x_pos < corner_zone
    my_near_right_wall = my_x_pos > (1.0 - corner_zone)
    my_cornered = my_near_left_wall or my_near_right_wall
    opp_near_left_wall = opp_x_pos < corner_zone
    opp_near_right_wall = opp_x_pos > (1.0 - corner_zone)
    opp_cornered = opp_near_left_wall or opp_near_right_wall
    
    # Enhanced movement and timing analysis
    opponent_approaching = (relative_pos > 0 and opp_x_velocity < -0.15) or (relative_pos < 0 and opp_x_velocity > 0.15)
    opponent_retreating = (relative_pos > 0 and opp_x_velocity > 0.15) or (relative_pos < 0 and opp_x_velocity < -0.15)
    opponent_jumping = abs(opp_y_velocity) > 0.2
    my_momentum = abs(my_x_velocity)
    opp_momentum = abs(opp_x_velocity)
    combined_momentum = my_momentum + opp_momentum
    
    # Cooldown and readiness assessment
    projectile_ready = my_projectile_cooldown < 0.08
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.1
    opp_projectile_threat = opp_projectile_cooldown < 0.1
    opp_attack_threat = opp_attack_cooldown < 0.15
    
    # Threat and opportunity assessment
    immediate_danger = opp_attacking and distance < close_range
    projectile_danger = opp_projectile_threat and distance > medium_range
    counter_opportunity = opp_attacking or opp_stunned
    finishing_opportunity = opp_health < critical_health and health_advantage > 0
    
    # Randomization for unpredictability
    randomness = random.random()
    tactical_choice = random.random()
    
    # Emergency defensive state - cannot act while stunned
    if my_stunned:
        return 0
    
    # Ultra-critical health survival protocol
    if my_health <= critical_health or health_advantage < -0.45:
        if immediate_danger:
            if block_ready:
                return 6  # Emergency block
            elif distance > 0.05:
                return 3  # Desperate jump
            else:
                return 0  # Cannot avoid
        
        if distance < close_range:
            # Emergency escape tactics
            if my_cornered:
                if abs(height_diff) < 0.2 and randomness < 0.6:
                    return 3  # Jump escape from corner
                elif block_ready:
                    return 6  # Corner defense
                else:
                    return 0  # Wait for opportunity
            else:
                # Mobile escape with protection
                escape_direction = randomness
                if escape_direction < 0.4:
                    return 7 if relative_pos > 0 else 8  # Protected retreat
                elif escape_direction < 0.7:
                    return 1 if relative_pos > 0 else 2  # Quick retreat
                else:
                    return 3  # Jump retreat
        
        elif distance < medium_range:
            # Create safe distance while threatening
            if projectile_ready and randomness < 0.7:
                return 9  # Desperate projectile
            elif not my_cornered:
                return 1 if relative_pos > 0 else 2  # Continue retreat
            else:
                return 6 if block_ready else 0  # Defensive waiting
        
        else:
            # Safe distance - projectile harassment
            if projectile_ready:
                return 9
            elif opponent_approaching and block_ready:
                return 6  # Prepare for incoming
            else:
                return 0