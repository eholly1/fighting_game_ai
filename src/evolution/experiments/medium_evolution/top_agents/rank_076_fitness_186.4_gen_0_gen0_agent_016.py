"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_016
Rank: 76/100
Generation: 0
Fighting Style: counter_puncher

Performance Metrics:
- Fitness: 186.44
- Win Rate: 0.0%
- Average Reward: 186.44

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
    
    # Extract player and opponent states with bounds checking
    my_health = max(0.0, min(1.0, state[2])) if len(state) > 2 else 0.5
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[1] if len(state) > 1 else 0.0
    my_x_vel = state[3] if len(state) > 3 else 0.0
    my_y_vel = state[4] if len(state) > 4 else 0.0
    my_is_attacking = state[5] if len(state) > 5 else 0.0
    my_is_blocking = state[6] if len(state) > 6 else 0.0
    my_attack_cooldown = state[7] if len(state) > 7 else 0.0
    my_block_cooldown = state[8] if len(state) > 8 else 0.0
    my_stun_duration = state[9] if len(state) > 9 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opp_health = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[12] if len(state) > 12 else 0.0
    opp_x_vel = state[14] if len(state) > 14 else 0.0
    opp_y_vel = state[15] if len(state) > 15 else 0.0
    opp_is_attacking = state[16] if len(state) > 16 else 0.0
    opp_is_blocking = state[17] if len(state) > 17 else 0.0
    opp_attack_cooldown = state[18] if len(state) > 18 else 0.0
    opp_block_cooldown = state[19] if len(state) > 19 else 0.0
    opp_stun_duration = state[20] if len(state) > 20 else 0.0
    opp_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define strategic thresholds for counter-puncher style
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    critical_health = 0.25
    low_health = 0.4
    winning_threshold = 0.2
    losing_threshold = -0.2
    
    # Counter-puncher patience factor - wait for opportunities
    patience_factor = 0.3 + (health_advantage * 0.2)
    aggression_modifier = max(0.1, min(0.8, patience_factor))
    
    # Emergency survival mode when critically low health
    if my_health < critical_health and health_advantage < -0.4:
        if distance < close_range and opp_is_attacking > 0.5:
            # Emergency block against incoming attack
            return 6
        elif distance > medium_range:
            # Keep distance and use projectiles
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                # Move away while blocking
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
        else:
            # Medium range, create distance
            if relative_pos > 0:
                return 7  # Move left block
            else:
                return 8  # Move right block
    
    # Counter-puncher core: Detect opponent vulnerability windows
    opponent_vulnerable = False
    if opp_attack_cooldown > 0.3 or opp_stun_duration > 0.1:
        opponent_vulnerable = True
    elif opp_is_attacking > 0.5 and distance < close_range:
        # Opponent is attacking at close range - prepare counter
        opponent_vulnerable = True
    elif abs(opp_x_vel) > 0.8:
        # Opponent moving fast, likely vulnerable after movement
        opponent_vulnerable = True
    
    # Stunned state - can't act effectively
    if my_stun_duration > 0.2:
        return 6  # Block while stunned
    
    # Close range tactics (0.0 - 0.12)
    if distance < close_range:
        # Opponent is attacking - counter opportunity
        if opp_is_attacking > 0.5 and opponent_vulnerable:
            if my_attack_cooldown < 0.1:
                # Quick counter punch
                return 4
            else:
                # Block the attack first
                return 6
        
        # Opponent just finished attacking (cooldown active)
        elif opp_attack_cooldown > 0.2 and my_attack_cooldown < 0.1:
            # Perfect counter window
            if random.random() < 0.7:
                return 5  # Strong kick counter
            else:
                return 4  # Quick punch
        
        # Opponent is blocking - mix up or create space
        elif opp_is_blocking > 0.5:
            if random.random() < 0.4:
                # Try to break guard with kick
                return 5
            else:
                # Create space and reset
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        # Health disadvantage - play defensive
        elif health_advantage < losing_threshold:
            if random.random() < 0.6:
                return 6  # Block
            else:
                # Create distance while blocking
                if relative_pos > 0:
                    return 7
                else:
                    return 8
        
        # Health advantage - controlled aggression
        elif health_advantage > winning_threshold and opponent_vulnerable:
            if my_attack_cooldown < 0.1:
                return 4 if random.random() < 0.6 else 5
            else:
                return 6  # Block until ready
        
        # Default close range - cautious blocking
        else:
            return 6
    
    # Medium range tactics (0.12 - 0.35)
    elif distance < medium_range:
        # Opponent approaching with attack
        if opp_is_attacking > 0.5 and abs(opp_x_vel) > 0.3:
            # Prepare counter - move back and block
            if relative_pos > 0:
                return 7  # Block while moving left
            else:
                return 8  # Block while moving right
        
        # Opponent vulnerable and we have health advantage
        elif opponent_vulnerable and health_advantage > 0 and my_attack_cooldown < 0.1:
            # Close distance for counter attack
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        
        # Opponent moving away - projectile opportunity
        elif abs(opp_x_vel) > 0.5 and my_projectile_cooldown < 0.1:
            # Sign they're creating distance - intercept with projectile
            return 9