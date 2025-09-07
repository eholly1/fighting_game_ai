"""
Evolutionary Agent: gen0_agent_027
==================================

Metadata:
{
  "generation": 0,
  "fitness": 300.09999999999974,
  "fighting_style": "hit_and_run",
  "win_rate": 0.5
}

Code Hash: bd85a60aca509e32
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
    my_attack_status = state[7]
    opponent_attack_status = state[18]
    my_block_status = state[8]
    opponent_block_status = state[19]
    projectile_cooldown = max(0.0, state[9])
    opponent_projectile_cooldown = max(0.0, state[20])
    height_difference = state[24]
    
    # Define tactical parameters for hit-and-run style
    close_range = 0.12
    medium_range = 0.28
    safe_range = 0.45
    retreat_threshold = 0.18
    health_panic_threshold = -0.4
    winning_threshold = 0.3
    
    # Emergency defensive behavior when health is critical
    if my_health < 0.2 or health_advantage < health_panic_threshold:
        if distance < retreat_threshold:
            # Immediate retreat with blocking
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < safe_range and projectile_cooldown < 0.1:
            return 9  # Projectile to keep opponent away
        else:
            return 6  # Block and wait for opportunity
    
    # Opportunistic behavior when winning significantly
    if health_advantage > winning_threshold and opponent_health < 0.3:
        if distance < close_range:
            # Quick strike then prepare to retreat
            if random.random() < 0.7:
                return 4  # Fast punch
            else:
                return 5  # Stronger kick
        elif distance < medium_range:
            # Move in for finishing blow
            if relative_pos > 0:
                return 2  # Move right toward opponent
            else:
                return 1  # Move left toward opponent
    
    # Hit-and-run core strategy implementation
    if distance < close_range:
        # In close range - strike or retreat decision
        if opponent_block_status > 0.5:
            # Opponent is blocking, retreat immediately
            if relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away
        
        # Opponent not blocking - quick strike opportunity
        if my_attack_status < 0.1:  # Not currently attacking
            strike_choice = random.random()
            if strike_choice < 0.6:
                return 4  # Quick punch for hit-and-run
            elif strike_choice < 0.85:
                return 5  # Kick for more damage
            else:
                # Immediate retreat without striking
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
        else:
            # Currently attacking, prepare retreat
            if relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away
    
    elif distance < retreat_threshold:
        # Just outside close range - critical retreat zone
        retreat_urgency = random.random()
        
        if opponent_attack_status > 0.5:
            # Opponent is attacking, defensive retreat
            if relative_pos > 0:
                return 7  # Move left with block
            else:
                return 8  # Move right with block
        
        if retreat_urgency < 0.7:
            # Standard retreat
            if relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away
        else:
            # Retreat with protection
            if relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
    
    elif distance < medium_range:
        # Medium range - positioning and opportunity assessment
        opponent_vulnerable = opponent_attack_status > 0.5 or opponent_projectile_cooldown > 0.3
        
        if opponent_vulnerable and health_advantage > -0.2:
            # Move in for hit-and-run attack
            approach_method = random.random()
            if approach_method < 0.6:
                # Direct approach
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            else:
                # Cautious approach with blocking
                if relative_pos > 0:
                    return 8  # Move right with block
                else:
                    return 7  # Move left with block
        
        # Maintain distance or use projectile
        if projectile_cooldown < 0.1 and random.random() < 0.4:
            return 9  # Projectile attack
        
        # Lateral movement for positioning
        movement_pattern = random.random()
        if movement_pattern < 0.3:
            return 1  # Move left
        elif movement_pattern < 0.6:
            return 2  # Move right
        else:
            return 0  # Wait and observe
    
    elif distance < safe_range:
        # Preferred hit-and-run range - projectile and positioning
        if projectile_cooldown < 0.1:
            projectile_decision = random.random()
            
            # More aggressive projectile use when winning
            projectile_threshold = 0.7 if health_advantage > 0 else 0.5
            
            if projectile_decision < projectile_threshold:
                return 9  # Projectile attack
        
        # Setup for approach or maintain position
        if opponent_projectile_cooldown > 0.2 and health_advantage > -0.1:
            # Opponent can't counter-projectile, consider approach
            if random.random() < 0.3:
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
        
        # Default positioning behavior
        positioning_choice = random.random()
        if positioning_choice < 0.25:
            return 1  # Move left
        elif positioning_choice < 0.5:
            return 2  # Move right
        elif positioning_choice < 0.65:
            return 3  # Jump for unpredictability
        else:
            return 0  # Idle observation
    
    else:
        # Long range - projectile focused with setup
        if projectile_cooldown < 0.1:
            # High probability projectile use at long range
            if random.random() < 0.8:
                return 9  # Projectile attack
        
        # Close distance gradually for hit-and-run setup
        if opponent_projectile_cooldown > 0.3:
            # Safe to approach
            approach_choice = random.random()
            if approach_choice < 0.4:
                if relative_pos > 0:
                    return 2  # Move right toward opponent
                else:
                    return 1  # Move left toward opponent
            elif approach_choice < 0.6:
                return 3  # Jump approach
        
        # Long range positioning
        long_range_action = random.random()
        if long_range_action < 0.3:
            return 1  # Move left
        elif long_range_action < 0.6:
            return 2  # Move right
        elif long_range_action < 0.75:
            return 3  # Jump
        else:
            return 0  # Wait
    
    # Fallback