"""
Evolutionary Agent: gen1_agent_007
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: a6c01063df2d2bff
Serialization Version: 1.0
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
    opp_velocity_x = float(state[13])
    opp_is_attacking = bool(state[16])
    opp_is_blocking = bool(state[17])
    opp_projectile_cooldown = max(0.0, float(state[20]))
    
    # Tactical range definitions
    close_range = 0.13
    medium_range = 0.26
    far_range = 0.42
    
    # Hybrid balance parameters
    aggression_base = 0.6
    defensive_threshold = 0.4
    patience_factor = 0.3
    adaptability_bonus = 0.2
    
    # Dynamic style adaptation based on game state
    if health_advantage > 0.3:
        # Winning - lean slightly aggressive
        current_aggression = min(0.8, aggression_base + 0.2)
        defensive_priority = 0.2
    elif health_advantage > -0.1:
        # Even match - pure hybrid
        current_aggression = aggression_base
        defensive_priority = defensive_threshold
    elif health_advantage > -0.4:
        # Slightly losing - more defensive
        current_aggression = max(0.3, aggression_base - 0.2)
        defensive_priority = 0.6
    else:
        # Losing badly - heavily defensive with calculated risks
        current_aggression = max(0.2, aggression_base - 0.3)
        defensive_priority = 0.7
    
    # Crisis management - override normal behavior
    if my_health < 0.15 and health_advantage < -0.5:
        # Desperate situation
        if distance < close_range and opp_is_attacking:
            return 6  # Emergency block
        elif distance > medium_range and my_projectile_cooldown <= 0:
            return 9  # Desperate projectile
        else:
            # Create space while blocking
            if relative_pos > 0:
                return 7  # Move left blocking
            else:
                return 8  # Move right blocking
    
    # Opportunity recognition - counter-attack timing
    if opp_is_attacking and distance < close_range:
        counter_decision = random.random()
        if counter_decision < defensive_priority:
            return 6  # Block and absorb
        elif counter_decision < defensive_priority + 0.3:
            # Quick counter
            return 4  # Fast punch
        else:
            # Power counter
            return 5  # Strong kick
    
    # Stamina management affects decision making
    stamina_modifier = 1.0
    if my_stamina < 0.4:
        stamina_modifier = 0.7  # Reduced aggression when tired
        if distance < close_range and opp_is_attacking:
            return 6  # Block to recover
    elif my_stamina > 0.8:
        stamina_modifier = 1.2  # Boost aggression with high stamina
    
    adjusted_aggression = current_aggression * stamina_modifier
    
    # Close range hybrid tactics
    if distance <= close_range:
        close_decision = random.random()
        
        if opp_is_blocking:
            # Guard breaking tactics
            if close_decision < 0.5:
                return 5  # Kick to break guard
            elif close_decision < 0.7:
                # Reposition for better angle
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
            else:
                return 6  # Wait and block
        
        elif close_decision < adjusted_aggression * 0.6:
            # Primary attack choice
            attack_mix = random.random()
            if attack_mix < 0.5:
                return 4  # Quick punch
            else:
                return 5  # Strong kick
        
        elif close_decision < adjusted_aggression:
            # Secondary attack with movement
            if abs(my_velocity_x) < 0.2:  # Not moving much
                movement_attack = random.random()
                if movement_attack < 0.5:
                    return 1 if relative_pos < 0 else 2  # Move toward opponent
                else:
                    return 4  # Quick punch
            else:
                return 5  # Kick while moving
        
        else:
            # Defensive choice in close range
            return 6  # Block
    
    # Medium range hybrid positioning
    elif distance <= medium_range:
        medium_decision = random.random()
        
        # Check opponent's intentions
        if abs(opp_velocity_x) > 0.3:
            # Opponent moving fast - prepare defensively
            if medium_decision < 0.6:
                return 6  # Block incoming rush
            else:
                # Counter-movement
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        
        elif opp_is_attacking:
            # Opponent preparing attack - stay safe
            safety_choice = random.random()
            if safety_choice < 0.4:
                return 6  # Block
            elif safety_choice < 0.7:
                # Backing away with guard
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
            else:
                return 3  # Jump to avoid
        
        else:
            # Safe to position
            if medium_decision < adjusted_aggression * 0.7:
                # Aggressive positioning
                approach_style = random.random()
                if approach_style < 0.4:
                    # Direct approach
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                elif approach_style < 0.8:
                    # Attack while closing
                    return 4  # Punch to close gap
                else:
                    return 3  # Jump approach
            
            else:
                # Cautious positioning
                if relative_pos > 0:
                    return 7  # Move left with guard
                else:
                    return 8  # Move right with guard
    
    # Far range hybrid strategy
    elif distance <= far_range:
        far_decision = random.random()
        
        # Projectile consideration
        if my_projectile_cooldown <= 0:
            projectile_chance = 0.4 + (0.3 * (1.0 - adjusted_aggression))
            
            if far_decision < projectile_chance:
                return 9  # Use projectile