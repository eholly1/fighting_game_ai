"""
Evolutionary Agent: gen2_agent_020
==================================

Metadata:
{
  "generation": 2,
  "fitness": 201.7893333333309,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 71a9fab1b2f38b2d
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
    
    # Extract comprehensive fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    my_velocity_x = state[7] if len(state) > 7 else 0
    opponent_velocity_x = state[18] if len(state) > 18 else 0
    
    # Combat state analysis
    my_attack_status = state[4] if len(state) > 4 else 0
    opponent_attack_status = state[15] if len(state) > 15 else 0
    my_block_status = state[5] if len(state) > 5 else 0
    opponent_block_status = state[16] if len(state) > 16 else 0
    
    # Projectile and movement tracking
    my_projectile_cooldown = max(0.0, state[6] if len(state) > 6 else 0)
    opponent_projectile_cooldown = max(0.0, state[17] if len(state) > 17 else 0)
    height_diff = state[24] if len(state) > 24 else 0
    
    # Advanced tactical ranges with overlap zones
    immediate_danger = 0.06
    close_combat = 0.14
    transition_zone = 0.22
    medium_range = 0.35
    projectile_optimal = 0.50
    max_effective = 0.70
    
    # Health state thresholds
    critical_health = 0.12
    low_health = 0.28
    moderate_health = 0.55
    high_health = 0.80
    
    # Stage position awareness
    stage_left_edge = -0.85
    stage_right_edge = 0.85
    left_corner_zone = -0.65
    right_corner_zone = 0.65
    
    my_near_left_wall = my_position < left_corner_zone
    my_near_right_wall = my_position > right_corner_zone
    opponent_cornered = opponent_position < left_corner_zone or opponent_position > right_corner_zone
    
    # Frame data and timing analysis
    projectile_ready = my_projectile_cooldown < 0.05
    opponent_projectile_threat = opponent_projectile_cooldown < 0.15
    
    # Movement prediction system
    opponent_advancing = False
    if relative_pos > 0 and opponent_velocity_x > 0.08:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_velocity_x < -0.08:
        opponent_advancing = True
    
    # Combat tempo analysis
    frame_advantage = 0
    if my_attack_status > 0.3 and opponent_attack_status < 0.2:
        frame_advantage = 1
    elif opponent_attack_status > 0.3 and my_attack_status < 0.2:
        frame_advantage = -1
    
    # Dynamic aggression calculation
    base_aggression = 0.52
    health_modifier = health_advantage * 0.25
    distance_modifier = max(0, (medium_range - distance) * 0.3)
    current_aggression = max(0.15, min(0.85, base_aggression + health_modifier + distance_modifier))
    
    # Emergency survival protocols
    if my_health <= critical_health:
        if distance < close_combat and opponent_attack_status > 0.2:
            return 6  # Emergency defensive block
        
        if distance < transition_zone:
            # Desperate escape with blocking movement
            if opponent_advancing:
                if relative_pos > 0 and not my_near_left_wall:
                    return 7  # Block retreat left
                elif not my_near_right_wall:
                    return 8  # Block retreat right
                else:
                    return 6  # Block in place if trapped
            else:
                # Create separation distance
                if relative_pos > 0 and not my_near_left_wall:
                    return 1  # Move away left
                elif not my_near_right_wall:
                    return 2  # Move away right
                else:
                    return 6  # Block
        
        # Desperation projectile zoning
        if projectile_ready and distance > close_combat:
            return 9
        
        # Last resort blocking
        return 6
    
    # Dominant finishing sequence
    if health_advantage > 0.4 and opponent_health < 0.3:
        if distance < close_combat:
            if opponent_block_status > 0.3:
                # Guard break tactics
                break_choice = random.random()
                if break_choice < 0.35:
                    return 5  # Power kick to break guard
                elif break_choice < 0.6:
                    # Reset spacing for better angle
                    if relative_pos > 0:
                        return 1
                    else:
                        return 2
                else:
                    return 4  # Quick punch mix-up
            else:
                # Finishing combo opportunity
                finish_choice = random.random()
                if finish_choice < 0.45:
                    return 4  # Fast punch
                elif finish_choice < 0.75:
                    return 5  # Strong kick
                else:
                    return 6  # Stay ready for counter
        
        elif distance < medium_range:
            # Aggressive closing for finish
            if relative_pos > 0:
                return 2  # Close distance right
            else:
                return 1  # Close distance left
        
        else:
            # Long range pressure to force approach
            if projectile_ready:
                return 9
            else:
                # Advance while projectile recharges
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Anti-air response system
    if height_diff < -0.25:
        if distance < medium_range:
            if projectile_ready and distance > close_combat:
                return 9  # Projectile anti-air
            elif distance < transition_zone:
                return 4  # Quick anti-air punch
            else:
                # Reposition for better anti-air angle
                if relative_pos > 0:
                    return 1
                else:
                    return 2
    
    # Opponent attack response matrix
    if opponent_attack_status > 0.2:
        if distance < medium_range:
            if frame_advantage >= 0 and distance < close_combat:
                # Counter-attack window
                counter_aggression = current_aggression * 0.8
                counter_choice = random.random()
                if counter_choice < counter_aggression * 0.5:
                    return 4  # Quick counter
                elif counter_choice < counter_aggression * 0.75:
                    return 5  # Power counter
                else:
                    return 6  # Safe block
            else:
                # Defensive response based on health
                if my_health <= low_health:
                    return 6  # Priority block when low
                else:
                    # Evasive blocking
                    if opponent_advancing:
                        if relative_pos > 0 and not my_near_left_wall:
                            return 7  # Block left
                        elif not my_near_right_wall:
                            return 8  # Block right
                        else:
                            return 6  # Block
                    else:
                        return 6  #