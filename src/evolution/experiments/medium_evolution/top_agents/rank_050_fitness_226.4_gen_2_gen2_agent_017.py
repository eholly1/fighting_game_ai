"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_017
Rank: 50/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 226.40
- Win Rate: 0.0%
- Average Reward: 226.40

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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = state[2] if len(state) > 2 else 0.5
    my_velocity_x = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[7] if len(state) > 7 else 0.0
    my_block_status = state[8] if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = state[13] if len(state) > 13 else 0.5
    opponent_velocity_x = state[15] if len(state) > 15 else 0.0
    opponent_attack_status = state[18] if len(state) > 18 else 0.0
    opponent_block_status = state[19] if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Define enhanced tactical ranges
    danger_range = 0.05
    ultra_close_range = 0.10
    close_range = 0.18
    medium_range = 0.30
    ideal_range = 0.42
    far_range = 0.60
    max_range = 0.85
    
    # Hybrid fighting parameters - evolved from parents
    base_aggression = 0.68
    zone_preference = 0.72
    counter_timing = 0.20
    defensive_threshold = 0.65
    
    # Advanced health-based adaptation
    health_ratio = my_health / max(0.1, opponent_health)
    critical_health = my_health < 0.12
    low_health = my_health < 0.28
    winning_health = health_advantage > 0.35
    losing_health = health_advantage < -0.35
    
    # Dynamic aggression calculation
    if winning_health:
        current_aggression = min(0.9, base_aggression + 0.22)
        zone_priority = 0.4
    elif losing_health:
        current_aggression = max(0.35, base_aggression - 0.33)
        zone_priority = 0.85
    else:
        current_aggression = base_aggression
        zone_priority = zone_preference
    
    # Projectile management
    projectile_ready = my_projectile_cooldown < 0.05
    projectile_soon = my_projectile_cooldown < 0.15
    opponent_projectile_threat = opponent_projectile_cooldown < 0.08
    
    # Enhanced opponent behavior analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_aggressive = opponent_attack_status > 0.4 or opponent_approaching
    opponent_defensive = opponent_block_status > 0.5
    opponent_jumping = height_diff < -0.2
    
    # Advanced wall awareness
    near_left_wall = my_pos_x < -0.6
    near_right_wall = my_pos_x > 0.6
    opponent_cornered = opponent_pos_x < -0.65 or opponent_pos_x > 0.65
    wall_behind_me = (relative_pos > 0 and near_left_wall) or (relative_pos < 0 and near_right_wall)
    
    # Critical survival mode
    if critical_health:
        if opponent_attack_status > 0.3 and distance < close_range:
            return 6  # Emergency block
        
        if distance < ultra_close_range:
            # Escape with blocking movement
            if wall_behind_me:
                if height_diff > -0.15:
                    return 3  # Jump escape
                else:
                    return 6  # Block and hope
            else:
                if relative_pos > 0:
                    return 7  # Block retreat left
                else:
                    return 8  # Block retreat right
        
        if projectile_ready and distance > medium_range:
            return 9  # Desperate projectile
        
        # Create distance
        if distance < medium_range and not wall_behind_me:
            if relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        
        return 6  # Default block in crisis
    
    # Anti-air response
    if opponent_jumping and distance < medium_range:
        if projectile_ready:
            return 9  # Anti-air projectile
        elif distance < close_range:
            return 6  # Block potential dive
        else:
            # Create space for landing
            if relative_pos > 0 and not near_left_wall:
                return 1
            elif not near_right_wall:
                return 2
            else:
                return 6
    
    # Immediate threat response
    if opponent_attack_status > 0.6:
        if distance < close_range:
            if low_health or random.random() < defensive_threshold:
                return 6  # Block confirmed attacks
            elif distance > ultra_close_range and projectile_ready:
                return 9  # Counter with projectile
            else:
                return 6  # Safe block
        elif distance < medium_range and projectile_ready:
            return 9  # Punish whiffed attacks
    
    # Counter-attack window detection
    if opponent_attack_status < 0.1 and my_attack_status < 0.1:
        # Opponent just finished attacking
        if distance <= close_range and random.random() < (current_aggression + 0.2):
            if winning_health:
                return 5  # Power counter when ahead
            else:
                return 4  # Safe counter
    
    # Range-based hybrid strategy
    if distance <= danger_range:
        # Extreme close - prioritize defense and spacing
        if opponent_aggressive:
            return 6  # Block imminent attacks
        elif opponent_defensive:
            # Mix up guard breaks
            mixup = random.random()
            if mixup < 0.25 and projectile_ready:
                return 9  # Point-blank projectile
            elif mixup < 0.55:
                return 5  # Strong attack vs block
            else:
                return 4  # Quick attack
        else:
            # Neutral danger range
            if current_aggression > 0.7:
                return 4 if random.random() < 0.7 else 5
            else:
                return 6  # Defensive stance
    
    elif distance <= ultra_close_range:
        # Ultra-close combat
        if opponent_defensive:
            # Patient pressure
            action_roll = random.random()
            if action_roll < 0.3:
                return 5