"""
Evolutionary Agent: gen4_agent_007
==================================

Metadata:
{
  "generation": 4,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: d60df4cf3e25f0a6
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
    
    # Extract my fighter status
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 0.5
    my_pos_x = max(-1.0, min(1.0, state[2])) if len(state) > 2 else 0.0
    my_velocity_x = max(-2.0, min(2.0, state[4])) if len(state) > 4 else 0.0
    my_block_status = max(0.0, state[5]) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, state[6]) if len(state) > 6 else 0.0
    my_attack_cooldown = max(0.0, state[7]) if len(state) > 7 else 0.0
    my_projectile_cooldown = max(0.0, state[10]) if len(state) > 10 else 0.0
    
    # Extract opponent status
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 0.5
    opponent_pos_x = max(-1.0, min(1.0, state[13])) if len(state) > 13 else 0.0
    opponent_velocity_x = max(-2.0, min(2.0, state[15])) if len(state) > 15 else 0.0
    opponent_block_status = max(0.0, state[16]) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, state[17]) if len(state) > 17 else 0.0
    opponent_attack_cooldown = max(0.0, state[18]) if len(state) > 18 else 0.0
    
    # Define tactical ranges and thresholds
    close_range = 0.13
    medium_range = 0.32
    far_range = 0.55
    
    critical_health = 0.2
    low_health = 0.35
    good_health = 0.65
    
    # Analyze tactical situation
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = medium_range <= distance < far_range
    is_very_far = distance >= far_range
    
    am_critical = my_health <= critical_health
    am_low = my_health <= low_health
    am_healthy = my_health >= good_health
    
    am_winning = health_advantage > 0.25
    am_losing = health_advantage < -0.25
    am_dominating = health_advantage > 0.5
    am_desperate = health_advantage < -0.5
    
    # Combat readiness states
    can_attack = my_attack_cooldown < 0.08
    can_projectile = my_projectile_cooldown < 0.08
    am_attacking = my_attack_status > 0.1
    am_blocking = my_block_status > 0.1
    
    opponent_attacking = opponent_attack_status > 0.1
    opponent_blocking = opponent_block_status > 0.1
    opponent_can_attack = opponent_attack_cooldown < 0.1
    opponent_vulnerable = opponent_attack_cooldown > 0.3
    
    # Movement analysis
    opponent_approaching = (relative_pos > 0 and opponent_velocity_x > 0.15) or (relative_pos < 0 and opponent_velocity_x < -0.15)
    opponent_retreating = (relative_pos > 0 and opponent_velocity_x < -0.15) or (relative_pos < 0 and opponent_velocity_x > 0.15)
    opponent_fast_approach = abs(opponent_velocity_x) > 0.4 and opponent_approaching
    
    # Positional awareness
    am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    center_control = abs(my_pos_x) < 0.3
    
    # Critical survival mode - highest priority
    if am_desperate and am_critical:
        if opponent_attacking and is_close:
            # Emergency block
            return 6
        elif opponent_fast_approach:
            # Escape with blocking movement
            if am_cornered:
                if my_pos_x > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
            else:
                # Create maximum distance
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
        elif is_very_far and can_projectile:
            # Desperate projectile spam
            return 9
        else:
            # Default defensive stance
            return 6
    
    # Adaptive strategy based on health advantage
    if am_losing or am_low:
        # Defensive hybrid approach
        if is_close:
            if opponent_attacking:
                # Block incoming attacks
                return 6
            elif opponent_blocking:
                # Try to break guard with mixed attacks
                if can_attack:
                    break_guard_roll = random.random()
                    if break_guard_roll < 0.3:
                        return 5  # Heavy kick
                    elif break_guard_roll < 0.5:
                        return 4  # Quick punch
                    else:
                        # Create space for projectile
                        if relative_pos > 0:
                            return 7  # Move left block
                        else:
                            return 8  # Move right block
                else:
                    return 6  # Block while waiting
            elif can_attack and opponent_vulnerable:
                # Counter-attack opportunity
                if my_health > critical_health:
                    return 4  # Safe quick attack
                else:
                    return 6  # Too risky when critical
            else:
                # Maintain distance
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
        
        elif is_medium:
            if opponent_attacking or opponent_fast_approach:
                # Defensive positioning
                if relative_pos > 0:
                    return 7  # Move left block
                else:
                    return 8  # Move right block
            elif opponent_blocking:
                # Reposition for better angle
                if center_control:
                    flank_choice = random.random()
                    if flank_choice < 0.5:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    # Move toward center
                    if my_pos_x > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            elif can_projectile and not opponent_approaching:
                # Safe projectile
                return 9
            else:
                # Cautious positioning
                positioning_roll = random.random()
                if positioning_roll < 0.4:
                    return 6  # Block
                elif positioning_roll < 0.7:
                    if relative_pos > 0:
                        return 7  # Move left block
                    else:
                        return 8  # Move right block
                else:
                    return 3  # Jump for unpre