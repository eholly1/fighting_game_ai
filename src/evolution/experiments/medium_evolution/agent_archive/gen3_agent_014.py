"""
Evolutionary Agent: gen3_agent_014
==================================

Metadata:
{
  "generation": 3,
  "fitness": 100.09999999999464,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: d7c4324ae85edbf6
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
    my_pos_x = max(0.0, min(1.0, state[0])) if len(state) > 0 else 0.5
    my_pos_y = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_health = max(0.0, min(1.0, state[2])) if len(state) > 2 else 1.0
    my_velocity_x = max(-1.0, min(1.0, state[3])) if len(state) > 3 else 0.0
    my_velocity_y = max(-1.0, min(1.0, state[4])) if len(state) > 4 else 0.0
    my_attacking = max(0.0, min(1.0, state[5])) if len(state) > 5 else 0.0
    my_blocking = max(0.0, min(1.0, state[6])) if len(state) > 6 else 0.0
    my_stunned = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0.0
    my_recovery = max(0.0, min(1.0, state[8])) if len(state) > 8 else 0.0
    my_charge = max(0.0, min(1.0, state[9])) if len(state) > 9 else 0.0
    my_projectile_cd = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    # Extract opponent status
    opp_pos_x = max(0.0, min(1.0, state[11])) if len(state) > 11 else 0.5
    opp_pos_y = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_health = max(0.0, min(1.0, state[13])) if len(state) > 13 else 1.0
    opp_velocity_x = max(-1.0, min(1.0, state[14])) if len(state) > 14 else 0.0
    opp_velocity_y = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opp_attacking = max(0.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opp_blocking = max(0.0, min(1.0, state[17])) if len(state) > 17 else 0.0
    opp_stunned = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opp_recovery = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opp_charge = max(0.0, min(1.0, state[20])) if len(state) > 20 else 0.0
    opp_projectile_cd = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Define enhanced tactical ranges for hybrid fighting
    ultra_close = 0.08
    very_close = 0.15
    close_range = 0.25
    medium_range = 0.40
    far_range = 0.60
    max_range = 0.85
    
    # Calculate situational awareness
    wall_distance = min(my_pos_x, 1.0 - my_pos_x)
    opp_wall_distance = min(opp_pos_x, 1.0 - opp_pos_x)
    im_cornered = wall_distance < 0.2
    opp_cornered = opp_wall_distance < 0.2
    center_control = abs(my_pos_x - 0.5) < 0.25
    
    # Advanced movement pattern analysis
    opp_advancing = (relative_pos > 0 and opp_velocity_x > 0.15) or (relative_pos < 0 and opp_velocity_x < -0.15)
    opp_retreating = (relative_pos > 0 and opp_velocity_x < -0.15) or (relative_pos < 0 and opp_velocity_x > 0.15)
    opp_circling = abs(opp_velocity_x) > 0.1 and not opp_advancing and not opp_retreating
    opp_stationary = abs(opp_velocity_x) < 0.05
    
    # Enhanced behavioral pattern recognition
    opp_aggressive = opp_attacking > 0.4 or (opp_advancing and distance < medium_range)
    opp_defensive = opp_blocking > 0.5 or (opp_retreating and my_attacking > 0.3)
    opp_zoning = opp_projectile_cd < 0.3 and distance > close_range
    opp_vulnerable = opp_stunned > 0.4 or opp_recovery > 0.5
    
    # Calculate dynamic aggression level
    base_aggression = 0.65  # Hybrid balance point
    aggression_modifiers = 0.0
    
    # Health-based aggression scaling
    health_ratio = my_health / max(0.1, opp_health)
    if health_advantage > 0.5:
        aggression_modifiers += 0.3
    elif health_advantage > 0.2:
        aggression_modifiers += 0.15
    elif health_advantage < -0.5:
        aggression_modifiers -= 0.35
    elif health_advantage < -0.2:
        aggression_modifiers -= 0.2
    
    # Position-based aggression adjustment
    if opp_cornered and not im_cornered:
        aggression_modifiers += 0.25  # Press advantage
    elif im_cornered and not opp_cornered:
        aggression_modifiers -= 0.2   # Play safer
    elif center_control:
        aggression_modifiers += 0.1   # Slight advantage
    
    # Opponent state adjustments
    if opp_vulnerable:
        aggression_modifiers += 0.4
    elif opp_aggressive and health_advantage < 0:
        aggression_modifiers -= 0.25
    elif opp_defensive and health_advantage > 0:
        aggression_modifiers += 0.2
    
    current_aggression = max(0.25, min(0.9, base_aggression + aggression_modifiers))
    
    # Emergency protocols - cannot act when stunned
    if my_stunned > 0.5:
        return 0
    
    # Critical health survival mode
    if my_health < 0.15:
        if opp_attacking > 0.6 and distance < close_range:
            return 6  # Emergency block
        elif distance > medium_range and my_projectile_cd < 0.2:
            return 9  # Safe projectile harassment
        elif im_cornered:
            # Desperate corner escape
            if distance < very_close:
                return