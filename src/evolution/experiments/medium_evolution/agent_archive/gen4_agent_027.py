"""
Evolutionary Agent: gen4_agent_027
==================================

Metadata:
{
  "generation": 4,
  "fitness": -15.459999999999846,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: f9ff2d26191f6a00
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate core strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract detailed fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_pos_x = max(0.0, min(1.0, state[0]))
    my_velocity_x = max(-1.0, min(1.0, state[3]))
    my_attack_status = max(0.0, min(1.0, state[7]))
    my_block_status = max(0.0, min(1.0, state[8]))
    my_projectile_cooldown = max(0.0, state[9])
    
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_pos_x = max(0.0, min(1.0, state[11]))
    opponent_velocity_x = max(-1.0, min(1.0, state[14]))
    opponent_attack_status = max(0.0, min(1.0, state[18]))
    opponent_block_status = max(0.0, min(1.0, state[19]))
    opponent_projectile_cooldown = max(0.0, state[20])
    
    # Enhanced tactical range system
    ultra_close = 0.05
    close_range = 0.12
    mid_close = 0.20
    medium_range = 0.32
    mid_far = 0.48
    far_range = 0.65
    
    # Dynamic health thresholds
    critical_health = 0.15
    low_health = 0.30
    good_health = 0.60
    excellent_health = 0.85
    
    # Cooldown and readiness analysis
    projectile_ready = my_projectile_cooldown < 0.15
    projectile_charging = my_projectile_cooldown < 0.35
    opponent_projectile_ready = opponent_projectile_cooldown < 0.20
    opponent_projectile_charging = opponent_projectile_cooldown < 0.40
    
    # Advanced positioning metrics
    stage_center = 0.5
    my_corner_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_corner_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    i_am_cornered = my_corner_distance < 0.10
    i_am_near_corner = my_corner_distance < 0.22
    opponent_cornered = opponent_corner_distance < 0.10
    opponent_near_corner = opponent_corner_distance < 0.22
    
    # Enhanced behavioral pattern recognition
    opponent_aggressive = opponent_attack_status > 0.35
    opponent_very_aggressive = opponent_attack_status > 0.70
    opponent_defensive = opponent_block_status > 0.45
    opponent_very_defensive = opponent_block_status > 0.75
    
    # Movement and positioning analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.03) or (relative_pos < 0 and opponent_velocity_x < -0.03)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.03) or (relative_pos < 0 and opponent_velocity_x > 0.03)
    opponent_stationary = abs(opponent_velocity_x) < 0.03
    
    my_advancing = (relative_pos > 0 and my_velocity_x > 0.03) or (relative_pos < 0 and my_velocity_x < -0.03)
    my_retreating = (relative_pos > 0 and my_velocity_x < -0.03) or (relative_pos < 0 and my_velocity_x > 0.03)
    
    # Combat flow analysis
    total_momentum = abs(my_velocity_x) + abs(opponent_velocity_x)
    combat_intensity = my_attack_status + opponent_attack_status
    health_ratio = my_health / max(opponent_health, 0.05)
    pressure_level = combat_intensity + (1.2 - distance)
    
    # Strategic state determination
    crisis_mode = my_health < critical_health or health_advantage < -0.75
    survival_mode = my_health < low_health or health_advantage < -0.45
    balanced_mode = abs(health_advantage) < 0.25 and my_health > 0.25
    advantage_mode = health_advantage > 0.20 and my_health > 0.35
    finishing_mode = opponent_health < 0.18 or health_advantage > 0.65
    domination_mode = health_advantage > 0.50 and my_health > 0.50
    
    # Randomization for tactical unpredictability
    chaos_factor = random.random()
    tactical_roll = random.random()
    timing_variance = random.random()
    mix_factor = random.random()
    
    # Advanced attack pattern mix-ups
    combo_preference = 0.6 if advantage_mode else 0.4
    defensive_preference = 0.7 if survival_mode else 0.3
    aggressive_preference = 0.8 if finishing_mode else 0.5
    
    # CRISIS MODE - Emergency survival protocols
    if crisis_mode:
        if distance < ultra_close:
            if opponent_very_aggressive and chaos_factor < 0.6:
                return 6  # Emergency block
            elif i_am_cornered:
                if chaos_factor < 0.35:
                    return 3  # Desperate jump escape
                else:
                    escape_direction = 8 if my_pos_x < stage_center else 7
                    return escape_direction
            else:
                # Counter-attack opportunity
                if opponent_attack_status > 0.8 and tactical_roll < 0.3:
                    return 4  # Quick counter punch
                else:
                    return 6  # Defensive block
        
        elif distance < close_range:
            if opponent_advancing and opponent_aggressive:
                return 6  # Block incoming pressure
            elif i_am_cornered:
                if projectile_ready and chaos_factor < 0.4:
                    return 9  # Projectile to create space
                else:
                    # Escape corner with movement
                    if chaos_factor < 0.3:
                        return 3  # Jump escape
                    else:
                        escape_direction = 8 if my_pos_x < stage_center else 7
                        return escape_direction
            else:
                # Controlled retreat with defensive options
                if projectile_ready and tactical_roll < 0.6:
                    return 9  # Zone control
                else:
                    retreat_direction = 2 if relative_pos < 0 else 1
                    return retreat_direction
        
        elif distance < medium_range:
            if opponent_projectile_charging:
                # Anti-projectile maneuvers
                if chaos_factor < 0.35:
                    return 3  # Jump over projectile
                else:
                    dodge_direction = 2 if chaos_factor < 0.7 else 1
                    return dodge_direction
            elif projectile_ready:
                return 9  # Counter-zone
            else:
                # Maintain safe spacing
                if opponent_advancing:
                    retreat_direction = 2 if relative_pos < 0 else 1
                    return retreat_direction
                else:
                    return 0  # Wait and assess