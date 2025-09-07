"""
Evolutionary Agent: gen0_agent_007
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "hit_and_run",
  "win_rate": 0.5
}

Code Hash: 1e2cefc59b5235c8
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate key game state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity = state[3]
    opponent_velocity = state[14]
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    my_projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    height_difference = state[24]
    
    # Define tactical ranges and thresholds
    very_close_range = 0.08
    close_range = 0.15
    medium_range = 0.3
    far_range = 0.5
    
    # Hit and run style parameters
    retreat_health_threshold = 0.4
    aggressive_health_threshold = 0.7
    quick_strike_distance = 0.12
    retreat_distance = 0.25
    
    # Determine current tactical situation
    is_very_close = distance < very_close_range
    is_close = distance < close_range
    is_medium = close_range <= distance < medium_range
    is_far = distance >= medium_range
    
    # Health-based urgency assessment
    critical_health = my_health < 0.25
    low_health = my_health < 0.5
    opponent_low_health = opponent_health < 0.5
    opponent_critical = opponent_health < 0.25
    
    # Movement direction helpers
    opponent_to_left = relative_pos < 0
    opponent_to_right = relative_pos > 0
    
    # Opponent behavior analysis
    opponent_attacking = opponent_attack_status > 0
    opponent_blocking = opponent_block_status > 0
    opponent_can_projectile = opponent_projectile_cooldown <= 0
    can_use_projectile = my_projectile_cooldown <= 0
    
    # Emergency defensive situations
    if critical_health and opponent_attacking and is_very_close:
        # Desperate escape when critically low and under attack
        if opponent_to_left:
            return 8  # Move right while blocking
        else:
            return 7  # Move left while blocking
    
    if critical_health and distance < 0.2:
        # Critical health - prioritize survival and distance
        if can_use_projectile and distance > 0.15:
            return 9  # Projectile while retreating
        elif opponent_to_left:
            return 2  # Move away from opponent
        else:
            return 1  # Move away from opponent
    
    # Hit and run core logic - quick strikes when opportunity presents
    if not opponent_blocking and is_very_close and not opponent_attacking:
        # Perfect strike opportunity - opponent vulnerable and very close
        strike_choice = random.random()
        if strike_choice < 0.4:
            return 4  # Quick punch
        elif strike_choice < 0.7:
            return 5  # Kick for more damage
        else:
            # Mix in immediate retreat after implied strike
            if opponent_to_left:
                return 2  # Move right away
            else:
                return 1  # Move left away
    
    # Opportunistic finishing moves when opponent is critical
    if opponent_critical and distance < quick_strike_distance:
        if not opponent_blocking:
            return 5  # Strong kick to finish
        else:
            # Try to break guard or reposition
            if random.random() < 0.5:
                return 4  # Quick punch to test defense
            else:
                return 3  # Jump over defense
    
    # Hit and run tactical positioning based on range
    if is_very_close:
        # Too close for comfort - execute hit and run
        if opponent_attacking:
            # Block and retreat
            if opponent_to_left:
                return 8  # Block and move right
            else:
                return 7  # Block and move left
        elif opponent_blocking:
            # Opponent defensive - create distance for next approach
            if opponent_to_left:
                return 2  # Move right to create space
            else:
                return 1  # Move left to create space
        else:
            # Quick strike opportunity
            if random.random() < 0.6:
                return 4  # Fast punch
            else:
                return 5  # Stronger kick
    
    elif is_close:
        # Optimal hit and run range - choose between strike and positioning
        if health_advantage > 0.3:
            # Winning - be more aggressive
            if not opponent_blocking and not opponent_attacking:
                # Clean strike opportunity
                return 4 if random.random() < 0.7 else 5
            elif opponent_blocking:
                # Try to outmaneuver
                if abs(height_difference) > 0.1:
                    return 3  # Jump attack
                else:
                    # Circle around
                    if opponent_to_left:
                        return 2  # Move right
                    else:
                        return 1  # Move left
            else:
                # Opponent attacking - defensive maneuver
                return 6  # Block
        
        elif health_advantage < -0.2:
            # Losing - more cautious hit and run
            if opponent_attacking:
                # Retreat while blocking
                if opponent_to_left:
                    return 8  # Block and retreat right
                else:
                    return 7  # Block and retreat left
            elif can_use_projectile:
                return 9  # Ranged attack while maintaining distance
            else:
                # Quick strike and prepare to retreat
                if not opponent_blocking:
                    return 4  # Quick punch
                else:
                    # Create distance
                    if opponent_to_left:
                        return 2  # Move right
                    else:
                        return 1  # Move left
        
        else:
            # Even match - balanced hit and run approach
            tactical_choice = random.random()
            if tactical_choice < 0.3:
                # Strike option
                if not opponent_blocking:
                    return 4 if random.random() < 0.8 else 5
                else:
                    return 6  # Block if opponent is defensive
            elif tactical_choice < 0.6:
                # Movement option
                if opponent_to_left:
                    return 1  # Move toward opponent
                else:
                    return 2  # Move toward opponent
            else:
                # Defensive option
                if opponent_attacking:
                    return 6  # Block
                elif can_use_projectile:
                    return 9  # Projectile
                else:
                    return 0  # Wait for better opportunity
    
    elif is_medium:
        # Medium range - setup for hit and run approach
        if opponent_low_health and not low_health:
            # Press advantage - close distance for finishing combination
            if opponent_to_left:
                return 1  # Move left toward opponent
            else:
                return 2  # Move right toward opponent
        
        elif low_health and not opponent_low_health:
            # Losing - use range advantage
            if can_use_projectile:
                return 9  # Projectile attack
            else:
                # Maintain distance while looking for opening
                if opponent_velocity > 0.1:  # Opponent approaching
                    if opponent_to_left:
                        return 2  # Move away right
                    else:
                        return 1  # Move away left
                else:
                    # Opponent stationary - careful approach
                    return 3  # Jump approach for