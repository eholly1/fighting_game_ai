"""
Evolutionary Agent: gen4_agent_028
==================================

Metadata:
{
  "generation": 4,
  "fitness": 12.97999999999974,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: ab90d581bbceedec
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
    
    # Extract detailed fighter status with enhanced bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_pos_x = max(0.0, min(1.0, state[0]))
    my_velocity_x = max(-1.0, min(1.0, state[3]))
    my_velocity_y = max(-1.0, min(1.0, state[4]))
    my_attack_status = max(0.0, min(1.0, state[7]))
    my_block_status = max(0.0, min(1.0, state[8]))
    my_projectile_cooldown = max(0.0, state[9])
    
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_pos_x = max(0.0, min(1.0, state[11]))
    opponent_velocity_x = max(-1.0, min(1.0, state[14]))
    opponent_velocity_y = max(-1.0, min(1.0, state[15]))
    opponent_attack_status = max(0.0, min(1.0, state[18]))
    opponent_block_status = max(0.0, min(1.0, state[19]))
    opponent_projectile_cooldown = max(0.0, state[20])
    
    # Advanced tactical range system
    micro_range = 0.04
    ultra_close = 0.09
    very_close = 0.16
    close_range = 0.24
    mid_range = 0.35
    medium_range = 0.48
    far_range = 0.62
    extreme_range = 0.80
    
    # Positional awareness calculations
    stage_center = 0.5
    my_corner_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_corner_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    i_am_cornered = my_corner_distance < 0.10
    i_am_near_corner = my_corner_distance < 0.22
    opponent_cornered = opponent_corner_distance < 0.10
    opponent_near_corner = opponent_corner_distance < 0.22
    
    # Enhanced cooldown and readiness system
    my_projectile_ready = my_projectile_cooldown < 0.25
    my_projectile_charging = my_projectile_cooldown < 0.45
    opponent_projectile_ready = opponent_projectile_cooldown < 0.25
    opponent_projectile_threat = opponent_projectile_cooldown < 0.50
    
    # Advanced behavioral pattern recognition
    opponent_highly_aggressive = opponent_attack_status > 0.65
    opponent_aggressive = opponent_attack_status > 0.35
    opponent_defensive = opponent_block_status > 0.45
    opponent_very_defensive = opponent_block_status > 0.75
    opponent_mobile = abs(opponent_velocity_x) > 0.10
    opponent_highly_mobile = abs(opponent_velocity_x) > 0.25
    
    # Movement and positioning analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > 0.08) or (relative_pos < 0 and opponent_velocity_x < -0.08)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.08) or (relative_pos < 0 and opponent_velocity_x > 0.08)
    opponent_closing_fast = opponent_advancing and abs(opponent_velocity_x) > 0.20
    opponent_in_air = abs(opponent_velocity_y) > 0.15
    i_am_in_air = abs(my_velocity_y) > 0.15
    
    # Combat flow and momentum analysis
    health_ratio = my_health / max(0.08, opponent_health)
    combat_pressure = (my_attack_status + opponent_attack_status) * (1.2 - distance)
    positioning_advantage = 0.0
    
    if opponent_cornered and not i_am_cornered:
        positioning_advantage += 0.4
    elif i_am_cornered and not opponent_cornered:
        positioning_advantage -= 0.4
    
    if opponent_near_corner and distance < medium_range:
        positioning_advantage += 0.2
    elif i_am_near_corner and opponent_advancing:
        positioning_advantage -= 0.3
    
    # Strategic state classification with hybrid focus
    critical_health = 0.15
    low_health = 0.30
    good_health = 0.60
    
    crisis_state = my_health <= critical_health or health_advantage <= -0.75
    survival_state = my_health <= low_health or health_advantage <= -0.45
    balanced_state = abs(health_advantage) <= 0.25 and my_health > 0.35
    advantage_state = health_advantage >= 0.25 or (health_ratio > 1.4 and my_health > 0.4)
    domination_state = health_advantage >= 0.55 or opponent_health <= 0.20
    
    # Hybrid fighting style core parameters
    base_aggression = 0.50  # Balanced hybrid baseline
    range_preference_close = 0.35
    range_preference_medium = 0.40
    range_preference_far = 0.25
    
    # Dynamic aggression calculation
    aggression_modifier = 0.0
    
    if advantage_state:
        aggression_modifier += 0.20
    elif domination_state:
        aggression_modifier += 0.35
    elif survival_state:
        aggression_modifier -= 0.25
    elif crisis_state:
        aggression_modifier -= 0.40
    
    if positioning_advantage > 0.2:
        aggression_modifier += 0.15
    elif positioning_advantage < -0.2:
        aggression_modifier -= 0.20
    
    if opponent_very_defensive and distance < close_range:
        aggression_modifier += 0.10
    elif opponent_highly_aggressive and my_health < opponent_health:
        aggression_modifier -= 0.15
    
    current_aggression = max(0.10, min(0.90, base_aggression + aggression_modifier))
    
    # Randomization for unpredictability
    tactical_variance = random.random()
    timing_chaos = random.random()
    mix_up_factor = random.random()
    
    # CRISIS MODE - Emergency survival tactics
    if crisis_state:
        if distance <= micro_range:
            if opponent_highly_aggressive and timing_chaos < 0.6:
                return 6  # Emergency block
            elif i_am_cornered and tactical_variance < 0.35:
                return 3  # Desperate escape jump
            elif opponent_very_defensive and mix_up_factor < 0.4:
                return 5  # Heavy attack gamble
            else:
                return 4  # Quick punch and hope
        
        elif distance <= very_close:
            if opponent_advancing and not i_am_cornered:
                retreat_dir = 2 if relative_pos < 0 else 1
                return 8 if retreat_dir == 2 else 7  # Defensive retreat
            elif i_am_cornered:
                if opponent_attack_status > 0.5:
                    return 6