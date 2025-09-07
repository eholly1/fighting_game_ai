"""
Hall of Fame Agent
==================

Agent ID: gen1_agent_006
Rank: 79/100
Generation: 1
Fighting Style: evolved

Performance Metrics:
- Fitness: 180.75
- Win Rate: 33.3%
- Average Reward: 258.21

Created: 2025-06-01 01:24:51
Lineage: Original

Tournament Stats:
None
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
    my_velocity = state[3] if len(state) > 3 else 0
    opponent_velocity = state[14] if len(state) > 14 else 0
    
    # Extract combat status information
    my_block_status = state[5] if len(state) > 5 else 0
    opponent_attack_status = state[16] if len(state) > 16 else 0
    my_projectile_cooldown = state[7] if len(state) > 7 else 0
    opponent_projectile_cooldown = state[18] if len(state) > 18 else 0
    my_attack_status = state[4] if len(state) > 4 else 0
    opponent_block_status = state[17] if len(state) > 17 else 0
    
    # Advanced zoner strategy constants
    perfect_zone = 0.45      # Ideal projectile distance
    comfort_zone = 0.35      # Good projectile range
    danger_zone = 0.15       # Too close, need escape
    panic_zone = 0.08        # Emergency escape needed
    max_range = 0.6          # Maximum effective range
    
    # Health and aggression thresholds
    critical_health = 0.25
    low_health = 0.4
    dominating_threshold = 0.5
    losing_threshold = -0.3
    
    # Stage positioning awareness
    stage_center = 0.5
    corner_proximity = 0.75
    my_corner_distance = abs(my_position_x - stage_center)
    opponent_corner_distance = abs(opponent_position_x - stage_center)
    
    # Calculate tactical situation
    im_cornered = my_corner_distance > corner_proximity
    opponent_cornered = opponent_corner_distance > corner_proximity
    projectile_available = my_projectile_cooldown < 0.15
    opponent_projectile_ready = opponent_projectile_cooldown < 0.15
    
    # Movement prediction based on velocity
    opponent_approaching = (relative_pos > 0 and opponent_velocity < -0.1) or (relative_pos < 0 and opponent_velocity > 0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity > 0.1) or (relative_pos < 0 and opponent_velocity < -0.1)
    
    # Combat state analysis
    under_pressure = opponent_attack_status > 0.3 or opponent_approaching
    safe_to_attack = opponent_block_status < 0.2 and not opponent_approaching
    opponent_vulnerable = opponent_attack_status > 0.5 or opponent_cornered
    
    # Health-based strategy modifiers
    desperate_mode = my_health < critical_health
    conservative_mode = my_health < low_health and health_advantage < 0
    aggressive_mode = health_advantage > dominating_threshold
    patience_mode = health_advantage > 0.2 and my_health > 0.6
    
    # Emergency panic situations
    if desperate_mode and distance < panic_zone:
        if under_pressure:
            # Block and try to escape
            if im_cornered:
                return 6  # Block in place
            elif relative_pos > 0:
                return 7  # Move left blocking
            else:
                return 8  # Move right blocking
        else:
            # Quick escape without blocking
            if im_cornered:
                if my_position_x < stage_center:
                    return 2  # Move toward center
                else:
                    return 1  # Move toward center
            elif relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
    
    # Ultra close range - immediate escape protocol
    if distance < panic_zone:
        escape_direction = 1 if relative_pos > 0 else 2
        
        # If cornered, move toward center
        if im_cornered:
            center_direction = 2 if my_position_x < stage_center else 1
            if under_pressure:
                return 7 if center_direction == 1 else 8  # Block while escaping
            else:
                return center_direction
        
        # Normal escape
        if under_pressure or conservative_mode:
            return 7 if escape_direction == 1 else 8  # Block while escaping
        else:
            return escape_direction
    
    # Danger zone - careful retreat
    elif distance < danger_zone:
        # If opponent is attacking, prioritize defense
        if under_pressure:
            if desperate_mode:
                return 6  # Pure block
            elif random.random() < 0.7:
                return 6  # Block most of the time
            else:
                # Try to escape with block
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        
        # Aggressive counter if dominating and opponent vulnerable
        elif aggressive_mode and opponent_vulnerable and random.random() < 0.4:
            if random.random() < 0.7:
                return 4  # Quick punch
            else:
                return 5  # Kick for more damage
        
        # Standard retreat
        else:
            retreat_direction = 1 if relative_pos > 0 else 2
            
            # Handle corner situations
            if im_cornered:
                center_direction = 2 if my_position_x < stage_center else 1
                if conservative_mode:
                    return 7 if center_direction == 1 else 8  # Block while moving
                else:
                    return center_direction
            
            # Normal retreat
            if conservative_mode or random.random() < 0.5:
                return 7 if retreat_direction == 1 else 8  # Block while retreating
            else:
                return retreat_direction
    
    # Medium range - transition zone
    elif distance < comfort_zone:
        # If losing badly, prioritize getting to projectile range
        if health_advantage < losing_threshold:
            retreat_direction = 1 if relative_pos > 0 else 2
            
            if im_cornered:
                center_direction = 2 if my_position_x < stage_center else 1
                return center_direction
            else:
                return retreat_direction
        
        # If projectile ready and good position
        elif projectile_available and safe_to_attack:
            if random.random() < 0.8:
                return 9  # Fire projectile
            else:
                # Reposition for better angle
                if random.random() < 0.5:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        # Projectile on cooldown - maintain distance and wait
        else:
            target_distance = comfort_zone + 0.1
            
            if distance < target_distance - 0.05:
                # Too close, back up
                retreat_direction = 1 if relative_pos > 0 else 2
                return retreat_direction
            elif distance > target_distance + 0.05:
                # Too far, move closer
                approach_direction = 2 if relative_pos > 0 else 1
                return approach