"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_000
Rank: 12/13
Generation: 0
Fighting Style: aggressive

Performance Metrics:
- Fitness: 25.48
- Win Rate: 50.0%
- Average Reward: 0.00

Created: 2025-06-01 11:35:24
Lineage: Original

Tournament Stats:
None
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Validate and extract key state information
    if len(state) < 26:
        return 4  # Default punch if invalid state
    
    # Core state variables with bounds checking
    distance = max(0.0, min(1.0, float(state[22])))
    relative_pos = max(-1.0, min(1.0, float(state[23])))
    health_advantage = max(-1.0, min(1.0, float(state[25])))
    height_diff = float(state[24]) if len(state) > 24 else 0.0
    
    # My fighter status (indices 0-10)
    my_health = max(0.0, float(state[1]))
    my_x_pos = float(state[0])
    my_velocity_x = float(state[2])
    my_is_attacking = bool(state[5])
    my_is_blocking = bool(state[6])
    my_projectile_cooldown = max(0.0, float(state[9]))
    my_stamina = max(0.0, float(state[10]))
    
    # Opponent status (indices 11-21)
    opp_health = max(0.0, float(state[12]))
    opp_x_pos = float(state[11])
    opp_is_attacking = bool(state[16])
    opp_is_blocking = bool(state[17])
    opp_projectile_cooldown = max(0.0, float(state[20]))
    
    # Tactical range definitions
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    
    # Aggressive style parameters
    base_aggression = 0.85
    chase_threshold = 0.6
    pressure_distance = 0.35
    attack_mix_ratio = 0.65
    
    # Health-based aggression modifiers
    if health_advantage > 0.4:
        aggression_modifier = 1.2  # Even more aggressive when winning
    elif health_advantage > 0.0:
        aggression_modifier = 1.0  # Standard aggression
    elif health_advantage > -0.3:
        aggression_modifier = 0.9  # Slightly less reckless
    else:
        aggression_modifier = 0.7  # Desperate but still aggressive
    
    final_aggression = min(1.0, base_aggression * aggression_modifier)
    
    # Emergency defensive situations
    if my_health < 0.2 and health_advantage < -0.5:
        if distance < close_range and opp_is_attacking:
            return 6  # Block incoming attack
        elif distance > medium_range:
            return 9  # Try projectile for chip damage
    
    # Counter-attack when opponent is vulnerable
    if opp_is_attacking and distance < close_range:
        if random.random() < 0.3:  # Sometimes block, but prefer trading
            return 6
        else:
            return 5 if random.random() < 0.7 else 4  # Favor kick counter
    
    # Aggressive close-range combat
    if distance <= close_range:
        # Don't block too much - stay aggressive
        if opp_is_blocking and random.random() < 0.4:
            return 5  # Kick to break guard
        
        # Mix up attacks heavily in close range
        attack_choice = random.random()
        if attack_choice < 0.4:
            return 4  # Quick punch
        elif attack_choice < 0.75:
            return 5  # Strong kick
        else:
            # Occasional movement to reset positioning
            if relative_pos > 0:
                return 2  # Move right to maintain pressure
            else:
                return 1  # Move left to maintain pressure
    
    # Medium range - positioning for aggression
    elif distance <= medium_range:
        # Always move toward opponent for pressure
        movement_urgency = random.random()
        
        if movement_urgency < final_aggression:
            # Direct approach
            if relative_pos > 0.1:
                return 2  # Chase right
            elif relative_pos < -0.1:
                return 1  # Chase left
            else:
                # Close enough to attack
                if random.random() < 0.6:
                    return 4  # Quick punch to close gap
                else:
                    return 5  # Kick
        else:
            # Cautious approach with blocking movement
            if relative_pos > 0:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
    
    # Far range - close distance aggressively
    elif distance <= far_range:
        # Projectile if available and tactical
        projectile_chance = 0.3 - (final_aggression * 0.2)  # Less projectiles when more aggressive
        
        if my_projectile_cooldown <= 0 and random.random() < projectile_chance:
            return 9  # Projectile
        
        # Mostly chase opponent
        chase_urgency = random.random()
        if chase_urgency < final_aggression:
            # Direct chase
            if relative_pos > 0:
                return 2
            else:
                return 1
        else:
            # Protected advance
            if relative_pos > 0:
                return 8
            else:
                return 7
    
    # Very far range - mixed approach
    else:
        # Use projectiles more at very long range
        if my_projectile_cooldown <= 0 and random.random() < 0.6:
            return 9
        
        # Jump forward occasionally for surprise
        if random.random() < 0.15:
            return 3
        
        # Otherwise close distance
        if relative_pos > 0:
            return 2
        else:
            return 1
    
    # Height advantage tactics
    if abs(height_diff) > 0.3:
        if height_diff > 0:  # I'm higher
            if distance < close_range:
                return 5  # Kick down
            else:
                return 9  # Projectile down
        else:  # Opponent is higher
            if distance < medium_range:
                return 3  # Jump up
            else:
                # Close distance first
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Stamina management - stay aggressive but smart
    if my_stamina < 0.3:
        if distance < close_range and opp_is_attacking:
            return 6  # Block to recover stamina
        elif distance > medium_range:
            return 9  # Low stamina projectile
        else:
            # Light attacks to maintain pressure
            return 4
    
    # Opponent behavior adaptation
    if opp_is_blocking and distance < medium_range:
        # Break guard with kicks or positioning
        if random.random() < 0.6:
            return 5  # Kick
        else:
            # Move to different angle
            if random.random() < 0.5:
                return 1
            else:
                return 2
    
    # Opponent projectile management
    if opp_projectile_cooldown <= 0 and distance > medium_range:
        # Close distance quickly before they can projectile
        if relative_pos > 0:
            return 2
        else:
            return 1
    
    # Pressure maintenance - don't let opponent breathe
    if distance < pressure_distance:
        pressure_action = random.random()
        if pressure_action < 0.35:
            return 4  # Quick punch
        elif pressure_action < 0.65:
            return 5  # Strong kick
        elif pressure_action < 0.8:
            # Reposition for continued pressure
            if relative_pos > 0:
                return 2
            else:
                return