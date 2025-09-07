"""
Evolutionary Agent: gen4_agent_012
==================================

Metadata:
{
  "generation": 4,
  "fitness": 53.57999999999669,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 5d481fa4059da4db
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
    
    # Extract fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2] if len(state) > 2 else 1.0))
    my_pos_x = state[0] if len(state) > 0 else 0.0
    my_velocity_x = state[7] if len(state) > 7 else 0.0
    my_velocity_y = state[8] if len(state) > 8 else 0.0
    my_attack_status = state[4] if len(state) > 4 else 0.0
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[13] if len(state) > 13 else 1.0))
    opponent_pos_x = state[11] if len(state) > 11 else 0.0
    opponent_velocity_x = state[18] if len(state) > 18 else 0.0
    opponent_velocity_y = state[19] if len(state) > 19 else 0.0
    opponent_attack_status = state[15] if len(state) > 15 else 0.0
    opponent_block_status = state[16] if len(state) > 16 else 0.0
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0.0)
    
    # Enhanced tactical range definitions
    danger_zone = 0.04
    point_blank = 0.08
    ultra_close = 0.13
    close_range = 0.20
    medium_close = 0.30
    medium_range = 0.42
    medium_far = 0.58
    far_range = 0.75
    
    # Positional awareness
    left_corner_trap = my_pos_x < -0.70
    right_corner_trap = my_pos_x > 0.70
    opponent_cornered_left = opponent_pos_x < -0.70
    opponent_cornered_right = opponent_pos_x > 0.70
    center_control = abs(my_pos_x) < 0.30
    
    # Movement pattern recognition
    opponent_rushing = False
    opponent_retreating = False
    opponent_aggressive = False
    
    if abs(opponent_velocity_x) > 0.15:
        if (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15):
            opponent_rushing = True
            opponent_aggressive = True
        elif (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15):
            opponent_retreating = True
    
    # Aerial combat analysis
    opponent_airborne = abs(opponent_velocity_y) > 0.05 or height_diff < -0.12
    my_airborne = abs(my_velocity_y) > 0.05
    opponent_landing = opponent_airborne and opponent_velocity_y > 0.03
    opponent_jumping = opponent_airborne and opponent_velocity_y < -0.03
    
    # Projectile readiness
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_charging = my_projectile_cooldown < 0.15
    opponent_projectile_threat = opponent_projectile_cooldown < 0.08
    
    # Dynamic aggression system
    base_aggression = 0.65
    aggression_modifier = 1.0
    
    # Health-based aggression scaling
    if health_advantage > 0.6:
        aggression_modifier *= 1.5  # Dominating
    elif health_advantage > 0.3:
        aggression_modifier *= 1.25  # Strong advantage
    elif health_advantage > 0.1:
        aggression_modifier *= 1.1  # Slight edge
    elif health_advantage > -0.1:
        aggression_modifier *= 0.95  # Even
    elif health_advantage > -0.3:
        aggression_modifier *= 0.75  # Slight disadvantage
    elif health_advantage > -0.6:
        aggression_modifier *= 0.55  # Losing
    else:
        aggression_modifier *= 0.35  # Critical
    
    # Distance-based aggression adjustment
    if distance < ultra_close:
        aggression_modifier *= 1.2
    elif distance < close_range:
        aggression_modifier *= 1.1
    elif distance > medium_far:
        aggression_modifier *= 0.85
    
    # Opponent behavior modifier
    if opponent_aggressive:
        aggression_modifier *= 0.8  # Be more careful
    elif opponent_retreating:
        aggression_modifier *= 1.2  # Press advantage
    
    current_aggression = min(1.0, max(0.25, base_aggression * aggression_modifier))
    
    # Critical health emergency mode
    if my_health < 0.12:
        # Survival priority with calculated risks
        if opponent_attack_status > 0.5:
            if distance < close_range:
                # Emergency defensive maneuvers
                if left_corner_trap:
                    if relative_pos < 0:
                        return 3 if random.random() < 0.25 else 8
                    else:
                        return 6
                elif right_corner_trap:
                    if relative_pos > 0:
                        return 3 if random.random() < 0.25 else 7
                    else:
                        return 6
                else:
                    return 7 if relative_pos > 0 else 8
            else:
                return 6  # Block at safe distance
        
        # Desperation offense when opponent is also critical
        if opponent_health < 0.15 and distance < close_range:
            if opponent_attack_status < 0.3:
                return 5 if random.random() < 0.8 else 4
            else:
                return 6  # Still block if they're attacking
        
        # Create space and harass
        if distance > ultra_close and projectile_ready:
            return 9
        elif distance < medium_close and not (left_corner_trap or right_corner_trap):
            return 7 if relative_pos > 0 else 8
        else:
            return 6 if opponent_projectile_threat else 0
    
    # Anti-air opportunities
    if opponent_landing and distance < medium_close:
        if distance < ultra_close:
            # Close range landing punish
            return 5 if random.random() < 0.85 else 4
        elif distance < close_range:
            # Medium close anti-air
            if projectile_ready:
                return 9
            else:
                return 2 if relative_pos > 0 else 1  # Move in for punish
        else:
            # Position for followup
            return 2 if relative_pos > 0 else 1
    
    # Enhanced opponent attack response
    if opponent_attack_status > 0.4:
        threat_level = opponent_attack_status * (1.2 - distance)