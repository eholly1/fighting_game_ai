"""
Evolutionary Agent: gen4_agent_010
==================================

Metadata:
{
  "generation": 4,
  "fitness": 174.41666666666202,
  "fighting_style": "evolved",
  "win_rate": 0.3333333333333333
}

Code Hash: a90d4374b21dc654
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
    
    # Extract my fighter status with bounds checking
    my_health = max(0.0, min(1.0, state[2]))
    my_position = state[0]
    my_velocity_x = state[7]
    my_velocity_y = state[8]
    my_attack_status = max(0.0, state[4])
    my_block_status = max(0.0, state[5])
    my_projectile_cooldown = max(0.0, state[6])
    
    # Extract opponent status
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_position = state[11]
    opponent_velocity_x = state[18]
    opponent_velocity_y = state[19]
    opponent_attack_status = max(0.0, state[15])
    opponent_block_status = max(0.0, state[16])
    opponent_projectile_cooldown = max(0.0, state[17])
    
    # Hybrid tactical range definitions
    point_blank_range = 0.03
    ultra_close_range = 0.08
    close_range = 0.15
    mid_close_range = 0.22
    mid_range = 0.35
    far_range = 0.5
    ultra_far_range = 0.7
    
    # Health and positioning thresholds
    critical_health = 0.12
    low_health = 0.3
    good_health = 0.7
    corner_threshold = 0.75
    center_zone = 0.4
    
    # Status analysis
    projectile_ready = my_projectile_cooldown < 0.1
    projectile_available = my_projectile_cooldown < 0.2
    opponent_projectile_threat = opponent_projectile_cooldown < 0.15
    opponent_airborne = abs(height_diff) > 0.2
    
    # Movement and positioning analysis
    opponent_advancing = (relative_pos > 0 and opponent_velocity_x > -0.1) or (relative_pos < 0 and opponent_velocity_x < 0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.25) or (relative_pos < 0 and opponent_velocity_x > 0.25)
    am_cornered = abs(my_position) > corner_threshold
    opponent_cornered = abs(opponent_position) > corner_threshold
    in_center = abs(my_position) < center_zone
    
    # Dynamic aggression calculation for hybrid approach
    base_aggression = 0.6
    health_modifier = health_advantage * 0.3
    distance_modifier = max(-0.2, min(0.2, (mid_range - distance) * 0.5))
    position_modifier = 0.2 if opponent_cornered else (-0.15 if am_cornered else 0.05)
    momentum_modifier = 0.1 if opponent_retreating else (-0.05 if opponent_advancing else 0)
    
    current_aggression = max(0.2, min(0.95, base_aggression + health_modifier + distance_modifier + position_modifier + momentum_modifier))
    
    # Adaptive defense priority
    defense_priority = 0.35
    if my_health < critical_health:
        defense_priority = 0.8
    elif my_health < low_health:
        defense_priority = 0.55
    elif health_advantage < -0.35:
        defense_priority = 0.65
    elif opponent_attack_status > 0.6:
        defense_priority = 0.7
    
    # Critical survival mode
    if my_health <= critical_health:
        if opponent_attack_status > 0.4 and distance < mid_range:
            return 6  # Emergency block
        
        if distance <= ultra_close_range:
            if projectile_ready and random.random() < 0.35:
                return 9  # Desperate point-blank projectile
            elif opponent_airborne:
                return 4  # Anti-air attempt
            else:
                return 6  # Block and pray
        
        if distance < close_range and not am_cornered:
            # Escape with defensive movement
            escape_dir = 7 if relative_pos > 0 else 8
            return escape_dir
        
        if distance > mid_range and projectile_ready:
            return 9  # Long range chip damage
        
        if distance < mid_range:
            retreat_dir = 1 if relative_pos > 0 else 2
            return retreat_dir
        
        return 6  # Default defensive
    
    # Enhanced opponent attack response
    if opponent_attack_status > 0.3:
        threat_proximity = 1.0 - distance
        
        if distance <= point_blank_range:
            return 6  # Must block at point blank
        
        elif distance <= ultra_close_range:
            if my_health > low_health and current_aggression > 0.7:
                # Risky counter-attack
                return 4 if random.random() < 0.4 else 6
            else:
                return 6  # Safe block
        
        elif distance <= close_range:
            defense_chance = defense_priority + (threat_proximity * 0.3)
            if random.random() < defense_chance:
                if am_cornered:
                    return 6  # Static block when cornered
                else:
                    # Mobile defense
                    return 7 if relative_pos > 0 else 8
            else:
                # Counter with projectile if available
                if projectile_ready:
                    return 9
                else:
                    return 6
        
        elif distance <= mid_range:
            if projectile_ready and random.random() < 0.6:
                return 9  # Counter-projectile
            elif random.random() < 0.4:
                return 6  # Block
            else:
                # Advance during opponent's attack
                return 2 if relative_pos > 0 else 1
        
        else:
            # Long range opponent attack - advance or counter
            if projectile_ready:
                return 9
            else:
                return 2 if relative_pos > 0 else 1
    
    # Advanced anti-air system
    if opponent_airborne:
        if distance <= mid_range:
            if projectile_ready and distance > ultra_close_range:
                return 9  # Projectile anti-air
            elif distance <= close_range:
                return 4  # Quick anti-air punch
            else:
                # Position for landing punish
                return 2 if relative_pos > 0 else 1
        elif distance <= far_range and projectile_ready:
            return 9  # Long range anti-air
        else:
            # Close distance while opponent is airborne
            return 2 if relative_pos > 0 else 1
    
    # Projectile warfare and spacing
    if opponent_projectile_threat and distance > mid_close_range:
        if projectile_ready:
            projectile_duel_chance = 0.7 if distance > mid_range else 0.4
            if random.random() < projectile_duel_chance:
                return 9  # Projectile trade
            else:
                # Evasive advance
                if random.random() < 0.3:
                    return 3  # Jump approach
                else:
                    return 2 if relative_pos > 0 else 1