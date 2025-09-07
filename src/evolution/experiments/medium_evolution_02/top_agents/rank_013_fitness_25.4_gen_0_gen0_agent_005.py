"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_005
Rank: 13/13
Generation: 0
Fighting Style: rushdown

Performance Metrics:
- Fitness: 25.39
- Win Rate: 50.0%
- Average Reward: 0.00

Created: 2025-06-01 11:35:24
Lineage: Original

Tournament Stats:
None
"""

# Agent Code:
def get_action(state):
    import random
    import numpy as np
    
    # Extract and validate key strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    
    # Extract fighter status information
    my_health = max(0.0, min(1.0, state[3]))
    opponent_health = max(0.0, min(1.0, state[14]))
    my_attack_status = state[6]
    opponent_attack_status = state[17]
    my_block_status = state[7]
    opponent_block_status = state[18]
    my_projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = max(0.0, state[21])
    height_difference = state[24]
    
    # Define strategic parameters for rushdown style
    close_range = 0.12
    medium_range = 0.25
    far_range = 0.4
    critical_health = 0.2
    dominant_health = 0.3
    
    # Rushdown aggression factors
    base_aggression = 0.8
    health_desperation = 0.9
    winning_aggression = 0.85
    
    # Emergency defensive mode when critically low health
    if my_health < critical_health and health_advantage < -0.4:
        if distance < close_range:
            if opponent_attack_status > 0:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 7  # Move left while blocking
            else:
                return 8  # Move right while blocking
        elif distance < medium_range:
            if my_projectile_cooldown <= 0:
                return 9  # Projectile to create space
            else:
                return 6  # Block and wait
        else:
            if my_projectile_cooldown <= 0:
                return 9  # Long range projectile
            else:
                return 0  # Wait for cooldown
    
    # Rushdown primary strategy - get close and attack
    if distance > far_range:
        # Too far - need to close distance quickly
        if my_projectile_cooldown <= 0 and random.random() < 0.3:
            return 9  # Occasional projectile while closing
        elif relative_pos > 0.1:
            return 2  # Rush right toward opponent
        elif relative_pos < -0.1:
            return 1  # Rush left toward opponent
        else:
            return 2 if random.random() < 0.5 else 1  # Random approach
    
    elif distance > medium_range:
        # Medium-far range - aggressive approach with some caution
        if opponent_projectile_cooldown <= 0 and random.random() < 0.4:
            # Opponent might projectile, be ready
            if relative_pos > 0:
                return 8  # Move right with block
            else:
                return 7  # Move left with block
        elif my_projectile_cooldown <= 0 and random.random() < 0.25:
            return 9  # Quick projectile before closing
        else:
            # Aggressive approach
            if relative_pos > 0:
                return 2  # Move right
            else:
                return 1  # Move left
    
    elif distance > close_range:
        # Medium range - prime rushdown positioning
        if opponent_attack_status > 0:
            # Opponent is attacking, decide counter-strategy
            if health_advantage > 0.2:
                # Winning, can afford to trade or rush through
                if relative_pos > 0:
                    return 2  # Rush through attack
                else:
                    return 1  # Rush through attack
            else:
                # Need to be more careful
                if random.random() < 0.6:
                    return 6  # Block the attack
                else:
                    return 3  # Jump over attack
        
        elif opponent_block_status > 0:
            # Opponent blocking, mix up approach
            if random.random() < 0.4:
                return 3  # Jump to confuse timing
            elif random.random() < 0.3:
                if my_projectile_cooldown <= 0:
                    return 9  # Projectile to break guard
                else:
                    return 5  # Strong kick to break guard
            else:
                # Continue approach
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        else:
            # Opponent neutral, perfect rush opportunity
            rush_chance = base_aggression
            if health_advantage > dominant_health:
                rush_chance = winning_aggression
            elif health_advantage < -dominant_health:
                rush_chance = health_desperation
            
            if random.random() < rush_chance:
                if relative_pos > 0:
                    return 2  # Aggressive approach right
                else:
                    return 1  # Aggressive approach left
            else:
                return 3  # Jump approach for unpredictability
    
    else:
        # Close range - prime rushdown combat zone
        if opponent_block_status > 0:
            # Opponent blocking, need to break guard
            mix_options = []
            if random.random() < 0.3:
                mix_options.append(5)  # Heavy kick to break guard
            if random.random() < 0.2:
                mix_options.append(3)  # Jump for overhead
            if my_projectile_cooldown <= 0 and random.random() < 0.15:
                mix_options.append(9)  # Point blank projectile
            if random.random() < 0.35:
                mix_options.append(4)  # Fast punch to pressure
            
            if mix_options:
                return random.choice(mix_options)
            else:
                return 5  # Default guard break attempt
        
        elif opponent_attack_status > 0:
            # Opponent attacking in close range
            if my_health > opponent_health * 1.3:
                # Healthy enough to trade hits
                counter_options = [4, 5]  # Counter attack
                if random.random() < 0.7:
                    return random.choice(counter_options)
                else:
                    return 6  # Block occasionally
            else:
                # Need to be defensive
                if random.random() < 0.7:
                    return 6  # Block most attacks
                elif random.random() < 0.5:
                    return 3  # Jump to escape
                else:
                    return 4  # Quick counter punch
        
        else:
            # Opponent neutral in close range - prime attack opportunity
            attack_intensity = base_aggression
            
            # Adjust intensity based on health situation
            if health_advantage > dominant_health:
                attack_intensity = 0.95  # Maximum aggression when winning
            elif health_advantage < -dominant_health:
                attack_intensity = health_desperation  # Desperate attacks when losing
            elif my_health < critical_health:
                attack_intensity = 0.92  # High aggression when low health
            
            if random.random() < attack_intensity:
                # Choose attack type based on situation
                attack_choice = random.random()
                
                if attack_choice < 0.45:
                    return 4  # Fast punch - rushdown bread and butter
                elif attack_choice < 0.75:
                    return 5  # Heavy kick - more damage
                elif attack_choice < 0.85:
                    # Mix in movement attacks
                    if relative_pos > 0:
                        return 2  # Aggressive positioning
                    else:
                        return 1  # Aggressive positioning
                elif attack_choice < 0.92:
                    return 3  # Jump attack for mix-up