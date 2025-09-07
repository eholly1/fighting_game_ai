"""
Evolutionary Agent: gen1_agent_004
==================================

Metadata:
{
  "generation": 1,
  "fitness": 0.0,
  "fighting_style": "evolved",
  "win_rate": 0.5
}

Code Hash: 8013d9515f620d44
Serialization Version: 1.0
"""

# Agent Code:
def get_action(state):
    import random
    import numpy as np
    import math
    
    # Validate input and extract core state information
    if len(state) < 26:
        return 4  # Default safe action
    
    # Core strategic variables with defensive bounds checking
    distance = max(0.0, min(1.0, float(state[22])))
    relative_pos = max(-1.0, min(1.0, float(state[23])))
    health_advantage = max(-1.0, min(1.0, float(state[25])))
    height_diff = float(state[24]) if abs(float(state[24])) < 10 else 0.0
    
    # My fighter detailed status
    my_health = max(0.0, min(1.0, float(state[3])))
    my_x_pos = float(state[0])
    my_y_pos = float(state[1])
    my_velocity_x = float(state[2])
    my_attack_status = max(0.0, float(state[6]))
    my_block_status = max(0.0, float(state[7]))
    my_projectile_cooldown = max(0.0, float(state[10]))
    
    # Opponent fighter status
    opp_health = max(0.0, min(1.0, float(state[14])))
    opp_x_pos = float(state[11])
    opp_y_pos = float(state[12])
    opp_attack_status = max(0.0, float(state[17]))
    opp_block_status = max(0.0, float(state[18]))
    opp_projectile_cooldown = max(0.0, float(state[21]))
    
    # Hybrid fighting style range definitions
    ultra_close_range = 0.08
    close_range = 0.16
    medium_range = 0.32
    far_range = 0.48
    ultra_far_range = 0.65
    
    # Adaptive aggression system
    base_aggression = 0.75  # Balanced hybrid approach
    defensive_threshold = 0.65
    offensive_threshold = 0.85
    
    # Dynamic aggression based on multiple factors
    health_factor = 1.0
    if health_advantage > 0.3:
        health_factor = 1.15  # More aggressive when winning
    elif health_advantage > 0.0:
        health_factor = 1.05  # Slightly more aggressive
    elif health_advantage > -0.3:
        health_factor = 0.95  # Slightly defensive
    else:
        health_factor = 0.8   # More defensive when losing badly
    
    # Distance-based aggression modifier
    distance_factor = 1.0
    if distance < close_range:
        distance_factor = 1.1  # More aggressive up close
    elif distance > far_range:
        distance_factor = 0.9  # Less aggressive at range
    
    # Calculate final aggression level
    current_aggression = min(1.0, base_aggression * health_factor * distance_factor)
    
    # Critical health emergency mode
    if my_health < 0.15 and health_advantage < -0.6:
        if distance < close_range:
            if opp_attack_status > 0:
                return 6  # Desperate blocking
            elif my_projectile_cooldown <= 0 and random.random() < 0.4:
                return 9  # Desperate projectile
            else:
                # Try to escape to safer range
                if relative_pos > 0:
                    return 7  # Retreat left with block
                else:
                    return 8  # Retreat right with block
        else:
            if my_projectile_cooldown <= 0:
                return 9  # Chip damage attempt
            else:
                return 6  # Wait and block
    
    # Opponent vulnerability detection
    opponent_vulnerable = (opp_attack_status <= 0 and opp_block_status <= 0)
    opponent_attacking = (opp_attack_status > 0)
    opponent_blocking = (opp_block_status > 0)
    
    # Counter-attack system when opponent is attacking
    if opponent_attacking and distance <= close_range:
        counter_chance = 0.4
        if health_advantage > 0.2:
            counter_chance = 0.6  # More willing to trade when ahead
        elif my_health > opp_health * 1.3:
            counter_chance = 0.55  # Trade when health advantage is significant
        
        if random.random() < counter_chance:
            # Choose counter attack
            if random.random() < 0.7:
                return 4  # Fast counter punch
            else:
                return 5  # Power counter kick
        else:
            # Defensive response
            if random.random() < 0.8:
                return 6  # Block
            else:
                return 3  # Jump to avoid
    
    # Ultra close range combat (grappling distance)
    if distance <= ultra_close_range:
        if opponent_blocking:
            # Guard break tactics
            guard_break_options = []
            if random.random() < 0.45:
                guard_break_options.append(5)  # Heavy kick
            if random.random() < 0.25:
                guard_break_options.append(3)  # Jump attack
            if my_projectile_cooldown <= 0 and random.random() < 0.2:
                guard_break_options.append(9)  # Point blank projectile
            if random.random() < 0.3:
                guard_break_options.append(4)  # Pressure with punches
            
            if guard_break_options:
                return random.choice(guard_break_options)
            else:
                return 5  # Default guard break
        
        elif opponent_vulnerable:
            # Maximum punishment opportunity
            attack_mix = random.random()
            if attack_mix < 0.5:
                return 4  # Fast punch combo starter
            elif attack_mix < 0.8:
                return 5  # Heavy damage kick
            else:
                # Mix in movement for pressure
                if relative_pos > 0:
                    return 2  # Pressure right
                else:
                    return 1  # Pressure left
        
        else:
            # Neutral ultra-close situation
            if random.random() < current_aggression:
                return 4 if random.random() < 0.6 else 5
            else:
                return 6  # Cautious block
    
    # Close range tactical combat
    elif distance <= close_range:
        if opponent_blocking:
            # Varied guard break approach
            break_choice = random.random()
            if break_choice < 0.4:
                return 5  # Kick to break guard
            elif break_choice < 0.6:
                return 3  # Jump overhead
            elif break_choice < 0.75:
                # Reposition for better angle
                if relative_pos > 0:
                    return 2
                else:
                    return 1
            else:
                return 4  # Fast punch pressure
        
        elif opponent_vulnerable:
            # Prime attacking opportunity
            if random.random() < current_aggression:
                # Attack selection based on situation
                if health_advantage > 0.3:
                    # Winning - can afford to be aggressive
                    return 5 if random.random() < 0.6 else 4
                elif health_advantage < -0.2:
                    # Losing - need damage fast
                    return 4 if random.random() < 0.7 else 5
                else:
                    # Even fight - balanced approach
                    return 4 if random.random() < 0.55 else 5
            else:
                # Cautious approach
                if random.random() < 0.7:
                    return 4  # Safe fast attack