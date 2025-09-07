"""
Evolutionary Agent: gen0_agent_001
==================================

Metadata:
{
  "generation": 0,
  "fitness": 26.340000000000853,
  "fighting_style": "defensive",
  "win_rate": 0.5
}

Code Hash: 4b19fe08ab9a416b
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
    my_block_status = state[5] if len(state) > 5 else 0.0
    my_attack_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opponent_health = state[12] if len(state) > 12 else 1.0
    opponent_attack_status = state[17] if len(state) > 17 else 0.0
    opponent_velocity_x = state[14] if len(state) > 14 else 0.0
    
    # Define strategic thresholds for defensive play
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    critical_health = 0.3
    safe_health = 0.7
    
    # Emergency defensive reactions - highest priority
    if health_advantage < -0.6 and my_health < critical_health:
        # Desperate situation - prioritize survival
        if distance < close_range and opponent_attack_status > 0.5:
            return 6  # Block incoming attack
        elif distance < medium_range:
            # Create distance while blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            # Far range - use projectiles if available
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile to maintain distance
            else:
                return 6  # Block and wait
    
    # Defensive counter-attack opportunities
    if opponent_attack_status > 0.7 and distance < close_range:
        # Opponent is attacking - block then counter
        if my_block_status < 0.3:
            return 6  # Block first
        else:
            # Counter attack after successful block
            counter_choice = random.random()
            if counter_choice < 0.6:
                return 4  # Quick punch counter
            else:
                return 5  # Powerful kick counter
    
    # Range-based defensive positioning
    if distance < close_range:
        # Close range - high risk area for defensive style
        if health_advantage > 0.2:
            # Slight advantage - can afford some aggression
            if opponent_attack_status < 0.2:
                # Safe to attack
                attack_roll = random.random()
                if attack_roll < 0.4:
                    return 4  # Quick punch
                elif attack_roll < 0.7:
                    return 5  # Strong kick
                else:
                    return 6  # Stay defensive
            else:
                return 6  # Block opponent's attack
        else:
            # Losing or even - stay defensive
            if abs(opponent_velocity_x) > 0.3:
                # Opponent moving fast - prepare to block
                return 6
            else:
                # Look for safe counter opportunity
                if random.random() < 0.3:
                    return 4  # Cautious punch
                else:
                    return 6  # Default block
    
    elif distance < medium_range:
        # Medium range - positioning phase
        if health_advantage < -0.2:
            # Losing - maintain safe distance
            if relative_pos > 0:
                return 7  # Move left with guard up
            else:
                return 8  # Move right with guard up
        else:
            # Even or winning - controlled approach
            if opponent_attack_status > 0.5:
                # Opponent preparing attack - stay back and block
                return 6
            else:
                # Safe to position for attack
                approach_style = random.random()
                if approach_style < 0.4:
                    # Direct approach
                    if relative_pos > 0:
                        return 1  # Move left toward opponent
                    else:
                        return 2  # Move right toward opponent
                elif approach_style < 0.7:
                    # Guarded approach
                    if relative_pos > 0:
                        return 7  # Move left while blocking
                    else:
                        return 8  # Move right while blocking
                else:
                    # Jump approach for unpredictability
                    return 3
    
    elif distance < far_range:
        # Far range - projectile and positioning game
        if my_projectile_cooldown < 0.1:
            # Projectile available
            if health_advantage > 0.1:
                # Ahead - maintain pressure with projectiles
                return 9
            else:
                # Behind or even - use projectile defensively
                projectile_decision = random.random()
                if projectile_decision < 0.6:
                    return 9  # Use projectile
                else:
                    return 6  # Stay defensive
        else:
            # No projectile - positioning
            if health_advantage < -0.1:
                # Losing - maintain distance
                if relative_pos > 0:
                    return 7  # Move away with guard
                else:
                    return 8  # Move away with guard
            else:
                # Even or ahead - controlled advance
                positioning_choice = random.random()
                if positioning_choice < 0.5:
                    # Advance carefully
                    if relative_pos > 0:
                        return 7  # Guarded advance left
                    else:
                        return 8  # Guarded advance right
                else:
                    # Wait and block
                    return 6
    
    else:
        # Maximum range - long distance tactics
        if my_projectile_cooldown < 0.1:
            # Always use projectile at max range when available
            return 9
        else:
            # No projectile available
            if health_advantage > 0.3:
                # Winning significantly - can afford to advance
                advance_method = random.random()
                if advance_method < 0.4:
                    # Direct advance
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                elif advance_method < 0.7:
                    # Guarded advance
                    if relative_pos > 0:
                        return 7  # Move left while blocking
                    else:
                        return 8  # Move right while blocking
                else:
                    # Jump advance
                    return 3
            else:
                # Even or losing - stay back and wait
                defensive_wait = random.random()
                if defensive_wait < 0.8:
                    return 6  # Block and wait
                else:
                    # Slight repositioning
                    if relative_pos > 0:
                        return 7  # Move left with guard
                    else:
                        return 8  # Move right with guard
    
    # Height-based adjustments for defensive play
    if abs(height_diff) > 0.3:
        if height_diff > 0:
            # Opponent is higher - defensive ground game
            if distance < close_range:
                return 6  # Block high attacks
            else:
                return 5  # Kick to control low space
        else:
            # Opponent is lower - use reach advantage
            if distance < medium_range and my_projectile_cooldown < 0.1:
                return 9  # Projectile from height
            else:
                return 6  # Maintain defensive posture