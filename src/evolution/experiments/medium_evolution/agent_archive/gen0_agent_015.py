"""
Evolutionary Agent: gen0_agent_015
==================================

Metadata:
{
  "generation": 0,
  "fitness": 13.956000000000714,
  "fighting_style": "rushdown",
  "win_rate": 0.0
}

Code Hash: 54aa128d8f84d0fa
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
    
    # Extract fighter status information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_airborne = state[8] if len(state) > 8 else 0.0
    my_projectile_cd = state[9] if len(state) > 9 else 0.0
    my_last_action = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent status information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[13] if len(state) > 13 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    opp_stunned = state[18] if len(state) > 18 else 0.0
    opp_airborne = state[19] if len(state) > 19 else 0.0
    opp_projectile_cd = state[20] if len(state) > 20 else 0.0
    opp_last_action = state[21] if len(state) > 21 else 0.0
    
    # Define rushdown tactical parameters
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    critical_health = 0.3
    dominant_health = 0.4
    
    # Rushdown aggression modifiers
    base_aggression = 0.8
    winning_aggression = 0.9
    losing_aggression = 0.6
    desperate_aggression = 0.4
    
    # Emergency defensive situations
    if my_health < critical_health and health_advantage < -0.5:
        if distance < close_range and opp_attacking > 0.5:
            return 6  # Block incoming attack
        elif distance > medium_range and my_projectile_cd < 0.3:
            return 9  # Try to chip damage with projectile
        elif opp_attacking > 0.5 and distance < medium_range:
            # Defensive movement while blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
    
    # Punish opponent vulnerabilities (core rushdown opportunity)
    if opp_stunned > 0.5 or (opp_attacking > 0.5 and distance < close_range):
        attack_choice = random.random()
        if attack_choice < 0.4:
            return 4  # Quick punch
        elif attack_choice < 0.7:
            return 5  # Stronger kick
        else:
            return 4  # Default to punch for speed
    
    # Opponent is blocking - mix up approach
    if opp_blocking > 0.5 and distance < medium_range:
        mix_up = random.random()
        if mix_up < 0.3:
            return 5  # Kick to break guard
        elif mix_up < 0.5:
            # Reposition for better angle
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        elif mix_up < 0.7 and my_projectile_cd < 0.2:
            return 9  # Projectile to pressure
        else:
            return 4  # Quick punch attempt
    
    # Core rushdown range-based tactics
    if distance < close_range:
        # Close combat - rushdown excels here
        if my_stunned > 0.5:
            return 6  # Block if stunned
        
        current_aggression = base_aggression
        if health_advantage > dominant_health:
            current_aggression = winning_aggression
        elif health_advantage < -dominant_health:
            current_aggression = losing_aggression
        
        if random.random() < current_aggression:
            # Aggressive rushdown sequence
            combo_choice = random.random()
            if combo_choice < 0.5:
                return 4  # Fast punch
            elif combo_choice < 0.8:
                return 5  # Power kick
            else:
                return 4  # Another punch for pressure
        else:
            # Brief defensive moment
            if opp_attacking > 0.3:
                return 6  # Block
            else:
                return 4  # Quick counter-attack
    
    elif distance < medium_range:
        # Medium range - close the gap aggressively
        if opp_airborne > 0.5 and abs(height_diff) > 0.1:
            return 3  # Jump to match opponent
        
        # Aggressive approach with some caution
        if opp_attacking > 0.5 and random.random() < 0.3:
            # Defensive approach while closing
            if relative_pos > 0:
                return 8  # Move right with block
            else:
                return 7  # Move left with block
        else:
            # Standard rushdown approach
            gap_closer = random.random()
            if gap_closer < 0.7:
                # Direct movement toward opponent
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif gap_closer < 0.85 and my_projectile_cd < 0.3:
                return 9  # Projectile while approaching
            else:
                # Mix in jump approach
                return 3
    
    elif distance < far_range:
        # Far range - need to get closer for rushdown
        if my_projectile_cd < 0.2 and random.random() < 0.4:
            return 9  # Projectile to cover approach
        
        # Aggressive movement toward opponent
        approach_method = random.random()
        if approach_method < 0.6:
            # Direct movement
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        elif approach_method < 0.8:
            return 3  # Jump approach
        else:
            # Cautious approach if losing
            if health_advantage < -0.2:
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with