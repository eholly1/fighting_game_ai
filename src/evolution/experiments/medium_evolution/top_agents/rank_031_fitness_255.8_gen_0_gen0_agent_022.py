"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_022
Rank: 31/100
Generation: 0
Fighting Style: zoner

Performance Metrics:
- Fitness: 255.82
- Win Rate: 50.0%
- Average Reward: 255.82

Created: 2025-06-01 00:36:59
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
    
    # Extract player and opponent info
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position_x = state[0]
    opponent_position_x = state[11]
    
    # Extract combat status
    my_block_status = state[5] if len(state) > 5 else 0
    opponent_attack_status = state[16] if len(state) > 16 else 0
    my_projectile_cooldown = state[7] if len(state) > 7 else 0
    opponent_projectile_cooldown = state[18] if len(state) > 18 else 0
    
    # Define zoner strategy constants
    optimal_distance = 0.4  # Preferred fighting distance
    danger_zone = 0.12      # Too close for comfort
    projectile_range = 0.35 # Effective projectile distance
    retreat_threshold = 0.2 # When to retreat
    health_crisis = 0.3     # Critical health level
    
    # Calculate stage position awareness
    stage_center = 0.5
    near_corner = abs(my_position_x - stage_center) > 0.7
    opponent_cornered = abs(opponent_position_x - stage_center) > 0.7
    
    # Determine current tactical situation
    is_critical_health = my_health < health_crisis
    is_dominating = health_advantage > 0.4
    is_losing = health_advantage < -0.2
    projectile_ready = my_projectile_cooldown < 0.1
    opponent_aggressive = opponent_attack_status > 0.5
    
    # Emergency defensive situations
    if is_critical_health and distance < danger_zone:
        if opponent_aggressive:
            return 6  # Block incoming attack
        elif relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Ultra close range - escape immediately
    if distance < danger_zone:
        # Try to create space with movement
        if near_corner:
            # If near corner, move toward center
            if my_position_x < stage_center:
                if random.random() < 0.7:
                    return 8  # Move right blocking
                else:
                    return 2  # Move right quickly
            else:
                if random.random() < 0.7:
                    return 7  # Move left blocking
                else:
                    return 1  # Move left quickly
        else:
            # Normal escape
            if relative_pos > 0:
                if random.random() < 0.6:
                    return 7  # Move left blocking
                else:
                    return 1  # Move left
            else:
                if random.random() < 0.6:
                    return 8  # Move right blocking
                else:
                    return 2  # Move right
    
    # Close range but not ultra close
    elif distance < retreat_threshold:
        # If opponent is attacking, prioritize defense
        if opponent_aggressive:
            if random.random() < 0.8:
                return 6  # Block
            else:
                # Try to escape while blocking
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        
        # If we're dominating, might risk a quick attack
        elif is_dominating and random.random() < 0.3:
            if random.random() < 0.6:
                return 4  # Quick punch
            else:
                return 5  # Kick
        
        # Default: create space
        else:
            if near_corner:
                # Move toward center
                if my_position_x < stage_center:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                # Move away from opponent
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
    
    # Medium range - positioning phase
    elif distance < projectile_range:
        # If we're losing badly, try to get to projectile range
        if is_losing:
            if near_corner:
                # Escape corner first
                if my_position_x < stage_center:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                # Create more distance
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        # If projectile is ready and good positioning
        elif projectile_ready:
            # Sometimes reposition for better angle
            if random.random() < 0.2:
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                return 9  # Fire projectile
        
        # Wait for projectile cooldown while maintaining distance
        else:
            if distance < 0.25:  # Too close, back up
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                # Good distance, wait and watch
                if random.random() < 0.7:
                    return 0  # Idle, wait for cooldown
                else:
                    # Minor repositioning
                    if random.random() < 0.5:
                        return 1  # Move left
                    else:
                        return 2  # Move right
    
    # Optimal projectile range
    elif distance <= optimal_distance:
        if projectile_ready:
            # Perfect zoner range
            if random.random() < 0.85:
                return 9  # Fire projectile
            else:
                # Occasional repositioning for unpredictability
                if random.random() < 0.5:
                    return 1  # Move left
                else:
                    return 2  # Move right
        else:
            # Wait for projectile while maintaining position
            if opponent_projectile_cooldown < 0.1:
                # Opponent might fire, be ready to move
                if random.random() < 0.4:
                    return 1 if random.random() < 0.5 else 2
                else:
                    return 0  # Stand ground
            else:
                # Safe to wait
                if random.random() < 0.8:
                    return 0  # Idle
                else:
                    # Minor positioning adjustment
                    if random.random() < 0.5:
                        return 1  # Move left
                    else:
                        return 2  # Move right
    
    # Long range - maximum zoner effectiveness
    else:
        if projectile_ready:
            if random.random() < 0.9:
                return 9  # Fire projectile
            else:
                # Move to better angle
                if abs(relative_pos) < 0.1:  # Directly facing
                    return 9  # Perfect shot
                else:
                    # Adjust angle slightly
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
        
        # Projectile on cooldown at long range
        else:
            # If opponent is also at long range, maintain distance
            if opponent_cornered and not near_corner:
                # Perfect position, wait for cooldown
                return 0  # Idle