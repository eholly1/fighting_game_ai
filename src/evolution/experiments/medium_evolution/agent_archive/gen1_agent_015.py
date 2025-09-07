"""
Evolutionary Agent: gen1_agent_015
==================================

Metadata:
{
  "generation": 1,
  "fitness": 158.1999999999932,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 5210f42cd3e035ea
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0
    
    # Extract player and opponent info
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position_x = state[0]
    opponent_position_x = state[11]
    my_velocity_x = state[3] if len(state) > 3 else 0
    opponent_velocity_x = state[14] if len(state) > 14 else 0
    
    # Extract combat status with bounds checking
    my_block_status = max(0.0, min(1.0, state[5])) if len(state) > 5 else 0
    opponent_attack_status = max(0.0, min(1.0, state[16])) if len(state) > 16 else 0
    my_projectile_cooldown = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0
    my_attack_status = max(0.0, min(1.0, state[6])) if len(state) > 6 else 0
    opponent_block_status = max(0.0, min(1.0, state[17])) if len(state) > 17 else 0
    
    # Enhanced zoner strategy constants
    optimal_distance = 0.42     # Preferred fighting distance
    max_zoner_range = 0.55      # Maximum effective range
    danger_zone = 0.11          # Ultra close combat threshold
    retreat_threshold = 0.18    # When to start retreating
    projectile_range = 0.32     # Effective projectile distance
    health_crisis = 0.25        # Critical health level
    domination_threshold = 0.35 # When we're winning decisively
    
    # Stage position and movement analysis
    stage_center = 0.5
    stage_quarter = 0.25
    my_corner_distance = min(abs(my_position_x), abs(my_position_x - 1.0))
    opponent_corner_distance = min(abs(opponent_position_x), abs(opponent_position_x - 1.0))
    near_corner = my_corner_distance < 0.2
    opponent_cornered = opponent_corner_distance < 0.15
    
    # Advanced tactical analysis
    is_critical_health = my_health < health_crisis
    is_dominating = health_advantage > domination_threshold
    is_losing_badly = health_advantage < -0.3
    is_losing = health_advantage < -0.1
    projectile_ready = my_projectile_cooldown < 0.05
    opponent_projectile_ready = opponent_projectile_cooldown < 0.05
    opponent_aggressive = opponent_attack_status > 0.3
    currently_attacking = my_attack_status > 0.3
    opponent_blocking = opponent_block_status > 0.3
    
    # Movement prediction and positioning
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    closing_speed = abs(my_velocity_x) + abs(opponent_velocity_x) if opponent_approaching else 0
    
    # Zoner pattern recognition
    opponent_rushdown = opponent_approaching and distance < 0.3
    opponent_zoning = opponent_projectile_ready and distance > 0.4
    space_control_needed = distance < optimal_distance and not is_dominating
    
    # Emergency survival mode
    if is_critical_health:
        # Absolute priority: survive
        if distance < danger_zone:
            if opponent_aggressive:
                return 6  # Block critical attack
            elif near_corner:
                # Escape corner with movement
                if my_position_x < stage_center:
                    return 8  # Move right blocking
                else:
                    return 7  # Move left blocking
            else:
                # Create emergency distance
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        
        elif distance < retreat_threshold:
            # Still too close when critical
            if opponent_aggressive and random.random() < 0.7:
                return 6  # Block first
            else:
                # Retreat to safety
                if near_corner:
                    if my_position_x < stage_center:
                        return 2  # Move right toward center
                    else:
                        return 1  # Move left toward center
                else:
                    if relative_pos > 0:
                        return 1  # Move left away
                    else:
                        return 2  # Move right away
        
        elif projectile_ready and distance > 0.25:
            # Desperate projectile attempts
            return 9
        
        else:
            # Get to projectile range safely
            if distance < projectile_range:
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                return 0  # Wait for projectile cooldown
    
    # Ultra close range - immediate escape protocols
    if distance < danger_zone:
        # Cannot allow close combat as zoner
        if opponent_aggressive:
            # Block and escape
            if near_corner:
                if my_position_x < stage_center:
                    return 8  # Move right blocking
                else:
                    return 7  # Move left blocking
            else:
                if random.random() < 0.6:
                    if relative_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
                else:
                    return 6  # Pure block
        
        elif is_dominating and random.random() < 0.25:
            # Rare aggressive option when dominating
            if random.random() < 0.7:
                return 4  # Quick punch
            else:
                return 5  # Kick
        
        else:
            # Standard escape
            if near_corner:
                # Priority: escape corner
                if my_position_x < stage_center:
                    if random.random() < 0.4:
                        return 8  # Move right blocking
                    else:
                        return 2  # Move right fast
                else:
                    if random.random() < 0.4:
                        return 7  # Move left blocking
                    else:
                        return 1  # Move left fast
            else:
                # Normal retreat
                if closing_speed > 0.3:
                    # Fast approach, block while moving
                    if relative_pos > 0:
                        return 7  # Move left blocking
                    else:
                        return 8  # Move right blocking
                else:
                    # Standard retreat
                    if relative_pos > 0:
                        if random.random() < 0.3:
                            return 7  # Move left blocking
                        else:
                            return 1  # Move left
                    else:
                        if random.random() < 0.3:
                            return 8  # Move