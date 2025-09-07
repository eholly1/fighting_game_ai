"""
Evolutionary Agent: gen0_agent_023
==================================

Metadata:
{
  "generation": 0,
  "fitness": 181.4695999999951,
  "fighting_style": "balanced",
  "win_rate": 0.5
}

Code Hash: 8a88bb9a69764e15
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
    
    # Extract player and opponent information
    my_health = state[1] if state[1] >= 0 else 0.5
    my_x_pos = state[0]
    my_y_pos = state[2] if len(state) > 2 else 0.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    opp_health = state[12] if len(state) > 12 else 0.5
    opp_x_pos = state[11] if len(state) > 11 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    
    # Define strategic thresholds
    close_range = 0.12
    medium_range = 0.35
    critical_health = 0.25
    winning_threshold = 0.15
    losing_threshold = -0.2
    
    # Calculate situational awareness
    am_winning = health_advantage > winning_threshold
    am_losing = health_advantage < losing_threshold
    critical_situation = my_health < critical_health
    opponent_attacking = opp_attack_status > 0.5
    opponent_blocking = opp_block_status > 0.5
    can_use_projectile = my_projectile_cooldown < 0.1
    
    # Emergency defensive situations
    if critical_situation and opponent_attacking:
        if distance < close_range:
            return 6  # Block incoming attack
        elif relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Adapt strategy based on health advantage
    aggression_level = 0.5
    if am_winning:
        aggression_level = 0.75
    elif am_losing:
        aggression_level = 0.3
    elif critical_situation:
        aggression_level = 0.15
    
    # Range-based tactical decisions
    if distance < close_range:
        # Close combat tactics
        if opponent_blocking:
            # Mix up against blocking opponent
            if random.random() < 0.4:
                return 5  # Heavy kick to break guard
            elif relative_pos > 0:
                return 1  # Move left to reposition
            else:
                return 2  # Move right to reposition
        
        elif opponent_attacking:
            # Counter-attack or defend
            if am_losing or my_health < 0.4:
                return 6  # Block the attack
            else:
                # Counter with quick attack
                return 4 if random.random() < 0.7 else 5
        
        else:
            # Opponent is neutral, decide based on health
            if am_winning and random.random() < aggression_level:
                # Aggressive close combat when winning
                attack_choice = random.random()
                if attack_choice < 0.6:
                    return 4  # Quick punch
                else:
                    return 5  # Power kick
            elif am_losing:
                # More cautious when losing
                if random.random() < 0.6:
                    return 6  # Block
                else:
                    return 4  # Safe quick attack
            else:
                # Balanced approach
                choice = random.random()
                if choice < 0.4:
                    return 4  # Punch
                elif choice < 0.6:
                    return 5  # Kick
                else:
                    return 6  # Block
    
    elif distance < medium_range:
        # Medium range positioning and tactics
        if opponent_attacking and distance < 0.25:
            # Opponent might reach us, be defensive
            if random.random() < 0.5:
                return 6  # Block
            elif relative_pos > 0:
                return 7  # Move left blocking
            else:
                return 8  # Move right blocking
        
        elif can_use_projectile and distance > 0.2:
            # Good projectile range
            if am_winning or random.random() < 0.4:
                return 9  # Projectile attack
        
        # Positioning for advantage
        if am_winning:
            # Advance when winning
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        elif am_losing and critical_situation:
            # Create distance when in trouble
            if can_use_projectile:
                return 9  # Projectile
            elif relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        else:
            # Neutral positioning
            positioning_choice = random.random()
            if positioning_choice < 0.3:
                return 1 if relative_pos > 0 else 2  # Move toward opponent
            elif positioning_choice < 0.5 and can_use_projectile:
                return 9  # Projectile
            elif positioning_choice < 0.7:
                return 3  # Jump for positioning
            else:
                return 0  # Wait and observe
    
    else:
        # Long range tactics
        if can_use_projectile:
            # Primary long-range option
            projectile_chance = 0.7
            if am_losing:
                projectile_chance = 0.8  # More projectiles when losing
            elif am_winning:
                projectile_chance = 0.6  # Slightly fewer when winning
            
            if random.random() < projectile_chance:
                return 9  # Projectile attack
        
        # Movement and positioning at long range
        if am_winning:
            # Advance to pressure opponent
            advance_choice = random.random()
            if advance_choice < 0.4:
                return 2 if relative_pos > 0 else 1  # Move toward opponent
            elif advance_choice < 0.6:
                return 3  # Jump advance
            else:
                return 0  # Patient approach
        
        elif am_losing and not critical_situation:
            # Careful advance when behind
            if random.random() < 0.5:
                return 2 if relative_pos > 0 else 1  # Cautious advance
            else:
                return 0  # Wait for opportunity
        
        else:
            # Neutral or critical situation
            if critical_situation:
                # Very defensive
                if can_use_projectile:
                    return 9  # Keep distance with projectiles
                else:
                    return 0  # Wait for projectile cooldown
            else:
                # Balanced long-range approach
                choice = random.random()
                if choice < 0.3:
                    return 2 if relative_pos > 0 else 1  # Advance
                elif choice < 0.5:
                    return 3  # Jump