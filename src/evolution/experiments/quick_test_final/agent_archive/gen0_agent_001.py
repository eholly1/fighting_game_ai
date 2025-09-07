"""
Evolutionary Agent: gen0_agent_001
==================================

Metadata:
{
  "generation": 0,
  "fitness": 235.0999999999963,
  "fighting_style": "defensive",
  "win_rate": 0.0
}

Code Hash: e7abe02014503753
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Extract and validate core game state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[2]))
    opponent_health = max(0.0, min(1.0, state[13]))
    my_position = state[0]
    opponent_position = state[11]
    
    # Extract attack and defense states
    my_attack_cooldown = max(0.0, state[6])
    my_block_status = state[7]
    opponent_attack_cooldown = max(0.0, state[17])
    opponent_block_status = state[18]
    
    # Projectile information
    my_projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = max(0.0, state[21])
    
    # Define strategic thresholds for defensive play
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    safe_distance = 0.35
    
    # Health-based defensive parameters
    critical_health = 0.3
    low_health = 0.5
    comfortable_health = 0.7
    
    # Defensive strategy: prioritize survival when health is low
    if my_health < critical_health:
        # Critical health - maximum defense
        if distance < close_range:
            # Too close, need to block or escape
            if opponent_attack_cooldown < 0.3:
                return 6  # Block incoming attack
            else:
                # Try to create distance while blocking
                if relative_pos > 0:
                    return 7  # Move left while blocking
                else:
                    return 8  # Move right while blocking
        
        elif distance < medium_range:
            # Medium range - maintain distance
            if my_projectile_cooldown < 0.1:
                return 9  # Safe projectile attack
            else:
                # Create more distance
                if relative_pos > 0:
                    return 1  # Move away (left)
                else:
                    return 2  # Move away (right)
        
        else:
            # Far range - projectile harassment
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile attack
            else:
                return 6  # Block while waiting for cooldown
    
    # Low health - cautious defensive play
    elif my_health < low_health:
        if distance < close_range:
            # Close range - selective engagement
            if opponent_attack_cooldown > 0.5 and my_attack_cooldown < 0.2:
                # Safe counter-attack opportunity
                if random.random() < 0.7:
                    return 4  # Quick punch
                else:
                    return 5  # Stronger kick
            else:
                # Defensive positioning
                if opponent_attack_cooldown < 0.3:
                    return 6  # Block
                else:
                    # Create space while blocking
                    if abs(my_position) > 0.7:  # Near wall
                        if my_position > 0:
                            return 7  # Move left (away from right wall)
                        else:
                            return 8  # Move right (away from left wall)
                    else:
                        if relative_pos > 0:
                            return 7  # Move left while blocking
                        else:
                            return 8  # Move right while blocking
        
        elif distance < medium_range:
            # Medium range - control distance
            if opponent_attack_cooldown > 0.4 and distance > 0.18:
                # Safe approach for quick attack
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                # Maintain safe distance
                if my_projectile_cooldown < 0.2:
                    return 9  # Projectile
                else:
                    if distance < 0.2:
                        # Too close, back up
                        if relative_pos > 0:
                            return 1  # Move left (away)
                        else:
                            return 2  # Move right (away)
                    else:
                        return 6  # Block and assess
        
        else:
            # Far range - projectile game
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile attack
            elif opponent_projectile_cooldown < 0.2:
                return 6  # Block incoming projectile
            else:
                # Maintain distance
                if distance < safe_distance:
                    if relative_pos > 0:
                        return 1  # Move away
                    else:
                        return 2  # Move away
                else:
                    return 0  # Wait for projectile cooldown
    
    # Comfortable health - balanced defensive approach
    elif my_health > comfortable_health or health_advantage > 0.2:
        if distance < close_range:
            # Close range - measured aggression
            if opponent_block_status > 0.5:
                # Opponent is blocking, create space or throw
                if random.random() < 0.4:
                    return 5  # Kick (can break blocks better)
                else:
                    # Create space for projectile
                    if relative_pos > 0:
                        return 1  # Move left
                    else:
                        return 2  # Move right
            
            elif opponent_attack_cooldown < 0.3:
                # Opponent can attack, be defensive
                if random.random() < 0.8:
                    return 6  # Block
                else:
                    # Counter-attack timing
                    return 4  # Quick punch
            
            else:
                # Good opportunity to attack
                attack_choice = random.random()
                if attack_choice < 0.5:
                    return 4  # Punch
                elif attack_choice < 0.8:
                    return 5  # Kick
                else:
                    return 6  # Defensive block
        
        elif distance < medium_range:
            # Medium range - positioning game
            if my_projectile_cooldown < 0.1 and distance > 0.2:
                return 9  # Projectile attack
            
            elif opponent_projectile_cooldown < 0.3:
                # Opponent might shoot, be ready
                if distance < 0.22:
                    # Close enough to pressure
                    if relative_pos > 0:
                        return 2  # Move right toward opponent
                    else:
                        return 1  # Move left toward opponent
                else:
                    return 6  # Block potential projectile
            
            else:
                # Control spacing
                if distance < 0.18:
                    # Too close for comfort
                    if relative_pos > 0:
                        return 1  # Back up left
                    else:
                        return 2  # Back up right
                elif distance > 0.23:
                    # Can close distance safely
                    if relative_pos > 0:
                        return 2  # Move right toward opponent
                    else:
                        return 1  # Move left toward opponent
                else:
                    # Good medium range position
                    if random.random() < 0.3:
                        return 0  # Wait and observe
                    else:
                        return 6  # Ready to block
        
        else:
            # Far range - projectile and positioning
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile attack
            elif opponent_projectile_cooldown < 0.2:
                return 6  # Block incoming