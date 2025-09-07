"""
Evolutionary Agent: gen2_agent_012
==================================

Metadata:
{
  "generation": 2,
  "fitness": 273.9399999999984,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 3fbb20d270bf6848
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
    
    # Enhanced tactical parameters for evolved balanced fighter
    close_range = 0.13
    medium_range = 0.28
    far_range = 0.45
    critical_health = -0.4
    winning_health = 0.3
    retreat_distance = 0.18
    
    # Dynamic aggression system with momentum tracking
    base_aggression = 0.55
    momentum_factor = 0.0
    
    # Calculate momentum based on health trends and positioning
    if health_advantage > 0.1:
        momentum_factor = min(0.3, health_advantage * 0.5)
    elif health_advantage < -0.1:
        momentum_factor = max(-0.4, health_advantage * 0.7)
    
    # Adjust aggression based on distance advantage
    distance_factor = 0.0
    if distance < 0.2 and health_advantage > 0:
        distance_factor = 0.2
    elif distance > 0.4 and my_projectile_cooldown < 0.3:
        distance_factor = 0.15
    
    current_aggression = max(0.1, min(0.85, base_aggression + momentum_factor + distance_factor))
    
    # Advanced opponent behavior analysis
    opponent_advancing = False
    opponent_retreating = False
    opponent_velocity_threshold = 0.04
    
    if relative_pos > 0 and opponent_x_vel > opponent_velocity_threshold:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_x_vel < -opponent_velocity_threshold:
        opponent_advancing = True
    elif relative_pos > 0 and opponent_x_vel < -opponent_velocity_threshold:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > opponent_velocity_threshold:
        opponent_retreating = True
    
    # Opponent pattern recognition
    opponent_aggressive = opponent_attacking > 0.4 and distance < 0.25
    opponent_defensive = opponent_blocking > 0.5 or (opponent_retreating and health_advantage < 0)
    opponent_projectile_focused = opponent_projectile_cooldown < 0.2 and distance > 0.3
    
    # Critical health emergency protocols
    if my_health < 0.12 or health_advantage < -0.6:
        if distance < retreat_distance:
            if opponent_attacking > 0.6:
                return 6  # Emergency block
            else:
                # Smart retreat with blocking
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        elif my_projectile_cooldown < 0.15 and distance > 0.25:
            return 9  # Desperate projectile
        else:
            # Last resort blocking
            return 6
    
    # Finishing move detection when opponent is very low
    if opponent_health < 0.15 and health_advantage > 0.3:
        if distance < close_range + 0.05:
            # Aggressive finish
            finish_choice = random.random()
            if finish_choice < 0.6:
                return 5  # Strong kick finish
            else:
                return 4  # Fast punch finish
        elif distance < medium_range:
            # Close distance for finish
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
    
    # Close range combat with enhanced tactics (0.0 - 0.13)
    if distance < close_range:
        # Counter-attack timing
        if opponent_attacking > 0.6:
            counter_chance = 0.65 if health_advantage > 0 else 0.8
            if random.random() < counter_chance:
                return 6  # Block first
            else:
                # Risky counter-attack
                return 4  # Fast punch through
        
        # Advanced anti-blocking strategies
        if opponent_blocking > 0.7:
            block_break_strategy = random.random()
            if block_break_strategy < 0.35:
                return 5  # Heavy kick to break guard
            elif block_break_strategy < 0.55:
                return 3  # Jump over guard
            elif block_break_strategy < 0.75:
                # Feint with movement then attack
                if relative_pos > 0:
                    return 1  # Move left to reposition
                else:
                    return 2  # Move right to reposition
            else:
                return 9 if my_projectile_cooldown < 0.3 else 0  # Reset with projectile
        
        # Combo system for sustained pressure
        if health_advantage > 0.1 and opponent_blocking < 0.3:
            combo_choice = random.random()
            if combo_choice < 0.4:
                return 4  # Punch for speed
            elif combo_choice < 0.7:
                return 5  # Kick for power
            elif combo_choice < 0.85:
                return 3  # Jump attack for mix-up
            else:
                return 6  # Block to reset rhythm
        
        # Defensive close combat with counter opportunities
        elif health_advantage < 0:
            defensive_counter = random.random()
            if defensive_counter < 0.25:
                return 4  # Quick counter punch
            elif defensive_counter < 0.4:
                return 5  # Power counter kick
            elif defensive_counter < 0.6:
                return 6  # Safe block
            else:
                # Create space
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        
        # Balanced close combat
        else:
            balanced_close = random.random()
            if balanced_close < 0.3:
                return 4  # Punch
            elif balanced_close < 0.55:
                return 5  # Kick  
            elif balanced_close < 0.7:
                return 6  # Block
            else:
                return 3  # Jump attack
    
    # Medium range with enhanced positioning (0.13 - 0.28)
    elif distance < medium_range:
        # Exploit opponent vulnerabilities
        if opponent_attacking > 0.5 and distance > 0.18:
            # Punish whiffed attacks
            if current_aggression > 0.5:
                if relative_pos > 0:
                    return 2  # Rush in right
                else:
                    return 1