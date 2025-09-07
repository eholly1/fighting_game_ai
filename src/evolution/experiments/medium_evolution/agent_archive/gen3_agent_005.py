"""
Evolutionary Agent: gen3_agent_005
==================================

Metadata:
{
  "generation": 3,
  "fitness": -7.3126666666669315,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 8e979183bc686751
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
    
    # Extract my fighter information with defensive bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_pos_y = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_block_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information with defensive bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_pos_y = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_block_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Advanced hybrid fighter tactical ranges
    point_blank = 0.05
    ultra_close = 0.10
    close_range = 0.15
    medium_close = 0.25
    medium_range = 0.35
    medium_far = 0.50
    far_range = 0.70
    max_range = 0.85
    
    # Enhanced positioning constants
    stage_left_edge = 0.10
    stage_right_edge = 0.90
    stage_center = 0.50
    corner_danger_zone = 0.18
    optimal_spacing = 0.20
    
    # Combat readiness analysis
    projectile_ready = my_projectile_cooldown < 0.08
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.15
    full_combat_ready = attack_ready and block_ready
    
    # Opponent threat assessment
    opp_projectile_threat = opp_projectile_cooldown < 0.15
    opp_attack_threat = opp_attack_cooldown < 0.18
    opp_dangerous = opp_attacking or (opp_attack_threat and distance < close_range)
    
    # Advanced positioning analysis
    is_cornered_left = my_pos_x < stage_left_edge + corner_danger_zone
    is_cornered_right = my_pos_x > stage_right_edge - corner_danger_zone
    is_cornered = is_cornered_left or is_cornered_right
    opp_cornered = opp_pos_x < stage_left_edge + corner_danger_zone or opp_pos_x > stage_right_edge - corner_danger_zone
    
    # Movement pattern recognition
    opponent_advancing = (relative_pos > 0 and opp_velocity_x > 0.2) or (relative_pos < 0 and opp_velocity_x < -0.2)
    opponent_retreating = (relative_pos > 0 and opp_velocity_x < -0.15) or (relative_pos < 0 and opp_velocity_x > 0.15)
    opponent_stationary = abs(opp_velocity_x) < 0.1
    
    # Dynamic aggression calculation
    base_aggression = 0.72
    health_factor = 1.0
    position_factor = 1.0
    distance_factor = 1.0
    momentum_factor = 1.0
    
    # Health-based aggression modulation
    if health_advantage > 0.5:
        health_factor = 1.4  # Dominating
    elif health_advantage > 0.25:
        health_factor = 1.25  # Winning decisively
    elif health_advantage > 0.1:
        health_factor = 1.1  # Slight advantage
    elif health_advantage > -0.1:
        health_factor = 1.0  # Even match
    elif health_advantage > -0.25:
        health_factor = 0.85  # Slight disadvantage
    elif health_advantage > -0.4:
        health_factor = 0.7  # Losing
    else:
        health_factor = 0.55  # Critical situation
    
    # Position-based aggression
    if opp_cornered and not is_cornered:
        position_factor = 1.3  # Press advantage
    elif is_cornered and not opp_cornered:
        position_factor = 0.7  # More cautious
    elif distance < optimal_spacing:
        position_factor = 1.15  # Good spacing for pressure
    
    # Distance-based aggression
    if distance < close_range:
        distance_factor = 1.2  # Aggressive in close
    elif distance > medium_range:
        distance_factor = 0.9  # More measured at range
    
    # Momentum-based adjustments
    if opponent_advancing and distance < medium_range:
        momentum_factor = 1.1  # Counter-aggression
    elif opponent_retreating:
        momentum_factor = 1.15  # Press the advantage
    
    current_aggression = min(1.0, base_aggression * health_factor * position_factor * distance_factor * momentum_factor)
    
    # Emergency protocols - stunned state
    if my_stunned:
        return 0  # Cannot act while stunned
    
    # Critical health emergency protocols
    if my_health < 0.15:
        if opp_dangerous and distance < close_range:
            if block_ready:
                return 6  # Desperate block
            else:
                return 0  # Wait for recovery
        
        if distance < ultra_close and opp_stunned:
            # Last chance offense
            if attack_ready:
                return 5