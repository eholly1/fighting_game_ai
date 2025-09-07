"""
Evolutionary Agent: gen0_agent_002
==================================

Metadata:
{
  "generation": 0,
  "fitness": -20.089999999999932,
  "fighting_style": "zoner",
  "win_rate": 0.0
}

Code Hash: 443a272d6d5399ac
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
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_block_status = state[7] if len(state) > 7 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Opponent information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_attack_status = state[17] if len(state) > 17 else 0.0
    opp_block_status = state[18] if len(state) > 18 else 0.0
    
    # Define strategic thresholds for ZONER style
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    critical_health = 0.25
    winning_threshold = 0.3
    losing_threshold = -0.3
    
    # Emergency defensive measures when health is critical
    if my_health < critical_health:
        if distance < close_range:
            # Too close and low health - block and retreat
            if relative_pos > 0:
                return 7  # move_left_block (retreat)
            else:
                return 8  # move_right_block (retreat)
        elif distance < medium_range:
            # Medium range - maintain distance while blocking
            if opp_attack_status > 0.5:
                return 6  # block incoming attack
            # Create space for projectiles
            if relative_pos > 0:
                return 1  # move_left to create distance
            else:
                return 2  # move_right to create distance
        else:
            # Far range - projectile if available
            if my_projectile_cooldown < 0.3:
                return 9  # projectile
            else:
                return 6  # block while waiting for cooldown
    
    # Dominant zoning when winning decisively
    if health_advantage > winning_threshold:
        if distance < close_range:
            # Push opponent away even when winning
            if relative_pos > 0:
                return 1  # move_left to create space
            else:
                return 2  # move_right to create space
        elif distance < medium_range:
            # Control medium range with movement
            if abs(opp_velocity_x) > 0.3:  # Opponent moving fast
                if opp_velocity_x * relative_pos > 0:  # Moving toward me
                    # Counter-move to maintain distance
                    if relative_pos > 0:
                        return 1  # move_left
                    else:
                        return 2  # move_right
                else:
                    # Opponent retreating, advance carefully
                    if my_projectile_cooldown < 0.2:
                        return 9  # projectile while advancing
                    else:
                        if relative_pos > 0:
                            return 2  # move_right
                        else:
                            return 1  # move_left
            else:
                # Opponent stationary, perfect for projectiles
                if my_projectile_cooldown < 0.4:
                    return 9  # projectile
                else:
                    # Position for next projectile
                    edge_distance = min(my_pos_x, 1.0 - my_pos_x)
                    if edge_distance < 0.2:  # Too close to edge
                        if my_pos_x < 0.5:
                            return 2  # move_right away from left edge
                        else:
                            return 1  # move_left away from right edge
                    else:
                        return 0  # idle while cooldown recovers
        else:
            # Far range - ideal zoning distance
            if my_projectile_cooldown < 0.5:
                return 9  # projectile
            else:
                # Maintain optimal positioning
                if my_pos_x < 0.15 or my_pos_x > 0.85:  # Near stage edge
                    if my_pos_x < 0.5:
                        return 2  # move_right toward center
                    else:
                        return 1  # move_left toward center
                else:
                    return 0  # idle, good position
    
    # Losing situation - tactical retreat and spacing
    elif health_advantage < losing_threshold:
        if distance < close_range:
            # Dangerous close range when losing
            if opp_attack_status > 0.6:
                return 6  # block the attack
            else:
                # Retreat with blocking
                if relative_pos > 0:
                    return 7  # move_left_block
                else:
                    return 8  # move_right_block
        elif distance < medium_range:
            # Medium range when losing - create space carefully
            if opp_block_status > 0.5:
                # Opponent blocking, safe to reposition
                if relative_pos > 0:
                    return 1  # move_left
                else:
                    return 2  # move_right
            elif my_projectile_cooldown < 0.3:
                return 9  # projectile
            else:
                # Stay defensive while waiting
                return 6  # block
        else:
            # Far range when losing - zone patiently
            if my_projectile_cooldown < 0.6:
                return 9  # projectile
            else:
                # Defensive positioning
                center_pull = 0.5 - my_pos_x
                if abs(center_pull) > 0.3:
                    if center_pull > 0:
                        return 2  # move_right toward center
                    else:
                        return 1  # move_left toward center
                else:
                    return 0  # idle in good position
    
    # Even match or slight advantage/disadvantage - standard zoner tactics
    else:
        if distance < close_range:
            # Close range - zoner's weakness, need to escape
            urgency = random.random()
            if opp_attack_status > 0.4:
                return 6  # block first
            elif urgency < 0.3:
                # Sometimes fight back briefly
                if random.random() < 0.7:
                    return 4  # quick punch
                else:
                    return 5  # kick
            else:
                # Usually retreat
                if relative_pos > 0:
                    if random.random() < 0.6:
                        return 7  # move_left_block
                    else:
                        return 1  # move_left
                else:
                    if random.random() < 0.6:
                        return 8  # move_right_block
                    else:
                        return 2  # move_right
        
        elif distance < medium_range:
            # Medium range - transitional zone, key for zoners
            opponent_advancing = (opp_velocity_x * relative_pos) > 0