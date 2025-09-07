#!/usr/bin/env python3
"""
Enhanced LLM Prompting Templates for Evolutionary Training

Provides structured prompts and context for generating high-quality,
bug-free fighting game AI agents using Claude API.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class PromptContext:
    """Context information for LLM prompting"""
    fighting_style: str
    generation: int
    parent_codes: List[str]
    performance_feedback: Optional[str] = None
    specific_improvements: Optional[List[str]] = None

class PromptTemplateManager:
    """
    Manages LLM prompt templates for agent generation
    """
    
    def __init__(self, max_lines: int = 1400, max_chars: int = 40000):
        self.max_lines = max_lines
        self.max_chars = max_chars
        
        # Fighting style descriptions
        self.fighting_styles = {
            'aggressive': "Focus on constant pressure, frequent attacks, chase opponent relentlessly",
            'defensive': "Prioritize blocking, counter-attack opportunities, maintain safe distance", 
            'zoner': "Use projectiles to control space, avoid close combat, keep opponent at range",
            'adaptive': "Change strategy based on health advantage and opponent behavior patterns",
            'rushdown': "Get close quickly, overwhelm with rapid attack sequences",
            'balanced': "Mix of all strategies, adapt to situation with good fundamentals",
            'counter_puncher': "Wait for opponent mistakes, punish with precise counter-attacks",
            'hit_and_run': "Quick strikes followed by immediate retreat, avoid prolonged exchanges",
            'pressure_fighter': "Maintain close range, constant attack pressure, corner opponent",
            'patient_defender': "Excellent blocking, wait for perfect opportunities to strike"
        }
    
    def generate_agent_prompt(self, context: PromptContext) -> str:
        """
        Generate a comprehensive prompt for agent creation
        
        Args:
            context: Context information for the prompt
            
        Returns:
            Complete prompt string for Claude API
        """
        base_prompt = self._get_base_prompt()
        style_prompt = self._get_style_prompt(context.fighting_style)
        constraints_prompt = self._get_constraints_prompt()
        examples_prompt = self._get_examples_prompt()
        
        # Add generation-specific context
        if context.generation > 0:
            evolution_prompt = self._get_evolution_prompt(context)
        else:
            evolution_prompt = self._get_initial_generation_prompt()
        
        # Combine all parts
        full_prompt = f"""
{base_prompt}

{style_prompt}

{constraints_prompt}

{examples_prompt}

{evolution_prompt}

FINAL REQUIREMENTS:
- Generate ONLY the Python code for the get_action function
- No explanations, comments outside the code, or markdown formatting
- Code must be under {self.max_lines} lines and {self.max_chars} characters
- Focus on clean, readable, strategic decision-making logic
- Test your logic mentally before outputting

Generate the fighting AI code now:
"""
        
        return full_prompt.strip()
    
    def _get_base_prompt(self) -> str:
        """Base prompt with interface requirements"""
        return """
You are creating a fighting game AI agent. The agent must implement a get_action function that analyzes the game state and returns strategic actions.

INTERFACE REQUIREMENTS:
- Function signature: def get_action(state) -> int
- Input: state is a numpy array with 26 elements representing game state
- Output: integer from 0-9 representing the action to take

ACTION SPACE:
0 = idle (do nothing)
1 = move_left (move toward left side of stage)  
2 = move_right (move toward right side of stage)
3 = jump (jump upward)
4 = punch (close-range attack, fast but weak)
5 = kick (close-range attack, slower but stronger)
6 = block (reduce incoming damage by 75%)
7 = move_left_block (move left while blocking)
8 = move_right_block (move right while blocking)  
9 = projectile (ranged attack, can be charged for more damage)

STATE VECTOR (26 elements):
Key elements for strategy:
- state[22] = distance to opponent (0.0=touching, 1.0=maximum distance)
- state[23] = relative position (-1.0=opponent to left, +1.0=opponent to right)
- state[25] = health advantage (-1.0=losing badly, +1.0=winning decisively)

Additional context:
- state[0-10]: Your fighter info (position, health, velocity, attack/block status, projectile cooldown)
- state[11-21]: Opponent fighter info (same structure as above)
- state[24]: Height difference between fighters

TACTICAL RANGES:
- Close (distance < 0.15): Punch/kick range, high risk/reward, blocking important
- Medium (0.15-0.3): Positioning critical, movement and timing key
- Far (distance > 0.3): Projectile range, safer but slower damage

WINNING STRATEGIES:
- Control distance: Close for attacks, far for projectiles
- Manage health: Block when losing, attack when winning  
- Use positioning: Corner opponents, avoid being cornered
- Mix up attacks: Don't be predictable, vary your approach
- Adapt to opponent: Change strategy based on their behavior
"""
    
    def _get_style_prompt(self, fighting_style: str) -> str:
        """Style-specific prompt"""
        style_description = self.fighting_styles.get(fighting_style, "balanced fighter")
        
        return f"""
FIGHTING STYLE: {fighting_style.upper()}
Strategy Focus: {style_description}

Implement this fighting style by:
- Making decisions that reflect this strategic approach
- Prioritizing actions that support this style
- Adapting the core strategy to different game situations
- Maintaining style consistency while being tactically flexible
"""
    
    def _get_constraints_prompt(self) -> str:
        """Code quality and safety constraints"""
        return """
CODE QUALITY REQUIREMENTS:
- Maximum 1400 lines of code
- Maximum 40,000 characters
- Use clear, descriptive variable names (distance, health_advantage, etc.)
- Add brief comments explaining key strategic decisions
- Structure code with clear if/elif/else blocks
- Avoid deeply nested logic (maximum 3 levels)
- Use helper variables to make logic readable

ALLOWED IMPORTS AND FUNCTIONS:
- numpy/np: for array operations and math
- random: for randomization and unpredictability  
- math: for mathematical functions
- Basic Python: if/else, for/while, basic math operations
- Built-in functions: min, max, abs, len, range, etc.

FORBIDDEN:
- File operations (open, read, write)
- Network operations (requests, urllib, socket)
- System operations (os, sys, subprocess)
- Dangerous functions (eval, exec, compile)
- External libraries beyond numpy, random, math

SAFETY REQUIREMENTS:
- Always return a valid integer 0-9
- Handle edge cases gracefully (invalid state values)
- Use defensive programming (check bounds, validate inputs)
- Avoid infinite loops or excessive computation
"""
    
    def _get_examples_prompt(self) -> str:
        """Example code patterns"""
        return """
GOOD CODE EXAMPLE:
```python
def get_action(state):
    # Extract key strategic information
    distance = max(0.0, min(1.0, state[22]))  # Defensive programming
    relative_pos = state[23]
    health_advantage = state[25]
    
    # Define strategic parameters
    close_threshold = 0.15
    medium_threshold = 0.3
    aggression_when_winning = 0.7
    
    # Adaptive strategy based on health
    if health_advantage < -0.3:  # Losing badly
        if distance > 0.4:
            return 9  # Projectile to keep distance
        else:
            return 6  # Block to survive
    
    # Range-based tactics
    if distance < close_threshold:
        # Close combat
        if health_advantage > 0:
            return 4 if random.random() < 0.6 else 5  # Mix punches and kicks
        else:
            return 6  # Block when losing
    
    elif distance < medium_threshold:
        # Medium range positioning
        if relative_pos > 0:
            return 2  # Move right toward opponent
        else:
            return 1  # Move left toward opponent
    
    else:
        # Long range
        return 9  # Projectile attack
```

KEY PATTERNS:
- Extract and validate state information first
- Use meaningful variable names and constants
- Implement clear range-based decision making
- Add health-based adaptations
- Include some randomization for unpredictability
- Always have a fallback return value
"""
    
    def _get_initial_generation_prompt(self) -> str:
        """Prompt for initial generation agents"""
        return """
GENERATION 0 - INITIAL CREATION:
Create a fresh fighting AI from scratch. Focus on:
- Implementing the core fighting style effectively
- Creating solid fundamental tactics
- Building a strong foundation for future evolution
- Balancing strategic coherence with tactical flexibility

Make this agent competitive and interesting to fight against.
"""
    
    def _get_evolution_prompt(self, context: PromptContext) -> str:
        """Prompt for evolved generation agents"""
        evolution_text = f"""
GENERATION {context.generation} - EVOLUTION:
This agent is evolved from previous generation(s). 
"""
        
        if context.performance_feedback:
            evolution_text += f"""
PERFORMANCE FEEDBACK:
{context.performance_feedback}

Use this feedback to improve the agent's strategy and decision-making.
"""
        
        if context.specific_improvements:
            evolution_text += f"""
SPECIFIC IMPROVEMENTS NEEDED:
{chr(10).join(f'- {improvement}' for improvement in context.specific_improvements)}

Address these specific weaknesses while maintaining the agent's strengths.
"""
        
        if context.parent_codes:
            evolution_text += f"""
PARENT AGENT(S) FOR INSPIRATION:
The following code represents successful strategies from the previous generation.
Learn from their approaches but create something new and improved:

"""
            for i, parent_code in enumerate(context.parent_codes[:2]):  # Limit to 2 parents
                evolution_text += f"""
Parent {i+1}:
```python
{parent_code}
```

"""
        
        evolution_text += """
EVOLUTION GOALS:
- Improve upon parent strategies while maintaining their strengths
- Address identified weaknesses and performance issues
- Introduce new tactical innovations
- Create a more effective and adaptable fighter
- Maintain code clarity and strategic coherence
"""
        
        return evolution_text
    
    def create_mutation_prompt(self, agent_code: str, generation: int) -> str:
        """Create a prompt for mutating an existing agent"""
        context = PromptContext(
            fighting_style="adaptive",
            generation=generation,
            parent_codes=[agent_code],
            specific_improvements=[
                "Improve decision-making in close combat",
                "Better adaptation to opponent patterns", 
                "More effective use of projectiles",
                "Enhanced defensive capabilities"
            ]
        )
        
        return self.generate_agent_prompt(context)
    
    def create_crossover_prompt(self, parent1_code: str, parent2_code: str, generation: int) -> str:
        """Create a prompt for crossing over two parent agents"""
        context = PromptContext(
            fighting_style="hybrid",
            generation=generation,
            parent_codes=[parent1_code, parent2_code],
            performance_feedback="Combine the best strategies from both parents",
            specific_improvements=[
                "Merge complementary tactical approaches",
                "Balance aggressive and defensive elements",
                "Create synergistic strategy combinations"
            ]
        )
        
        return self.generate_agent_prompt(context)

def test_prompt_templates():
    """Test the prompt template system"""
    print("🧪 Testing Prompt Templates")
    print("=" * 50)
    
    manager = PromptTemplateManager()
    
    # Test 1: Initial generation prompt
    context = PromptContext(
        fighting_style="aggressive",
        generation=0,
        parent_codes=[]
    )
    
    prompt = manager.generate_agent_prompt(context)
    print(f"Initial prompt length: {len(prompt)} characters")
    print(f"Contains style info: {'✅ PASS' if 'aggressive' in prompt.lower() else '❌ FAIL'}")
    print(f"Contains constraints: {'✅ PASS' if 'maximum' in prompt.lower() else '❌ FAIL'}")
    
    # Test 2: Evolution prompt
    parent_code = "def get_action(state): return 4"
    evolution_context = PromptContext(
        fighting_style="defensive",
        generation=5,
        parent_codes=[parent_code],
        performance_feedback="Agent needs better blocking",
        specific_improvements=["Improve defensive timing", "Better counter-attacks"]
    )
    
    evolution_prompt = manager.generate_agent_prompt(evolution_context)
    print(f"Evolution prompt contains parent: {'✅ PASS' if parent_code in evolution_prompt else '❌ FAIL'}")
    print(f"Evolution prompt contains feedback: {'✅ PASS' if 'blocking' in evolution_prompt else '❌ FAIL'}")
    
    print(f"\n📊 Prompt Template Tests Complete")

if __name__ == "__main__":
    test_prompt_templates()
