"""
Evolutionary Agent: gen2_agent_010
==================================

Metadata:
{
  "generation": 2,
  "fitness": 254.4999999999925,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 720215df5c70cf48
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
    my_velocity_y = max(-1.0, min(1.0, state[5])) if len(state) > 5 else 0.0
    my_attack_status = max(0.0, min(1.0, state[7])) if len(state) > 7 else 0.0
    my_block_status = max(0.0, min(1.0, state[8])) if len(state) > 8 else 0.0
    my_projectile_cooldown = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opponent_velocity_x = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opponent_velocity_y = max(-1.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Define hybrid tactical ranges
    ultra_close_range = 0.05
    very_close_range = 0.12
    close_range = 0.18
    medium_range = 0.35
    far_range = 0.55
    
    # Calculate situational awareness factors
    wall_proximity = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_proximity = min(opponent_pos_x, 1.0 - opponent_pos_x)
    corner_pressure = wall_proximity < 0.15
    opponent_cornered = opponent_wall_proximity < 0.15
    
    # Analyze opponent patterns
    opponent_aggressive = opponent_attack_status > 0.4 or abs(opponent_velocity_x) > 0.2
    opponent_defensive = opponent_block_status > 0.5
    opponent_mobile = abs(opponent_velocity_x) > 0.1
    opponent_projectile_ready = opponent_projectile_cooldown < 0.2
    my_projectile_ready = my_projectile_cooldown < 0.2
    
    # Calculate adaptive aggression based on multiple factors
    base_aggression = 0.6  # Hybrid balance
    aggression_modifier = 0.0
    
    # Health-based aggression adjustment
    if health_advantage > 0.4:
        aggression_modifier += 0.25
    elif health_advantage < -0.4:
        aggression_modifier -= 0.3
    
    # Position-based adjustment
    if opponent_cornered and not corner_pressure:
        aggression_modifier += 0.2
    elif corner_pressure and not opponent_cornered:
        aggression_modifier -= 0.15
    
    # Opponent behavior adjustment
    if opponent_defensive and not opponent_mobile:
        aggression_modifier += 0.15  # Pressure turtling opponent
    elif opponent_aggressive and my_health < opponent_health:
        aggression_modifier -= 0.2  # Be cautious against aggressive opponent when losing
    
    current_aggression = max(0.2, min(0.9, base_aggression + aggression_modifier))
    
    # Emergency survival protocols
    if my_health < 0.15 and health_advantage < -0.6:
        # Critical health - prioritize survival
        if opponent_attack_status > 0.6:
            return 6  # Block immediate danger
        elif distance > medium_range and my_projectile_ready:
            return 9  # Safe projectile from distance
        elif distance < close_range and not corner_pressure:
            # Try to escape with defensive movement
            escape_direction = 1 if relative_pos > 0 else 2
            return 7 if escape_direction == 1 else 8
        else:
            return 6  # Default to blocking
    
    # Corner escape priority
    if corner_pressure and distance < medium_range:
        if opponent_attack_status > 0.5:
            return 6  # Block while cornered
        elif distance < very_close_range:
            # Try to jump out of corner
            if abs(height_diff) < 0.4 and random.random() < 0.6:
                return 3
            else:
                # Fight back to discourage pressure
                return 4 if random.random() < 0.7 else 5
        else:
            # Move toward center when possible
            center_direction = 2 if my_pos_x < 0.5 else 1
            if opponent_projectile_ready and random.random() < 0.4:
                return 7 if center_direction == 1 else 8  # Move with block
            else:
                return center_direction
    
    # Ultra-close range combat - frame trap and pressure game
    if distance < ultra_close_range:
        # Immediate threat response
        if opponent_attack_status > 0.7:
            if my_health > opponent_health * 1.2:
                return 4  # Counter-attack when health advantage is significant
            else:
                return 6  # Block when health is close
        
        # Break opponent's guard with mixups
        if opponent_defensive:
            mixup_roll = random.random()
            if mixup_roll < 0.2:
                return 3  # Jump to break guard
            elif mixup_roll < 0.4:
                return 5  # Strong kick
            elif mixup_roll < 0.6:
                return 9 if my_projectile_ready else 4  # Point blank projectile or punch
            elif mixup_roll < 0.8:
                return 4  # Quick punch
            else:
                return 0  # Brief pause to bait
        
        # Aggressive pressure when opponent is open
        if current_aggression > 0.7:
            pressure_choice = random.random()
            if pressure_choice < 0.45:
                return 4  # Fast punch for frame advantage
            elif pressure_choice < 0.75:
                return 5  # Kick for damage
            elif pressure_choice < 0.9:
                return 3  # Jump for mixup
            else:
                return 6  # Block to reset
        
        # Balanced ultra-close approach
        balanced_choice = random.random()
        if balanced_choice < 0.35:
            return 4