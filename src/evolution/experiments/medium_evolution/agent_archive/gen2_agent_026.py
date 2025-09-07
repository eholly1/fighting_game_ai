"""
Evolutionary Agent: gen2_agent_026
==================================

Metadata:
{
  "generation": 2,
  "fitness": 125.01066666666055,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: ec8695ca908097e7
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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity = state[3]
    opponent_velocity = state[14]
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    projectile_cooldown = max(0.0, state[9])
    opponent_projectile_cooldown = max(0.0, state[20])
    height_difference = state[24]
    
    # Enhanced tactical parameters for evolved hybrid style
    strike_range = 0.12
    danger_zone = 0.18
    medium_range = 0.30
    control_range = 0.45
    safe_range = 0.60
    critical_health = 0.20
    danger_health = 0.35
    winning_margin = 0.30
    dominance_margin = 0.50
    
    # Dynamic aggression calculation
    base_aggression = 0.55
    health_modifier = health_advantage * 0.25
    distance_modifier = (0.4 - distance) * 0.15 if distance < 0.4 else 0
    momentum = abs(my_velocity) - abs(opponent_velocity)
    momentum_modifier = momentum * 0.10
    
    current_aggression = max(0.1, min(0.9, base_aggression + health_modifier + distance_modifier + momentum_modifier))
    
    # Unpredictability factor
    chaos_factor = random.random()
    tactical_roll = random.random()
    
    # Emergency survival mode - refined
    if my_health < critical_health or health_advantage < -0.45:
        if distance < danger_zone:
            if opponent_attack_status > 0.4:
                # Opponent attacking - maximum defense
                if chaos_factor < 0.3:
                    return 6  # Full block
                elif chaos_factor < 0.65:
                    if relative_pos > 0:
                        return 7  # Protected retreat left
                    else:
                        return 8  # Protected retreat right
                else:
                    return 3  # Desperate jump escape
            else:
                # Quick escape from danger
                if relative_pos > 0:
                    return 1 if chaos_factor < 0.7 else 7
                else:
                    return 2 if chaos_factor < 0.7 else 8
        elif distance < control_range:
            if projectile_cooldown < 0.2 and opponent_projectile_cooldown > 0.3:
                return 9  # Safe projectile harassment
            else:
                # Defensive positioning
                if chaos_factor < 0.5:
                    return 6  # Block and wait
                else:
                    # Evasive movement
                    if relative_pos > 0:
                        return 1  # Move away
                    else:
                        return 2  # Move away
        else:
            # Long range survival
            if projectile_cooldown < 0.15:
                return 9  # Keep opponent at bay
            else:
                return 6  # Defensive stance
    
    # Dominance finishing mode - enhanced
    if health_advantage > dominance_margin and opponent_health < 0.30:
        if distance < strike_range:
            if opponent_block_status > 0.3:
                # Break guard tactics
                if tactical_roll < 0.4:
                    return 5  # Kick to break guard
                elif tactical_roll < 0.7:
                    # Create space then pressure
                    if relative_pos > 0:
                        return 1  # Step back
                    else:
                        return 2  # Step back
                else:
                    return 3  # Jump mix-up
            else:
                # Finishing sequence
                if my_attack_status > 0.3:
                    return 0  # Let attack complete
                else:
                    finish_choice = tactical_roll
                    if finish_choice < 0.45:
                        return 4  # Quick finisher
                    elif finish_choice < 0.75:
                        return 5  # Power finisher
                    else:
                        return 6  # Stay ready for counter
        elif distance < medium_range:
            # Aggressive closing
            if opponent_attack_status > 0.4:
                # Counter while closing
                if current_aggression > 0.7:
                    if relative_pos > 0:
                        return 8  # Move in with guard
                    else:
                        return 7  # Move in with guard
                else:
                    return 6  # Block then counter
            else:
                # Direct pressure
                if relative_pos > 0:
                    return 2  # Close distance
                else:
                    return 1  # Close distance
        else:
            # Long range pressure
            if projectile_cooldown < 0.25:
                return 9  # Projectile pressure
            else:
                # Advance while cooling down
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Close range hybrid combat - evolved
    if distance < strike_range:
        # Analyze opponent's defensive state
        if opponent_block_status > 0.4:
            # Opponent blocking heavily
            block_counter_choice = tactical_roll
            if block_counter_choice < 0.25:
                return 5  # Kick to break guard
            elif block_counter_choice < 0.5:
                # Reset positioning
                if relative_pos > 0:
                    return 1  # Step back left
                else:
                    return 2  # Step back right
            elif block_counter_choice < 0.75:
                return 3  # Jump over guard
            else:
                return 6  # Wait for opening
        
        # Opponent not blocking - strike opportunities
        if opponent_attack_status > 0.5:
            # Opponent attacking - timing critical
            if current_aggression > 0.65 and health_advantage > -0.2:
                # Aggressive counter-trade
                counter_choice = chaos_factor
                if counter_choice < 0.6:
                    return 4  # Quick counter
                else:
                    return 5  # Power counter
            else:
                # Defensive counter
                defense_choice = tactical_roll
                if defense_choice < 0.4:
                    return 6  # Block
                elif defense_choice < 0.7:
                    return 3  # Jump dodge
                else:
                    # Evasive retreat
                    if relative_pos > 0:
                        return 1
                    else:
                        return 2
        
        # Clean strike opportunity
        if not my_attack_status > 0.3:
            strike_aggression = current_aggression + (chaos_factor - 0.5) * 0.2
            strike_decision = tactical_roll
            
            if strike_decision < strike_aggression * 0.55:
                return 4  # Fast strike
            elif strike_decision < strike_aggression * 0.85:
                return 5  # Power strike
            elif strike_decision < 0.9:
                # Feint - no attack, reposition
                if relative_pos > 0:
                    return 1  # Feint retreat
                else:
                    return 2  # Feint retreat
            else:
                return 6  # Defensive wait