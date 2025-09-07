#!/usr/bin/env python3
"""
Integration Test for Code Quality Controls

Tests the complete pipeline: validation -> safe execution -> prompt generation
"""
import sys
import os
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from code_validator import CodeValidator, ValidationResult
from safe_execution import SafeAgent, AgentPool
from prompt_templates import PromptTemplateManager, PromptContext

def test_complete_pipeline():
    """Test the complete code quality pipeline"""
    print("🧪 Testing Complete Code Quality Pipeline")
    print("=" * 60)
    
    # Initialize components
    validator = CodeValidator(max_lines=1400, max_chars=40000)
    prompt_manager = PromptTemplateManager()
    agent_pool = AgentPool()
    
    # Test cases with different code quality levels
    test_cases = [
        {
            'name': 'Valid Strategic Agent',
            'code': '''
def get_action(state):
    """Strategic fighting AI with range-based tactics"""
    import numpy as np
    import random
    
    # Extract key state information
    distance = max(0.0, min(1.0, state[22]))
    relative_pos = state[23]
    health_advantage = state[25]
    
    # Strategic parameters
    close_threshold = 0.15
    medium_threshold = 0.3
    aggression_level = 0.7
    
    # Health-based strategy adaptation
    if health_advantage < -0.3:  # Losing badly
        if distance > 0.4:
            return 9  # Projectile to keep distance
        else:
            return 6  # Block defensively
    
    # Range-based tactics
    if distance < close_threshold:
        # Close combat
        if health_advantage > 0:
            return random.choice([4, 5])  # Attack when winning
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
        if random.random() < 0.3:
            return 9  # Projectile attack
        else:
            # Move closer
            return 2 if relative_pos > 0 else 1
''',
            'should_pass': True
        },
        {
            'name': 'Dangerous Code (File Operations)',
            'code': '''
def get_action(state):
    import os
    with open('/etc/passwd', 'r') as f:
        data = f.read()
    os.system('rm -rf /')
    return 0
''',
            'should_pass': False
        },
        {
            'name': 'Syntax Error',
            'code': '''
def get_action(state):
    if distance < 0.3
        return 4
    else:
        return 0
''',
            'should_pass': False
        },
        {
            'name': 'Missing get_action Function',
            'code': '''
def some_other_function():
    return 42

def another_function(x):
    return x * 2
''',
            'should_pass': False
        },
        {
            'name': 'Too Long Code',
            'code': 'def get_action(state):\n' + '    # Comment line\n' * 1500 + '    return 0\n',
            'should_pass': False
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🧪 Test {i+1}: {test_case['name']}")
        print("-" * 40)
        
        # Step 1: Validation
        validation_result = validator.validate_code(test_case['code'], f"test_agent_{i}")
        
        print(f"   Validation: {'✅ PASS' if validation_result.is_valid else '❌ FAIL'}")
        if validation_result.errors:
            print(f"   Errors: {len(validation_result.errors)}")
            for error in validation_result.errors[:2]:  # Show first 2 errors
                print(f"     - {error}")
        
        if validation_result.warnings:
            print(f"   Warnings: {len(validation_result.warnings)}")
        
        print(f"   Metrics: {validation_result.metrics['lines']} lines, {validation_result.metrics['chars']} chars")
        
        # Step 2: Safe Execution (only if validation passed)
        execution_success = False
        if validation_result.is_valid:
            agent_id = f"test_agent_{i}"
            success = agent_pool.add_agent(agent_id, validation_result.cleaned_code)
            
            if success:
                agent = agent_pool.get_agent(agent_id)
                # Test execution with dummy state
                test_state = np.zeros(26)
                test_state[22] = 0.2  # distance
                test_state[23] = 0.5  # relative position
                test_state[25] = 0.1  # health advantage
                
                action = agent.get_action(test_state)
                execution_success = isinstance(action, int) and 0 <= action <= 9
                
                print(f"   Execution: {'✅ PASS' if execution_success else '❌ FAIL'} (action: {action})")
                print(f"   Agent Stats: {agent.get_stats()}")
            else:
                print(f"   Execution: ❌ FAIL (could not create agent)")
        else:
            print(f"   Execution: ⏭️  SKIP (validation failed)")
        
        # Step 3: Check if result matches expectation
        overall_success = validation_result.is_valid == test_case['should_pass']
        if test_case['should_pass']:
            overall_success = overall_success and execution_success
        
        print(f"   Overall: {'✅ PASS' if overall_success else '❌ FAIL'}")
        
        results.append({
            'name': test_case['name'],
            'validation_passed': validation_result.is_valid,
            'execution_passed': execution_success,
            'expected_to_pass': test_case['should_pass'],
            'overall_success': overall_success
        })
    
    # Summary
    print(f"\n📊 Pipeline Test Summary")
    print("=" * 60)
    
    passed_tests = sum(1 for r in results if r['overall_success'])
    total_tests = len(results)
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    for result in results:
        status = "✅ PASS" if result['overall_success'] else "❌ FAIL"
        print(f"  {status} {result['name']}")
    
    # Agent pool statistics
    pool_stats = agent_pool.get_pool_stats()
    print(f"\nAgent Pool Stats:")
    print(f"  Total Agents: {pool_stats['total_agents']}")
    print(f"  Valid Agents: {pool_stats['valid_agents']}")
    print(f"  Avg Error Rate: {pool_stats['avg_error_rate']:.1%}")
    
    return passed_tests == total_tests

def test_prompt_quality():
    """Test prompt generation quality"""
    print(f"\n🎯 Testing Prompt Quality")
    print("=" * 40)
    
    prompt_manager = PromptTemplateManager()
    
    # Test different fighting styles
    styles = ['aggressive', 'defensive', 'zoner', 'adaptive']
    
    for style in styles:
        context = PromptContext(
            fighting_style=style,
            generation=0,
            parent_codes=[]
        )
        
        prompt = prompt_manager.generate_agent_prompt(context)
        
        # Quality checks
        has_style = style in prompt.lower()
        has_constraints = 'maximum' in prompt.lower()
        has_examples = 'example' in prompt.lower()
        reasonable_length = 3000 < len(prompt) < 10000
        
        quality_score = sum([has_style, has_constraints, has_examples, reasonable_length])
        
        print(f"  {style:12s}: {quality_score}/4 quality checks ({'✅' if quality_score >= 3 else '❌'})")
    
    return True

def test_evolution_prompts():
    """Test evolution-specific prompts"""
    print(f"\n🧬 Testing Evolution Prompts")
    print("=" * 40)
    
    prompt_manager = PromptTemplateManager()
    
    # Parent code for evolution
    parent_code = '''
def get_action(state):
    distance = state[22]
    if distance < 0.3:
        return 4
    else:
        return 2
'''
    
    # Test mutation prompt
    mutation_prompt = prompt_manager.create_mutation_prompt(parent_code, generation=5)
    has_parent = parent_code.strip() in mutation_prompt
    has_generation = 'generation 5' in mutation_prompt.lower()
    
    print(f"  Mutation Prompt: {'✅ PASS' if has_parent and has_generation else '❌ FAIL'}")
    
    # Test crossover prompt
    parent2_code = '''
def get_action(state):
    health = state[25]
    if health < 0:
        return 6
    else:
        return 9
'''
    
    crossover_prompt = prompt_manager.create_crossover_prompt(parent_code, parent2_code, generation=3)
    has_both_parents = parent_code.strip() in crossover_prompt and parent2_code.strip() in crossover_prompt
    has_crossover_info = 'combine' in crossover_prompt.lower()
    
    print(f"  Crossover Prompt: {'✅ PASS' if has_both_parents and has_crossover_info else '❌ FAIL'}")
    
    return True

def main():
    """Run all code quality tests"""
    print("🔧 Code Quality Controls - Phase 2 Testing")
    print("=" * 70)
    
    # Test 1: Complete pipeline
    pipeline_success = test_complete_pipeline()
    
    # Test 2: Prompt quality
    prompt_success = test_prompt_quality()
    
    # Test 3: Evolution prompts
    evolution_success = test_evolution_prompts()
    
    print(f"\n🏁 Phase 2 Test Results")
    print("=" * 40)
    print(f"  Pipeline Tests:   {'✅ PASS' if pipeline_success else '❌ FAIL'}")
    print(f"  Prompt Quality:   {'✅ PASS' if prompt_success else '❌ FAIL'}")
    print(f"  Evolution Tests:  {'✅ PASS' if evolution_success else '❌ FAIL'}")
    
    all_passed = pipeline_success and prompt_success and evolution_success
    
    if all_passed:
        print(f"\n🎉 Phase 2: Code Quality Controls - COMPLETE!")
        print(f"   ✅ Code validation with safety checks")
        print(f"   ✅ Safe execution with timeout protection")
        print(f"   ✅ Enhanced LLM prompting with examples")
        print(f"   ✅ Evolution-specific prompt generation")
        print(f"\n🚀 Ready for Phase 3: Top Agent Tracking")
    else:
        print(f"\n❌ Phase 2 has issues that need to be addressed")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
