"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_016
Rank: 75/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 188.22
- Win Rate: 0.0%
- Average Reward: 188.22

Created: 2025-06-01 02:16:30
Lineage: Original

Tournament Stats:
None
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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_pos_x = state[11] if len(state) > 11 else 0.5
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    
    # Hybrid tactical parameters - refined ranges
    ultra_close = 0.08
    close_range = 0.15
    medium_range = 0.32
    far_range = 0.50
    max_range = 0.70
    
    # Dynamic thresholds based on state
    critical_health = 0.20
    winning_threshold = 0.30
    projectile_ready = my_projectile_cooldown < 0.25
    opponent_projectile_ready = opponent_projectile_cooldown < 0.25
    
    # Stage positioning analysis
    stage_center = 0.5
    my_corner_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_corner_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    i_am_cornered = my_corner_distance < 0.15
    opponent_cornered = opponent_corner_distance < 0.15
    
    # Behavioral analysis
    opponent_aggressive = opponent_attack_status > 0.5
    opponent_defensive = opponent_block_status > 0.6
    opponent_moving_toward = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_moving_away = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # Momentum and unpredictability
    momentum = abs(my_velocity_x) + abs(opponent_velocity_x)
    unpredictability = random.random()
    health_ratio = my_health / max(opponent_health, 0.1)
    combat_intensity = my_attack_status + opponent_attack_status
    
    # Strategic mode determination
    survival_mode = my_health < critical_health or health_advantage < -0.6
    finishing_mode = opponent_health < 0.25 and health_advantage > 0.2
    control_mode = abs(health_advantage) < 0.3 and my_health > 0.4
    comeback_mode = health_advantage < -0.2 and my_health > 0.3
    
    # Emergency survival protocol
    if survival_mode:
        if distance < ultra_close:
            if opponent_aggressive:
                return 6  # Block incoming attack
            elif i_am_cornered:
                # Escape corner desperately
                if my_pos_x < stage_center:
                    return 8  # Move right blocking
                else:
                    return 7  # Move left blocking
            else:
                # Create immediate space
                if unpredictability < 0.6:
                    if relative_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
                else:
                    return 3  # Jump away
        
        elif distance < close_range:
            if opponent_moving_toward and opponent_aggressive:
                return 6  # Block approach
            elif i_am_cornered:
                # Escape corner with protection
                if my_pos_x < stage_center:
                    return 8 if unpredictability < 0.7 else 3  # Move right or jump
                else:
                    return 7 if unpredictability < 0.7 else 3  # Move left or jump
            else:
                # Controlled retreat
                if projectile_ready and unpredictability < 0.4:
                    return 9  # Projectile while retreating
                else:
                    if relative_pos > 0:
                        return 1  # Move away
                    else:
                        return 2  # Move away
        
        elif distance < medium_range:
            if projectile_ready:
                return 9  # Zone with projectile
            elif opponent_projectile_ready:
                # Avoid projectile
                if unpredictability < 0.5:
                    return 3  # Jump
                else:
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            else:
                # Maintain distance
                if relative_pos > 0:
                    return 1  # Move away
                else:
                    return 2  # Move away
        
        else:
            # At safe distance
            if projectile_ready:
                return 9  # Projectile zoning
            else:
                return 0  # Wait for cooldown
    
    # Finishing mode - close out the match
    elif finishing_mode:
        if opponent_cornered:
            if distance < close_range:
                if opponent_defensive:
                    # Mix up against blocking
                    mixup = unpredictability
                    if mixup < 0.3:
                        return 9 if projectile_ready else 5  # Throw or kick
                    elif mixup < 0.6:
                        return 3  # Jump attack
                    else:
                        return 4  # Quick punch
                else:
                    # Go for kill
                    if unpredictability < 0.6:
                        return 5  # Strong kick
                    else:
                        return 4  # Fast punch
            else:
                # Approach for finish
                if relative_pos > 0:
                    return 2  # Move in
                else:
                    return 1  # Move in
        
        elif distance < ultra_close:
            # Point blank finish
            if opponent_block_status < 0.3:
                return 5 if unpredictability < 0.7 else 4  # Strong or fast
            else:
                # Opponent blocking - reposition
                if unpredictability < 0.4:
                    return 3  # Jump
                elif relative_pos > 0:
                    return 2  # Circle right
                else:
                    return 1  # Circle left
        
        elif distance < close_range:
            if opponent_aggressive:
                # Counter their desperation
                return 4 if unpredictability < 0.6 else 6  # Punch or block