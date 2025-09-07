"""
Evolutionary Agent: gen1_agent_005
==================================

Metadata:
{
  "generation": 1,
  "fitness": 189.07933333332963,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 424824b4510697b8
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
    
    # Extract my fighter state
    my_health = max(0.0, min(1.0, state[2]))
    my_x_pos = state[0]
    my_y_pos = state[1]
    my_x_vel = state[3]
    my_y_vel = state[4]
    my_attacking = state[7]
    my_blocking = state[8]
    my_projectile_cooldown = max(0.0, state[9])
    
    # Extract opponent state
    opponent_health = max(0.0, min(1.0, state[13]))
    opponent_x_pos = state[11]
    opponent_y_pos = state[12]
    opponent_x_vel = state[14]
    opponent_y_vel = state[15]
    opponent_attacking = state[18]
    opponent_blocking = state[19]
    opponent_projectile_cooldown = max(0.0, state[20])
    
    # Define hybrid fighter tactical parameters
    close_range = 0.14
    medium_range = 0.32
    far_range = 0.5
    critical_health = -0.35
    winning_health = 0.25
    retreat_distance = 0.2
    
    # Adaptive aggression based on health and distance
    base_aggression = 0.6  # Hybrid balance
    if health_advantage < critical_health:
        aggression_modifier = -0.4
    elif health_advantage > winning_health:
        aggression_modifier = 0.3
    else:
        aggression_modifier = 0.0
    
    current_aggression = max(0.1, min(0.9, base_aggression + aggression_modifier))
    
    # Analyze opponent movement patterns
    opponent_advancing = False
    opponent_retreating = False
    if relative_pos > 0 and opponent_x_vel > 0.05:
        opponent_advancing = True
    elif relative_pos < 0 and opponent_x_vel < -0.05:
        opponent_advancing = True
    elif relative_pos > 0 and opponent_x_vel < -0.05:
        opponent_retreating = True
    elif relative_pos < 0 and opponent_x_vel > 0.05:
        opponent_retreating = True
    
    # Emergency health management
    if my_health < 0.15 or health_advantage < -0.5:
        if distance < retreat_distance:
            # Defensive retreat with blocking
            if opponent_attacking > 0.5:
                return 6  # Pure block
            else:
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        elif my_projectile_cooldown < 0.2:
            return 9  # Keep distance with projectiles
        else:
            return 6  # Block and recover
    
    # Opportunity recognition when opponent is vulnerable
    opponent_vulnerable = opponent_attacking > 0.5 or opponent_projectile_cooldown > 0.4
    
    # Close range combat (0.0 - 0.14)
    if distance < close_range:
        # Immediate threat assessment
        if opponent_attacking > 0.5:
            if random.random() < 0.7:
                return 6  # Block incoming attack
            else:
                # Counter-attack through opponent's attack
                return 4  # Fast punch counter
        
        # Anti-blocking tactics
        if opponent_blocking > 0.6:
            block_break_choice = random.random()
            if block_break_choice < 0.4:
                return 5  # Kick to break block
            elif block_break_choice < 0.6:
                return 3  # Jump attack
            else:
                # Create space and reset
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        # Aggressive close combat when opponent is open
        if health_advantage > 0 or current_aggression > 0.6:
            attack_pattern = random.random()
            if attack_pattern < 0.45:
                return 4  # Fast punch
            elif attack_pattern < 0.75:
                return 5  # Strong kick
            elif attack_pattern < 0.85:
                return 3  # Jumping attack
            else:
                return 6  # Block for safety
        
        # Defensive close combat when disadvantaged
        else:
            defensive_choice = random.random()
            if defensive_choice < 0.3:
                return 4  # Quick punch
            elif defensive_choice < 0.5:
                return 5  # Kick
            else:
                return 6  # Block
    
    # Medium range positioning (0.14 - 0.32)
    elif distance < medium_range:
        # Capitalize on opponent vulnerability
        if opponent_vulnerable and health_advantage > -0.2:
            if current_aggression > 0.5:
                # Aggressive approach
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                # Cautious approach
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
        
        # Respond to opponent advancing
        if opponent_advancing:
            if health_advantage < 0:
                # Defensive response
                if my_projectile_cooldown < 0.2:
                    return 9  # Projectile to slow advance
                else:
                    return 6  # Block and prepare
            else:
                # Meet the advance
                medium_counter = random.random()
                if medium_counter < 0.5:
                    if relative_pos > 0:
                        return 2  # Move toward
                    else:
                        return 1  # Move toward
                else:
                    return 6  # Block and counter
        
        # Respond to opponent retreating
        if opponent_retreating and health_advantage > -0.1:
            chase_decision = random.random()
            if chase_decision < current_aggression:
                if relative_pos > 0:
                    return 2  # Chase right
                else:
                    return 1  # Chase left
            elif my_projectile_cooldown < 0.3:
                return 9  # Projectile chase
        
        # Standard medium range tactics
        medium_action = random.random()
        if medium_action < 0.25:
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile
            else:
                return 0  # Wait for cooldown
        elif medium_action < 0.4:
            return 3  # Jump for positioning
        elif medium_action < 0.6:
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
        elif medium_action < 0.8:
            return 6  # Block
        else:
            return 0  # Observe
    
    # Far range combat (0.32 - 0.5)
    elif distance < far_range:
        # Projectile warfare priority
        if my_projectile_cooldown < 0.1:
            projectile_chance = 0.6 + (health_advantage * 0.2)
            if random.random() < projectile_chance:
                return 9  # Projectile