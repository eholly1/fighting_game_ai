"""
Evolutionary Agent: gen4_agent_026
==================================

Metadata:
{
  "generation": 4,
  "fitness": -21.599999999999813,
  "fighting_style": "evolved",
  "win_rate": 0.0
}

Code Hash: b04200b95b697225
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
    my_stunned = max(0.0, min(1.0, state[9])) if len(state) > 9 else 0.0
    my_projectile_cooldown = max(0.0, min(1.0, state[10])) if len(state) > 10 else 0.0
    
    opponent_health = max(0.0, min(1.0, state[12])) if len(state) > 12 else 1.0
    opponent_pos_x = max(0.0, min(1.0, state[13])) if len(state) > 13 else 0.5
    opponent_velocity_x = max(-1.0, min(1.0, state[15])) if len(state) > 15 else 0.0
    opponent_velocity_y = max(-1.0, min(1.0, state[16])) if len(state) > 16 else 0.0
    opponent_attack_status = max(0.0, min(1.0, state[18])) if len(state) > 18 else 0.0
    opponent_block_status = max(0.0, min(1.0, state[19])) if len(state) > 19 else 0.0
    opponent_stunned = max(0.0, min(1.0, state[20])) if len(state) > 20 else 0.0
    opponent_projectile_cooldown = max(0.0, min(1.0, state[21])) if len(state) > 21 else 0.0
    
    # Enhanced tactical ranges for hybrid fighting
    crushing_range = 0.04
    brutal_range = 0.09
    close_combat_range = 0.16
    mid_close_range = 0.28
    control_range = 0.42
    zoning_range = 0.58
    projectile_range = 0.75
    max_range = 0.90
    
    # Advanced positioning and tactical state analysis
    wall_distance = min(my_pos_x, 1.0 - my_pos_x)
    opponent_wall_distance = min(opponent_pos_x, 1.0 - opponent_pos_x)
    am_cornered = wall_distance < 0.08
    severely_cornered = wall_distance < 0.04
    opponent_cornered = opponent_wall_distance < 0.08
    opponent_severely_cornered = opponent_wall_distance < 0.04
    near_wall = wall_distance < 0.20
    opponent_near_wall = opponent_wall_distance < 0.20
    
    # Dynamic opponent pattern recognition
    opponent_rushing = opponent_attack_status > 0.4 and abs(opponent_velocity_x) > 0.2
    opponent_ultra_aggressive = opponent_attack_status > 0.7 or abs(opponent_velocity_x) > 0.35
    opponent_defensive_stance = opponent_block_status > 0.5
    opponent_turtle_mode = opponent_block_status > 0.8 and abs(opponent_velocity_x) < 0.05
    opponent_zoning = distance > control_range and opponent_projectile_cooldown < 0.3
    opponent_mobile = abs(opponent_velocity_x) > 0.12
    opponent_hyper_mobile = abs(opponent_velocity_x) > 0.25
    
    # Movement prediction and interception
    opponent_closing_in = False
    opponent_retreating = False
    if relative_pos > 0.05:
        opponent_closing_in = opponent_velocity_x > 0.12
        opponent_retreating = opponent_velocity_x < -0.12
    elif relative_pos < -0.05:
        opponent_closing_in = opponent_velocity_x < -0.12
        opponent_retreating = opponent_velocity_x > 0.12
    
    # Projectile availability and threat assessment
    my_projectile_ready = my_projectile_cooldown < 0.25
    my_projectile_optimal = my_projectile_cooldown < 0.15
    opponent_projectile_threat = opponent_projectile_cooldown < 0.20 and distance > mid_close_range
    opponent_projectile_immediate = opponent_projectile_cooldown < 0.10
    
    # Hybrid fighting tactical assessment
    health_ratio = my_health / max(0.1, opponent_health)
    health_critical = my_health < 0.18
    health_low = my_health < 0.35
    opponent_health_critical = opponent_health < 0.18
    opponent_health_low = opponent_health < 0.35
    
    # Advanced aggression calculation with hybrid balance
    base_aggression = 0.62  # Hybrid balanced aggression
    tactical_modifier = 0.0
    
    # Health-based tactical shifts
    if health_advantage > 0.4:
        tactical_modifier += 0.25  # Press advantage hard
    elif health_advantage > 0.2:
        tactical_modifier += 0.15  # Moderate pressure
    elif health_advantage > -0.1:
        tactical_modifier += 0.05  # Slight aggression
    elif health_advantage > -0.3:
        tactical_modifier -= 0.10  # Cautious approach
    else:
        tactical_modifier -= 0.25  # Defensive survival
    
    # Distance-based hybrid adjustments
    if distance < brutal_range:
        tactical_modifier += 0.20  # Capitalize on ultra-close
    elif distance < close_combat_range:
        tactical_modifier += 0.12  # Favor close combat
    elif distance < control_range:
        tactical_modifier += 0.05  # Slight preference for control
    elif distance > zoning_range:
        tactical_modifier -= 0.08  # More cautious at range
    
    # Momentum and positioning bonuses
    if opponent_cornered and not am_cornered:
        tactical_modifier += 0.30
    elif am_cornered and not opponent_cornered:
        tactical_modifier -= 0.35
    elif opponent_severely_cornered:
        tactical_modifier += 0.45
    elif severely_cornered:
        tactical_modifier -= 0.50
    
    # Opponent state exploitation
    if opponent_stunned > 0.4:
        tactical_modifier += 0.40
    elif opponent_stunned > 0.2:
        tactical_modifier += 0.20
    
    if opponent_turtle_mode and distance < control_range:
        tactical_modifier += 0.15  # Pressure