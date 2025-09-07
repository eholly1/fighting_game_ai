"""
Evolutionary Agent: gen1_agent_008
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 1dbc6c8f7caa451b
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
    my_y_pos = float(state[3])
    my_velocity_y = float(state[4])
    my_is_attacking = bool(state[5])
    my_is_blocking = bool(state[6])
    my_attack_cooldown = max(0.0, float(state[7]))
    my_block_cooldown = max(0.0, float(state[8]))
    my_projectile_cooldown = max(0.0, float(state[9]))
    my_stamina = max(0.0, float(state[10]))
    
    # Opponent status (indices 11-21)
    opp_health = max(0.0, float(state[12]))
    opp_x_pos = float(state[11])
    opp_velocity_x = float(state[13])
    opp_y_pos = float(state[14])
    opp_velocity_y = float(state[15])
    opp_is_attacking = bool(state[16])
    opp_is_blocking = bool(state[17])
    opp_attack_cooldown = max(0.0, float(state[18]))
    opp_block_cooldown = max(0.0, float(state[19]))
    opp_projectile_cooldown = max(0.0, float(state[20]))
    opp_stamina = max(0.0, float(state[21]))
    
    # Enhanced tactical range definitions
    close_range = 0.13
    medium_range = 0.25
    far_range = 0.42
    
    # Hybrid style parameters - balanced approach
    base_aggression = 0.65  # More balanced than pure aggressive
    defensive_threshold = 0.4
    zone_control_preference = 0.7
    adaptation_factor = 0.8
    
    # Dynamic fighting stance based on situation
    current_stance = "neutral"
    
    # Health-based strategy adjustment
    if health_advantage > 0.3:
        current_stance = "aggressive"
        aggression_modifier = 1.3
    elif health_advantage > 0.0:
        current_stance = "pressure"
        aggression_modifier = 1.1
    elif health_advantage > -0.3:
        current_stance = "defensive"
        aggression_modifier = 0.7
    else:
        current_stance = "survival"
        aggression_modifier = 0.5
    
    final_aggression = min(1.0, base_aggression * aggression_modifier)
    
    # Stamina-based adjustments
    stamina_factor = 1.0
    if my_stamina < 0.3:
        stamina_factor = 0.6
        current_stance = "conservative"
    elif my_stamina > 0.8:
        stamina_factor = 1.2
    
    # Opponent pattern recognition
    opp_vulnerability_window = (opp_attack_cooldown > 0 or 
                               opp_block_cooldown > 0 or 
                               opp_stamina < 0.4)
    
    # Critical emergency situations
    if my_health < 0.15 and health_advantage < -0.6:
        if distance < close_range and opp_is_attacking:
            return 6  # Desperate block
        elif distance > far_range and my_projectile_cooldown <= 0:
            return 9  # Last chance projectile
        elif distance > medium_range:
            # Try to create space
            if relative_pos > 0:
                return 8  # Move right while blocking
            else:
                return 7  # Move left while blocking
    
    # Opponent prediction and counter-strategy
    predicted_opp_action = "unknown"
    if opp_velocity_x > 0.1:
        predicted_opp_action = "advancing"
    elif opp_velocity_x < -0.1:
        predicted_opp_action = "retreating"
    elif opp_is_blocking:
        predicted_opp_action = "defensive"
    elif opp_is_attacking:
        predicted_opp_action = "attacking"
    
    # Counter-attack opportunities
    if opp_is_attacking and distance < close_range:
        counter_chance = 0.4 if current_stance == "aggressive" else 0.6
        if random.random() < counter_chance:
            return 6  # Block then counter
        else:
            # Trade blows - favor stronger attack
            return 5 if random.random() < 0.8 else 4
    
    # Close range combat - hybrid approach
    if distance <= close_range:
        if current_stance == "survival":
            if opp_is_attacking:
                return 6  # Block everything when desperate
            else:
                return 4  # Quick jabs only
        
        elif current_stance == "aggressive":
            # Relentless pressure
            if opp_is_blocking:
                return 5  # Kick to break guard
            else:
                attack_roll = random.random()
                if attack_roll < 0.5:
                    return 4  # Fast punch
                elif attack_roll < 0.8:
                    return 5  # Power kick
                else:
                    # Mix in movement for angles
                    return 2 if relative_pos > 0 else 1
        
        else:  # Balanced/defensive/pressure stance
            threat_level = 0.3 if opp_is_attacking else 0.6
            
            if random.random() < threat_level:
                # Defensive action
                if opp_is_attacking:
                    return 6
                else:
                    # Safe positioning
                    if abs(relative_pos) < 0.2:
                        return 2 if random.random() < 0.5 else 1
                    else:
                        return 4  # Quick jab
            else:
                # Offensive action
                if opp_is_blocking:
                    return 5  # Break guard
                elif opp_vulnerability_window:
                    return 5  # Punish vulnerability
                else:
                    return 4 if random.random() < 0.7 else 5
    
    # Medium range - zone control focus
    elif distance <= medium_range:
        if current_stance == "survival":
            # Maintain distance
            if predicted_opp_action == "advancing":
                if relative_pos > 0:
                    return 8  # Block while moving right
                else:
                    return 7  # Block while moving left
            else:
                return 9 if my_projectile_cooldown <= 0 else 6
        
        elif current_stance == "aggressive":
            # Close distance rapidly
            if relative_pos > 0.1:
                return 2  # Chase right
            elif relative_pos < -0.1:
                return 1  # Chase left
            else:
                # In range for attack
                return 5 if random.random() < 0.6 else 4
        
        else:  # Balanced approach
            zone_control_roll = random.random()