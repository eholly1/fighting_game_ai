"""
Evolutionary Agent: gen0_agent_003
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "balanced",
  "win_rate": 0.5
}

Code Hash: c9eb2d6c40dddd91
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate core state information
    distance = max(0.0, min(1.0, float(state[22])))
    relative_pos = max(-1.0, min(1.0, float(state[23])))
    health_advantage = max(-1.0, min(1.0, float(state[25])))
    height_diff = float(state[24])
    
    # Extract player state info
    my_health = max(0.0, min(1.0, float(state[1])))
    my_velocity_x = float(state[2])
    my_velocity_y = float(state[3])
    my_attacking = bool(state[4])
    my_blocking = bool(state[5])
    my_projectile_cooldown = max(0.0, float(state[10]))
    
    # Extract opponent state info
    opp_health = max(0.0, min(1.0, float(state[12])))
    opp_velocity_x = float(state[13])
    opp_velocity_y = float(state[14])
    opp_attacking = bool(state[15])
    opp_blocking = bool(state[16])
    opp_projectile_cooldown = max(0.0, float(state[21]))
    
    # Define strategic thresholds
    close_range = 0.15
    medium_range = 0.35
    critical_health = 0.25
    winning_threshold = 0.2
    losing_threshold = -0.2
    projectile_ready_threshold = 0.1
    
    # Calculate aggression level based on health advantage
    base_aggression = 0.5
    if health_advantage > winning_threshold:
        aggression = min(0.8, base_aggression + health_advantage * 0.4)
    elif health_advantage < losing_threshold:
        aggression = max(0.2, base_aggression + health_advantage * 0.3)
    else:
        aggression = base_aggression
    
    # Emergency defensive behavior when critically low health
    if my_health < critical_health and health_advantage < -0.3:
        if distance < close_range:
            if opp_attacking:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking to escape
            else:
                return 8  # Move right while blocking to escape
        elif distance < medium_range:
            if my_projectile_cooldown < projectile_ready_threshold:
                return 9  # Projectile to create space
            else:
                return 3  # Jump to avoid ground attacks
        else:
            return 9 if my_projectile_cooldown < projectile_ready_threshold else 0
    
    # Opponent analysis for counter-strategies
    opp_aggressive = opp_attacking or (abs(opp_velocity_x) > 0.3)
    opp_defensive = opp_blocking
    opp_can_projectile = opp_projectile_cooldown < projectile_ready_threshold
    
    # Close range combat (high intensity)
    if distance < close_range:
        # Respond to opponent's immediate actions
        if opp_attacking:
            if random.random() < 0.7:
                return 6  # Block most attacks
            else:
                return 3  # Jump over low attacks
        
        if opp_blocking:
            # Mix up attacks against blocking opponent
            if random.random() < 0.4:
                return 3  # Jump for overhead approach
            elif random.random() < 0.6:
                return 5  # Strong kick to break guard
            else:
                # Reposition for better angle
                if relative_pos > 0:
                    return 1  # Move left to flank
                else:
                    return 2  # Move right to flank
        
        # Aggressive close combat when winning
        if health_advantage > 0:
            attack_choice = random.random()
            if attack_choice < 0.4:
                return 4  # Fast punch
            elif attack_choice < 0.7:
                return 5  # Strong kick
            else:
                return 3  # Jump attack setup
        
        # Defensive close combat when losing
        else:
            if random.random() < 0.5:
                return 6  # Block
            else:
                # Try to escape close range
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
    
    # Medium range combat (positioning and timing)
    elif distance < medium_range:
        # Height advantage consideration
        if abs(height_diff) > 0.3:
            if height_diff > 0:  # Opponent below
                if my_projectile_cooldown < projectile_ready_threshold:
                    return 9  # Projectile from height advantage
                else:
                    return 4  # Quick descending attack
            else:  # Opponent above
                return 3  # Jump to match height
        
        # Projectile warfare in medium range
        if my_projectile_cooldown < projectile_ready_threshold:
            if not opp_blocking and abs(opp_velocity_x) < 0.2:
                return 9  # Projectile on stationary target
        
        # Movement-based positioning
        if opp_aggressive:
            # Counter-movement against aggressive opponent
            if relative_pos > 0 and opp_velocity_x > 0:
                return 1  # Move left to avoid rush
            elif relative_pos < 0 and opp_velocity_x < 0:
                return 2  # Move right to avoid rush
            else:
                return 6  # Block if can't avoid
        
        # Controlled advance when winning
        if health_advantage > winning_threshold:
            if aggression > 0.6:
                if relative_pos > 0:
                    return 2  # Advance right
                else:
                    return 1  # Advance left
            else:
                return 9 if my_projectile_cooldown < projectile_ready_threshold else 0
        
        # Cautious positioning when losing
        elif health_advantage < losing_threshold:
            if opp_can_projectile:
                if random.random() < 0.6:
                    return 3  # Jump over projectiles
                else:
                    return 6  # Block projectiles
            else:
                if relative_pos > 0:
                    return 2  # Advance right cautiously
                else:
                    return 1  # Advance left cautiously
        
        # Balanced medium range approach
        else:
            movement_choice = random.random()
            if movement_choice < 0.3:
                if relative_pos > 0:
                    return 2  # Move toward opponent
                else:
                    return 1  # Move toward opponent
            elif movement_choice < 0.5:
                return 3  # Jump for positioning
            elif movement_choice < 0.7 and my_projectile_cooldown < projectile_ready_threshold:
                return 9  # Projectile
            else:
                return 0  # Wait and observe
    
    # Long range combat (projectile focused)
    else:
        # Projectile priority at long range
        if my_projectile_cooldown < projectile_ready_threshold:
            if not opp_blocking or random.random() < 0.3:
                return 9  # Projectile attack
        
        # Counter opponent's projectiles
        if opp_can_projectile and distance > 0.6:
            evasion_choice = random.random()
            if evasion_choice < 0.4:
                return 3  # Jump over projectile
            elif evasion_choice < 0.7:
                if relative_pos > 0:
                    return 1  # Strafe left
                else:
                    return 2  # Strafe right