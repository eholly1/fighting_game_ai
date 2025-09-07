"""
Evolutionary Agent: gen0_agent_008
==================================

Metadata:
{
  "generation": 0,
  "fitness": 204.93866666666378,
  "fighting_style": "pressure_fighter",
  "win_rate": 0.5
}

Code Hash: 62954f16f7dea0fa
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
    my_attack_status = state[6]
    opponent_attack_status = state[17]
    my_block_status = state[7]
    opponent_block_status = state[18]
    my_projectile_cooldown = max(0.0, state[10])
    opponent_projectile_cooldown = max(0.0, state[21])
    height_difference = state[24]
    
    # Define pressure fighter constants
    close_range_threshold = 0.15
    medium_range_threshold = 0.35
    aggression_threshold = 0.8
    corner_pressure_distance = 0.4
    health_desperation_threshold = -0.4
    winning_threshold = 0.3
    
    # Calculate aggression level based on health and style
    base_aggression = 0.75  # High base aggression for pressure fighter
    health_modifier = health_advantage * 0.2
    aggression_level = min(1.0, max(0.3, base_aggression + health_modifier))
    
    # Emergency defensive behavior when critically low health
    if health_advantage < health_desperation_threshold and my_health < 0.25:
        if distance < close_range_threshold and opponent_attack_status > 0:
            return 6  # Block incoming attacks
        elif distance > medium_range_threshold and my_projectile_cooldown <= 0:
            return 9  # Projectile to create space
        elif relative_pos > 0:
            return 7  # Move left while blocking
        else:
            return 8  # Move right while blocking
    
    # Pressure fighter core strategy - maintain close range aggression
    if distance > medium_range_threshold:
        # Too far - need to close distance aggressively
        if my_projectile_cooldown <= 0 and random.random() < 0.3:
            return 9  # Occasional projectile while closing
        elif relative_pos > 0.1:
            # Opponent to the right
            if opponent_projectile_cooldown <= 0 and random.random() < 0.4:
                return 8  # Move right with block against projectile
            else:
                return 2  # Move right aggressively
        elif relative_pos < -0.1:
            # Opponent to the left
            if opponent_projectile_cooldown <= 0 and random.random() < 0.4:
                return 7  # Move left with block against projectile
            else:
                return 1  # Move left aggressively
        else:
            # Opponent centered, choose random approach
            if random.random() < 0.5:
                return 1
            else:
                return 2
    
    elif distance > close_range_threshold:
        # Medium range - perfect for pressure fighter setup
        if abs(height_difference) > 0.3:
            return 3  # Jump to adjust height for better positioning
        
        # Check if opponent is blocking frequently
        if opponent_block_status > 0:
            if random.random() < 0.6:
                # Try to grab or throw - use kick for more power
                return 5  # Kick to break block
            else:
                # Position for better angle
                if relative_pos > 0:
                    return 2
                else:
                    return 1
        
        # Approach with aggression
        if aggression_level > aggression_threshold:
            if relative_pos > 0.05:
                return 2  # Close distance to right
            elif relative_pos < -0.05:
                return 1  # Close distance to left
            else:
                # Close enough to start pressure
                if random.random() < 0.7:
                    return 4  # Quick punch to start combo
                else:
                    return 5  # Power kick
        else:
            # More cautious approach when not fully aggressive
            if opponent_attack_status > 0:
                return 6  # Block incoming attack
            elif relative_pos > 0:
                return 8  # Cautious advance right
            else:
                return 7  # Cautious advance left
    
    else:
        # Close range - pressure fighter's domain
        
        # Counter opponent's attacks
        if opponent_attack_status > 0:
            if health_advantage < -0.2:
                return 6  # Block when behind in health
            elif random.random() < 0.4:
                return 6  # Sometimes block to mix up defense
            else:
                # Counter attack with speed
                if random.random() < 0.8:
                    return 4  # Fast punch counter
                else:
                    return 5  # Power kick counter
        
        # Pressure when opponent is blocking
        if opponent_block_status > 0:
            if random.random() < 0.3:
                # Try to reposition for better angle
                if relative_pos > 0:
                    return 1  # Move to left side
                else:
                    return 2  # Move to right side
            elif random.random() < 0.6:
                return 5  # Power kick to break block
            else:
                return 4  # Quick punch to maintain pressure
        
        # Apply maximum pressure when opponent is vulnerable
        if opponent_attack_status <= 0 and opponent_block_status <= 0:
            # Opponent is open - full aggression
            attack_choice = random.random()
            
            if attack_choice < 0.5:
                return 4  # Fast punch for combo potential
            elif attack_choice < 0.8:
                return 5  # Power kick for damage
            else:
                # Mix in movement to avoid becoming predictable
                if relative_pos > 0.1:
                    return 1  # Adjust position left
                elif relative_pos < -0.1:
                    return 2  # Adjust position right
                else:
                    return 4  # Default to punch
        
        # When winning significantly, maintain pressure but be smarter
        if health_advantage > winning_threshold:
            if random.random() < 0.6:
                return 4  # Continue pressure with punches
            elif random.random() < 0.8:
                return 5  # Power kick
            else:
                return 6  # Occasional block to stay safe
        
        # When losing, take more risks for damage
        if health_advantage < -0.2:
            if random.random() < 0.7:
                return 5  # More power kicks when desperate
            else:
                return 4  # Quick punches
        
        # Default close range pressure
        combo_choice = random.random()
        if combo_choice < 0.6:
            return 4  # Punch - fast and combo-friendly
        elif combo_choice < 0.85:
            return 5  # Kick - more damage
        else:
            # Occasional defensive move to reset
            return 6  # Block to reset pressure
    
    # Fallback action - should rarely reach here
    if distance > close_range_threshold:
        if relative_pos > 0:
            return 2  # Move toward opponent
        else:
            return 1  # Move toward opponent
    else:
        return 4  # Default attack