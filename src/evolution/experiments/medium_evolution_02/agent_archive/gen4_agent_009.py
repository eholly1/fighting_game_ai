"""
Evolutionary Agent: gen4_agent_009
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: b732b17751333bc9
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
    
    # Extract detailed fighter states with bounds checking
    my_health = max(0.0, min(1.0, state[1] if len(state) > 1 else 1.0))
    my_pos_x = max(-1.0, min(1.0, state[2] if len(state) > 2 else 0.0))
    my_pos_y = max(-1.0, min(2.0, state[3] if len(state) > 3 else 0.0))
    my_velocity_x = max(-2.0, min(2.0, state[4] if len(state) > 4 else 0.0))
    my_block_status = max(0.0, state[5] if len(state) > 5 else 0.0)
    my_attack_status = max(0.0, state[6] if len(state) > 6 else 0.0)
    my_attack_cooldown = max(0.0, state[7] if len(state) > 7 else 0.0)
    my_stun_time = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_projectile_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    opponent_health = max(0.0, min(1.0, state[12] if len(state) > 12 else 1.0))
    opponent_pos_x = max(-1.0, min(1.0, state[13] if len(state) > 13 else 0.0))
    opponent_pos_y = max(-1.0, min(2.0, state[14] if len(state) > 14 else 0.0))
    opponent_velocity_x = max(-2.0, min(2.0, state[15] if len(state) > 15 else 0.0))
    opponent_block_status = max(0.0, state[16] if len(state) > 16 else 0.0)
    opponent_attack_status = max(0.0, state[17] if len(state) > 17 else 0.0)
    opponent_attack_cooldown = max(0.0, state[18] if len(state) > 18 else 0.0)
    opponent_stun_time = max(0.0, state[19] if len(state) > 19 else 0.0)
    
    # Enhanced strategic range definitions
    melee_range = 0.12
    close_range = 0.18
    mid_range = 0.35
    long_range = 0.6
    max_range = 0.85
    
    # Health thresholds for tactical decisions
    critical_health = 0.15
    low_health = 0.3
    medium_health = 0.5
    high_health = 0.7
    full_health = 0.9
    
    # Combat state analysis
    am_in_melee = distance < melee_range
    am_in_close = melee_range <= distance < close_range
    am_in_mid = close_range <= distance < mid_range
    am_in_long = mid_range <= distance < long_range
    am_at_max = distance >= long_range
    
    # Health status checks
    am_critical = my_health <= critical_health
    am_low = my_health <= low_health
    am_healthy = my_health >= high_health
    opponent_critical = opponent_health <= critical_health
    opponent_low = opponent_health <= low_health
    
    # Action availability
    can_attack = my_attack_cooldown < 0.1
    can_projectile = my_projectile_cooldown < 0.1
    am_stunned = my_stun_time > 0.1
    am_blocking = my_block_status > 0.2
    am_attacking = my_attack_status > 0.2
    
    # Opponent state analysis
    opponent_attacking = opponent_attack_status > 0.3
    opponent_blocking = opponent_block_status > 0.2
    opponent_stunned = opponent_stun_time > 0.1
    opponent_can_attack = opponent_attack_cooldown < 0.1
    opponent_vulnerable = opponent_stunned or (opponent_attack_cooldown > 0.3)
    
    # Movement and positioning analysis
    am_airborne = my_pos_y > 0.1
    opponent_airborne = opponent_pos_y > 0.1
    height_advantage = my_pos_y - opponent_pos_y
    
    # Positional assessments
    am_cornered = abs(my_pos_x) > 0.7
    opponent_cornered = abs(opponent_pos_x) > 0.7
    space_behind_me = 1.0 - abs(my_pos_x) if my_pos_x != 0 else 1.0
    space_behind_opponent = 1.0 - abs(opponent_pos_x) if opponent_pos_x != 0 else 1.0
    
    # Velocity-based predictions
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.1) or (relative_pos < 0 and opponent_velocity_x < -0.1)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.1) or (relative_pos < 0 and opponent_velocity_x > 0.1)
    
    # Calculate dynamic aggression based on situation
    base_aggression = 0.5
    
    # Health-based aggression adjustments
    if am_healthy and opponent_low:
        base_aggression += 0.35
    elif am_healthy and health_advantage > 0.2:
        base_aggression += 0.2
    elif am_critical:
        base_aggression -= 0.4
    elif am_low:
        base_aggression -= 0.2
    
    # Positional aggression modifiers
    if opponent_cornered and not am_cornered:
        base_aggression += 0.25
    elif am_cornered:
        base_aggression -= 0.3
    
    # Opportunity-based aggression
    if opponent_vulnerable:
        base_aggression += 0.3
    if opponent_critical:
        base_aggression += 0.4
    
    current_aggression = max(0.1, min(0.9, base_aggression))
    
    # Emergency defensive protocols
    if am_stunned:
        return 0  # Can't act while stunned
    
    if am_critical and opponent_attacking and (am_in_melee or am_in_close):
        # Critical health emergency response
        if random.random() < 0.7:
            return 6  # Priority block
        else:
            # Escape with guard
            if space_behind_me > 0.3:
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
            else:
                return 6  # Block if no escape room
    
    # Advanced corner escape system
    if am_cornered and distance < mid_range:
        if opponent_approaching and not opponent_vulnerable:
            # Defend while cornered
            if opponent_attacking:
                return 6  # Block incoming attack
            else:
                # Create escape opportunity
                escape_roll