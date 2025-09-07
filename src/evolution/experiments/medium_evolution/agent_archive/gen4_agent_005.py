"""
Evolutionary Agent: gen4_agent_005
==================================

Metadata:
{
  "generation": 4,
  "fitness": -6.584666666666789,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 49fe470aa8cf1ead
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
    
    # Extract my fighter status with defensive bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(0.0, min(1.0, state[0] if len(state) > 0 else 0.5))
    my_pos_y = state[2] if len(state) > 2 else 0.5
    my_velocity_x = max(-1.0, min(1.0, state[3] if len(state) > 3 else 0.0))
    my_velocity_y = max(-1.0, min(1.0, state[4] if len(state) > 4 else 0.0))
    my_attacking = state[5] > 0.5 if len(state) > 5 else False
    my_blocking = state[6] > 0.5 if len(state) > 6 else False
    my_stunned = state[7] > 0.5 if len(state) > 7 else False
    my_projectile_cooldown = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_attack_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_block_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent status with defensive bounds checking
    opp_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opp_pos_x = max(0.0, min(1.0, state[11] if len(state) > 11 else 0.5))
    opp_pos_y = state[13] if len(state) > 13 else 0.5
    opp_velocity_x = max(-1.0, min(1.0, state[14] if len(state) > 14 else 0.0))
    opp_velocity_y = max(-1.0, min(1.0, state[15] if len(state) > 15 else 0.0))
    opp_attacking = state[16] > 0.5 if len(state) > 16 else False
    opp_blocking = state[17] > 0.5 if len(state) > 17 else False
    opp_stunned = state[18] > 0.5 if len(state) > 18 else False
    opp_projectile_cooldown = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_attack_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_block_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Define refined tactical ranges for hybrid approach
    point_blank = 0.05
    ultra_close = 0.09
    very_close = 0.14
    close = 0.19
    mid_close = 0.26
    medium = 0.34
    mid_far = 0.42
    far = 0.55
    max_distance = 0.7
    
    # Position awareness calculations
    wall_distance_me = min(my_pos_x, 1.0 - my_pos_x)
    wall_distance_opp = min(opp_pos_x, 1.0 - opp_pos_x)
    im_cornered = wall_distance_me < 0.15
    opp_cornered = wall_distance_opp < 0.15
    im_near_wall = wall_distance_me < 0.25
    opp_near_wall = wall_distance_opp < 0.25
    
    # Enhanced opponent behavior analysis
    opp_aggressive = opp_attacking or (abs(opp_velocity_x) > 0.3 and distance <= close)
    opp_defensive = opp_blocking or (abs(opp_velocity_x) < 0.1 and not opp_attacking)
    opp_rushing = (relative_pos > 0 and opp_velocity_x < -0.25) or (relative_pos < 0 and opp_velocity_x > 0.25)
    opp_retreating = (relative_pos > 0 and opp_velocity_x > 0.25) or (relative_pos < 0 and opp_velocity_x < -0.25)
    opp_airborne = abs(height_diff) > 0.2
    opp_grounded = abs(height_diff) < 0.1
    
    # Cooldown and readiness states
    can_attack = my_attack_cooldown < 0.08
    can_block = my_block_cooldown < 0.05
    can_projectile = my_projectile_cooldown < 0.1
    projectile_ready = my_projectile_cooldown < 0.03
    opp_can_attack = opp_attack_cooldown < 0.08
    opp_can_projectile = opp_projectile_cooldown < 0.1
    
    # Calculate dynamic fighting parameters
    health_ratio = my_health / max(opp_health, 0.05)
    momentum_factor = health_advantage + (my_velocity_x * 0.2)
    
    # Determine current combat phase
    if health_advantage > 0.6:
        combat_phase = "dominating"
        base_aggression = 0.85
    elif health_advantage > 0.3:
        combat_phase = "winning"
        base_aggression = 0.75
    elif health_advantage > 0.1:
        combat_phase = "slight_lead"
        base_aggression = 0.7
    elif health_advantage > -0.1:
        combat_phase = "even"
        base_aggression = 0.65
    elif health_advantage > -0.3:
        combat_phase = "behind"
        base_aggression = 0.55
    elif health_advantage > -0.6:
        combat_phase = "losing"
        base_aggression = 0.4
    else:
        combat_phase = "critical"
        base_aggression = 0.25
    
    # Adjust aggression based on position
    aggression_modifier = 0.0
    if opp_cornered and not im_cornered:
        aggression_modifier += 0.2
    elif im_cornered and not opp_cornered:
        aggression_modifier -= 0.25
    
    if opp_stunned:
        aggression_modifier += 0.3
    elif my_stunned:
        aggression_modifier -= 0.4
    
    current_aggression = max(0.1, min(0.95, base_aggression + aggression_modifier))
    
    # Critical emergency responses
    if my_stunned:
        if distance < very_close and opp_attacking:
            if can_block:
                return 6
            else:
                return 3 if random.random() < 0.4 else 0
        elif distance < close:
            if can_block:
                return 7 if relative_pos > 0 else 8
            else:
                return 1