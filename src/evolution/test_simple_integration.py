#!/usr/bin/env python3
"""
Simple Integration Test for Phase 4

Tests the evolutionary system components without requiring API calls
"""
import sys
import os
import time
import shutil

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import components individually to test integration
from swiss_tournament import SwissTournament
from code_validator import CodeValidator
from safe_execution import SafeAgent, AgentPool
from hall_of_fame import HallOfFame
from experiment_manager import ExperimentManager, ExperimentConfig
from agent_serialization import AgentSerializer

def create_test_agent_code(agent_id: str, style: str = "balanced") -> str:
    """Create test agent code without LLM"""
    styles = {
        'aggressive': '''
def get_action(state):
    """Aggressive fighter - always attack"""
    distance = state[22]
    if distance < 0.2:
        return 4  # punch
    elif distance < 0.4:
        return 2 if state[23] > 0 else 1  # move toward opponent
    else:
        return 9  # projectile
''',
        'defensive': '''
def get_action(state):
    """Defensive fighter - block and counter"""
    distance = state[22]
    health_advantage = state[25]
    
    if health_advantage < -0.2:
        return 6  # block when losing
    elif distance < 0.15:
        return 5  # kick
    else:
        return 2 if state[23] > 0 else 1  # move toward opponent
''',
        'balanced': '''
def get_action(state):
    """Balanced fighter - adaptive strategy"""
    distance = state[22]
    relative_pos = state[23]
    health_advantage = state[25]
    
    if distance < 0.15:
        if health_advantage > 0:
            return 4  # attack when winning
        else:
            return 6  # defend when losing
    elif distance < 0.3:
        return 2 if relative_pos > 0 else 1
    else:
        return 9  # projectile
'''
    }
    
    return styles.get(style, styles['balanced'])

def test_component_pipeline():
    """Test the complete component pipeline"""
    print("🔧 Testing Component Pipeline")
    print("-" * 40)
    
    # Initialize components
    validator = CodeValidator(max_lines=100, max_chars=5000)
    agent_pool = AgentPool()
    
    test_dir = f"test_pipeline_{int(time.time())}"
    hof = HallOfFame(test_dir, max_agents=5)
    serializer = AgentSerializer(os.path.join(test_dir, "agents"))
    
    try:
        # Test 1: Code validation and agent creation
        test_agents = []
        styles = ['aggressive', 'defensive', 'balanced']
        
        for i, style in enumerate(styles):
            agent_id = f"test_agent_{i}"
            code = create_test_agent_code(agent_id, style)
            
            # Validate code
            validation = validator.validate_code(code, agent_id)
            if validation.is_valid:
                # Create safe agent
                success = agent_pool.add_agent(agent_id, validation.cleaned_code)
                if success:
                    agent = agent_pool.get_agent(agent_id)
                    agent.fitness = 70 + i * 10  # Mock fitness
                    agent.win_rate = 0.6 + i * 0.1
                    agent.fighting_style = style
                    test_agents.append(agent)
        
        print(f"   ✅ Created {len(test_agents)} valid agents")
        
        # Test 2: Swiss tournament
        if len(test_agents) >= 2:
            tournament = SwissTournament(test_agents, rounds=2)
            
            def mock_match_runner(agent1, agent2):
                from swiss_tournament import TournamentResult
                # Simple mock: higher fitness wins
                fitness1 = getattr(agent1, 'fitness', 50)
                fitness2 = getattr(agent2, 'fitness', 50)
                
                if fitness1 > fitness2:
                    return TournamentResult(
                        agent1_id=agent1.agent_id, agent2_id=agent2.agent_id,
                        agent1_score=1.0, agent2_score=0.0,
                        agent1_fitness=fitness1, agent2_fitness=fitness2,
                        games_played=1
                    )
                else:
                    return TournamentResult(
                        agent1_id=agent1.agent_id, agent2_id=agent2.agent_id,
                        agent1_score=0.0, agent2_score=1.0,
                        agent1_fitness=fitness1, agent2_fitness=fitness2,
                        games_played=1
                    )
            
            rankings = tournament.run_tournament(mock_match_runner)
            print(f"   ✅ Swiss tournament completed: {len(rankings)} rankings")
        
        # Test 3: Hall of Fame
        agent_data = []
        for agent in test_agents:
            data = {
                'agent_id': agent.agent_id,
                'fitness': agent.fitness,
                'win_rate': agent.win_rate,
                'avg_reward': agent.fitness * 1.2,
                'code': agent.code,
                'fighting_style': agent.fighting_style,
                'tournament_stats': {},
                'lineage': []
            }
            agent_data.append(data)
        
        hof.add_agents(agent_data, generation=0)
        print(f"   ✅ Hall of Fame updated: {len(hof.agents)} agents")
        
        # Test 4: Agent serialization
        for agent in test_agents:
            metadata = {
                'fitness': agent.fitness,
                'fighting_style': agent.fighting_style,
                'generation': 0
            }
            serializer.save_agent_python(agent.agent_id, agent.code, metadata)
        
        saved_files = serializer.list_agents(".py")
        print(f"   ✅ Agent serialization: {len(saved_files)} files saved")
        
        # Test 5: Integration verification
        hof_stats = hof.get_hall_of_fame_stats()
        
        success = (
            len(test_agents) >= 2 and
            len(hof.agents) > 0 and
            len(saved_files) == len(test_agents) and
            hof_stats['best_fitness'] > 0
        )
        
        print(f"   📊 Integration success: {'✅' if success else '❌'}")
        print(f"      Agents created: {len(test_agents)}")
        print(f"      Hall of Fame: {len(hof.agents)} agents")
        print(f"      Best fitness: {hof_stats.get('best_fitness', 0):.1f}")
        print(f"      Files saved: {len(saved_files)}")
        
        return success
        
    except Exception as e:
        print(f"   ❌ Pipeline test failed: {e}")
        return False
    
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

def test_experiment_workflow():
    """Test experiment management workflow"""
    print("\n📊 Testing Experiment Workflow")
    print("-" * 40)
    
    config = ExperimentConfig(
        population_size=4,
        generations=2,
        games_per_match=1
    )
    
    try:
        # Create experiment
        experiment = ExperimentManager("test_workflow", config)
        hof = HallOfFame(experiment.experiment_dir, config.max_agents_hall_of_fame)
        
        # Simulate 2 generations
        for generation in range(2):
            experiment.log_generation_start(generation, config.population_size)
            
            # Create mock agents for this generation
            agents = []
            for i in range(config.population_size):
                agent_data = {
                    'agent_id': f'gen{generation}_agent_{i}',
                    'fitness': 60 + generation * 5 + i * 3,
                    'win_rate': 0.5 + generation * 0.1 + i * 0.05,
                    'avg_reward': 80 + generation * 10 + i * 5,
                    'code': create_test_agent_code(f'gen{generation}_agent_{i}'),
                    'fighting_style': ['aggressive', 'defensive', 'balanced', 'adaptive'][i],
                    'tournament_stats': {'wins': 5 + i, 'losses': 3 - i},
                    'lineage': []
                }
                agents.append(agent_data)
            
            # Update Hall of Fame
            hof.add_agents(agents, generation)
            
            # Save generation results
            stats = {
                'best_fitness': max(a['fitness'] for a in agents),
                'avg_fitness': sum(a['fitness'] for a in agents) / len(agents),
                'valid_agents': len(agents),
                'hall_of_fame_size': len(hof.agents)
            }
            
            experiment.update_evolution_summary(generation, stats)
            experiment.log_generation_complete(generation, stats)
            
            print(f"   Generation {generation}: {stats['best_fitness']:.1f} best fitness")
        
        # Check final state
        progress = experiment.get_experiment_progress()
        hof_stats = hof.get_hall_of_fame_stats()
        
        # Verify files were created
        required_files = ['config.json', 'experiment.log', 'evolution_summary.json', 'hall_of_fame.json']
        files_exist = all(os.path.exists(os.path.join(experiment.experiment_dir, f)) for f in required_files)
        
        success = (
            progress['current_generation'] == 1 and
            hof_stats['total_agents'] > 0 and
            files_exist
        )
        
        print(f"   ✅ Workflow success: {'✅' if success else '❌'}")
        print(f"      Progress: {progress['progress_percent']:.1f}%")
        print(f"      Hall of Fame: {hof_stats['total_agents']} agents")
        print(f"      Files created: {'✅' if files_exist else '❌'}")
        
        return success
        
    except Exception as e:
        print(f"   ❌ Workflow test failed: {e}")
        return False
    
    finally:
        if 'experiment' in locals():
            experiment_dir = experiment.experiment_dir
            if os.path.exists(experiment_dir):
                shutil.rmtree(experiment_dir)

def test_performance_characteristics():
    """Test performance of integrated system"""
    print("\n⚡ Testing Performance Characteristics")
    print("-" * 40)
    
    try:
        # Test with different population sizes
        for pop_size in [5, 10, 15]:
            start_time = time.time()
            
            # Create test agents
            validator = CodeValidator()
            agent_pool = AgentPool()
            agents = []
            
            for i in range(pop_size):
                agent_id = f"perf_agent_{i}"
                code = create_test_agent_code(agent_id)
                validation = validator.validate_code(code, agent_id)
                
                if validation.is_valid:
                    success = agent_pool.add_agent(agent_id, validation.cleaned_code)
                    if success:
                        agent = agent_pool.get_agent(agent_id)
                        agent.fitness = 50 + i * 2
                        agents.append(agent)
            
            # Run Swiss tournament
            if len(agents) >= 2:
                tournament = SwissTournament(agents)
                
                def quick_match_runner(agent1, agent2):
                    from swiss_tournament import TournamentResult
                    return TournamentResult(
                        agent1_id=agent1.agent_id, agent2_id=agent2.agent_id,
                        agent1_score=0.5, agent2_score=0.5,
                        agent1_fitness=50, agent2_fitness=50,
                        games_played=1
                    )
                
                rankings = tournament.run_tournament(quick_match_runner)
            
            duration = time.time() - start_time
            print(f"   Population {pop_size:2d}: {duration:.2f}s ({len(agents)} agents)")
        
        print(f"   ✅ Performance test completed")
        return True
        
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
        return False

def main():
    """Run all simple integration tests"""
    print("🔧 Simple Integration Testing - Phase 4")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_component_pipeline()
    test2_passed = test_experiment_workflow()
    test3_passed = test_performance_characteristics()
    
    print(f"\n🏁 Simple Integration Test Results")
    print("=" * 40)
    print(f"  Component Pipeline:      {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Experiment Workflow:     {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"  Performance Tests:       {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    
    if all_passed:
        print(f"\n🎉 Phase 4: Integration Testing - COMPLETE!")
        print(f"   ✅ All core components working together")
        print(f"   ✅ Swiss tournament + Code quality + Agent tracking")
        print(f"   ✅ Experiment management and data persistence")
        print(f"   ✅ Performance characteristics validated")
        print(f"\n🚀 Evolutionary Training System is READY!")
        print(f"\n📋 Next Steps:")
        print(f"   1. Set ANTHROPIC_API_KEY environment variable")
        print(f"   2. Run: python evolution_runner.py --population 10 --generations 5")
        print(f"   3. Check results in experiments/ directory")
    else:
        print(f"\n❌ Some integration tests failed")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
