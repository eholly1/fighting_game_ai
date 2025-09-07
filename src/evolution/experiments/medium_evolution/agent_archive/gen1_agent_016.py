"""
Evolutionary Agent: gen1_agent_016
==================================

Metadata:
{
  "generation": 1,
  "fitness": 254.27999999999003,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: a5b0fe639d5cad55
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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[3]))
    opponent_health = max(0.0, min(1.0, state[14]))
    my_position = state[1]
    opponent_position = state[12]
    my_velocity = abs(state[2])
    opponent_velocity = abs(state[13])
    
    # Attack and defense states
    my_attacking = state[7] > 0.5
    opponent_attacking = state[18] > 0.5
    my_blocking = state[8] > 0.5
    opponent_blocking = state[19] > 0.5
    my_projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = max(0.0, state[21])
    
    # Height difference for aerial considerations
    height_diff = state[24]
    
    # Strategic thresholds for hybrid balanced approach
    close_range = 0.14
    medium_range = 0.32
    long_range = 0.55
    critical_health = 0.2
    danger_health = 0.35
    winning_threshold = 0.25
    decisive_advantage = 0.5
    
    # Timing and positioning variables
    attack_window = opponent_projectile_cooldown > 0.4
    safe_to_move = not opponent_attacking or distance > 0.25
    cornered = abs(my_position) > 0.75
    opponent_cornered = abs(opponent_position) > 0.75
    
    # Emergency survival protocol
    if my_health < critical_health:
        if opponent_attacking and distance < 0.2:
            return 6  # Priority block
        
        if distance > long_range and my_projectile_cooldown < 0.15:
            return 9  # Safe long-range harassment
        
        if cornered:
            # Escape corner with defensive movement
            if my_position > 0:
                return 7  # Move left with block
            else:
                return 8  # Move right with block
        
        # Defensive spacing when critically low
        if distance < 0.4:
            if relative_pos > 0:
                return 7  # Retreat left defensively
            else:
                return 8  # Retreat right defensively
        
        return 6  # Default block when critical
    
    # Defensive-oriented play when health is low
    if my_health < danger_health:
        # Enhanced blocking against attacks
        if opponent_attacking:
            if distance < medium_range:
                # Perfect block timing at medium-close range
                return 6
            else:
                # Defensive movement at longer ranges
                if distance < long_range:
                    if relative_pos > 0:
                        return 7  # Block and create space
                    else:
                        return 8  # Block and create space
        
        # Conservative counter-attacks when safe
        if distance < close_range and not opponent_blocking:
            if opponent_velocity < 0.2 and attack_window:
                # Calculated low-risk counter
                if random.random() < 0.6:
                    return 4  # Quick punch
                else:
                    return 6  # Stay defensive
        
        # Long-range tactical play
        if distance > medium_range:
            if my_projectile_cooldown < 0.2 and not opponent_blocking:
                return 9  # Safe projectile pressure
            
            # Maintain optimal spacing
            if distance < 0.45:
                if relative_pos > 0:
                    return 1  # Back away
                else:
                    return 2  # Back away
        
        return 6  # Default defensive stance
    
    # Balanced aggressive-defensive play when health is stable
    if health_advantage > -0.15 and health_advantage < winning_threshold:
        # React to opponent attacks with smart defense
        if opponent_attacking:
            if distance < close_range:
                return 6  # Block close attacks
            elif distance < medium_range:
                # Mixed defensive responses
                if random.random() < 0.7:
                    return 6  # Block
                else:
                    # Evasive movement
                    if relative_pos > 0:
                        return 7  # Move left with block
                    else:
                        return 8  # Move right with block
        
        # Close range hybrid tactics
        if distance < close_range:
            if not opponent_blocking and not opponent_attacking:
                # Optimal attack window
                attack_choice = random.random()
                if attack_choice < 0.35:
                    return 4  # Quick punch
                elif attack_choice < 0.6:
                    return 5  # Power kick
                else:
                    return 6  # Maintain guard
            elif opponent_blocking:
                # Pressure blocked opponent
                if random.random() < 0.4:
                    return 5  # Strong kick to break guard
                else:
                    return 6  # Wait for opening
        
        # Medium range positioning and control
        elif distance < medium_range:
            if opponent_projectile_cooldown < 0.3:
                return 6  # Guard against incoming projectile
            
            # Intelligent positioning
            if safe_to_move:
                if distance > 0.25:
                    # Close distance for attack opportunities
                    if relative_pos > 0:
                        return 2  # Move right toward opponent
                    else:
                        return 1  # Move left toward opponent
                else:
                    # Perfect medium range - hold position
                    if random.random() < 0.3 and my_projectile_cooldown < 0.3:
                        return 9  # Medium range projectile
                    else:
                        return 6  # Maintain guard
        
        # Long range hybrid tactics
        else:
            if my_projectile_cooldown < 0.25 and attack_window:
                return 9  # Long range projectile pressure
            
            # Control spacing intelligently
            if distance > 0.7:
                # Close distance gradually
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            elif opponent_cornered and distance < 0.5:
                # Press advantage against cornered opponent
                if my_projectile_cooldown < 0.4:
                    return 9  # Projectile pressure
                else:
                    if relative_pos > 0:
                        return 2  # Close in
                    else:
                        return 1  # Close in
            else:
                return 6  # Maintain defensive readiness
    
    # Controlled aggression when winning
    elif health_advantage >= winning_threshold and health_advantage < decisive_advantage:
        # Still respect opponent attacks but more confident
        if opponent_attacking:
            if distance < close_range:
                if random.random() < 0.8:
                    return 6  # Block most attacks
                else:
                    # Occasional counter-attack timing
                    return 4  # Quick counter
            else:
                # More mobile defense when winning
                if relative_pos > 0:
                    return 7  # Move with block
                else:
                    return 8  # Move with block
        
        # Increased aggression at close range
        if distance < close_range:
            if not opponent_blocking:
                # Higher attack frequency when winning
                attack_choice = random.random()
                if attack_choice < 0.45:
                    return 4  # Quick punch
                elif attack_choice < 0.7:
                    return 5  # Power kick
                else:
                    return