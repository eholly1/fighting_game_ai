#!/usr/bin/env python3
"""
Integration Test for Top Agent Tracking (Phase 3)

Tests the complete agent tracking pipeline: Hall of Fame + Experiment Manager + Serialization
"""
import sys
import os
import time
import shutil
import json

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from hall_of_fame import HallOfFame, AgentRecord
from experiment_manager import ExperimentManager, ExperimentConfig
from agent_serialization import AgentSerializer

def create_test_agents(generation: int, count: int = 5):
    """Create test agents with varying performance"""
    agents = []
    
    fighting_styles = ['aggressive', 'defensive', 'zoner', 'balanced', 'adaptive']
    
    for i in range(count):
        # Create agents with different fitness levels
        base_fitness = 60 + (i * 8) + (generation * 2)  # Improving over generations
        
        agent_data = {
            'agent_id': f'gen{generation}_agent_{i:03d}',
            'fitness': base_fitness + (i * 5),  # Spread fitness values
            'win_rate': 0.5 + (i * 0.1),
            'avg_reward': base_fitness * 1.2,
            'code': f'''
def get_action(state):
    """Generation {generation} agent {i} - {fighting_styles[i % len(fighting_styles)]} style"""
    distance = state[22]
    relative_pos = state[23]
    health_advantage = state[25]
    
    # {fighting_styles[i % len(fighting_styles)]} strategy
    if distance < 0.15:
        return {4 + (i % 2)}  # Punch or kick
    elif distance < 0.3:
        return 2 if relative_pos > 0 else 1  # Move toward opponent
    else:
        return 9  # Projectile
''',
            'fighting_style': fighting_styles[i % len(fighting_styles)],
            'tournament_stats': {
                'wins': 10 + i,
                'losses': 5 - i,
                'total_matches': 15
            },
            'lineage': [f'gen{generation-1}_agent_{(i-1):03d}'] if generation > 0 else []
        }
        
        agents.append(agent_data)
    
    return agents

def test_hall_of_fame_integration():
    """Test Hall of Fame with multiple generations"""
    print("🏆 Testing Hall of Fame Integration")
    print("-" * 40)
    
    test_dir = f"test_hof_{int(time.time())}"
    
    try:
        # Initialize Hall of Fame
        hof = HallOfFame(test_dir, max_agents=10)
        
        # Simulate 3 generations
        for generation in range(3):
            agents = create_test_agents(generation, count=4)
            hof.add_agents(agents, generation)
            
            print(f"   Generation {generation}: Added {len(agents)} agents")
        
        # Test results
        top_agents = hof.get_top_agents(5)
        stats = hof.get_hall_of_fame_stats()
        
        # Verify ranking (should be sorted by fitness)
        fitness_values = [agent.fitness for agent in top_agents]
        is_sorted = all(fitness_values[i] >= fitness_values[i+1] for i in range(len(fitness_values)-1))
        
        print(f"   ✅ Ranking correct: {is_sorted}")
        print(f"   ✅ Total agents: {stats['total_agents']}")
        print(f"   ✅ Best fitness: {stats['best_fitness']:.1f}")
        print(f"   ✅ Generation range: {stats['generation_range']}")
        
        # Check file generation
        agent_files = [f for f in os.listdir(hof.hall_of_fame_dir) if f.endswith('.py')]
        files_correct = len(agent_files) == len(hof.agents)
        
        print(f"   ✅ Agent files: {len(agent_files)} files created")
        
        return is_sorted and files_correct and stats['total_agents'] > 0
        
    except Exception as e:
        print(f"   ❌ Hall of Fame integration failed: {e}")
        return False
    
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

def test_experiment_manager_integration():
    """Test Experiment Manager with full workflow"""
    print("\n🧪 Testing Experiment Manager Integration")
    print("-" * 40)
    
    try:
        # Create experiment
        config = ExperimentConfig(
            population_size=8,
            generations=3,
            max_agents_hall_of_fame=15
        )
        
        experiment = ExperimentManager("test_integration", config)
        
        # Simulate evolutionary run
        for generation in range(3):
            # Start generation
            experiment.log_generation_start(generation, config.population_size)
            
            # Create agents for this generation
            agents = create_test_agents(generation, count=config.population_size)
            
            # Simulate tournament results
            tournament_results = {
                'total_matches': 20,
                'avg_fitness': sum(a['fitness'] for a in agents) / len(agents),
                'best_agent': max(agents, key=lambda x: x['fitness'])['agent_id'],
                'valid_agents': len(agents)
            }
            
            # Save tournament results
            experiment.save_tournament_results(generation, tournament_results)
            
            # Update evolution summary
            summary_stats = {
                'best_fitness': max(a['fitness'] for a in agents),
                'avg_fitness': tournament_results['avg_fitness'],
                'valid_agents': len(agents),
                'total_matches': tournament_results['total_matches']
            }
            
            experiment.update_evolution_summary(generation, summary_stats)
            
            # Log completion
            experiment.log_generation_complete(generation, summary_stats)
            
            print(f"   Generation {generation}: Best fitness {summary_stats['best_fitness']:.1f}")
        
        # Test progress tracking
        progress = experiment.get_experiment_progress()
        progress_correct = (progress['current_generation'] == 2 and 
                           progress['total_generations'] == 3)
        
        print(f"   ✅ Progress tracking: {progress_correct}")
        
        # Test analysis report
        report_path = experiment.create_analysis_report()
        report_exists = os.path.exists(report_path)
        
        print(f"   ✅ Analysis report: {report_exists}")
        
        # Check file structure
        required_files = ['config.json', 'experiment.log', 'evolution_summary.json']
        files_exist = all(os.path.exists(os.path.join(experiment.experiment_dir, f)) 
                         for f in required_files)
        
        print(f"   ✅ Required files: {files_exist}")
        
        return progress_correct and report_exists and files_exist
        
    except Exception as e:
        print(f"   ❌ Experiment Manager integration failed: {e}")
        return False
    
    finally:
        # Cleanup
        if 'experiment' in locals() and os.path.exists(experiment.experiment_dir):
            shutil.rmtree(experiment.experiment_dir)

def test_agent_serialization_integration():
    """Test Agent Serialization with realistic data"""
    print("\n💾 Testing Agent Serialization Integration")
    print("-" * 40)
    
    test_dir = f"test_serialization_{int(time.time())}"
    
    try:
        serializer = AgentSerializer(test_dir)
        
        # Create and save multiple agents
        agents = create_test_agents(generation=5, count=3)
        saved_paths = []
        
        for agent_data in agents:
            # Save as Python file
            py_path = serializer.save_agent_python(
                agent_data['agent_id'],
                agent_data['code'],
                {k: v for k, v in agent_data.items() if k != 'code'}
            )
            saved_paths.append(py_path)
            
            # Save as JSON file
            json_path = serializer.save_agent_json(
                agent_data['agent_id'] + "_json",
                agent_data['code'],
                {k: v for k, v in agent_data.items() if k != 'code'}
            )
            saved_paths.append(json_path)
        
        print(f"   ✅ Saved {len(saved_paths)} agent files")
        
        # Test loading and validation
        loaded_count = 0
        valid_count = 0
        
        for path in saved_paths:
            if path.endswith('.py'):
                agent = serializer.load_agent_python(path)
            else:
                agent = serializer.load_agent_json(path)
            
            if agent:
                loaded_count += 1
                if serializer.validate_agent_code(agent.code):
                    valid_count += 1
        
        print(f"   ✅ Loaded {loaded_count}/{len(saved_paths)} agents")
        print(f"   ✅ Valid code: {valid_count}/{loaded_count} agents")
        
        # Test agent listing and summaries
        py_files = serializer.list_agents(".py")
        json_files = serializer.list_agents(".json")
        
        print(f"   ✅ Listed {len(py_files)} Python files, {len(json_files)} JSON files")
        
        # Test summaries
        summaries = []
        for path in py_files[:2]:  # Test first 2
            summary = serializer.get_agent_summary(path)
            if summary:
                summaries.append(summary)
        
        summaries_correct = len(summaries) == 2 and all('fitness' in s for s in summaries)
        print(f"   ✅ Agent summaries: {summaries_correct}")
        
        return (loaded_count == len(saved_paths) and 
                valid_count == loaded_count and 
                summaries_correct)
        
    except Exception as e:
        print(f"   ❌ Agent Serialization integration failed: {e}")
        return False
    
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

def test_complete_integration():
    """Test complete integration of all Phase 3 components"""
    print("\n🔗 Testing Complete Phase 3 Integration")
    print("-" * 40)
    
    try:
        # Create experiment with all components
        config = ExperimentConfig(
            population_size=6,
            generations=2,
            max_agents_hall_of_fame=10
        )
        
        experiment = ExperimentManager("complete_integration_test", config)
        hof = HallOfFame(experiment.experiment_dir, max_agents=config.max_agents_hall_of_fame)
        serializer = AgentSerializer(os.path.join(experiment.experiment_dir, "agent_archive"))
        
        # Simulate complete evolutionary run
        all_agents_created = 0
        
        for generation in range(config.generations):
            experiment.log_generation_start(generation, config.population_size)
            
            # Create generation
            agents = create_test_agents(generation, config.population_size)
            all_agents_created += len(agents)
            
            # Add to Hall of Fame
            hof.add_agents(agents, generation)
            
            # Archive all agents
            for agent_data in agents:
                serializer.save_agent_python(
                    agent_data['agent_id'],
                    agent_data['code'],
                    {k: v for k, v in agent_data.items() if k != 'code'}
                )
            
            # Update experiment tracking
            summary_stats = {
                'best_fitness': max(a['fitness'] for a in agents),
                'avg_fitness': sum(a['fitness'] for a in agents) / len(agents),
                'valid_agents': len(agents),
                'hall_of_fame_size': len(hof.agents)
            }
            
            experiment.update_evolution_summary(generation, summary_stats)
            experiment.log_generation_complete(generation, summary_stats)
        
        # Verify integration
        hof_stats = hof.get_hall_of_fame_stats()
        progress = experiment.get_experiment_progress()
        archived_files = serializer.list_agents(".py")
        
        print(f"   ✅ Agents created: {all_agents_created}")
        print(f"   ✅ Hall of Fame: {hof_stats['total_agents']}/{config.max_agents_hall_of_fame}")
        print(f"   ✅ Archived files: {len(archived_files)}")
        print(f"   ✅ Experiment progress: {progress['progress_percent']:.1f}%")
        print(f"   ✅ Best fitness: {hof_stats['best_fitness']:.1f}")
        
        # Check that everything is properly connected
        integration_success = (
            hof_stats['total_agents'] > 0 and
            len(archived_files) == all_agents_created and
            progress['current_generation'] == config.generations - 1 and
            hof_stats['best_fitness'] > 60
        )
        
        return integration_success
        
    except Exception as e:
        print(f"   ❌ Complete integration failed: {e}")
        return False
    
    finally:
        # Cleanup
        if 'experiment' in locals() and os.path.exists(experiment.experiment_dir):
            shutil.rmtree(experiment.experiment_dir)

def main():
    """Run all Phase 3 integration tests"""
    print("🔧 Top Agent Tracking - Phase 3 Integration Testing")
    print("=" * 70)
    
    # Run individual component tests
    test1_passed = test_hall_of_fame_integration()
    test2_passed = test_experiment_manager_integration()
    test3_passed = test_agent_serialization_integration()
    test4_passed = test_complete_integration()
    
    print(f"\n🏁 Phase 3 Integration Test Results")
    print("=" * 50)
    print(f"  Hall of Fame:        {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Experiment Manager:  {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"  Agent Serialization: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    print(f"  Complete Integration:{'✅ PASS' if test4_passed else '❌ FAIL'}")
    
    all_passed = test1_passed and test2_passed and test3_passed and test4_passed
    
    if all_passed:
        print(f"\n🎉 Phase 3: Top Agent Tracking - COMPLETE!")
        print(f"   ✅ Hall of Fame system with top 100 agent preservation")
        print(f"   ✅ Experiment management with organized directory structure")
        print(f"   ✅ Agent serialization with multiple formats")
        print(f"   ✅ Complete integration and workflow coordination")
        print(f"\n🚀 Ready for Phase 4: Integration Testing")
    else:
        print(f"\n❌ Phase 3 has issues that need to be addressed")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
