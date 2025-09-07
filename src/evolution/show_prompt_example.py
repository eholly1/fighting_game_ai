#!/usr/bin/env python3
"""
Show example prompts sent to Claude during evolutionary training
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from evolution.prompt_templates import PromptTemplateManager, PromptContext

def show_initial_generation_prompt():
    """Show what an initial generation prompt looks like"""
    print("🎯 INITIAL GENERATION PROMPT EXAMPLE")
    print("=" * 80)
    
    manager = PromptTemplateManager()
    
    context = PromptContext(
        fighting_style="rushdown",
        generation=0,
        parent_codes=[]
    )
    
    prompt = manager.generate_agent_prompt(context)
    
    print(f"📊 Prompt Statistics:")
    print(f"   Length: {len(prompt):,} characters")
    print(f"   Lines: {len(prompt.split(chr(10)))}")
    print(f"   Words: {len(prompt.split())}")
    print()
    print("📝 FULL PROMPT:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    return prompt

def show_evolution_prompt():
    """Show what an evolution prompt with parent code looks like"""
    print("\n\n🧬 EVOLUTION PROMPT EXAMPLE (with parent code)")
    print("=" * 80)
    
    manager = PromptTemplateManager()
    
    # Example parent code (simplified)
    parent_code = """def get_action(state):
    # Extract key strategic information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = state[23]
    health_advantage = state[25]
    
    # Rushdown strategy - always try to close distance
    if distance > 0.3:
        # Far range - move toward opponent
        if relative_pos > 0:
            return 2  # move_right
        else:
            return 1  # move_left
    elif distance > 0.15:
        # Medium range - aggressive approach
        if health_advantage > 0:
            return 4  # punch
        else:
            return 2 if relative_pos > 0 else 1  # move toward
    else:
        # Close range - attack aggressively
        if health_advantage < -0.3:
            return 6  # block when losing badly
        else:
            return 4 if random.random() < 0.7 else 5  # punch or kick
"""
    
    context = PromptContext(
        fighting_style="adaptive",
        generation=2,
        parent_codes=[parent_code],
        performance_feedback="Agent needs better defensive capabilities and projectile usage",
        specific_improvements=[
            "Improve blocking timing against aggressive opponents",
            "Better use of projectiles at long range",
            "More adaptive strategy based on opponent behavior"
        ]
    )
    
    prompt = manager.generate_agent_prompt(context)
    
    print(f"📊 Evolution Prompt Statistics:")
    print(f"   Length: {len(prompt):,} characters")
    print(f"   Lines: {len(prompt.split(chr(10)))}")
    print(f"   Words: {len(prompt.split())}")
    print(f"   Parent code included: {len(parent_code)} characters")
    print()
    print("📝 FULL EVOLUTION PROMPT:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)

def show_crossover_prompt():
    """Show what a crossover prompt looks like"""
    print("\n\n🔀 CROSSOVER PROMPT EXAMPLE (with 2 parents)")
    print("=" * 80)
    
    manager = PromptTemplateManager()
    
    parent1_code = """def get_action(state):
    distance = state[22]
    health_advantage = state[25]
    
    # Aggressive rushdown
    if distance > 0.2:
        return 2  # move_right
    else:
        return 4  # punch
"""
    
    parent2_code = """def get_action(state):
    distance = state[22]
    relative_pos = state[23]
    
    # Defensive zoner
    if distance < 0.3:
        return 6  # block
    else:
        return 9  # projectile
"""
    
    context = PromptContext(
        fighting_style="hybrid",
        generation=3,
        parent_codes=[parent1_code, parent2_code],
        performance_feedback="Combine aggressive and defensive elements effectively",
        specific_improvements=[
            "Balance rushdown and zoning strategies",
            "Switch between aggressive and defensive based on situation"
        ]
    )
    
    prompt = manager.generate_agent_prompt(context)
    
    print(f"📊 Crossover Prompt Statistics:")
    print(f"   Length: {len(prompt):,} characters")
    print(f"   Lines: {len(prompt.split(chr(10)))}")
    print(f"   Words: {len(prompt.split())}")
    print(f"   Parent 1 code: {len(parent1_code)} characters")
    print(f"   Parent 2 code: {len(parent2_code)} characters")
    print()
    print("📝 FULL CROSSOVER PROMPT:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)

if __name__ == "__main__":
    print("🔍 CLAUDE PROMPT EXAMPLES")
    print("These are the actual prompts sent to Claude during evolutionary training")
    print()
    
    # Show initial generation prompt
    show_initial_generation_prompt()
    
    # Show evolution prompt
    show_evolution_prompt()
    
    # Show crossover prompt  
    show_crossover_prompt()
    
    print("\n✨ These prompts explain why agent compilation takes 30-60+ seconds!")
    print("   Claude is doing sophisticated strategic reasoning for each agent.")
