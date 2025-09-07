"""
Evolutionary Agent: gen2_agent_003
==================================

Metadata:
{
  "generation": 2,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 8dae8a57f70fbbec
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
    critical_range = 0.08
    
    # Evolved balanced fighter parameters
    base_aggression = 0.68
    adaptation_speed = 0.85
    zone_preference = 0.75
    counter_focus = 0.8
    
    # Advanced positioning awareness
    stage_position = my_x_pos
    corner_danger = 0.0
    if stage_position < 0.2 or stage_position > 0.8:
        corner_danger = 0.7
    elif stage_position < 0.35 or stage_position > 0.65:
        corner_danger = 0.3
    
    # Dynamic stance system - more sophisticated than parent
    current_stance = "balanced"
    urgency_level = 0.0
    
    # Multi-factor stance determination
    health_factor = health_advantage
    stamina_factor = (my_stamina - 0.5) * 2.0
    distance_factor = 1.0 - distance
    pressure_factor = 1.0 if opp_is_attacking else 0.5
    
    stance_score = (health_factor * 0.4 + 
                   stamina_factor * 0.2 + 
                   distance_factor * 0.2 + 
                   corner_danger * -0.3)
    
    if stance_score > 0.5:
        current_stance = "aggressive"
        aggression_modifier = 1.4
    elif stance_score > 0.1:
        current_stance = "pressure"
        aggression_modifier = 1.15
    elif stance_score > -0.2:
        current_stance = "balanced"
        aggression_modifier = 1.0
    elif stance_score > -0.5:
        current_stance = "defensive"
        aggression_modifier = 0.75
    else:
        current_stance = "survival"
        aggression_modifier = 0.4
        urgency_level = 0.8
    
    final_aggression = min(1.0, base_aggression * aggression_modifier)
    
    # Advanced opponent analysis
    opp_momentum = abs(opp_velocity_x) + abs(opp_velocity_y)
    opp_vulnerability = 0.0
    
    if opp_attack_cooldown > 0:
        opp_vulnerability += 0.4
    if opp_block_cooldown > 0:
        opp_vulnerability += 0.3
    if opp_stamina < 0.3:
        opp_vulnerability += 0.3
    if opp_is_attacking and distance < close_range:
        opp_vulnerability += 0.2  # Counter opportunity
    
    # Improved pattern prediction
    opp_behavior = "neutral"
    if opp_velocity_x > 0.15:
        opp_behavior = "rushing"
    elif opp_velocity_x < -0.15:
        opp_behavior = "retreating"
    elif opp_is_blocking and distance < medium_range:
        opp_behavior = "turtling"
    elif opp_is_attacking:
        opp_behavior = "aggressive"
    elif distance > far_range and opp_projectile_cooldown <= 0:
        opp_behavior = "zoning"
    
    # Emergency survival protocols
    if my_health < 0.2 and health_advantage < -0.5:
        urgency_level = 1.0
        
        if distance < critical_range and opp_is_attacking:
            return 6  # Block desperately
        elif corner_danger > 0.5:
            # Escape corner
            if stage_position < 0.5:
                return 8 if opp_is_attacking else 2
            else:
                return 7 if opp_is_attacking else 1
        elif distance > medium_range and my_projectile_cooldown <= 0:
            return 9  # Projectile from safety
        elif distance > close_range:
            # Maintain distance
            if relative_pos > 0:
                return 8
            else:
                return 7
    
    # Critical range combat - new ultra-close tactics
    if distance <= critical_range:
        if current_stance == "survival":
            if opp_is_attacking:
                return 6
            else:
                return 4  # Quick escape jab
        
        elif urgency_level > 0.5:
            # Desperate close combat
            if opp_vulnerability > 0.3:
                return 5  # Power attack
            else:
                return 6  # Block and reset
        
        else:
            # Aggressive clinch work
            clinch_action = random.random()
            if opp_is_blocking:
                return 5  # Break guard with kick
            elif clinch_action < 0.4:
                return 4  # Quick punch
            elif clinch_action < 0.7:
                return 5  # Power kick
            else:
                # Create angle
                return 2 if relative_pos < 0 else 1
    
    # Close range combat - refined from parent
    elif distance <= close_range:
        threat_assessment = 0.3
        if opp_is_attacking:
            threat_assessment = 0.8
        elif opp_vulnerability > 0.4:
            threat_assessment = 0.1
        
        if current_stance == "aggressive":
            if opp_is_blocking:
                return 5  # Power through
            elif opp_vulnerability > 0.3:
                return 5