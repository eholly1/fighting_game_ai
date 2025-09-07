"""
Evolutionary Agent: gen1_agent_013
==================================

Metadata:
{
  "generation": 1,
  "fitness": -1.6599999999997324,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 3d49b91f38e31663
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
    
    # Extract my fighter information
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_pos_x = state[0] if len(state) > 0 else 0.5
    my_velocity_x = state[2] if len(state) > 2 else 0.0
    my_velocity_y = state[3] if len(state) > 3 else 0.0
    my_is_attacking = state[4] > 0.5 if len(state) > 4 else False
    my_is_blocking = state[5] > 0.5 if len(state) > 5 else False
    my_projectile_cooldown = max(0.0, state[6]) if len(state) > 6 else 0.0
    my_stun_timer = max(0.0, state[7]) if len(state) > 7 else 0.0
    my_combo_count = max(0.0, state[8]) if len(state) > 8 else 0.0
    my_energy = max(0.0, min(1.0, state[9])) if len(state) > 9 else 1.0
    my_is_grounded = state[10] > 0.5 if len(state) > 10 else True
    
    # Extract opponent information
    opp_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opp_pos_x = state[11] if len(state) > 11 else 0.5
    opp_velocity_x = state[13] if len(state) > 13 else 0.0
    opp_velocity_y = state[14] if len(state) > 14 else 0.0
    opp_is_attacking = state[15] > 0.5 if len(state) > 15 else False
    opp_is_blocking = state[16] > 0.5 if len(state) > 16 else False
    opp_projectile_cooldown = max(0.0, state[17]) if len(state) > 17 else 0.0
    opp_stun_timer = max(0.0, state[18]) if len(state) > 18 else 0.0
    opp_combo_count = max(0.0, state[19]) if len(state) > 19 else 0.0
    opp_energy = max(0.0, min(1.0, state[20])) if len(state) > 20 else 1.0
    opp_is_grounded = state[21] > 0.5 if len(state) > 21 else True
    
    # Define hybrid tactical parameters
    ultra_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    critical_health = 0.2
    winning_margin = 0.25
    losing_margin = -0.25
    
    # Hybrid balance parameters
    aggression_base = 0.7
    patience_factor = 0.65
    counter_sensitivity = 0.75
    pressure_intensity = 0.8
    defensive_priority = 0.6
    
    # Calculate dynamic aggression based on game state
    dynamic_aggression = aggression_base
    if health_advantage > winning_margin:
        dynamic_aggression += 0.15  # More aggressive when winning
    elif health_advantage < losing_margin:
        dynamic_aggression -= 0.2   # More cautious when losing
    
    # Adjust aggression based on opponent behavior
    if opp_is_attacking and distance < medium_range:
        dynamic_aggression -= 0.1  # More defensive against aggression
    elif opp_is_blocking and distance < close_range:
        dynamic_aggression += 0.1  # More aggressive against passive play
    
    # Emergency survival mode
    if my_health < critical_health and health_advantage < -0.4:
        if my_stun_timer > 0.2:
            return 6  # Block while stunned
        
        if distance < close_range:
            if opp_is_attacking:
                return 6  # Block incoming attack
            elif opp_stun_timer > 0.3:
                # Counter-attack opportunity
                return 4  # Quick punch
            else:
                # Escape close range
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        
        elif distance < medium_range:
            # Create distance and harass
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile while retreating
            else:
                if relative_pos > 0:
                    return 7  # Retreat left
                else:
                    return 8  # Retreat right
        
        else:
            # Long range survival
            if my_projectile_cooldown < 0.5:
                return 9  # Projectile harassment
            else:
                return 6  # Block and wait
    
    # Punish opponent vulnerabilities
    if opp_stun_timer > 0.4 or (opp_is_attacking and not opp_is_grounded):
        if distance < close_range:
            # Big punishment opportunity
            if my_energy > 0.6 and random.random() < 0.8:
                return 5  # Strong kick for maximum damage
            else:
                return 4  # Safe punch combo
        elif distance < medium_range:
            # Close distance for punishment
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        else:
            # Long range punishment
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile
            else:
                # Get closer for better punishment
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Counter-attack system
    if opp_is_attacking:
        if distance < ultra_close_range:
            # Immediate threat - react based on health and position
            if my_health < opp_health * 0.7:
                return 6  # Block when at disadvantage
            elif random.random() < counter_sensitivity:
                # Counter-attack
                if my_velocity_x * relative_pos < -0.2:  # Moving away
                    return 6  # Block instead of risky counter
                else:
                    return 4  # Quick counter punch
            else:
                return 6  # Default to blocking
        
        elif distance < close_range:
            # Close range threat assessment
            if opp_velocity_x * relative_pos > 0.3:  # Opponent advancing
                # Prepare for incoming attack
                if random.random() < defensive_priority:
                    return 6  # Block
                else:
                    # Pre-emptive counter
                    return 4  # Punch to interrupt
            else:
                # Opponent attacking but not advancing
                if my_projectile_cooldown < 0.3:
                    return 9  # Projectile while they whiff
                else:
                    # Position for counter
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1