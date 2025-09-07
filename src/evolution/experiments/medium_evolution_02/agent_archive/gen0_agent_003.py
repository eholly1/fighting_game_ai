"""
Evolutionary Agent: gen0_agent_003
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "balanced",
  "win_rate": 0.5
}

Code Hash: 96401c74cfc453cd
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22])) if len(state) > 22 else 0.5
    relative_pos = max(-1.0, min(1.0, state[23])) if len(state) > 23 else 0.0
    health_advantage = max(-1.0, min(1.0, state[25])) if len(state) > 25 else 0.0
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    opponent_health = state[12] if len(state) > 12 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    opponent_x_pos = state[11] if len(state) > 11 else 0.5
    
    # Check if opponent is attacking (high velocity or specific states)
    opponent_attacking = False
    if len(state) > 15:
        opponent_vel = abs(state[13]) + abs(state[14])  # x and y velocity
        opponent_attacking = opponent_vel > 0.3 or state[15] > 0.5  # attack state
    
    # Check my current status
    my_blocking = state[7] if len(state) > 7 else 0.0
    my_attacking = state[4] if len(state) > 4 else 0.0
    projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Strategic thresholds
    close_range = 0.12
    medium_range = 0.35
    far_range = 0.6
    
    # Health-based aggression levels
    desperate_health = -0.4
    confident_health = 0.3
    dominant_health = 0.6
    
    # Randomization factor for unpredictability
    rand_factor = random.random()
    
    # EMERGENCY DEFENSIVE BEHAVIOR - Critically low health
    if health_advantage < desperate_health:
        if distance < close_range:
            # Very close and losing - emergency block or retreat
            if opponent_attacking:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking (retreat)
            else:
                return 8  # Move right while blocking (retreat)
        elif distance < medium_range:
            # Medium range - create distance with projectiles
            if projectile_cooldown < 0.3:
                return 9  # Projectile to keep distance
            else:
                # Move away from opponent
                if relative_pos > 0:
                    return 1  # Move left (away)
                else:
                    return 2  # Move right (away)
        else:
            # Far range - spam projectiles if possible
            if projectile_cooldown < 0.5:
                return 9  # Long range projectile
            else:
                return 6  # Block while waiting for cooldown
    
    # DOMINANT BEHAVIOR - Significant health advantage
    elif health_advantage > dominant_health:
        if distance < close_range:
            # Close range dominance - aggressive mixing
            if rand_factor < 0.4:
                return 4  # Quick punch
            elif rand_factor < 0.7:
                return 5  # Strong kick
            elif rand_factor < 0.85:
                return 3  # Jump attack setup
            else:
                return 6  # Occasional block for safety
        elif distance < medium_range:
            # Medium range - close distance aggressively
            if rand_factor < 0.3:
                return 9  # Projectile pressure
            elif relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        else:
            # Far range - projectile pressure
            if projectile_cooldown < 0.6:
                return 9  # Projectile spam
            elif relative_pos > 0:
                return 2  # Close distance
            else:
                return 1  # Close distance
    
    # CONFIDENT BEHAVIOR - Moderate health advantage
    elif health_advantage > confident_health:
        if distance < close_range:
            # Close combat with measured aggression
            if opponent_attacking and rand_factor < 0.3:
                return 6  # Smart blocking
            elif rand_factor < 0.5:
                return 4  # Balanced punch/kick mix
            elif rand_factor < 0.8:
                return 5  # Kick for damage
            else:
                return 3  # Jump for positioning
        elif distance < medium_range:
            # Optimal positioning range
            if rand_factor < 0.4:
                return 9  # Projectile setup
            elif rand_factor < 0.6:
                # Move toward optimal range
                if relative_pos > 0:
                    return 2  # Approach
                else:
                    return 1  # Approach
            elif rand_factor < 0.8:
                return 4  # Quick strike
            else:
                return 6  # Defensive option
        else:
            # Long range control
            if projectile_cooldown < 0.4:
                return 9  # Projectile control
            else:
                # Close to medium range
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
    
    # BALANCED/EVEN BEHAVIOR - Close health situation
    elif health_advantage > -0.2:
        if distance < close_range:
            # Careful close combat
            if opponent_attacking:
                if rand_factor < 0.6:
                    return 6  # Block most attacks
                elif relative_pos > 0:
                    return 7  # Block and reposition
                else:
                    return 8  # Block and reposition
            else:
                # Opponent not attacking - mixed offense
                if rand_factor < 0.35:
                    return 4  # Quick punch
                elif rand_factor < 0.65:
                    return 5  # Power kick
                elif rand_factor < 0.8:
                    return 6  # Block anticipation
                else:
                    return 3  # Jump mix-up
        elif distance < medium_range:
            # Medium range tactical play
            if rand_factor < 0.25:
                return 9  # Projectile option
            elif rand_factor < 0.4:
                return 4  # Quick strike
            elif rand_factor < 0.6:
                # Positioning
                if relative_pos > 0:
                    return 2  # Move toward opponent
                else:
                    return 1  # Move toward opponent
            elif rand_factor < 0.8:
                return 6  # Defensive stance
            else:
                return 3  # Jump for position
        else:
            # Long range neutral game
            if projectile_cooldown < 0.5:
                return 9  # Projectile game
            elif rand_factor < 0.6:
                # Close distance
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                return 6  # Patient defense
    
    # DEFENSIVE BEHAVIOR - Moderate disadvantage
    else:
        if distance < close_range:
            # Close range defense
            if opponent_attacking:
                return 6  # Priority block
            elif rand_factor < 0.3:
                return 4  # Quick counterattack
            elif rand_factor < 0.5:
                return 5  # Strong counter
            elif rand_factor < 0.7:
                return 6  # Continue blocking
            else:
                # Repositioning retreat
                if relative_pos > 0:
                    return 7  # Move left with