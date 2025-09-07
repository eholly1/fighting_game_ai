"""
Evolutionary Agent: gen3_agent_004
==================================

Metadata:
{
  "generation": 3,
  "fitness": 18.267333333333934,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 6a98268cea36371f
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
    
    # Extract comprehensive fighter status information
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_pos_y = state[3] if len(state) > 3 else 0.0
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_velocity_y = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_stunned = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_pos_y = state[14] if len(state) > 14 else 0.0
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_velocity_y = state[16] if len(state) > 16 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_stunned = state[20] if len(state) > 20 else 0.0
    opponent_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Advanced tactical ranges for hybrid strategy
    point_blank_range = 0.05
    ultra_close_range = 0.10
    close_range = 0.16
    medium_close_range = 0.25
    medium_range = 0.38
    far_range = 0.55
    max_range = 0.75
    
    # Health state classifications
    critical_health = 0.15
    low_health = 0.35
    moderate_health = 0.65
    high_health = 0.85
    
    # Positional awareness
    stage_center = 0.0
    corner_danger = 0.8
    near_corner = 0.65
    
    # Dynamic state analysis
    projectile_ready = my_projectile_cooldown < 0.08
    projectile_cooling = my_projectile_cooldown < 0.2
    opponent_projectile_ready = opponent_projectile_cooldown < 0.1
    opponent_airborne = height_diff < -0.15 or opponent_pos_y > 0.1
    i_am_airborne = my_pos_y > 0.1
    
    # Movement pattern detection
    opponent_advancing = False
    opponent_retreating = False
    if relative_pos > 0:
        opponent_advancing = opponent_velocity_x < -0.1
        opponent_retreating = opponent_velocity_x > 0.1
    else:
        opponent_advancing = opponent_velocity_x > 0.1
        opponent_retreating = opponent_velocity_x < -0.1
    
    # Corner analysis
    i_am_cornered = abs(my_pos_x) > corner_danger
    opponent_cornered = abs(opponent_pos_x) > corner_danger
    i_near_corner = abs(my_pos_x) > near_corner
    opponent_near_corner = abs(opponent_pos_x) > near_corner
    
    # Calculate adaptive aggression based on multiple factors
    base_aggression = 0.72
    health_modifier = 1.0
    position_modifier = 1.0
    momentum_modifier = 1.0
    range_modifier = 1.0
    
    # Health-based aggression scaling
    if health_advantage > 0.5:
        health_modifier = 1.4  # Dominating
    elif health_advantage > 0.25:
        health_modifier = 1.2  # Winning clearly
    elif health_advantage > 0.05:
        health_modifier = 1.05  # Slight edge
    elif health_advantage > -0.15:
        health_modifier = 0.95  # Slightly behind
    elif health_advantage > -0.35:
        health_modifier = 0.75  # Losing
    else:
        health_modifier = 0.55  # Desperate
    
    # Position-based aggression
    if opponent_cornered and not i_am_cornered:
        position_modifier = 1.3
    elif i_am_cornered and not opponent_cornered:
        position_modifier = 0.7
    elif opponent_near_corner and distance < medium_range:
        position_modifier = 1.15
    
    # Momentum consideration
    if opponent_advancing and my_health > low_health:
        momentum_modifier = 1.1  # Counter aggression
    elif opponent_retreating:
        momentum_modifier = 1.2  # Chase down
    
    # Range-based aggression
    if distance < close_range:
        range_modifier = 1.25  # Aggressive in close
    elif distance > far_range:
        range_modifier = 0.85  # Cautious at range
    
    current_aggression = min(1.0, max(0.3, base_aggression * health_modifier * position_modifier * momentum_modifier * range_modifier))
    
    # Critical survival protocols
    if my_health <= critical_health:
        # Stunned while critical - desperate measures
        if my_stunned > 0.5:
            if opponent_attack_status > 0.5 and distance < medium_range:
                return 6  # Block desperately
            elif distance > far_range and projectile_ready:
                return 9  # Last chance projectile
            else:
                return 6
        
        # Opponent attacking while I'm critical
        if opponent_attack_status > 0.6:
            if distance < medium_close_range:
                return 6  # Must block
            elif distance < far_range and not i_am_cornered:
                return 7 if relative_pos > 0 else 8
            else:
                return 6
        
        # Exploit stunned opponent even when critical
        if opponent_stunned > 0.5 and distance < close_range:
            if random.random() < 0.8:
                return 5  # Take the opportunity
            else:
                return 4
        
        # Create distance when possible
        if distance < medium_range and not i_am_cornered:
            if opponent_projectile_ready:
                return 6  # Block expected projectile
            else:
                return 1 if relative_pos < 0 else 2
        
        # Long range desperate tactics
        if distance > medium_range:
            if projectile_ready:
                return 9  # Chip damage attempt
            elif opponent_projectile_ready:
                return 6  # Defend against projectile
            else:
                return 6  # Default defensive
        
        return 6  # Last resort blocking
    
    # Handle stunned states