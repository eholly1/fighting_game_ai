"""
Evolutionary Agent: gen2_agent_025
==================================

Metadata:
{
  "generation": 2,
  "fitness": 192.0199999999906,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: daad4e6315387da4
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
    height_diff = state[24]
    
    # Extract comprehensive fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity_x = state[3]
    my_velocity_y = state[4]
    my_attack_status = state[5]
    my_block_status = state[6]
    opponent_velocity_x = state[14]
    opponent_velocity_y = state[15]
    opponent_attack_status = state[16]
    opponent_block_status = state[17]
    projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = max(0.0, state[21])
    
    # Enhanced tactical ranges for hybrid fighting
    very_close = 0.08
    close_range = 0.16
    medium_range = 0.32
    long_range = 0.50
    max_range = 0.75
    
    # Dynamic threshold system
    critical_health = 0.18
    low_health = 0.35
    high_health = 0.75
    decisive_advantage = 0.35
    significant_disadvantage = -0.30
    
    # Adaptive parameters based on game state
    base_aggression = 0.5
    aggression_modifier = 0.0
    defensive_modifier = 0.0
    
    # Calculate dynamic aggression
    if health_advantage > decisive_advantage:
        aggression_modifier += 0.4
    elif health_advantage < significant_disadvantage:
        aggression_modifier -= 0.5
        defensive_modifier += 0.3
    
    if my_health < critical_health:
        aggression_modifier -= 0.4
        defensive_modifier += 0.5
    elif my_health > high_health:
        aggression_modifier += 0.2
    
    current_aggression = max(0.1, min(0.9, base_aggression + aggression_modifier))
    defensive_priority = max(0.1, min(0.8, 0.3 + defensive_modifier))
    
    # Advanced opponent analysis
    opponent_is_aggressive = opponent_attack_status > 0.2 or abs(opponent_velocity_x) > 0.1
    opponent_is_defensive = opponent_block_status > 0.3
    opponent_is_mobile = abs(opponent_velocity_x) > 0.08
    opponent_can_projectile = opponent_projectile_cooldown < 0.2
    i_can_projectile = projectile_cooldown < 0.1
    opponent_momentum = abs(opponent_velocity_x) + abs(opponent_velocity_y)
    my_momentum = abs(my_velocity_x) + abs(my_velocity_y)
    
    # Randomization for unpredictability
    tactical_roll = random.random()
    combat_roll = random.random()
    movement_roll = random.random()
    
    # Emergency survival protocol
    if my_health < critical_health and health_advantage < -0.4:
        if distance < close_range:
            if opponent_attack_status > 0.4:
                # Immediate threat - block
                return 6
            else:
                # Create distance urgently
                if relative_pos > 0:
                    return 7 if tactical_roll < 0.7 else 1
                else:
                    return 8 if tactical_roll < 0.7 else 2
        elif distance < medium_range and i_can_projectile:
            # Safe projectile harassment
            return 9
        elif distance < long_range:
            # Maintain distance
            if relative_pos > 0:
                return 1
            else:
                return 2
        else:
            # Long range safety
            if i_can_projectile and not opponent_is_defensive:
                return 9
            else:
                return 0
    
    # Aggressive finishing mode
    if health_advantage > decisive_advantage and opponent_health < 0.25:
        if distance < very_close:
            if opponent_is_defensive:
                # Break guard with variety
                break_guard_choice = combat_roll
                if break_guard_choice < 0.3:
                    return 5  # Heavy kick
                elif break_guard_choice < 0.5:
                    return 3  # Jump attack
                elif break_guard_choice < 0.7:
                    # Reposition to flank
                    return 2 if relative_pos < 0 else 1
                else:
                    return 4  # Quick punch
            else:
                # Unleash finishing combo
                finish_choice = combat_roll
                if finish_choice < 0.6:
                    return 5  # Power kick
                else:
                    return 4  # Fast punch
        elif distance < close_range:
            # Approach for finish
            if opponent_can_projectile:
                # Approach with protection
                if relative_pos > 0:
                    return 8
                else:
                    return 7
            else:
                # Direct approach
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        elif distance < medium_range and i_can_projectile:
            # Projectile pressure
            return 9
    
    # Very close range combat - hybrid intensity
    if distance < very_close:
        # Analyze immediate threats and opportunities
        immediate_threat = opponent_attack_status > 0.3
        counter_opportunity = opponent_attack_status > 0.5 and my_attack_status < 0.2
        
        if immediate_threat and defensive_priority > 0.5:
            # Prioritize defense in close quarters
            if tactical_roll < 0.6:
                return 6  # Block
            elif tactical_roll < 0.8:
                # Defensive movement
                if relative_pos > 0:
                    return 7
                else:
                    return 8
            else:
                # Quick counter
                return 4
        
        if counter_opportunity and current_aggression > 0.6:
            # Counter-attack opportunity
            if combat_roll < 0.7:
                return 5  # Strong counter kick
            else:
                return 4  # Fast counter punch
        
        if opponent_is_defensive:
            # Opponent blocking - tactical response
            guard_break_strategy = tactical_roll
            if guard_break_strategy < 0.25:
                return 5  # Heavy attack
            elif guard_break_strategy < 0.45:
                return 3  # Jump over guard
            elif guard_break_strategy < 0.65:
                # Positional advantage
                return 2 if relative_pos < 0 else 1
            elif guard_break_strategy < 0.8:
                return 4  # Quick jab
            else:
                # Create space and reset
                if relative_pos > 0:
                    return 1
                else:
                    return 2
        
        # Standard very close combat
        if current_aggression > 0.65:
            # Aggressive close combat
            attack_pattern = combat_roll
            if attack_pattern < 0.4:
                return 4  # Fast punch
            elif attack_pattern < 0.7:
                return 5  # Power kick
            elif attack_pattern < 0.85:
                return 3  # Jump attack
            else:
                return 6  # Defensive block
        else:
            # Balanced close combat
            balanced_choice = combat_roll
            if balanced_choice < 0.35:
                return 6