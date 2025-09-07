"""
Hall of Fame Agent
==================

Agent ID: gen2_agent_006
Rank: 86/100
Generation: 2
Fighting Style: evolved

Performance Metrics:
- Fitness: 168.65
- Win Rate: 50.0%
- Average Reward: 240.93

Created: 2025-06-01 02:16:30
Lineage: Original

Tournament Stats:
None
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
    
    # Extract detailed fighter status
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_velocity = state[3]
    opponent_velocity = state[14]
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    projectile_cooldown = max(0.0, state[9])
    opponent_projectile_cooldown = max(0.0, state[20])
    height_difference = state[24]
    
    # Enhanced balanced fighter parameters
    strike_range = 0.12
    close_range = 0.18
    medium_range = 0.35
    long_range = 0.55
    critical_health = 0.20
    dominant_health = 0.30
    winning_threshold = 0.20
    losing_threshold = -0.25
    
    # Dynamic adaptation factors
    momentum = abs(my_velocity) + abs(opponent_velocity)
    randomness = random.random()
    aggression_level = min(1.0, max(0.2, 0.6 + health_advantage * 0.4))
    
    # Emergency survival mode
    if my_health < critical_health or health_advantage < -0.4:
        if distance < close_range:
            if opponent_attack_status > 0.4:
                # Defensive evasion under pressure
                if randomness < 0.3:
                    return 6  # Block
                elif randomness < 0.6:
                    return 3  # Jump away
                else:
                    if relative_pos > 0:
                        return 7  # Move left with block
                    else:
                        return 8  # Move right with block
            else:
                # Quick escape
                if randomness < 0.7:
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 3  # Jump retreat
        elif distance < medium_range and projectile_cooldown < 0.2:
            return 9  # Maintain distance with projectile
        else:
            # Defensive positioning
            if randomness < 0.5:
                return 6  # Block and wait
            else:
                return 0  # Stay ready
    
    # Finishing aggression when dominant
    if health_advantage > winning_threshold and opponent_health < dominant_health:
        if distance < strike_range:
            if opponent_block_status < 0.3:
                # Execute finishing combination
                if randomness < 0.4:
                    return 5  # Power kick
                elif randomness < 0.7:
                    return 4  # Quick punch
                else:
                    # Setup for next strike
                    if relative_pos > 0:
                        return 2  # Position right
                    else:
                        return 1  # Position left
            else:
                # Break guard
                if randomness < 0.4:
                    return 3  # Jump attack
                elif randomness < 0.7:
                    if relative_pos > 0:
                        return 2  # Circle right
                    else:
                        return 1  # Circle left
                else:
                    return 4  # Pressure with punch
        elif distance < medium_range:
            # Aggressive approach
            if opponent_projectile_cooldown > 0.3:
                if relative_pos > 0:
                    return 2  # Close in
                else:
                    return 1  # Close in
            elif projectile_cooldown < 0.15:
                return 9  # Projectile pressure
    
    # Balanced close combat strategy
    if distance < strike_range:
        # Immediate post-attack retreat for hit-and-run
        if my_attack_status > 0.4:
            retreat_method = randomness
            if retreat_method < 0.4:
                if relative_pos > 0:
                    return 1  # Quick left retreat
                else:
                    return 2  # Quick right retreat
            elif retreat_method < 0.7:
                return 3  # Jump retreat
            else:
                if relative_pos > 0:
                    return 7  # Protected left retreat
                else:
                    return 8  # Protected right retreat
        
        # Counter opponent blocking
        if opponent_block_status > 0.5:
            counter_block = randomness
            if counter_block < 0.3:
                return 3  # Jump over guard
            elif counter_block < 0.6:
                if relative_pos > 0:
                    return 2  # Reposition right
                else:
                    return 1  # Reposition left
            elif counter_block < 0.8:
                return 5  # Power kick to break
            else:
                return 6  # Wait for opening
        
        # Respond to opponent attacks
        if opponent_attack_status > 0.5:
            counter_response = randomness
            if health_advantage > 0 and counter_response < 0.3:
                return 4  # Counter punch
            elif counter_response < 0.5:
                return 6  # Block counter
            elif counter_response < 0.7:
                return 3  # Jump counter
            else:
                if relative_pos > 0:
                    return 7  # Retreat with block
                else:
                    return 8  # Retreat with block
        
        # Clean striking opportunity
        strike_choice = randomness * aggression_level
        if strike_choice < 0.25:
            return 4  # Fast punch
        elif strike_choice < 0.45:
            return 5  # Power kick
        elif strike_choice < 0.65:
            # Feint and reposition
            if relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
        elif strike_choice < 0.8:
            return 3  # Jump attack
        else:
            return 6  # Block and counter setup
    
    elif distance < close_range:
        # Close range tactical zone
        threat_level = opponent_attack_status + max(0, 1.0 - opponent_projectile_cooldown)
        
        # High threat response
        if threat_level > 0.7:
            defensive_action = randomness
            if defensive_action < 0.4:
                return 6  # Block threat
            elif defensive_action < 0.7:
                if relative_pos > 0:
                    return 7  # Move left with block
                else:
                    return 8  # Move right with block
            else:
                return 3  # Jump over threat
        
        # Balanced positioning based on health
        if health_advantage > 0:
            # Winning - controlled aggression
            if randomness < aggression_level * 0.6:
                if relative_pos > 0:
                    return 2  # Move in right
                else:
                    return 1  # Move in left
            elif randomness < 0.8:
                if projectile_cooldown < 0.2:
                    return 9  # Projectile pressure
                else:
                    return 0  # Wait for opportunity
            else:
                return 3  # Jump approach
        else:
            # Losing - cautious positioning
            if randomness < 0.4:
                if relative_pos > 0:
                    return 1  # Move left away