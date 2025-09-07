"""
Evolutionary Agent: gen1_agent_028
==================================

Metadata:
{
  "generation": 1,
  "fitness": 250.15999999999153,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: dac60de293d071cf
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
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity = state[3]
    opponent_velocity = state[14]
    my_attacking = state[6] > 0.5
    opponent_attacking = state[17] > 0.5
    my_blocking = state[7] > 0.5
    opponent_blocking = state[18] > 0.5
    my_projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = state[21]
    height_diff = state[24]
    
    # Enhanced tactical parameters for hybrid style
    close_range = 0.13
    medium_range = 0.32
    safe_range = 0.48
    critical_health = 0.18
    danger_health = 0.35
    winning_threshold = 0.25
    dominant_threshold = 0.5
    
    # Adaptive aggression based on game state
    base_aggression = 0.5
    if health_advantage > winning_threshold:
        aggression_modifier = 0.3
    elif health_advantage < -winning_threshold:
        aggression_modifier = -0.4
    else:
        aggression_modifier = 0.0
    
    current_aggression = base_aggression + aggression_modifier
    
    # Emergency survival protocol
    if my_health < critical_health:
        if opponent_attacking and distance < medium_range:
            return 6  # Block immediate threats
        elif distance < safe_range:
            # Defensive retreat with blocking
            if relative_pos > 0:
                return 7  # Move left with block
            else:
                return 8  # Move right with block
        elif my_projectile_cooldown < 0.2:
            return 9  # Safe projectile harassment
        else:
            return 6  # Block and recover
    
    # Dominant finishing mode
    if health_advantage > dominant_threshold and opponent_health < 0.25:
        if distance < close_range:
            if opponent_blocking:
                # Mix up attacks against blocking opponent
                if random.random() < 0.4:
                    return 5  # Kick to break guard
                else:
                    # Create space then re-engage
                    if relative_pos > 0:
                        return 1  # Step back left
                    else:
                        return 2  # Step back right
            else:
                # Aggressive finishing sequence
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Quick punch
                elif attack_choice < 0.8:
                    return 5  # Power kick
                else:
                    return 6  # Stay ready for counter
        elif distance < medium_range:
            # Pressure opponent into corner
            if relative_pos > 0:
                return 2  # Move right to close
            else:
                return 1  # Move left to close
        else:
            # Long range pressure with projectiles
            if my_projectile_cooldown < 0.3:
                return 9
            else:
                # Close distance while cooldown recovers
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Close range hybrid tactics
    if distance < close_range:
        # React to opponent's defensive state
        if opponent_blocking:
            blocking_duration = random.random()
            if blocking_duration < 0.3:
                # Quick retreat to reset
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
            elif blocking_duration < 0.6:
                # Guard break attempt with kick
                return 5
            else:
                # Wait for opening
                return 6
        
        # Opponent not blocking - attack opportunity assessment
        if opponent_attacking:
            # Counter-attack timing
            if current_aggression > 0.6:
                # Trade hits aggressively
                return 4 if random.random() < 0.7 else 5
            else:
                # Defensive response
                return 6
        
        # Clean attack opportunity
        if not my_attacking:
            attack_pattern = random.random()
            if attack_pattern < current_aggression * 0.6:
                return 4  # Fast punch
            elif attack_pattern < current_aggression * 0.9:
                return 5  # Stronger kick
            else:
                # Defensive patience
                return 6
        
        # Currently attacking - follow through or retreat
        if my_attacking:
            if health_advantage > 0:
                return 0  # Let attack complete
            else:
                # Prepare defensive retreat
                if relative_pos > 0:
                    return 1
                else:
                    return 2
    
    # Medium range hybrid positioning
    elif distance < medium_range:
        # Threat assessment for positioning
        immediate_threat = opponent_attacking or (opponent_projectile_cooldown < 0.2 and distance > 0.2)
        
        if immediate_threat:
            threat_response = random.random()
            if threat_response < 0.4:
                return 6  # Block threat
            elif threat_response < 0.7:
                # Evasive movement with block
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                # Counter-approach
                if relative_pos > 0:
                    return 2  # Move toward opponent
                else:
                    return 1  # Move toward opponent
        
        # Opportunity-based positioning
        opponent_vulnerable = opponent_projectile_cooldown > 0.4 or opponent_attacking
        
        if opponent_vulnerable and current_aggression > 0.4:
            # Aggressive positioning to close distance
            approach_style = random.random()
            if approach_style < 0.6:
                # Direct approach
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                # Cautious approach with guard
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
        
        # Neutral positioning and projectile use
        if my_projectile_cooldown < 0.3:
            projectile_decision = random.random()
            projectile_threshold = 0.5 + (current_aggression - 0.5) * 0.3
            
            if projectile_decision < projectile_threshold:
                return 9
        
        # Movement for better positioning
        positioning_choice = random.random()
        if positioning_choice < 0.25:
            return 1  # Move left
        elif positioning_choice < 0.5:
            return 2  # Move right
        elif positioning_choice < 0.65:
            return 3  # Jump for unpredictability
        elif positioning_choice < 0.85:
            return 6  # Guard up
        else:
            return 0  # Observe
    
    # Long range hybrid strategy
    else:
        # Projectile management at long range
        if my_projectile_cooldown < 0.2:
            projectile_aggression = 0.7 + current_aggression * 0.2
            if random.random() < projectile_aggression:
                return 9
        
        # Distance management based on strategy
        optimal_distance = 0.25