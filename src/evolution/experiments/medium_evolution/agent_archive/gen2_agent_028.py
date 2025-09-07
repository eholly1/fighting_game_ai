"""
Evolutionary Agent: gen2_agent_028
==================================

Metadata:
{
  "generation": 2,
  "fitness": 118.83333333333329,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: fb17b38ad4f657ba
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate core strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24]
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_pos_x = state[0]
    my_pos_y = state[1]
    my_vel_x = state[3]
    my_vel_y = state[4]
    my_attack_status = state[5]
    my_block_status = state[6]
    my_projectile_cooldown = max(0.0, state[10])
    
    opponent_pos_x = state[11]
    opponent_pos_y = state[12]
    opponent_vel_x = state[14]
    opponent_vel_y = state[15]
    opponent_attack_status = state[16]
    opponent_block_status = state[17]
    opponent_projectile_cooldown = max(0.0, state[21])
    
    # Advanced tactical parameters for hybrid fighting
    very_close_threshold = 0.09
    close_threshold = 0.16
    medium_threshold = 0.34
    far_threshold = 0.52
    extreme_range = 0.7
    
    critical_health = 0.18
    low_health = 0.32
    decent_health = 0.6
    excellent_health = 0.85
    
    major_advantage = 0.4
    moderate_advantage = 0.2
    slight_advantage = 0.1
    slight_disadvantage = -0.1
    moderate_disadvantage = -0.2
    major_disadvantage = -0.4
    
    # Situational awareness variables
    opponent_is_aggressive = opponent_attack_status > 0 or abs(opponent_vel_x) > 0.12
    opponent_is_defensive = opponent_block_status > 0
    opponent_is_mobile = abs(opponent_vel_x) > 0.08
    opponent_can_projectile = opponent_projectile_cooldown < 0.15
    i_can_projectile = my_projectile_cooldown < 0.15
    
    # Positioning analysis
    i_am_cornered = abs(my_pos_x) > 0.75
    opponent_cornered = abs(opponent_pos_x) > 0.75
    center_control = abs(my_pos_x) < 0.3
    
    # Movement prediction
    opponent_approaching = (relative_pos > 0 and opponent_vel_x > 0.05) or (relative_pos < 0 and opponent_vel_x < -0.05)
    opponent_retreating = (relative_pos > 0 and opponent_vel_x < -0.05) or (relative_pos < 0 and opponent_vel_x > 0.05)
    
    # Dynamic aggression calculation
    base_aggression = 0.55
    aggression_modifier = 0.0
    
    # Health-based aggression adjustments
    if my_health > excellent_health:
        aggression_modifier += 0.2
    elif my_health > decent_health:
        aggression_modifier += 0.1
    elif my_health < critical_health:
        aggression_modifier -= 0.4
    elif my_health < low_health:
        aggression_modifier -= 0.2
    
    # Advantage-based aggression adjustments
    if health_advantage > major_advantage:
        aggression_modifier += 0.25
    elif health_advantage > moderate_advantage:
        aggression_modifier += 0.15
    elif health_advantage < major_disadvantage:
        aggression_modifier -= 0.3
    elif health_advantage < moderate_disadvantage:
        aggression_modifier -= 0.15
    
    # Positional aggression adjustments
    if opponent_cornered and not i_am_cornered:
        aggression_modifier += 0.15
    elif i_am_cornered and not opponent_cornered:
        aggression_modifier -= 0.2
    
    current_aggression = max(0.15, min(0.85, base_aggression + aggression_modifier))
    
    # Emergency survival mode for critical health
    if my_health < critical_health and health_advantage < major_disadvantage:
        # Immediate threat response
        if distance < close_threshold and opponent_attack_status > 0:
            return 6  # Block immediate danger
        
        # Create maximum distance when critical
        if distance < medium_threshold:
            if i_am_cornered:
                # Fight way out of corner
                if my_pos_x > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Retreat with defense
                if relative_pos > 0:
                    return 7 if random.random() < 0.8 else 1
                else:
                    return 8 if random.random() < 0.8 else 2
        
        # Long range survival tactics
        if distance > medium_threshold and i_can_projectile and not opponent_is_defensive:
            return 9  # Safe harassment
        
        return 6  # Default survival block
    
    # Very close range combat - intense engagement
    if distance < very_close_threshold:
        # Counter-attack timing windows
        if opponent_attack_status > 0 and my_attack_status == 0:
            if current_aggression > 0.6 and random.random() < 0.5:
                return 5  # Counter with strong kick
            else:
                return 6  # Safe block counter
        
        # Break through defensive opponents
        if opponent_is_defensive and not opponent_is_mobile:
            breakthrough_choice = random.random()
            if breakthrough_choice < 0.3:
                return 5  # Power through with kick
            elif breakthrough_choice < 0.5:
                return 3  # Jump over guard
            elif breakthrough_choice < 0.7:
                # Reposition around guard
                if relative_pos > 0:
                    return 1
                else:
                    return 2
            else:
                return 4  # Quick punch test
        
        # Mobile defensive opponent handling
        if opponent_is_defensive and opponent_is_mobile:
            if opponent_vel_x > 0.05:  # Moving right
                return 2 if random.random() < 0.7 else 5  # Follow or intercept
            elif opponent_vel_x < -0.05:  # Moving left
                return 1 if random.random() < 0.7 else 5  # Follow or intercept
            else:
                return 3  # Jump attack surprise
        
        # Aggressive very close combat
        if current_aggression > 0.65:
            close_combat_choice = random.random()
            if close_combat_choice < 0.35:
                return 4  # Fast punch
            elif close_combat_choice < 0.65:
                return 5  # Strong kick
            elif close_combat_choice < 0.8:
                return 3  # Jump attack
            else:
                return 6  # Defensive pause
        
        # Balanced very close combat
        elif current_aggression > 0.35:
            if random.random() < 0.4:
                return 4  # Punch
            elif random.random() < 0.7:
                return 5  # Kick
            else:
                return 6  # Block
        
        # Defensive very close combat
        else:
            if random.random() < 0.6:
                return 6  # Block frequently