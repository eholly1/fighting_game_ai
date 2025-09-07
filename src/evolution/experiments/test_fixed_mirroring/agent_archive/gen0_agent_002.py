"""
Evolutionary Agent: gen0_agent_002
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "zoner",
  "win_rate": 0.5
}

Code Hash: dfe1c2217fd0614a
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
    
    # Extract fighter status information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    
    # Define zoner strategy constants
    optimal_range_min = 0.25
    optimal_range_max = 0.45
    danger_zone = 0.18
    max_range = 0.6
    
    # Health-based aggression modifiers
    desperate_threshold = -0.4
    winning_threshold = 0.3
    dominating_threshold = 0.6
    
    # Stage positioning awareness
    stage_left_limit = 0.1
    stage_right_limit = 0.9
    corner_danger_zone = 0.15
    
    # Calculate stage position risks
    near_left_edge = my_x_pos < stage_left_limit + corner_danger_zone
    near_right_edge = my_x_pos > stage_right_limit - corner_danger_zone
    opponent_cornering_me = (near_left_edge and relative_pos < 0) or (near_right_edge and relative_pos > 0)
    
    # Projectile availability check
    projectile_ready = my_projectile_cooldown <= 0.1
    
    # Opponent behavior analysis
    opponent_rushing = abs(opp_velocity_x) > 0.3 and distance < 0.3
    opponent_jumping = opp_velocity_y > 0.2
    opponent_retreating = (relative_pos > 0 and opp_velocity_x < -0.2) or (relative_pos < 0 and opp_velocity_x > 0.2)
    
    # Emergency defensive situations
    if health_advantage < desperate_threshold and my_health < 0.25:
        if distance < danger_zone:
            if opp_attacking > 0.5:
                return 6  # Block incoming attack
            elif opponent_cornering_me:
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
            else:
                return 6  # Default block
        elif distance < optimal_range_min and projectile_ready:
            return 9  # Desperate projectile
        elif not opponent_cornering_me:
            if relative_pos > 0:
                return 1  # Retreat left
            else:
                return 2  # Retreat right
        else:
            return 6  # Block if cornered
    
    # Handle being rushed or pressured
    if opponent_rushing and distance < danger_zone:
        if opp_attacking > 0.5:
            return 6  # Block the rush
        elif projectile_ready and random.random() < 0.4:
            return 9  # Quick projectile
        elif not opponent_cornering_me:
            if relative_pos > 0 and not near_left_edge:
                return 7  # Retreat left with block
            elif relative_pos < 0 and not near_right_edge:
                return 8  # Retreat right with block
            else:
                return 6  # Block in place
        else:
            if health_advantage > -0.2:
                return 4  # Counter punch
            else:
                return 6  # Defensive block
    
    # Optimal zoning range - primary gameplan
    if distance >= optimal_range_min and distance <= optimal_range_max:
        if projectile_ready:
            # Consider opponent movement for projectile timing
            if opponent_jumping:
                if random.random() < 0.8:
                    return 9  # High chance to punish jump
            elif opp_blocking > 0.5:
                if random.random() < 0.6:
                    return 9  # Pressure blocking opponent
            elif opponent_retreating:
                if random.random() < 0.7:
                    return 9  # Chase with projectile
            else:
                if random.random() < 0.85:
                    return 9  # Standard zoning projectile
        
        # Maintain optimal spacing when projectile not ready
        if distance < optimal_range_min + 0.05:
            if relative_pos > 0 and not near_left_edge:
                return 1  # Back up left
            elif relative_pos < 0 and not near_right_edge:
                return 2  # Back up right
            else:
                return 0  # Stay put if cornered
        elif distance > optimal_range_max - 0.05:
            if relative_pos > 0:
                return 2  # Close distance right
            else:
                return 1  # Close distance left
        else:
            return 0  # Hold position in optimal range
    
    # Too close - need to create space
    if distance < optimal_range_min:
        if distance < danger_zone:
            if opp_attacking > 0.5:
                return 6  # Block immediate threat
            elif health_advantage > winning_threshold and random.random() < 0.3:
                return 4  # Aggressive counter when winning
            elif projectile_ready and random.random() < 0.5:
                return 9  # Point blank projectile
            else:
                if relative_pos > 0 and not near_left_edge:
                    return 7  # Retreat left with block
                elif relative_pos < 0 and not near_right_edge:
                    return 8  # Retreat right with block
                else:
                    return 6  # Block if trapped
        else:
            # Medium-close range, create space
            if opponent_cornering_me:
                if health_advantage > 0:
                    if random.random() < 0.4:
                        return 4  # Fight back when winning
                    else:
                        return 3  # Jump over
                else:
                    return 3  # Jump to escape
            else:
                if relative_pos > 0 and not near_left_edge:
                    return 1  # Back away left
                elif relative_pos < 0 and not near_right_edge:
                    return 2  # Back away right
                else:
                    return 3