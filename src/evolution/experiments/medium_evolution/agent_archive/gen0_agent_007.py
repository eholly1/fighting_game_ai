"""
Evolutionary Agent: gen0_agent_007
==================================

Metadata:
{
  "generation": 0,
  "fitness": 237.43999999999104,
  "fighting_style": "hit_and_run",
  "win_rate": 0.0
}

Code Hash: 828eceb62132a815
Serialization Version: 1.0
"""

# Agent Code:
import numpy as np
import random
import math

def get_action(state):
    # Validate and extract key state information
    if len(state) < 26:
        return 0  # Safety fallback
    
    # Core strategic metrics
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # My fighter status
    my_health = state[1] if len(state) > 1 else 1.0
    my_velocity_x = state[3] if len(state) > 3 else 0.0
    my_velocity_y = state[4] if len(state) > 4 else 0.0
    my_attack_status = state[5] if len(state) > 5 else 0.0
    my_block_status = state[6] if len(state) > 6 else 0.0
    my_projectile_cooldown = state[10] if len(state) > 10 else 0.0
    
    # Opponent status
    opp_health = state[12] if len(state) > 12 else 1.0
    opp_velocity_x = state[14] if len(state) > 14 else 0.0
    opp_velocity_y = state[15] if len(state) > 15 else 0.0
    opp_attack_status = state[16] if len(state) > 16 else 0.0
    opp_block_status = state[17] if len(state) > 17 else 0.0
    
    # Hit and run tactical ranges
    close_range = 0.12
    strike_range = 0.18
    medium_range = 0.35
    far_range = 0.5
    
    # Hit and run aggression parameters
    base_aggression = 0.4
    winning_bonus = max(0.0, health_advantage * 0.3)
    losing_penalty = max(0.0, -health_advantage * 0.4)
    current_aggression = base_aggression + winning_bonus - losing_penalty
    
    # Emergency defensive behavior when health is critical
    if my_health < 0.25 and health_advantage < -0.4:
        if distance < 0.2:
            # Too close when critical - block and retreat
            if relative_pos > 0:
                return 7  # Block and move left
            else:
                return 8  # Block and move right
        elif distance < 0.4:
            # Create distance for projectiles
            if relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away
        else:
            # Safe projectile distance
            if my_projectile_cooldown < 0.1:
                return 9  # Projectile
            else:
                return 6  # Block while waiting
    
    # Opponent is attacking - hit and run counter tactics
    if opp_attack_status > 0.1:
        if distance < 0.15:
            # Very close to attacking opponent - immediate evasion
            if random.random() < 0.3:
                return 6  # Quick block
            elif relative_pos > 0:
                return 1  # Move left away
            else:
                return 2  # Move right away
        elif distance < 0.25:
            # Medium close - prepare counter or retreat
            if health_advantage > 0.2 and random.random() < 0.4:
                # Counter attack opportunity
                return 4 if random.random() < 0.7 else 5
            else:
                # Retreat and prepare projectile
                if relative_pos > 0:
                    return 1
                else:
                    return 2
        else:
            # Safe distance - projectile harassment
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                return 0  # Wait for cooldown
    
    # Opponent is blocking - hit and run positioning
    if opp_block_status > 0.1:
        if distance < 0.2:
            # Too close to blocker - create space
            if relative_pos > 0:
                return 1  # Move away left
            else:
                return 2  # Move away right
        elif distance < 0.4:
            # Good range for movement and positioning
            if abs(my_velocity_x) < 0.1:
                # Static - start movement
                if random.random() < 0.5:
                    return 1
                else:
                    return 2
            else:
                # Moving - prepare projectile
                if my_projectile_cooldown < 0.1:
                    return 9
                else:
                    return 0
        else:
            # Far range - projectile pressure
            if my_projectile_cooldown < 0.1:
                return 9
            else:
                # Close distance while waiting
                if relative_pos > 0:
                    return 2  # Move right toward
                else:
                    return 1  # Move left toward
    
    # Core hit and run range-based tactics
    if distance < close_range:
        # Danger zone - immediate hit and run
        strike_chance = current_aggression * 0.6
        
        if health_advantage > 0.3:
            # Winning - more aggressive strikes
            strike_chance += 0.2
        elif health_advantage < -0.2:
            # Losing - prioritize escape
            strike_chance -= 0.3
        
        if random.random() < strike_chance:
            # Quick strike decision
            if opp_health < 0.3:
                # Opponent low health - stronger attack
                return 5  # Kick for finish
            else:
                # Standard quick punch
                return 4
        else:
            # Retreat decision
            retreat_urgency = 0.7 + max(0.0, -health_advantage * 0.3)
            if random.random() < retreat_urgency:
                if relative_pos > 0:
                    return 1  # Move left away
                else:
                    return 2  # Move right away
            else:
                return 6  # Block while planning
    
    elif distance < strike_range:
        # Optimal hit and run engagement range
        engage_chance = current_aggression * 0.8
        
        # Adjust for opponent movement
        if abs(opp_velocity_x) > 0.1:
            # Opponent moving - harder to hit
            engage_chance -= 0.2
        
        # Height advantage consideration
        if abs(height_diff) > 0.1:
            if height_diff > 0:
                # I'm higher - slight advantage
                engage_chance += 0.1
            else:
                # I'm lower - slight disadvantage
                engage_chance -= 0.1
        
        if random.random() < engage_chance:
            # Engage with quick strike
            if distance < 0.15:
                # Close enough for melee
                if random.random() < 0.75:
                    return 4  # Quick punch
                else:
                    return 5  # Occasional kick
            else:
                # Move in for strike
                if relative_pos > 0:
                    return 2  # Move right toward
                else:
                    return 1  # Move left toward
        else:
            # Don't engage - maintain distance
            if my_projectile_cooldown < 0.1 and distance > 0.2:
                return 9  # Projectile
            else:
                # Lateral movement
                if abs(my_velocity_x) < 0.05:
                    if random.random() < 0.5:
                        return 1
                    else:
                        return