"""
Evolutionary Agent: gen0_agent_002
==================================

Metadata:
{
  "generation": 0,
  "fitness": 0.0,
  "fighting_style": "zoner",
  "win_rate": 0.5
}

Code Hash: 06130438221aef6f
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
    
    # Extract player state information
    my_health = state[1] if len(state) > 1 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_is_blocking = state[6] if len(state) > 6 else 0.0
    my_is_attacking = state[7] if len(state) > 7 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent state information
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_is_attacking = state[18] if len(state) > 18 else 0.0
    opp_is_blocking = state[17] if len(state) > 17 else 0.0
    opp_projectile_cooldown = state[21] if len(state) > 21 else 0.0
    
    # Define strategic ranges and thresholds
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    critical_health = 0.3
    winning_threshold = 0.15
    losing_threshold = -0.2
    
    # Zoner style: prioritize distance control and projectiles
    optimal_distance = 0.35
    retreat_distance = 0.5
    emergency_distance = 0.08
    
    # Emergency defensive measures when in critical danger
    if distance < emergency_distance and opp_is_attacking > 0.5:
        if my_health < critical_health:
            # Desperate escape attempt
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        else:
            return 6  # Block incoming attack
    
    # Critical health management - ultra defensive zoning
    if my_health < critical_health:
        if distance < close_range:
            # Too close, need to escape
            if my_x_pos < 0.2:  # Near left edge
                return 8  # Move right while blocking
            elif my_x_pos > 0.8:  # Near right edge
                return 7  # Move left while blocking
            else:
                # Choose escape direction away from opponent
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        
        elif distance < medium_range:
            # Create more distance
            if relative_pos > 0:
                return 1  # Move left
            else:
                return 2  # Move right
        
        else:
            # Safe distance, use projectiles if available
            if my_projectile_cooldown < 0.3:
                return 9  # Projectile
            else:
                # Maintain distance while cooldown recovers
                if distance < optimal_distance:
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
                else:
                    return 0  # Idle while waiting
    
    # Winning significantly - maintain zoning pressure
    if health_advantage > winning_threshold:
        if distance > far_range:
            # Too far, close in slightly for better projectile accuracy
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
        
        elif distance > medium_range:
            # Perfect zoning range
            if my_projectile_cooldown < 0.2:
                return 9  # Projectile attack
            else:
                # Maintain optimal positioning
                distance_from_optimal = abs(distance - optimal_distance)
                if distance_from_optimal > 0.1:
                    if distance < optimal_distance:
                        # Too close, back up
                        if relative_pos > 0:
                            return 1  # Move left
                        else:
                            return 2  # Move right
                    else:
                        # Too far, close slightly
                        if relative_pos > 0:
                            return 2  # Move right
                        else:
                            return 1  # Move left
                else:
                    return 0  # Hold position
        
        elif distance > close_range:
            # Medium range while winning - control space
            if opp_is_attacking > 0.5:
                return 6  # Block and wait for opening
            elif my_projectile_cooldown < 0.4:
                return 9  # Projectile
            else:
                # Create more distance
                if relative_pos > 0:
                    return 1  # Move left
                else:
                    return 2  # Move right
        
        else:
            # Too close while winning - retreat and zone
            if my_x_pos < 0.15:  # Near left edge
                return 8  # Move right while blocking
            elif my_x_pos > 0.85:  # Near right edge
                return 7  # Move left while blocking
            else:
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
    
    # Losing significantly - need to take calculated risks
    elif health_advantage < losing_threshold:
        if distance > far_range:
            # Long range - projectile duel
            if my_projectile_cooldown < opp_projectile_cooldown:
                return 9  # Projectile when we have advantage
            else:
                # Close distance to force different engagement
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        elif distance > medium_range:
            # Medium range while losing - mix up strategy
            if random.random() < 0.4:  # 40% chance to be aggressive
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                if my_projectile_cooldown < 0.3:
                    return 9  # Projectile
                else:
                    # Maintain current distance
                    return 0
        
        elif distance > close_range:
            # Close-medium range while losing
            if opp_is_attacking > 0.5:
                return 6  # Block
            elif random.random() < 0.6:  # 60% chance to attack
                if random.random() < 0.7:
                    return 4  # Punch (faster)
                else:
                    return 5  # Kick (stronger)
            else:
                if my_projectile_cooldown < 0.5:
                    return 9  # Projectile
                else:
                    return 0  # Wait
        
        else:
            # Very close while losing - must fight
            if opp_is_attacking > 0.5:
                if random.random() < 0.8:
                    return 6  # Block most of the time
                else:
                    return 4  # Counter punch
            else:
                # Attack while we have the chance
                if random.random() < 0.4:
                    return 4  # Punch
                elif random.random() < 0.7:
                    return 5