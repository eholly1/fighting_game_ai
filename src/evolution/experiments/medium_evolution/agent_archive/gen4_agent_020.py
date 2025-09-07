"""
Evolutionary Agent: gen4_agent_020
==================================

Metadata:
{
  "generation": 4,
  "fitness": 205.05999999999017,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 059e05fcbf31a480
Serialization Version: 1.0
"""

# Agent Code:
def get_action(state):
    import random
    import math
    import numpy as np
    
    # Extract and validate key state information with defensive bounds
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract my fighter information with bounds checking
    my_x_pos = max(-1.0, min(1.0, state[0]))
    my_y_pos = state[1]
    my_health = max(0.0, min(1.0, state[2]))
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = max(0.0, min(1.0, state[5]))
    my_blocking = max(0.0, min(1.0, state[6]))
    my_stunned = max(0.0, state[7]) if len(state) > 7 else 0.0
    my_projectile_cd = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent information with bounds checking
    opp_x_pos = max(-1.0, min(1.0, state[11]))
    opp_y_pos = state[12]
    opp_health = max(0.0, min(1.0, state[13]))
    opp_x_vel = state[14]
    opp_y_vel = state[15]
    opp_attacking = max(0.0, min(1.0, state[16]))
    opp_blocking = max(0.0, min(1.0, state[17]))
    opp_stunned = max(0.0, state[18]) if len(state) > 18 else 0.0
    
    # Enhanced tactical range definitions for hybrid fighting
    danger_zone = 0.06
    point_blank = 0.10
    ultra_close = 0.14
    close_range = 0.20
    medium_close = 0.30
    medium_range = 0.42
    medium_far = 0.58
    far_range = 0.75
    
    # Positioning analysis for stage control
    left_wall_proximity = my_x_pos < -0.65
    right_wall_proximity = my_x_pos > 0.65
    in_corner = left_wall_proximity or right_wall_proximity
    center_control = abs(my_x_pos) < 0.3
    
    opp_left_corner = opp_x_pos < -0.65
    opp_right_corner = opp_x_pos > 0.65
    opp_cornered = opp_left_corner or opp_right_corner
    
    # Movement and velocity analysis
    my_moving_fast = abs(my_x_vel) > 0.15
    opp_moving_fast = abs(opp_x_vel) > 0.15
    
    # Opponent pattern recognition
    opp_rushing = False
    opp_retreating = False
    opp_circling = False
    
    if opp_moving_fast:
        if (relative_pos > 0 and opp_x_vel < -0.15) or (relative_pos < 0 and opp_x_vel > 0.15):
            opp_rushing = True
        elif (relative_pos > 0 and opp_x_vel > 0.15) or (relative_pos < 0 and opp_x_vel < -0.15):
            opp_retreating = True
        else:
            opp_circling = True
    
    # Aerial combat assessment
    opp_airborne = abs(opp_y_vel) > 0.1 or abs(height_diff) > 0.2
    my_airborne = abs(my_y_vel) > 0.1
    opp_landing_soon = opp_airborne and opp_y_vel > 0.08
    
    # Projectile status and timing
    projectile_ready = my_projectile_cd < 0.08
    projectile_charging = my_projectile_cd < 0.25
    opp_projectile_threat = len(state) > 21 and state[21] < 0.12
    
    # Dynamic hybrid aggression system
    base_aggression = 0.62  # Balanced baseline
    aggression_modifier = 1.0
    
    # Health-based aggression adjustment
    health_ratio = my_health / max(0.05, opp_health)
    
    if health_advantage > 0.6:
        aggression_modifier = 1.55  # Press advantage hard
    elif health_advantage > 0.3:
        aggression_modifier = 1.25  # Solid pressure
    elif health_advantage > 0.1:
        aggression_modifier = 1.1   # Slight pressure
    elif health_advantage > -0.1:
        aggression_modifier = 0.95  # Neutral play
    elif health_advantage > -0.3:
        aggression_modifier = 0.75  # Cautious approach
    elif health_advantage > -0.6:
        aggression_modifier = 0.55  # Defensive focus
    else:
        aggression_modifier = 0.35  # Survival mode
    
    # Distance-based aggression scaling
    if distance < close_range:
        aggression_modifier *= 1.2  # Reward close combat
    elif distance > medium_far:
        aggression_modifier *= 0.85  # Cautious at long range
    
    # Opponent state modifiers
    if opp_stunned > 0.3:
        aggression_modifier *= 1.8  # Exploit vulnerability
    elif opp_attacking > 0.7:
        aggression_modifier *= 0.7  # Respect opponent offense
    elif opp_blocking > 0.7:
        aggression_modifier *= 1.15  # Pressure blocking opponent
    
    current_aggression = max(0.15, min(1.0, base_aggression * aggression_modifier))
    
    # Emergency state handling
    if my_stunned > 0.5:
        return 0  # Recover from stun
    
    # Critical health management (below 20%)
    if my_health < 0.2:
        # Emergency defense against incoming attacks
        if opp_attacking > 0.6 and distance < medium_range:
            if distance < close_range:
                # Close range emergency escape
                if in_corner:
                    if left_wall_proximity and relative_pos >= 0:
                        return 3 if random.random() < 0.4 else 8  # Jump or retreat right
                    elif right_wall_proximity and relative_pos <= 0:
                        return 3 if random.random() < 0.4 else 7  # Jump or retreat left
                    else:
                        return 6  # Block when truly cornered
                else:
                    # Open stage emergency retreat
                    escape_roll = random.random()
                    if escape_roll < 0.5:
                        return 7 if relative_pos > 0 else 8  # Block retreat
                    elif escape_roll < 0.75:
                        return 3  # Jump escape
                    else:
                        return 6  # Stand and block
            else:
                return 6  # Block at medium range
        
        # Desperation offense when opponent also critical
        if opp_health < 0.25 and distance < close_range:
            if opp_attacking < 0.3 and opp_stunned < 0.2:
                # Both critical - calculated aggression
                if random.random() < 0.65:
                    return 5  #