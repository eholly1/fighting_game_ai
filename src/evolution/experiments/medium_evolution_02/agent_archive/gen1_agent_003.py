"""
Evolutionary Agent: gen1_agent_003
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: fbea57548ccc4af9
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information with defensive programming
    distance = max(0.0, min(1.0, state[22])) if len(state) > 22 else 0.5
    relative_pos = max(-1.0, min(1.0, state[23])) if len(state) > 23 else 0.0
    health_advantage = max(-1.0, min(1.0, state[25])) if len(state) > 25 else 0.0
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract detailed fighter status information
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    opponent_x_pos = state[11] if len(state) > 11 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    opponent_y_pos = state[13] if len(state) > 13 else 0.0
    
    # Velocity and movement analysis
    my_x_vel = state[3] if len(state) > 3 else 0.0
    my_y_vel = state[4] if len(state) > 4 else 0.0
    opponent_x_vel = state[14] if len(state) > 14 else 0.0
    opponent_y_vel = state[15] if len(state) > 15 else 0.0
    
    # Combat state analysis
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    opponent_attacking = state[16] if len(state) > 16 else 0.0
    opponent_blocking = state[17] if len(state) > 17 else 0.0
    
    # Projectile and cooldown status
    my_projectile = state[7] if len(state) > 7 else 0.0
    opponent_projectile = state[18] if len(state) > 18 else 0.0
    my_cooldown = state[10] if len(state) > 10 else 0.0
    opponent_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Calculate dynamic threat assessment
    opponent_velocity = math.sqrt(opponent_x_vel**2 + opponent_y_vel**2)
    opponent_threat_level = opponent_attacking + (opponent_velocity * 0.5) + (1.0 if opponent_projectile > 0.5 else 0.0)
    my_mobility = math.sqrt(my_x_vel**2 + my_y_vel**2)
    
    # Advanced positioning analysis
    stage_position = my_x_pos  # Assuming 0-1 range for stage position
    near_corner = stage_position < 0.15 or stage_position > 0.85
    opponent_cornered = opponent_x_pos < 0.15 or opponent_x_pos > 0.85
    
    # Strategic range definitions with dynamic adjustment
    close_range = 0.10 + (0.03 * abs(height_diff))
    medium_range = 0.32 + (0.05 * opponent_velocity)
    far_range = 0.65
    
    # Health-based behavioral thresholds
    critical_health = -0.5
    low_health = -0.25
    even_health = 0.1
    advantage_health = 0.35
    dominant_health = 0.6
    
    # Randomization with weighted probabilities
    rand_primary = random.random()
    rand_secondary = random.random()
    rand_mix = random.random()
    
    # Time-based pattern mixing to avoid predictability
    pattern_shift = int((my_x_pos + opponent_x_pos) * 100) % 3
    
    # CRITICAL SURVIVAL MODE - Extremely low health
    if health_advantage < critical_health:
        if distance < close_range:
            # Desperate close-range survival
            if opponent_threat_level > 1.5:
                if near_corner:
                    # Cornered and threatened - try to escape with block-move
                    if relative_pos > 0:
                        return 7 if rand_primary < 0.7 else 6
                    else:
                        return 8 if rand_primary < 0.7 else 6
                else:
                    return 6  # Pure block when threatened
            elif rand_primary < 0.4:
                # Quick desperate attack
                return 4 if rand_secondary < 0.8 else 5
            else:
                # Defensive positioning
                if relative_pos > 0:
                    return 7  # Block-retreat left
                else:
                    return 8  # Block-retreat right
        
        elif distance < medium_range:
            # Medium range survival tactics
            if my_cooldown < 0.3 and rand_primary < 0.6:
                return 9  # Projectile to create space
            elif opponent_threat_level > 1.0:
                # Opponent approaching aggressively - create distance
                if relative_pos > 0:
                    return 1  # Move away left
                else:
                    return 2  # Move away right
            elif rand_primary < 0.3:
                return 9  # Try projectile
            else:
                return 6  # Defensive block
        
        else:
            # Far range - play keep-away
            if my_cooldown < 0.4:
                return 9  # Projectile spam
            elif opponent_velocity > 0.3:
                # Opponent closing distance - maintain range
                if relative_pos > 0:
                    return 1  # Move away
                else:
                    return 2  # Move away
            else:
                return 6  # Block and wait
    
    # DOMINANT AGGRESSIVE MODE - Large health advantage
    elif health_advantage > dominant_health:
        if distance < close_range:
            # Aggressive close combat with smart mixing
            if opponent_blocking > 0.5:
                # Opponent blocking - use throws/grabs or wait
                if rand_primary < 0.3:
                    return 5  # Strong kick to break guard
                elif rand_primary < 0.6:
                    return 3  # Jump to change angle
                else:
                    return 4  # Quick punch
            elif pattern_shift == 0:
                # Punch-focused pattern
                if rand_primary < 0.6:
                    return 4  # Quick punch
                elif rand_primary < 0.8:
                    return 5  # Mix in kick
                else:
                    return 3  # Jump attack
            elif pattern_shift == 1:
                # Kick-focused pattern
                if rand_primary < 0.6:
                    return 5  # Power kick
                elif rand_primary < 0.8:
                    return 4  # Quick punch
                else:
                    return 6  # Smart block
            else:
                # Mixed aggressive pattern
                if rand_primary < 0.4:
                    return 4 if rand_secondary < 0.5 else 5
                elif rand_primary < 0.7:
                    return 3  # Jump pressure
                else:
                    return 6  # Occasional defense
        
        elif distance < medium_range:
            # Medium range pressure
            if my_cooldown < 0.4 and rand_primary < 0.4:
                return 9