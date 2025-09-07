"""
Evolutionary Agent: gen3_agent_028
==================================

Metadata:
{
  "generation": 3,
  "fitness": 67.19999999999672,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 8615286631321fd4
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
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = state[0]
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[7]
    my_blocking = state[8]
    my_projectile_cooldown = max(0.0, state[9])
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_x_pos = state[11]
    opponent_y_pos = state[12]
    opponent_x_vel = state[14]
    opponent_y_vel = state[15]
    opponent_attacking = state[18]
    opponent_blocking = state[19]
    opponent_projectile_cooldown = max(0.0, state[20])
    
    # Advanced tactical parameters for next-gen hybrid fighter
    close_range = 0.12
    medium_range = 0.30
    far_range = 0.50
    critical_health = -0.45
    dominant_health = 0.35
    retreat_threshold = 0.16
    
    # Evolved aggression system with multi-factor analysis
    base_aggression = 0.58
    momentum_multiplier = 0.0
    positioning_bonus = 0.0
    risk_factor = 0.0
    
    # Enhanced momentum calculation with trend analysis
    if health_advantage > 0.15:
        momentum_multiplier = min(0.35, health_advantage * 0.6)
        if distance < 0.25:
            positioning_bonus = 0.15
    elif health_advantage < -0.15:
        momentum_multiplier = max(-0.45, health_advantage * 0.8)
        risk_factor = abs(health_advantage) * 0.3
    
    # Adaptive distance control bonus
    if distance < 0.18 and health_advantage > 0.1:
        positioning_bonus += 0.18
    elif distance > 0.42 and my_projectile_cooldown < 0.25:
        positioning_bonus += 0.12
    elif 0.2 < distance < 0.35:
        positioning_bonus += 0.08  # Sweet spot bonus
    
    current_aggression = max(0.15, min(0.88, base_aggression + momentum_multiplier + positioning_bonus - risk_factor))
    
    # Advanced opponent behavioral pattern detection
    opponent_advancing = False
    opponent_retreating = False
    opponent_circling = False
    velocity_threshold = 0.035
    
    # Movement pattern analysis
    if relative_pos > 0 and opponent_x_vel > velocity_threshold:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_x_vel < -velocity_threshold:
        opponent_advancing = True
    elif relative_pos > 0 and opponent_x_vel < -velocity_threshold:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > velocity_threshold:
        opponent_retreating = True
    elif abs(opponent_x_vel) > velocity_threshold * 0.6:
        opponent_circling = True
    
    # Enhanced opponent archetype recognition
    opponent_aggressive = opponent_attacking > 0.45 and distance < 0.28
    opponent_defensive = opponent_blocking > 0.55 or (opponent_retreating and health_advantage < -0.1)
    opponent_projectile_focused = opponent_projectile_cooldown < 0.18 and distance > 0.32
    opponent_combo_heavy = opponent_attacking > 0.6 and distance < 0.15
    opponent_counter_fighter = opponent_blocking > 0.4 and opponent_attacking > 0.3
    
    # Critical survival protocols with intelligent escape routes
    if my_health < 0.10 or health_advantage < -0.65:
        if distance < retreat_threshold:
            if opponent_attacking > 0.65:
                return 6  # Emergency block
            elif opponent_combo_heavy:
                # Escape combo pressure
                if relative_pos > 0:
                    return 7  # Block retreat left
                else:
                    return 8  # Block retreat right
            else:
                # Smart repositioning
                if my_projectile_cooldown < 0.2:
                    return 9  # Counter with projectile
                elif relative_pos > 0:
                    return 7  # Move left with guard
                else:
                    return 8  # Move right with guard
        elif distance < 0.25 and my_projectile_cooldown < 0.12:
            return 9  # Desperate zoning projectile
        else:
            return 6  # Conservative blocking
    
    # Dominant finishing protocols when opponent is vulnerable
    if opponent_health < 0.12 and health_advantage > 0.25:
        if distance < close_range + 0.06:
            # Execute finish with style mixing
            finish_roll = random.random()
            if finish_roll < 0.45:
                return 5  # Power kick finish
            elif finish_roll < 0.75:
                return 4  # Speed punch finish
            else:
                return 3  # Jump attack finish
        elif distance < medium_range + 0.05:
            # Aggressive approach for finish
            if relative_pos > 0:
                return 2  # Close right
            else:
                return 1  # Close left
        elif my_projectile_cooldown < 0.15:
            return 9  # Chip damage projectile
    
    # Close range combat with advanced frame data considerations
    if distance < close_range:
        # Sophisticated counter-attack system
        if opponent_attacking > 0.65:
            counter_probability = 0.70 if health_advantage > 0 else 0.85
            frame_advantage_check = random.random()
            
            if frame_advantage_check < counter_probability:
                if opponent_combo_heavy:
                    return 6  # Block string first
                else:
                    # Quick counter options
                    if random.random() < 0.7:
                        return 4  # Fast counter punch
                    else:
                        return 6  # Safe block
            else:
                # Risky interrupt attempts
                return 5  # Heavy counter kick
        
        # Advanced guard break and mix-up system
        if opponent_blocking > 0.72:
            guard_break_tactic = random.random()
            if guard_break_tactic < 0.28:
                return 5  # Heavy attack to break
            elif guard_break_tactic < 0.48:
                return 3  # Overhead jump attack
            elif guard_break_tactic < 0.68:
                # Throw attempt simulation with movement
                if relative_pos > 0:
                    return 1  # Move for throw setup
                else:
                    return 2  # Move for throw setup  
            elif guard_break_tactic < 0.82:
                return 0  # Reset neutral game
            else:
                return 9 if my_projectile_cooldown < 0.25 else 6  # Projectile reset
        
        # Pressure system with health-based adjustments
        if health_advantage > 0.12 and opponent_blocking < 0.35:
            pressure_sequence = random.random()
            if pressure_sequence < 0.35:
                return 4  # Light attack pressure