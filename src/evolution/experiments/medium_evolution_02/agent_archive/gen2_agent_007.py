"""
Evolutionary Agent: gen2_agent_007
==================================

Metadata:
{
  "generation": 2,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 80cfd0671d2b3406
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Validate and extract key state information with bounds checking
    if len(state) < 26:
        return 4  # Safe default if invalid state
    
    # Core tactical variables with defensive bounds
    distance = max(0.0, min(1.0, float(state[22])))
    relative_pos = max(-1.0, min(1.0, float(state[23])))
    health_advantage = max(-1.0, min(1.0, float(state[25])))
    height_diff = float(state[24]) if abs(state[24]) < 2.0 else 0.0
    
    # My fighter comprehensive status
    my_health = max(0.0, min(1.0, float(state[1])))
    my_x_pos = float(state[0])
    my_y_pos = float(state[3]) if len(state) > 3 else 0.0
    my_x_vel = float(state[2]) if len(state) > 2 else 0.0
    my_y_vel = float(state[4]) if len(state) > 4 else 0.0
    my_attacking = max(0.0, float(state[5])) if len(state) > 5 else 0.0
    my_blocking = max(0.0, float(state[6])) if len(state) > 6 else 0.0
    my_projectile_active = float(state[7]) if len(state) > 7 else 0.0
    my_stun = float(state[8]) if len(state) > 8 else 0.0
    my_cooldown = max(0.0, float(state[9])) if len(state) > 9 else 0.0
    my_stamina = max(0.0, min(1.0, float(state[10]))) if len(state) > 10 else 1.0
    
    # Opponent comprehensive status
    opp_health = max(0.0, min(1.0, float(state[12])))
    opp_x_pos = float(state[11])
    opp_y_pos = float(state[14]) if len(state) > 14 else 0.0
    opp_x_vel = float(state[13]) if len(state) > 13 else 0.0
    opp_y_vel = float(state[15]) if len(state) > 15 else 0.0
    opp_attacking = max(0.0, float(state[16])) if len(state) > 16 else 0.0
    opp_blocking = max(0.0, float(state[17])) if len(state) > 17 else 0.0
    opp_projectile_active = float(state[18]) if len(state) > 18 else 0.0
    opp_stun = float(state[19]) if len(state) > 19 else 0.0
    opp_cooldown = max(0.0, float(state[20])) if len(state) > 20 else 0.0
    opp_stamina = max(0.0, min(1.0, float(state[21]))) if len(state) > 21 else 1.0
    
    # Advanced tactical calculations
    opp_speed = math.sqrt(opp_x_vel**2 + opp_y_vel**2)
    my_speed = math.sqrt(my_x_vel**2 + my_y_vel**2)
    opp_threat = opp_attacking + (opp_speed * 0.3) + (0.7 if opp_projectile_active > 0.5 else 0.0)
    my_momentum = my_speed + (0.3 if my_attacking > 0.5 else 0.0)
    
    # Positional awareness
    stage_center = 0.5
    my_corner_distance = min(my_x_pos, 1.0 - my_x_pos)
    opp_corner_distance = min(opp_x_pos, 1.0 - opp_x_pos)
    cornered = my_corner_distance < 0.15
    opp_cornered = opp_corner_distance < 0.15
    
    # Dynamic range definitions based on context
    close_threshold = 0.12 + (0.02 * abs(height_diff)) + (0.01 * opp_speed)
    medium_threshold = 0.28 + (0.04 * opp_threat) + (0.02 * abs(my_x_vel))
    far_threshold = 0.55
    projectile_range = 0.35
    
    # Hybrid fighting style parameters with adaptation
    base_aggression = 0.58
    base_patience = 0.35
    base_adaptability = 0.25
    
    # Dynamic style modulation based on game state
    health_multiplier = 1.0
    position_multiplier = 1.0
    stamina_multiplier = max(0.6, my_stamina)
    
    if health_advantage > 0.4:
        # Significant advantage - controlled aggression
        health_multiplier = 1.15
        current_aggression = min(0.75, base_aggression * health_multiplier)
        defensive_weight = 0.25
    elif health_advantage > 0.1:
        # Slight advantage - maintain pressure
        health_multiplier = 1.05
        current_aggression = base_aggression * health_multiplier
        defensive_weight = 0.35
    elif health_advantage > -0.2:
        # Even fight - pure hybrid balance
        current_aggression = base_aggression
        defensive_weight = 0.45
    elif health_advantage > -0.45:
        # Disadvantage - more defensive
        health_multiplier = 0.85
        current_aggression = base_aggression * health_multiplier
        defensive_weight = 0.6
    else:
        # Critical disadvantage - survival mode
        health_multiplier = 0.7
        current_aggression = max(0.3, base_aggression * health_multiplier)
        defensive_weight = 0.75
    
    # Position-based adjustments
    if cornered:
        position_multiplier = 0.8
        defensive_weight += 0.15
    elif opp_cornered:
        position_multiplier = 1.2
        current_aggression += 0.1
    
    # Final aggression calculation
    final_aggression = current_aggression * position_multiplier * stamina_multiplier
    
    # Randomization seeds for unpredictability
    primary_rand = random.random()
    secondary_rand = random.random()
    tactical_rand = random.random()
    pattern_seed = int((my_x_pos + opp_x_pos + distance) * 100) % 4
    
    # Emergency reactions - highest priority
    if my_stun > 0.5:
        return 6  # Block while stunned
    
    if opp_projectile_active > 0.5 and distance > close_threshold:
        # Projectile incoming - react appropriately
        if distance < medium_threshold:
            return 6 if primary_rand < 0.7 else 3  # Block or jump
        else:
            dodge_choice = primary_rand < 0.5
            if relative_pos > 0:
                return 1 if dodge_choice else 6  # Move left or block
            else:
                return 2 if dodge_choice else 6  # Move right or block
    
    # Critical health management
    if health_advantage < -0.6:
        # Desperate situation - calculated risks only
        if distance < close_threshold and opp_threat > 1.5:
            if cornered:
                # Cornered desperately - try to escape
                escape_attempt