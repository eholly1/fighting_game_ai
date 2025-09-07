"""
Evolutionary Agent: gen2_agent_019
==================================

Metadata:
{
  "generation": 2,
  "fitness": -36.15999999999997,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 94f042d368ea6885
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
    
    # Extract comprehensive fighter status
    my_health = max(0.0, min(1.0, state[2] if len(state) > 2 else 1.0))
    my_x_pos = state[0] if len(state) > 0 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = max(0.0, state[7] if len(state) > 7 else 0.0)
    my_block_status = max(0.0, state[8] if len(state) > 8 else 0.0)
    my_projectile_cooldown = max(0.0, state[9] if len(state) > 9 else 0.0)
    my_attack_cooldown = max(0.0, state[10] if len(state) > 10 else 0.0)
    
    # Extract opponent information
    opp_health = max(0.0, min(1.0, state[13] if len(state) > 13 else 1.0))
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attack_status = max(0.0, state[18] if len(state) > 18 else 0.0)
    opp_block_status = max(0.0, state[19] if len(state) > 19 else 0.0)
    opp_projectile_cooldown = max(0.0, state[20] if len(state) > 20 else 0.0)
    opp_attack_cooldown = max(0.0, state[21] if len(state) > 21 else 0.0)
    
    # Hybrid fighter tactical parameters
    strike_range = 0.12
    close_range = 0.18
    medium_range = 0.32
    far_range = 0.48
    critical_health = 0.20
    winning_threshold = 0.25
    losing_threshold = -0.30
    desperation_threshold = -0.45
    
    # Calculate dynamic aggression and adaptability
    base_aggression = 0.68
    momentum = abs(my_velocity_x) + abs(opp_velocity_x)
    unpredictability = random.random()
    
    # Adaptive aggression calculation
    aggression_factor = base_aggression
    if health_advantage > winning_threshold:
        aggression_factor = 0.75  # More aggressive when winning
    elif health_advantage < losing_threshold:
        aggression_factor = 0.85  # Calculated aggression when losing
    elif health_advantage < desperation_threshold:
        aggression_factor = 0.95  # All-out when desperate
    
    # Distance-based aggression modulation
    if distance < close_range:
        aggression_factor *= 1.15
    elif distance > far_range:
        aggression_factor *= 0.85
    
    current_aggression = min(1.0, aggression_factor)
    
    # Emergency protocols - highest priority
    if my_health < critical_health:
        if distance < strike_range and opp_attack_status > 0.4:
            # Emergency defense at close range
            if my_block_status < 0.2:
                return 6  # Block incoming attack
            else:
                # Already blocking, try to escape
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
        elif distance < close_range:
            # Close range emergency tactics
            if opp_block_status < 0.3 and my_attack_cooldown < 0.2:
                # Quick strike opportunity
                return 4 if unpredictability < 0.6 else 5
            else:
                # Defensive repositioning
                if relative_pos > 0:
                    return 7  # Protected retreat left
                else:
                    return 8  # Protected retreat right
        elif distance > medium_range and my_projectile_cooldown < 0.15:
            return 9  # Projectile when safe
        else:
            # General emergency positioning
            if unpredictability < 0.4:
                return 6  # Block
            elif unpredictability < 0.7:
                return 3  # Jump for mobility
            else:
                return 0  # Wait for opportunity
    
    # Finishing opportunities when opponent is vulnerable
    if health_advantage > winning_threshold and opp_health < 0.30:
        if distance < strike_range:
            if opp_block_status < 0.25:
                # Clean finishing opportunity
                finish_roll = unpredictability
                if finish_roll < 0.45:
                    return 5  # Power kick finish
                elif finish_roll < 0.75:
                    return 4  # Quick punch combo
                else:
                    # Feint for positioning
                    return 3  # Jump attack
            else:
                # Opponent blocking, reposition for guard break
                if relative_pos > 0:
                    return 2  # Circle right
                else:
                    return 1  # Circle left
        elif distance < medium_range:
            # Approach for finish
            if opp_projectile_cooldown > 0.5:
                if relative_pos > 0:
                    return 2  # Move in aggressively
                else:
                    return 1  # Move in aggressively
            elif my_projectile_cooldown < 0.1:
                return 9  # Projectile pressure
    
    # Core hybrid strategy implementation
    if distance < strike_range:
        # Strike range - hit or reposition decision
        if my_attack_status > 0.4:
            # Currently in attack animation - prepare followup or retreat
            followup_decision = unpredictability * current_aggression
            if followup_decision < 0.3:
                # Immediate retreat after attack
                if relative_pos > 0:
                    return 1  # Move away left
                else:
                    return 2  # Move away right
            elif followup_decision < 0.6:
                # Protected retreat
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Hold position for combo potential
                return 0  # Brief pause
        
        # Evaluate opponent state for strike decision
        if opp_block_status > 0.5:
            # Opponent heavily blocking
            guard_break_strategy = unpredictability
            if guard_break_strategy < 0.3:
                # Quick repositioning
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            elif guard_break_strategy < 0.6:
                # Jump over guard
                return 3  # Jump attack
            elif guard_break_strategy < 0.8:
                # Heavy attack to break guard
                return 5  # Kick
            else:
                # Retreat and reset
                if relative_pos > 0:
                    return 7