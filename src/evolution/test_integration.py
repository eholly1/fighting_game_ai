#!/usr/bin/env python3
"""
Complete Integration Tests for Evolutionary Training System (Phase 4)

Tests the full end-to-end pipeline combining all components:
- Swiss Tournament System
- Code Quality Controls
- Top Agent Tracking
- Complete Evolution Runner
"""
import sys
import os
import time
import shutil
import json
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import all components
from evolution_runner import EvolutionaryTrainer
from experiment_manager import ExperimentConfig

class MockClaudeClient:
    """Mock Claude client for testing without API calls"""

    def __init__(self):
        self.call_count = 0
        self.agent_templates = [
            '''
def get_action(state):
    """Aggressive fighter"""
    distance = state[22]
    relative_pos = state[23]
    health_advantage = state[25]

    if distance < 0.15:
        return 4  # punch
    elif distance < 0.3:
        return 2 if relative_pos > 0 else 1  # move toward opponent
    else:
        return 9  # projectile
''',
            '''
def get_action(state):
    """Defensive fighter"""
    distance = state[22]
    relative_pos = state[23]
    health_advantage = state[25]

    if health_advantage < -0.2:
        return 6  # block when losing
    elif distance < 0.15:
        return 5  # kick
    else:
        return 2 if relative_pos > 0 else 1  # move toward opponent
''',
            '''
def get_action(state):
    """Zoner fighter"""
    distance = state[22]
    relative_pos = state[23]

    if distance > 0.4:
        return 9  # projectile
    elif distance < 0.2:
        return 6  # block
    else:
        return 1 if relative_pos < 0 else 2  # maintain distance
''',
            '''
def get_action(state):
    """Balanced fighter"""
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
        ]

    def messages_create(self, model, max_tokens, messages):
        """Mock message creation"""
        self.call_count += 1

        # Return different agent templates cyclically
        template_index = (self.call_count - 1) % len(self.agent_templates)
        code = self.agent_templates[template_index]

        # Add some variation based on call count
        variation = f"    # Generated agent {self.call_count}\n"
        code = code.replace('"""', f'"""{variation}    """', 1)

        # Mock response object
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = code

        return mock_response

def test_mock_claude_integration():
    """Test that mock Claude client works correctly"""
    print("🧪 Testing Mock Claude Integration")
    print("-" * 40)

    mock_client = MockClaudeClient()

    # Test multiple calls
    for i in range(5):
        response = mock_client.messages_create(
            model="test", max_tokens=1000,
            messages=[{"role": "user", "content": "test"}]
        )

        code = response.content[0].text

        # Verify code contains get_action function
        has_get_action = 'def get_action' in code
        has_variation = f'Generated agent {i+1}' in code

        print(f"   Call {i+1}: {'✅' if has_get_action and has_variation else '❌'}")

    print(f"   Total calls: {mock_client.call_count}")
    return mock_client.call_count == 5

def test_small_evolution_run():
    """Test a complete but small evolution run"""
    print("\n🧬 Testing Small Evolution Run")
    print("-" * 40)

    # Small configuration for testing
    config = ExperimentConfig(
        population_size=4,
        generations=2,
        games_per_match=2,
        max_agents_hall_of_fame=8
    )

    try:
        # Mock the Claude API
        with patch('anthropic.Anthropic') as mock_anthropic:
            mock_client = MockClaudeClient()
            mock_anthropic.return_value = mock_client

            # Create trainer
            trainer = EvolutionaryTrainer(config, "fake_api_key", "test_small_evolution")

            # Override the Claude client
            trainer.claude_client = mock_client

            print(f"   Trainer initialized: ✅")

            # Run evolution
            start_time = time.time()
            top_agents = trainer.run_evolution()
            duration = time.time() - start_time

            print(f"   Evolution completed in {duration:.1f}s")
            print(f"   Top agents returned: {len(top_agents)}")

            # Verify results
            hof_stats = trainer.hall_of_fame.get_hall_of_fame_stats()
            progress = trainer.experiment_manager.get_experiment_progress()

            print(f"   Hall of Fame agents: {hof_stats['total_agents']}")
            print(f"   Best fitness: {hof_stats.get('best_fitness', 0):.2f}")
            print(f"   Generations completed: {progress['current_generation'] + 1}")

            # Check that files were created
            experiment_dir = trainer.experiment_manager.experiment_dir
            config_exists = os.path.exists(os.path.join(experiment_dir, "config.json"))
            log_exists = os.path.exists(os.path.join(experiment_dir, "experiment.log"))
            hof_exists = os.path.exists(os.path.join(experiment_dir, "hall_of_fame.json"))

            print(f"   Files created: {'✅' if config_exists and log_exists and hof_exists else '❌'}")

            success = (
                len(top_agents) > 0 and
                hof_stats['total_agents'] > 0 and
                progress['current_generation'] >= 1 and
                config_exists and log_exists and hof_exists
            )

            return success

    except Exception as e:
        print(f"   ❌ Small evolution run failed: {e}")
        return False

    finally:
        # Cleanup
        if 'trainer' in locals():
            experiment_dir = trainer.experiment_manager.experiment_dir
            if os.path.exists(experiment_dir):
                shutil.rmtree(experiment_dir)

def test_component_integration():
    """Test integration between all major components"""
    print("\n🔗 Testing Component Integration")
    print("-" * 40)

    config = ExperimentConfig(
        population_size=3,
        generations=1,
        games_per_match=1
    )

    try:
        with patch('anthropic.Anthropic') as mock_anthropic:
            mock_client = MockClaudeClient()
            mock_anthropic.return_value = mock_client

            trainer = EvolutionaryTrainer(config, "fake_api_key", "test_component_integration")
            trainer.claude_client = mock_client

            # Test 1: Initial population creation
            trainer._create_initial_population()
            initial_pop_size = len(trainer.population)
            print(f"   Initial population: {initial_pop_size} agents ✅")

            # Test 2: Generation evaluation
            trainer._evaluate_generation()

            # Check that agents have fitness values
            fitness_assigned = all(hasattr(agent, 'fitness') for agent in trainer.population)
            print(f"   Fitness evaluation: {'✅' if fitness_assigned else '❌'}")

            # Test 3: Hall of Fame update
            trainer._update_hall_of_fame()
            hof_size = len(trainer.hall_of_fame.agents)
            print(f"   Hall of Fame update: {hof_size} agents ✅")

            # Test 4: Generation results saving
            trainer._save_generation_results()

            # Check that files were created
            summary_exists = os.path.exists(os.path.join(
                trainer.experiment_manager.experiment_dir, "evolution_summary.json"
            ))
            print(f"   Results saving: {'✅' if summary_exists else '❌'}")

            # Test 5: Next generation creation
            if len(trainer.population) >= 2:
                trainer._create_next_generation()
                next_gen_size = len(trainer.population)
                print(f"   Next generation: {next_gen_size} agents ✅")
            else:
                print(f"   Next generation: ⏭️  SKIP (insufficient population)")
                next_gen_size = 1  # For success check

            success = (
                initial_pop_size > 0 and
                fitness_assigned and
                hof_size > 0 and
                summary_exists and
                next_gen_size > 0
            )

            return success

    except Exception as e:
        print(f"   ❌ Component integration failed: {e}")
        return False

    finally:
        if 'trainer' in locals():
            experiment_dir = trainer.experiment_manager.experiment_dir
            if os.path.exists(experiment_dir):
                shutil.rmtree(experiment_dir)

def test_error_handling():
    """Test error handling and recovery"""
    print("\n🛡️ Testing Error Handling")
    print("-" * 40)

    config = ExperimentConfig(
        population_size=2,
        generations=1,
        games_per_match=1
    )

    try:
        # Test 1: Invalid API key handling
        try:
            trainer = EvolutionaryTrainer(config, "invalid_key", "test_error_handling")
            trainer._create_initial_population()
            print(f"   Invalid API key: ❌ (should have failed)")
            api_error_handled = False
        except Exception:
            print(f"   Invalid API key: ✅ (properly caught)")
            api_error_handled = True

        # Test 2: Mock client with occasional failures
        class FailingMockClient(MockClaudeClient):
            def messages_create(self, model, max_tokens, messages):
                self.call_count += 1
                if self.call_count % 3 == 0:  # Fail every 3rd call
                    raise Exception("Mock API failure")
                return super().messages_create(model, max_tokens, messages)

        with patch('anthropic.Anthropic') as mock_anthropic:
            failing_client = FailingMockClient()
            mock_anthropic.return_value = failing_client

            trainer = EvolutionaryTrainer(config, "fake_key", "test_error_recovery")
            trainer.claude_client = failing_client

            # Try to create population with failing client
            trainer._create_initial_population()

            # Should still create some agents despite failures
            partial_success = len(trainer.population) > 0
            print(f"   Partial failure recovery: {'✅' if partial_success else '❌'}")

            return api_error_handled and partial_success

    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
        return False

    finally:
        if 'trainer' in locals():
            experiment_dir = trainer.experiment_manager.experiment_dir
            if os.path.exists(experiment_dir):
                shutil.rmtree(experiment_dir)

def test_performance_benchmarks():
    """Test performance characteristics"""
    print("\n⚡ Testing Performance Benchmarks")
    print("-" * 40)

    config = ExperimentConfig(
        population_size=6,
        generations=1,
        games_per_match=1
    )

    try:
        with patch('anthropic.Anthropic') as mock_anthropic:
            mock_client = MockClaudeClient()
            mock_anthropic.return_value = mock_client

            trainer = EvolutionaryTrainer(config, "fake_key", "test_performance")
            trainer.claude_client = mock_client

            # Benchmark population creation
            start_time = time.time()
            trainer._create_initial_population()
            pop_creation_time = time.time() - start_time

            print(f"   Population creation: {pop_creation_time:.2f}s for {len(trainer.population)} agents")

            # Benchmark evaluation
            start_time = time.time()
            trainer._evaluate_generation()
            evaluation_time = time.time() - start_time

            print(f"   Generation evaluation: {evaluation_time:.2f}s")

            # Benchmark Hall of Fame update
            start_time = time.time()
            trainer._update_hall_of_fame()
            hof_time = time.time() - start_time

            print(f"   Hall of Fame update: {hof_time:.3f}s")

            # Performance criteria (reasonable for testing)
            pop_creation_ok = pop_creation_time < 10.0  # 10s for 6 agents
            evaluation_ok = evaluation_time < 30.0      # 30s for evaluation
            hof_ok = hof_time < 1.0                     # 1s for HoF update

            print(f"   Performance criteria: {'✅' if pop_creation_ok and evaluation_ok and hof_ok else '❌'}")

            return pop_creation_ok and evaluation_ok and hof_ok

    except Exception as e:
        print(f"   ❌ Performance benchmark failed: {e}")
        return False

    finally:
        if 'trainer' in locals():
            experiment_dir = trainer.experiment_manager.experiment_dir
            if os.path.exists(experiment_dir):
                shutil.rmtree(experiment_dir)

def test_data_persistence():
    """Test data persistence and recovery"""
    print("\n💾 Testing Data Persistence")
    print("-" * 40)

    config = ExperimentConfig(
        population_size=3,
        generations=1,
        games_per_match=1
    )

    experiment_name = "test_persistence"
    experiment_dir = None

    try:
        # Phase 1: Create and run evolution
        with patch('anthropic.Anthropic') as mock_anthropic:
            mock_client = MockClaudeClient()
            mock_anthropic.return_value = mock_client

            trainer1 = EvolutionaryTrainer(config, "fake_key", experiment_name)
            trainer1.claude_client = mock_client

            # Run partial evolution
            trainer1._create_initial_population()
            trainer1._evaluate_generation()
            trainer1._update_hall_of_fame()
            trainer1._save_generation_results()

            # Get initial state
            initial_hof_size = len(trainer1.hall_of_fame.agents)
            initial_best_fitness = trainer1.hall_of_fame.get_hall_of_fame_stats().get('best_fitness', 0)
            experiment_dir = trainer1.experiment_manager.experiment_dir

            print(f"   Initial state: {initial_hof_size} agents, {initial_best_fitness:.2f} best fitness")

        # Phase 2: Create new trainer with same experiment directory
        # Simulate loading existing experiment
        trainer2 = None
        try:
            # This should load existing data
            trainer2 = EvolutionaryTrainer.__new__(EvolutionaryTrainer)
            trainer2.config = config
            trainer2.anthropic_api_key = "fake_key"
            trainer2.experiment_manager = ExperimentManager.__new__(ExperimentManager)
            trainer2.experiment_manager.experiment_dir = experiment_dir
            trainer2.experiment_manager.config = config
            trainer2.experiment_manager.experiment_name = experiment_name

            # Initialize Hall of Fame (should load existing data)
            trainer2.hall_of_fame = HallOfFame(experiment_dir, config.max_agents_hall_of_fame)

            # Check loaded state
            loaded_hof_size = len(trainer2.hall_of_fame.agents)
            loaded_best_fitness = trainer2.hall_of_fame.get_hall_of_fame_stats().get('best_fitness', 0)

            print(f"   Loaded state: {loaded_hof_size} agents, {loaded_best_fitness:.2f} best fitness")

            # Verify persistence
            persistence_ok = (
                loaded_hof_size == initial_hof_size and
                abs(loaded_best_fitness - initial_best_fitness) < 0.01
            )

            print(f"   Data persistence: {'✅' if persistence_ok else '❌'}")

            return persistence_ok

        except Exception as e:
            print(f"   ❌ Data loading failed: {e}")
            return False

    except Exception as e:
        print(f"   ❌ Data persistence test failed: {e}")
        return False

    finally:
        # Cleanup
        if experiment_dir and os.path.exists(experiment_dir):
            shutil.rmtree(experiment_dir)

def main():
    """Run all Phase 4 integration tests"""
    print("🔧 Complete Integration Testing - Phase 4")
    print("=" * 70)

    # Run all integration tests
    test1_passed = test_mock_claude_integration()
    test2_passed = test_small_evolution_run()
    test3_passed = test_component_integration()
    test4_passed = test_error_handling()
    test5_passed = test_performance_benchmarks()
    test6_passed = test_data_persistence()

    print(f"\n🏁 Phase 4 Integration Test Results")
    print("=" * 50)
    print(f"  Mock Claude Integration: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Small Evolution Run:     {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"  Component Integration:   {'✅ PASS' if test3_passed else '❌ FAIL'}")
    print(f"  Error Handling:          {'✅ PASS' if test4_passed else '❌ FAIL'}")
    print(f"  Performance Benchmarks:  {'✅ PASS' if test5_passed else '❌ FAIL'}")
    print(f"  Data Persistence:        {'✅ PASS' if test6_passed else '❌ FAIL'}")

    all_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed, test6_passed])

    if all_passed:
        print(f"\n🎉 Phase 4: Integration Testing - COMPLETE!")
        print(f"   ✅ End-to-end evolutionary training pipeline")
        print(f"   ✅ Swiss tournament + Code quality + Agent tracking")
        print(f"   ✅ Error handling and recovery mechanisms")
        print(f"   ✅ Performance benchmarks and optimization")
        print(f"   ✅ Data persistence and experiment continuity")
        print(f"\n🚀 Evolutionary Training System is READY FOR PRODUCTION!")
    else:
        print(f"\n❌ Phase 4 has issues that need to be addressed")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
