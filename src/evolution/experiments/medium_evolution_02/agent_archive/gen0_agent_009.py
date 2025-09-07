"""
Evolutionary Agent: gen0_agent_009
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "patient_defender",
  "win_rate": 0.5
}

Code Hash: a4a813c5348df702
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
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_attack_status = state[5]
    opponent_attack_status = state[16]
    my_block_status = state[6]
    projectile_cooldown = state[10]
    opponent_projectile_cooldown = state[21]
    height_difference = state[24]
    
    # Define strategic thresholds for patient defender
    close_range = 0.12
    medium_range = 0.35
    danger_distance = 0.08
    critical_health = 0.25
    low_health = 0.4
    winning_threshold = 0.3
    losing_threshold = -0.3
    
    # Emergency defensive situations
    if my_health < critical_health and opponent_attack_status > 0:
        # Critical health and opponent attacking - prioritize survival
        if distance < danger_distance:
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        return 6  # Pure block
    
    # Opponent is attacking - patient defender response
    if opponent_attack_status > 0:
        if distance < close_range:
            # Very close and opponent attacking - block and reposition
            block_probability = 0.85 if health_advantage < 0 else 0.75
            if random.random() < block_probability:
                if distance < danger_distance:
                    if relative_pos > 0:
                        return 7  # Block and move away
                    else:
                        return 8  # Block and move away
                return 6  # Static block
            else:
                # Counter-attack opportunity
                return 4  # Quick punch counter
        else:
            # Medium range with opponent attacking - maintain distance
            if distance < medium_range:
                if relative_pos > 0:
                    return 1  # Move left away from opponent
                else:
                    return 2  # Move right away from opponent
            return 6  # Block at safer distance
    
    # Health-based strategic adjustments
    if health_advantage < losing_threshold:
        # Losing significantly - ultra defensive
        if distance > medium_range and projectile_cooldown <= 0:
            return 9  # Keep distance with projectiles
        elif distance < close_range:
            # Too close when losing - block and retreat
            retreat_probability = 0.8
            if random.random() < retreat_probability:
                if relative_pos > 0:
                    return 7  # Block left
                else:
                    return 8  # Block right
            return 6  # Just block
        else:
            # Medium range when losing - careful positioning
            if relative_pos > 0:
                return 1  # Move left cautiously
            else:
                return 2  # Move right cautiously
    
    # Opponent low on health - patient pressure
    if opponent_health < low_health:
        if distance < close_range:
            # Close range with weak opponent - measured aggression
            attack_probability = 0.6 if health_advantage > 0 else 0.4
            if random.random() < attack_probability:
                # Choose attack based on distance
                if distance < danger_distance:
                    return 4  # Quick punch
                else:
                    punch_vs_kick = random.random()
                    if punch_vs_kick < 0.65:
                        return 4  # Punch more often
                    else:
                        return 5  # Occasional kick
            else:
                return 6  # Still block frequently
        elif distance < medium_range:
            # Medium range vs weak opponent - controlled approach
            approach_probability = 0.7
            if random.random() < approach_probability:
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                return 6  # Block while considering approach
        else:
            # Long range vs weak opponent - projectile pressure
            if projectile_cooldown <= 0:
                return 9  # Projectile
            else:
                if relative_pos > 0:
                    return 2  # Close distance
                else:
                    return 1  # Close distance
    
    # Range-based patient defender tactics
    if distance < close_range:
        # Close range - patient defender's comfort zone
        if health_advantage > winning_threshold:
            # Winning and close - controlled aggression
            attack_probability = 0.55
            if random.random() < attack_probability:
                attack_choice = random.random()
                if attack_choice < 0.7:
                    return 4  # Favor punches for speed
                else:
                    return 5  # Occasional kicks for power
            else:
                return 6  # Still block often even when winning
        elif health_advantage > 0:
            # Slight advantage - balanced approach
            action_choice = random.random()
            if action_choice < 0.4:
                return 6  # Block
            elif action_choice < 0.75:
                return 4  # Punch
            else:
                return 5  # Kick
        else:
            # Disadvantage or even - defensive priority
            defensive_choice = random.random()
            if defensive_choice < 0.65:
                return 6  # Block
            elif defensive_choice < 0.85:
                return 4  # Quick counter
            else:
                return 5  # Surprise kick
    
    elif distance < medium_range:
        # Medium range - positioning phase
        if opponent_projectile_cooldown <= 2 and opponent_projectile_cooldown >= 0:
            # Opponent can projectile soon - prepare defense
            defensive_move = random.random()
            if defensive_move < 0.4:
                return 6  # Pre-emptive block
            elif defensive_move < 0.7:
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                # Counter-projectile if available
                if projectile_cooldown <= 0:
                    return 9
                else:
                    return 6  # Block
        
        # Normal medium range positioning
        if health_advantage > 0:
            # Advantage - patient pressure
            positioning_choice = random.random()
            if positioning_choice < 0.4:
                # Close distance carefully
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif positioning_choice < 0.7:
                return 6  # Block while thinking
            else:
                # Projectile if available
                if projectile_cooldown <= 0:
                    return 9
                else:
                    return 6  # Block
        else:
            # Disadvantage - very patient
            patient_choice = random.random()
            if patient_choice < 0.5:
                return 6  # Block frequently
            elif patient_choice < 0.8:
                # Maintain distance
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
            else:
                if projectile_cooldown <= 0:
                    return 9  # Projectile
                else:
                    return 6  # Block
    
    else:
        # Long range - projectile game
        if projectile_cooldown <= 0:
            # Can use projectile
            projectile_