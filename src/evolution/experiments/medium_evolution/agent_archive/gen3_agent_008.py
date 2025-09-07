"""
Evolutionary Agent: gen3_agent_008
==================================

Metadata:
{
  "generation": 3,
  "fitness": 26.520666666665782,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: d152e63aa6109748
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
    
    # Extract my fighter information with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_x_velocity = state[3] if len(state) > 3 else 0.0
    my_y_velocity = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_attack_cooldown = max(0.0, state[9]) if len(state) > 9 else 0.0
    my_block_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information with bounds checking
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_x_velocity = state[14] if len(state) > 14 else 0.0
    opp_y_velocity = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_attack_cooldown = max(0.0, state[20]) if len(state) > 20 else 0.0
    opp_block_cooldown = max(0.0, state[21]) if len(state) > 21 else 0.0
    
    # Enhanced hybrid fighter parameters with evolution improvements
    danger_zone = 0.08
    close_range = 0.15
    medium_range = 0.28
    ideal_range = 0.35
    far_range = 0.52
    max_projectile_range = 0.75
    
    # Critical thresholds
    critical_health = 0.15
    low_health = 0.35
    high_health = 0.75
    winning_margin = 0.25
    losing_margin = -0.25
    
    # Stage positioning
    stage_center = 0.5
    left_wall = 0.2
    right_wall = 0.8
    corner_zone = 0.15
    
    # Advanced positioning analysis
    is_cornered = my_x_pos < left_wall or my_x_pos > right_wall
    opp_cornered = opp_x_pos < left_wall or opp_x_pos > right_wall
    wall_pressure = is_cornered and distance < medium_range
    can_corner_opponent = not opp_cornered and distance < ideal_range
    
    # Movement and timing analysis
    opp_closing = (relative_pos > 0 and opp_x_velocity < -0.2) or (relative_pos < 0 and opp_x_velocity > 0.2)
    opp_retreating = (relative_pos > 0 and opp_x_velocity > 0.2) or (relative_pos < 0 and opp_x_velocity < -0.2)
    opp_jumping = abs(height_diff) > 0.25
    
    # Cooldown and readiness states
    projectile_ready = my_projectile_cooldown < 0.08
    attack_ready = my_attack_cooldown < 0.12
    block_ready = my_block_cooldown < 0.15
    
    # Opponent threat assessment
    opp_projectile_threat = opp_projectile_cooldown < 0.1
    opp_attack_threat = opp_attack_cooldown < 0.15
    immediate_danger = (opp_attacking or opp_attack_threat) and distance < close_range
    
    # Dynamic aggression calculation based on multiple factors
    base_aggression = 0.6
    health_factor = min(0.4, max(-0.4, health_advantage * 0.8))
    position_factor = 0.2 if opp_cornered else (-0.15 if is_cornered else 0.0)
    range_factor = 0.1 if distance < ideal_range else -0.1
    current_aggression = max(0.2, min(0.9, base_aggression + health_factor + position_factor + range_factor))
    
    # Emergency responses - cannot act while stunned
    if my_stunned:
        return 0
    
    # Critical health survival mode with enhanced escape logic
    if my_health <= critical_health:
        if immediate_danger:
            if block_ready:
                return 6
            elif distance > danger_zone and projectile_ready:
                return 9
            else:
                return 0
        
        if wall_pressure:
            if height_diff > -0.2 and opp_y_pos < 0.3:
                return 3  # Jump escape from wall pressure
            elif relative_pos > 0:
                return 8  # Block retreat right
            else:
                return 7  # Block retreat left
        
        if distance < close_range:
            if not is_cornered:
                escape_dir = 1 if relative_pos > 0 else 2
                return escape_dir
            else:
                return 6  # Block in desperation
        
        if distance > medium_range and projectile_ready:
            return 9  # Chip damage from safety
        
        # Default safe movement
        if relative_pos > 0 and my_x_pos > left_wall:
            return 1
        elif relative_pos < 0 and my_x_pos < right_wall:
            return 2
        else:
            return 6
    
    # Punish stunned opponent with optimal combo
    if opp_stunned:
        if distance <= danger_zone:
            if attack_ready:
                combo_choice = random.random()
                if combo_choice < 0.4:
                    return 5  # Heavy damage
                else:
                    return 4  # Quick follow-up
            else:
                return 0  # Wait for attack cooldown
        elif distance < close_range:
            return 2 if relative_pos > 0 else 1  # Close distance quickly
        elif distance < medium_range:
            if projectile_ready:
                return 9  # Projectile while approaching
            else:
                return 2