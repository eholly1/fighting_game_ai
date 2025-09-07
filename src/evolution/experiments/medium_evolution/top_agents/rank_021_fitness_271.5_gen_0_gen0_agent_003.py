"""
Hall of Fame Agent
==================

Agent ID: gen0_agent_003
Rank: 21/100
Generation: 0
Fighting Style: balanced

Performance Metrics:
- Fitness: 271.54
- Win Rate: 50.0%
- Average Reward: 271.54

Created: 2025-06-01 00:36:59
Lineage: Original

Tournament Stats:
None
"""

# Agent Code:
def get_action(state):
    import random
    import math
    
    # Extract and validate key state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = max(-1.0, min(1.0, state[23]))
    health_advantage = max(-1.0, min(1.0, state[25]))
    height_diff = state[24] if len(state) > 24 else 0.0
    
    # Extract fighter status information
    my_health = state[2] if len(state) > 2 else 1.0
    my_x_pos = state[0] if len(state) > 0 else 0.5
    my_y_pos = state[1] if len(state) > 1 else 0.0
    my_x_vel = state[3] if len(state) > 3 else 0.0
    my_y_vel = state[4] if len(state) > 4 else 0.0
    my_attacking = state[5] if len(state) > 5 else 0.0
    my_blocking = state[6] if len(state) > 6 else 0.0
    my_stunned = state[7] if len(state) > 7 else 0.0
    my_projectile_cd = state[10] if len(state) > 10 else 0.0
    
    # Extract opponent information
    opp_health = state[13] if len(state) > 13 else 1.0
    opp_x_pos = state[11] if len(state) > 11 else 0.5
    opp_y_pos = state[12] if len(state) > 12 else 0.0
    opp_x_vel = state[14] if len(state) > 14 else 0.0
    opp_y_vel = state[15] if len(state) > 15 else 0.0
    opp_attacking = state[16] if len(state) > 16 else 0.0
    opp_blocking = state[17] if len(state) > 17 else 0.0
    opp_stunned = state[18] if len(state) > 18 else 0.0
    
    # Define strategic thresholds
    close_range = 0.15
    medium_range = 0.35
    critical_health = 0.3
    winning_threshold = 0.2
    losing_threshold = -0.2
    
    # Emergency situations - highest priority
    if my_stunned > 0.5:
        return 0  # Can't act while stunned
    
    # Critical health management
    if my_health < critical_health:
        if opp_attacking > 0.5 and distance < close_range:
            return 6  # Block incoming attack
        elif distance > medium_range and my_projectile_cd < 0.3:
            return 9  # Keep distance with projectiles
        elif distance < close_range:
            # Try to escape close combat
            if my_x_pos < 0.3:  # Near left edge
                return 8  # Move right while blocking
            elif my_x_pos > 0.7:  # Near right edge
                return 7  # Move left while blocking
            else:
                return 8 if relative_pos < 0 else 7  # Move away while blocking
    
    # Opponent is stunned - capitalize
    if opp_stunned > 0.5:
        if distance < close_range:
            return 5 if random.random() < 0.7 else 4  # Prefer kick for damage
        elif distance < medium_range:
            if relative_pos > 0:
                return 2  # Move right to close distance
            else:
                return 1  # Move left to close distance
        else:
            return 9  # Projectile if too far
    
    # Opponent is attacking - defensive response
    if opp_attacking > 0.5:
        if distance < close_range:
            if my_blocking < 0.3:  # Not already blocking
                return 6  # Block the attack
            else:
                # Try to counter or reposition
                if random.random() < 0.4:
                    return 4  # Quick counter punch
                else:
                    return 7 if relative_pos > 0 else 8  # Move away while blocking
        elif distance < medium_range:
            # Medium range - prepare for their approach
            if opp_x_vel > 0.3 and relative_pos < 0:  # They're approaching from left
                return 8  # Move right while blocking
            elif opp_x_vel < -0.3 and relative_pos > 0:  # They're approaching from right
                return 7  # Move left while blocking
            else:
                return 6  # Just block
    
    # Winning strategy - be aggressive but smart
    if health_advantage > winning_threshold:
        if distance < close_range:
            # Close combat aggression
            if opp_blocking > 0.5:
                # Opponent is blocking - mix up attacks or reposition
                action_choice = random.random()
                if action_choice < 0.3:
                    return 5  # Strong kick to break guard
                elif action_choice < 0.6:
                    return 3  # Jump to change angle
                else:
                    # Reposition for better angle
                    return 2 if relative_pos < 0 else 1
            else:
                # Opponent not blocking - attack
                return 4 if random.random() < 0.6 else 5
        
        elif distance < medium_range:
            # Medium range control
            if abs(height_diff) > 0.3 and my_y_pos < opp_y_pos:
                return 3  # Jump to match height
            else:
                # Close the distance
                if relative_pos > 0:
                    return 2  # Move right
                else:
                    return 1  # Move left
        
        else:
            # Long range pressure
            if my_projectile_cd < 0.2:
                return 9  # Projectile attack
            else:
                # Move closer while projectile recharges
                if relative_pos > 0:
                    return 2
                else:
                    return 1
    
    # Losing strategy - play more defensively
    elif health_advantage < losing_threshold:
        if distance < close_range:
            # Close combat defense
            if opp_attacking > 0.3:
                return 6  # Block
            elif my_health > critical_health and opp_blocking < 0.3:
                # Safe attack opportunity
                return 4  # Quick punch
            else:
                # Try to escape close combat
                if my_x_pos < 0.2 or my_x_pos > 0.8:  # Near edge
                    return 6  # Block - can't retreat further
                else:
                    return 7 if relative_pos > 0 else 8  # Move away
        
        elif distance < medium_range:
            # Medium range caution
            if opp_x_vel > 0.5 or opp_x_vel < -0.5:  # Opponent moving fast
                return 6  # Prepare to block
            elif my_projectile_cd < 0.3:
                return 9  # Projectile to maintain distance
            else:
                # Maintain distance
                if relative_pos > 0 and my_x_pos < 0.7:
                    return 1  # Move away
                elif relative_pos < 0 and my_x_pos > 0.3:
                    return 2  # Move away
                else:
                    return 6  # Block if cornered
        
        else:
            # Long range recovery
            if my_projectile_cd < 0.2:
                return 9  # Projectile
            else:
                return 6  # Block and wait