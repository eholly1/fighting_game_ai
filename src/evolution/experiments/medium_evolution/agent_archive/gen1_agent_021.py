"""
Evolutionary Agent: gen1_agent_021
==================================

Metadata:
{
  "generation": 1,
  "fitness": 37.99999999999843,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: 792f28f436c8c8cf
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
    
    # Extract fighter status information with bounds checking
    my_health = max(0.0, min(1.0, state[1])) if len(state) > 1 else 1.0
    my_pos_x = max(0.0, min(1.0, state[2])) if len(state) > 2 else 0.5
    my_velocity_x = max(-1.0, min(1.0, state[4])) if len(state) > 4 else 0.0
    my_attack_status = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0.0
    my_block_status = max(0.0, min(1.0, state[8])) if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opponent_velocity_x = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Enhanced rushdown tactical parameters
    point_blank_range = 0.05
    ultra_close_range = 0.1
    close_range = 0.18
    medium_range = 0.32
    far_range = 0.5
    
    # Advanced aggression system
    base_aggression = 0.85
    health_ratio = my_health / max(0.1, opponent_health)
    
    # Calculate dynamic aggression based on multiple factors
    if health_advantage > 0.4:
        current_aggression = 0.95
    elif health_advantage > 0.1:
        current_aggression = 0.9
    elif health_advantage > -0.2:
        current_aggression = base_aggression
    elif health_advantage > -0.5:
        current_aggression = 0.7
    else:
        current_aggression = 0.55
    
    # Momentum factor - increase aggression when opponent is retreating
    momentum_bonus = 0.0
    if relative_pos > 0 and opponent_velocity_x < -0.2:
        momentum_bonus = 0.15
    elif relative_pos < 0 and opponent_velocity_x > 0.2:
        momentum_bonus = 0.15
    
    current_aggression = min(1.0, current_aggression + momentum_bonus)
    
    # Critical health emergency responses
    if my_health < 0.15 and health_advantage < -0.5:
        if opponent_attack_status > 0.6:
            return 6  # Desperate block
        if distance > medium_range and my_projectile_cooldown < 0.2:
            return 9  # Last resort projectile
        if distance < close_range and opponent_block_status < 0.3:
            # Desperation attack when opponent not blocking
            return 4 if random.random() < 0.7 else 5
        # Defensive movement with blocking
        if relative_pos > 0:
            return 7
        else:
            return 8
    
    # Analyze opponent patterns for counter-strategies
    opponent_defensive = opponent_block_status > 0.5
    opponent_aggressive = opponent_attack_status > 0.5
    opponent_passive = opponent_attack_status < 0.2 and opponent_block_status < 0.3
    
    # Point blank range - frame trap and mixup game
    if distance < point_blank_range:
        if opponent_attack_status > 0.8:
            # Opponent attacking, counter or block based on health
            if health_advantage < -0.3:
                return 6  # Block when behind
            else:
                # Counter attack with fast option
                return 4
        
        elif opponent_block_status > 0.7:
            # Heavy guard crushing
            mixup_roll = random.random()
            if mixup_roll < 0.2:
                return 9 if my_projectile_cooldown < 0.4 else 5  # Throw attempt or strong attack
            elif mixup_roll < 0.4:
                return 3  # Jump for overhead
            elif mixup_roll < 0.7:
                return 5  # Strong kick to break guard
            else:
                return 4  # Fast punch for frame trap
        
        else:
            # Opponent vulnerable - maximum pressure
            pressure_roll = random.random()
            if pressure_roll < 0.4:
                return 4  # Fast punch
            elif pressure_roll < 0.7:
                return 5  # Strong kick
            else:
                # Maintain pressure with slight repositioning
                if my_pos_x < 0.2 or my_pos_x > 0.8:
                    # Near wall, jump or attack
                    return 3 if random.random() < 0.3 else 4
                else:
                    return 4
    
    # Ultra close range - pressure maintenance
    elif distance < ultra_close_range:
        if opponent_aggressive:
            # Opponent is attacking, smart defense
            defense_roll = random.random()
            if health_advantage < -0.2:
                if defense_roll < 0.7:
                    return 6  # Block more when losing
                else:
                    return 4  # Quick counter
            else:
                if defense_roll < 0.4:
                    return 6  # Some blocking
                else:
                    return 4  # More counters when winning
        
        elif opponent_defensive:
            # Break guard with varied approaches
            guard_break_roll = random.random()
            if guard_break_roll < 0.15:
                return 9 if my_projectile_cooldown < 0.3 else 5
            elif guard_break_roll < 0.35:
                return 3  # Overhead jump
            elif guard_break_roll < 0.6:
                return 5  # Strong kick
            elif guard_break_roll < 0.8:
                return 4  # Fast punch for frame advantage
            else:
                # Slight repositioning while maintaining pressure
                return 1 if relative_pos > 0 else 2
        
        else:
            # Continue rushdown pressure
            attack_choice = random.random()
            aggression_modifier = current_aggression - 0.5
            
            if attack_choice < 0.5 + aggression_modifier * 0.3:
                return 4  # Favor punches for speed
            elif attack_choice < 0.8 + aggression_modifier * 0.2:
                return 5  # Strong kicks
            else:
                return 3  # Occasional jump for