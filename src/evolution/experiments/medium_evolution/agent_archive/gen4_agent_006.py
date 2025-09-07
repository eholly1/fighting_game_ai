"""
Evolutionary Agent: gen4_agent_006
==================================

Metadata:
{
  "generation": 4,
  "fitness": -19.226666666666603,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 36673d2dcbe4e2ed
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_pos_x = max(0.0, min(1.0, state[2])) if len(state) > 2 else 0.5
    my_velocity_x = max(-1.0, min(1.0, state[4])) if len(state) > 4 else 0.0
    my_velocity_y = max(-1.0, min(1.0, state[5])) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0.0
    my_block_status = max(0.0, min(1.0, state[8])) if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    # Extract opponent status with bounds checking
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opponent_velocity_x = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opponent_velocity_y = max(-1.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Enhanced tactical range definitions
    point_blank = 0.02
    ultra_close = 0.06
    very_close = 0.12
    close_range = 0.20
    mid_close = 0.30
    medium_range = 0.42
    mid_far = 0.58
    far_range = 0.75
    max_range = 0.90
    
    # Advanced positional awareness
    wall_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    corner_trapped = wall_distance < 0.08
    near_corner = wall_distance < 0.18
    opponent_cornered = opponent_wall_distance < 0.08
    opponent_near_corner = opponent_wall_distance < 0.18
    center_control = abs(my_pos_x - 0.5) < 0.15
    
    # Opponent behavior analysis with improved patterns
    opponent_aggressive = opponent_attack_status > 0.25 or abs(opponent_velocity_x) > 0.12
    opponent_very_aggressive = opponent_attack_status > 0.55 or abs(opponent_velocity_x) > 0.25
    opponent_defensive = opponent_block_status > 0.35
    opponent_very_defensive = opponent_block_status > 0.65
    opponent_mobile = abs(opponent_velocity_x) > 0.06
    opponent_highly_mobile = abs(opponent_velocity_x) > 0.18
    
    # Movement pattern recognition
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.08) or (relative_pos < 0 and opponent_velocity_x < -0.08)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.08) or (relative_pos < 0 and opponent_velocity_x > 0.08)
    opponent_circling = abs(opponent_velocity_x) > 0.15 and not opponent_advancing and not opponent_retreating
    
    # Projectile readiness assessment
    opponent_projectile_ready = opponent_projectile_cooldown < 0.2
    my_projectile_ready = my_projectile_cooldown < 0.25
    opponent_likely_projectile = opponent_projectile_ready and distance > mid_close and not opponent_advancing
    
    # Calculate dynamic aggression with evolved factors
    base_aggression = 0.50
    aggression_mod = 0.0
    
    # Health-based aggression adjustments
    health_ratio = my_health / max(0.05, opponent_health)
    if health_ratio > 1.8:
        aggression_mod += 0.25  # Dominating
    elif health_ratio > 1.3:
        aggression_mod += 0.15  # Winning
    elif health_ratio < 0.4:
        aggression_mod -= 0.35  # Losing badly
    elif health_ratio < 0.7:
        aggression_mod -= 0.15  # Behind
    
    # Position-based aggression
    if opponent_cornered and not corner_trapped:
        aggression_mod += 0.3  # Press advantage
    elif corner_trapped:
        aggression_mod -= 0.25  # Need to escape
    elif center_control and not opponent_cornered:
        aggression_mod += 0.1  # Good position
    
    # Opponent behavior adaptations
    if opponent_very_defensive and not opponent_mobile:
        aggression_mod += 0.2  # Punish turtling
    elif opponent_very_aggressive and health_advantage < 0:
        aggression_mod -= 0.2  # Be cautious when behind
    elif opponent_circling and distance > close_range:
        aggression_mod += 0.15  # Counter evasive play
    
    # Distance-based fine tuning
    if distance < very_close:
        aggression_mod += 0.05  # Slight boost in close combat
    elif distance > medium_range:
        aggression_mod -= 0.05  # More measured at range
    
    current_aggression = max(0.1, min(0.9, base_aggression + aggression_mod))
    
    # Critical survival mode
    if my_health < 0.15 and health_advantage < -0.4:
        if opponent_attack_status > 0.7 and distance < close_range:
            return 6  # Emergency block
        elif distance > mid_far and my_projectile_ready:
            return 9  # Desperation projectile
        elif corner_trapped and opponent_advancing:
            if abs(height_diff) < 0.25 and random.random() < 0.6:
                return 3  # Jump escape
            else:
                escape_dir = 2 if my_pos_x < 0.5 else 1
                return 7 if escape_dir == 1 else 8
        elif distance < ultra_close and my_health > 0.08:
            return 4 if random.random() < 0.7 else 5  # Last stand
        else:
            return 6