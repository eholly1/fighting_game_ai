"""
Evolutionary Agent: gen2_agent_004
==================================

Metadata:
{
  "generation": 2,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 060fb111886b4a75
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
    close_range = 0.12
    medium_range = 0.28
    far_range = 0.45
    max_range = 0.7
    
    # Advanced hybrid parameters - evolution from parents
    base_aggression = 0.62
    tactical_patience = 0.35
    risk_tolerance = 0.4
    adaptability_factor = 0.85
    counter_attack_priority = 0.65
    
    # Dynamic fighting mode calculation
    current_mode = "balanced"
    aggression_modifier = 1.0
    defensive_weight = 0.5
    
    # Health-based strategic adaptation - improved from parents
    if health_advantage > 0.4:
        current_mode = "dominating"
        aggression_modifier = 1.4
        defensive_weight = 0.3
    elif health_advantage > 0.15:
        current_mode = "winning"
        aggression_modifier = 1.2
        defensive_weight = 0.35
    elif health_advantage > -0.05:
        current_mode = "even"
        aggression_modifier = 1.0
        defensive_weight = 0.5
    elif health_advantage > -0.25:
        current_mode = "trailing"
        aggression_modifier = 0.8
        defensive_weight = 0.65
    elif health_advantage > -0.5:
        current_mode = "losing"
        aggression_modifier = 0.6
        defensive_weight = 0.75
    else:
        current_mode = "desperate"
        aggression_modifier = 0.4
        defensive_weight = 0.85
    
    # Calculate final aggression level
    final_aggression = min(0.95, base_aggression * aggression_modifier)
    
    # Advanced stamina management - learned from parent weaknesses
    stamina_impact = 1.0
    if my_stamina < 0.25:
        stamina_impact = 0.6
        current_mode = "conserving"
        defensive_weight += 0.2
    elif my_stamina < 0.5:
        stamina_impact = 0.8
        defensive_weight += 0.1
    elif my_stamina > 0.8:
        stamina_impact = 1.3
        final_aggression = min(0.95, final_aggression * 1.1)
    
    # Opponent analysis and prediction - new evolution feature
    opp_threat_level = 0.5
    opp_vulnerability = 0.5
    
    # Assess opponent threat
    if opp_is_attacking:
        opp_threat_level += 0.3
    if abs(opp_velocity_x) > 0.3:
        opp_threat_level += 0.2
    if opp_stamina > 0.7:
        opp_threat_level += 0.15
    if distance < close_range and opp_projectile_cooldown <= 0:
        opp_threat_level += 0.25
    
    # Assess opponent vulnerability
    if opp_attack_cooldown > 0:
        opp_vulnerability += 0.3
    if opp_block_cooldown > 0:
        opp_vulnerability += 0.2
    if opp_stamina < 0.4:
        opp_vulnerability += 0.25
    if opp_is_blocking and distance < close_range:
        opp_vulnerability += 0.15
    
    opp_threat_level = min(1.0, opp_threat_level)
    opp_vulnerability = min(1.0, opp_vulnerability)
    
    # Crisis override - enhanced emergency response
    if my_health < 0.2 and health_advantage < -0.4:
        if distance < close_range:
            if opp_is_attacking:
                return 6  # Emergency block
            elif opp_vulnerability > 0.6:
                return 5  # Desperate all-in kick
            else:
                # Try to create space
                escape_direction = 1 if relative_pos < 0 else 2
                return escape_direction
        elif distance < medium_range:
            if my_projectile_cooldown <= 0:
                return 9  # Hail mary projectile
            else:
                # Defensive movement
                if relative_pos > 0:
                    return 7  # Move left blocking
                else:
                    return 8  # Move right blocking
        else:
            return 9 if my_projectile_cooldown <= 0 else 6
    
    # Counter-attack timing - improved from parents
    if opp_is_attacking and distance <= close_range:
        counter_decision = random.random()
        counter_threshold = counter_attack_priority * (1.0 - defensive_weight)
        
        if counter_decision < counter_threshold and my_stamina > 0.3:
            # Aggressive counter based on opponent vulnerability
            if opp_vulnerability > 0.6:
                return 5  # Power counter kick
            elif opp_stamina < 0.4:
                return 4  # Quick counter punch
            else:
                return 6  # Safe block counter
        else:
            # Defensive response
            if opp_threat_level > 0.7:
                return 6  # Block high threat
            else:
                return 6 if random.random() < 0.7 else 4  # Mix block with quick counter
    
    # Close range combat - evolved hybrid approach
    if distance <= close_range:
        close_decision = random.random()
        
        if current_mode == "desperate":
            if opp_is_attacking:
                return 6  # Block