"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_012
Rank: 30/100
Generation: 0
Fighting Style: zoner

Performance Metrics:
- Fitness: 256.62
- Win Rate: 0.0%
- Average Reward: 256.62

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
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract player state information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent state information
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    
    # Define strategic thresholds for zoner playstyle
    optimal_distance = 0.4  # Preferred fighting distance
    danger_distance = 0.15  # Too close for comfort
    max_distance = 0.8      # Maximum effective range
    projectile_range = 0.3  # Minimum distance for projectiles
    
    # Health-based aggression modifiers
    desperate_threshold = -0.6  # When losing badly
    winning_threshold = 0.4     # When winning decisively
    conservative_threshold = -0.2  # When slightly behind
    
    # Movement and positioning parameters
    corner_threshold = 0.1  # Near stage edge
    retreat_urgency = 0.8   # How aggressively to retreat when close
    
    # Projectile management
    projectile_ready = my_projectile_cooldown <= 0.1
    projectile_spam_distance = 0.5  # Distance for safe projectile spam
    
    # Opponent behavior analysis
    opponent_rushing = opp_velocity_x != 0 and distance < 0.3
    opponent_blocking = opp_block_status > 0.5
    opponent_attacking = opp_attack_status > 0.5
    opponent_airborne = abs(height_diff) > 0.2
    
    # Emergency defensive situations
    if distance < danger_distance and opponent_attacking:
        if health_advantage < conservative_threshold:
            # Desperate situation - block and retreat
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            # Can afford to trade - quick counter
            if random.random() < 0.3:
                return 4  # Quick punch
            else:
                return 6  # Block
    
    # Critical health management
    if health_advantage < desperate_threshold:
        # Losing badly - play very defensively
        if distance < projectile_range:
            # Too close - retreat while blocking
            if my_x_pos < corner_threshold:
                return 8  # Move right while blocking
            elif my_x_pos > (1.0 - corner_threshold):
                return 7  # Move left while blocking
            else:
                # Choose retreat direction based on opponent position
                if relative_pos > 0:
                    return 7  # Move away left
                else:
                    return 8  # Move away right
        else:
            # Safe distance - spam projectiles
            if projectile_ready:
                return 9  # Projectile
            else:
                # Maintain distance while cooldown recovers
                if distance < optimal_distance:
                    if relative_pos > 0:
                        return 1  # Move left (away)
                    else:
                        return 2  # Move right (away)
                else:
                    return 0  # Idle while waiting
    
    # Winning decisively - controlled aggression
    elif health_advantage > winning_threshold:
        if distance > max_distance:
            # Too far - close in slightly
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        elif distance > projectile_range:
            # Perfect zoning range
            if projectile_ready:
                if opponent_blocking:
                    # Mix up timing against blocking opponent
                    if random.random() < 0.3:
                        return 0  # Idle to break rhythm
                    else:
                        return 9  # Projectile
                else:
                    return 9  # Projectile
            else:
                # Maintain position while cooldown recovers
                if opponent_rushing:
                    if relative_pos > 0:
                        return 1  # Move away left
                    else:
                        return 2  # Move away right
                else:
                    return 0  # Idle
        else:
            # Too close for comfort - create space
            if my_x_pos < corner_threshold:
                return 2  # Move right to avoid corner
            elif my_x_pos > (1.0 - corner_threshold):
                return 1  # Move left to avoid corner
            else:
                if relative_pos > 0:
                    return 1  # Move left (away)
                else:
                    return 2  # Move right (away)
    
    # Neutral or slightly losing game state
    else:
        # Core zoner gameplay
        if distance > projectile_spam_distance:
            # Long range - projectile pressure
            if projectile_ready:
                if opponent_airborne:
                    # Lead the target if opponent is jumping
                    return 9  # Projectile
                elif opponent_blocking:
                    # Vary timing against defensive opponents
                    if random.random() < 0.4:
                        # Pause to break their rhythm
                        return 0  # Idle
                    else:
                        return 9  # Projectile
                else:
                    return 9  # Projectile
            else:
                # No projectile available - manage distance
                if distance > max_distance:
                    # Close in slightly
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    # Maintain distance
                    return 0  # Idle
        
        elif distance > optimal_distance:
            # Medium-long range - optimal zoning distance
            if projectile_ready:
                if opponent_rushing:
                    # Opponent closing in - prioritize spacing
                    if random.random() < 0.7:
                        return 9  # Projectile to stop rush
                    else:
                        # Retreat while shooting
                        if relative_pos > 0:
                            return 1  # Move away left
                        else:
                            return 2  # Move away right
                else:
                    # Opponent not rushing - safe to projectile
                    return 9  # Project