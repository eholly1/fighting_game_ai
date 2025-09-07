"""
Evolutionary Agent: gen0_agent_009
==================================

Metadata:
{
  "generation": 0,
  "fitness": 253.19999999999231,
  "fighting_style": "patient_defender",
  "win_rate": 0.5
}

Code Hash: f3affd3307bb7832
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
    
    # Extract player status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_attack_status = state[5]
    opponent_attack_status = state[16]
    my_block_status = state[6]
    my_projectile_cooldown = max(0.0, state[7])
    opponent_projectile_cooldown = max(0.0, state[18])
    height_difference = state[24]
    
    # Define strategic thresholds for patient defender
    close_range = 0.12
    medium_range = 0.35
    critical_health = 0.25
    block_priority_threshold = -0.2
    patience_factor = 0.8
    
    # Emergency survival mode when critically low health
    if my_health < critical_health:
        if distance < close_range and opponent_attack_status > 0:
            # Immediate blocking when opponent is attacking close
            if relative_pos > 0:
                return 8  # Block while moving right
            else:
                return 7  # Block while moving left
        elif distance < medium_range:
            # Create distance while blocking
            if relative_pos > 0:
                return 8  # Block retreat right
            else:
                return 7  # Block retreat left
        else:
            # Long range defensive projectile
            if my_projectile_cooldown == 0:
                return 9
            else:
                return 6  # Pure block
    
    # Patient defender core logic - prioritize blocking when disadvantaged
    if health_advantage < block_priority_threshold:
        # Defensive posture when losing
        if distance < close_range:
            # Very close - high block priority
            if opponent_attack_status > 0:
                return 6  # Pure block against attacks
            elif random.random() < patience_factor:
                return 6  # Patient blocking
            else:
                # Rare counter-attack opportunity
                if random.random() < 0.3:
                    return 4  # Quick punch
                else:
                    return 6  # Back to blocking
        
        elif distance < medium_range:
            # Medium range defensive positioning
            if opponent_attack_status > 0:
                # Opponent attacking, block while positioning
                if relative_pos > 0:
                    return 8  # Block right
                else:
                    return 7  # Block left
            else:
                # Cautious positioning
                if random.random() < 0.6:
                    return 6  # Block while waiting
                elif distance > 0.25:
                    # Move closer carefully
                    if relative_pos > 0:
                        return 2  # Move right
                    else:
                        return 1  # Move left
                else:
                    return 6  # Block
        
        else:
            # Long range defensive tactics
            if my_projectile_cooldown == 0 and random.random() < 0.4:
                return 9  # Defensive projectile
            elif opponent_projectile_cooldown == 0:
                # Opponent can shoot, prepare to block
                return 6
            else:
                # Safe to move closer slowly
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Balanced to winning position - still patient but more opportunity seeking
    elif health_advantage < 0.3:
        if distance < close_range:
            # Close range with slight advantage
            if opponent_attack_status > 0:
                # Block first, counter second
                if random.random() < 0.7:
                    return 6
                else:
                    return 4  # Counter punch
            else:
                # Look for openings patiently
                if random.random() < 0.5:
                    return 6  # Still prioritize defense
                elif random.random() < 0.6:
                    return 4  # Quick punch
                else:
                    return 5  # Stronger kick
        
        elif distance < medium_range:
            # Medium range tactical positioning
            if opponent_attack_status > 0:
                if relative_pos > 0:
                    return 8  # Block right
                else:
                    return 7  # Block left
            else:
                # Methodical approach
                if random.random() < 0.4:
                    return 6  # Patient blocking
                elif distance > 0.25:
                    # Close distance
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                else:
                    # In striking range
                    if random.random() < 0.3:
                        return 4
                    else:
                        return 6  # Back to defense
        
        else:
            # Long range with slight advantage
            if my_projectile_cooldown == 0 and random.random() < 0.5:
                return 9
            elif opponent_projectile_cooldown == 0:
                return 6  # Defensive blocking
            else:
                # Advance position
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Winning decisively - patient aggression
    else:
        if distance < close_range:
            # Close range dominance but still careful
            if opponent_attack_status > 0:
                # Even when winning, respect opponent attacks
                if random.random() < 0.6:
                    return 6  # Block first
                else:
                    return 4  # Counter
            else:
                # Controlled aggression
                if random.random() < 0.3:
                    return 6  # Maintain defensive discipline
                elif random.random() < 0.5:
                    return 4  # Punch
                else:
                    return 5  # Kick
        
        elif distance < medium_range:
            # Medium range pressure
            if opponent_attack_status > 0:
                # Still block attacks even when winning
                if relative_pos > 0:
                    return 8
                else:
                    return 7
            else:
                # Press advantage methodically
                if random.random() < 0.2:
                    return 6  # Occasional defensive pause
                elif distance > 0.2:
                    # Move to attack range
                    if relative_pos > 0:
                        return 2
                    else:
                        return 1
                else:
                    # Attack opportunity
                    if random.random() < 0.6:
                        return 4
                    else:
                        return 5
        
        else:
            # Long range when winning
            if my_projectile_cooldown == 0 and random.random() < 0.7:
                return 9  # Projectile pressure
            elif opponent_projectile_cooldown == 0:
                return 6  # Block projectiles
            else:
                # Advance for finish
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Height-based adjustments for patient defender
    if abs(height_difference) > 0.3:
        if height_difference > 0:
            # Opponent below - patient high guard
            if distance < close_range:
                return 6  # Block low attacks
            else:
                return 9 if my_projectile_cooldown == 0 else 6
        else:
            # Opponent above - careful anti-air
            if distance < close_range and opponent_attack_status > 0:
                return 6
            elif distance < medium_range:
                return 6