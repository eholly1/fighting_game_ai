"""
Evolutionary Agent: gen3_agent_009
==================================

Metadata:
{
  "generation": 3,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 2f6f9a7914b57fa8
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
    
    # Extract my fighter state
    my_health = max(0.0, min(1.0, state[1]))
    my_pos_x = max(-1.0, min(1.0, state[2]))
    my_velocity_x = max(-2.0, min(2.0, state[4]))
    my_attack_cooldown = max(0.0, state[7])
    my_block_status = max(0.0, state[8])
    my_projectile_cooldown = max(0.0, state[9])
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[12]))
    opponent_pos_x = max(-1.0, min(1.0, state[13]))
    opponent_velocity_x = max(-2.0, min(2.0, state[15]))
    opponent_attack_cooldown = max(0.0, state[18])
    opponent_block_status = max(0.0, state[19])
    
    # Strategic thresholds
    close_range = 0.10
    medium_range = 0.30
    far_range = 0.55
    
    critical_health = 0.20
    low_health = 0.35
    good_health = 0.65
    
    # Situation analysis
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    am_winning = health_advantage > 0.25
    am_losing = health_advantage < -0.25
    am_critical = my_health < critical_health
    am_low_health = my_health < low_health
    am_healthy = my_health > good_health
    
    # Opponent behavior analysis
    opponent_attacking = opponent_attack_cooldown > 0.08
    opponent_blocking = opponent_block_status > 0.05
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # My capabilities
    can_attack = my_attack_cooldown < 0.03
    can_projectile = my_projectile_cooldown < 0.03
    am_blocking = my_block_status > 0.05
    
    # Positional awareness
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    stage_center = abs(my_pos_x) < 0.3
    
    # Adaptive strategy counter (using health and distance as seed)
    strategy_seed = int((my_health + distance) * 100) % 10
    aggression_modifier = 0.1 + (strategy_seed * 0.05)
    
    # Critical survival mode
    if am_critical:
        if opponent_attacking and is_close:
            if random.random() < 0.85:
                return 6  # Emergency block
            else:
                # Desperate escape
                escape_direction = 1 if relative_pos > 0 else 2
                return escape_direction
        
        elif is_close and not opponent_blocking:
            if can_attack and random.random() < 0.6:
                return 4  # Quick desperation attack
            else:
                return 6  # Defensive block
        
        elif is_medium:
            if can_projectile and not opponent_blocking:
                return 9  # Safe projectile
            elif opponent_approaching:
                return 6  # Block incoming approach
            else:
                # Create distance
                retreat_direction = 1 if relative_pos > 0 else 2
                return retreat_direction
        
        else:  # Far range
            if can_projectile:
                return 9  # Safe projectile harassment
            else:
                return 0  # Wait for cooldown
    
    # Winning aggressive strategy
    elif am_winning and am_healthy:
        if opponent_cornered:
            # Press advantage when opponent is cornered
            if is_close:
                if opponent_blocking:
                    # Break guard with varied attacks
                    if random.random() < 0.5:
                        return 5  # Strong kick
                    else:
                        return 4  # Fast punch
                elif can_attack:
                    # Finish combo
                    return 5 if random.random() < 0.7 else 4
                else:
                    return 0  # Wait for attack cooldown
            else:
                # Close distance to cornered opponent
                approach_direction = 2 if relative_pos > 0 else 1
                return approach_direction
        
        elif is_close:
            if opponent_blocking:
                # Mix up to break defense
                rand_val = random.random()
                if rand_val < 0.3:
                    return 5  # Kick
                elif rand_val < 0.6:
                    return 4  # Punch
                else:
                    # Create space for projectile
                    space_direction = 1 if relative_pos > 0 else 2
                    return space_direction
            elif can_attack:
                # Aggressive pressure
                if opponent_health < low_health:
                    return 5  # Finish with strong attack
                else:
                    return 4 if random.random() < 0.6 else 5
            else:
                # Maintain pressure while waiting
                if opponent_retreating:
                    chase_direction = 2 if relative_pos > 0 else 1
                    return chase_direction
                else:
                    return 0
        
        elif is_medium:
            if opponent_blocking:
                # Flank or projectile pressure
                if can_projectile and random.random() < 0.7:
                    return 9
                else:
                    flank_direction = 2 if relative_pos > 0 else 1
                    return flank_direction
            elif opponent_retreating:
                # Aggressive pursuit
                chase_direction = 2 if relative_pos > 0 else 1
                return chase_direction
            else:
                # Close for attack
                advance_direction = 2 if relative_pos > 0 else 1
                return advance_direction
        
        else:  # Far range
            if can_projectile and not opponent_blocking:
                return 9  # Projectile pressure
            elif opponent_blocking:
                # Advance while they defend
                advance_direction = 2 if relative_pos > 0 else 1
                return advance_direction
            else:
                # Maintain projectile pressure
                if can_projectile:
                    return 9
                else:
                    return 0
    
    # Losing defensive-counter strategy
    elif am_losing:
        if is_very_far:
            if can_projectile and not opponent_blocking:
                return 9  # Safe long-range harassment
            elif opponent_approaching:
                # Prepare defense
                if can_projectile:
                    return 9  # Slow their approach
                else:
                    return 6  # Block preparation
            else:
                # Patient positioning
                if abs(relative_pos) > 0.5:
                    center_direction = 2