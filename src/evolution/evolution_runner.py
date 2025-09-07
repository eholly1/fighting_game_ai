#!/usr/bin/env python3
"""
Main Evolution Runner - Complete Evolutionary Training System

Integrates all components: Swiss Tournament + Code Quality + Top Agent Tracking
to create a complete evolutionary training pipeline for fighting game AI.
"""
import os
import sys
import time
import argparse
import math
from typing import List, Dict, Any, Optional

# Import environment configuration
from env_config import setup_environment

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))

# Import all evolutionary components
from swiss_tournament import SwissTournament
from match_runner import MatchRunner, RuleBasedMatchRunner, create_rule_based_opponents
from code_validator import CodeValidator
from safe_execution import SafeAgent, AgentPool
from prompt_templates import PromptTemplateManager, PromptContext
from hall_of_fame import HallOfFame
from experiment_manager import ExperimentManager, ExperimentConfig
from agent_serialization import AgentSerializer

class EvolutionaryTrainer:
    """
    Complete evolutionary training system that integrates all components
    """

    def __init__(self, config: ExperimentConfig, anthropic_api_key: str,
                 experiment_name: Optional[str] = None):
        """
        Initialize the evolutionary trainer

        Args:
            config: Experiment configuration
            anthropic_api_key: API key for Claude
            experiment_name: Name for the experiment (auto-generated if None)
        """
        self.config = config
        self.anthropic_api_key = anthropic_api_key

        # Initialize core components
        self.experiment_manager = ExperimentManager(experiment_name, config)
        self.hall_of_fame = HallOfFame(
            self.experiment_manager.experiment_dir,
            max_agents=config.max_agents_hall_of_fame
        )
        self.agent_serializer = AgentSerializer(
            os.path.join(self.experiment_manager.experiment_dir, "agent_archive")
        )

        # Initialize validation and execution
        self.code_validator = CodeValidator(config.max_lines, config.max_chars)
        self.agent_pool = AgentPool()
        self.prompt_manager = PromptTemplateManager(config.max_lines, config.max_chars)

        # Initialize match running
        self.match_runner = MatchRunner(config.games_per_match, config.timeout_seconds)
        self.rule_based_opponents = create_rule_based_opponents()
        self.rule_based_runner = RuleBasedMatchRunner(
            self.rule_based_opponents,
            config.games_per_match
        )

        # Evolution state
        self.current_generation = 0
        self.population: List[SafeAgent] = []

        print(f"🧬 Evolutionary Trainer initialized")
        print(f"   Experiment: {self.experiment_manager.experiment_name}")
        print(f"   Population: {config.population_size}")
        print(f"   Generations: {config.generations}")
        print(f"   Swiss Rounds: {config.swiss_rounds}")

    def run_evolution(self) -> List[Dict[str, Any]]:
        """
        Run the complete evolutionary training process

        Returns:
            List of top agents from Hall of Fame
        """
        print(f"\n🚀 Starting evolutionary training")
        start_time = time.time()

        try:
            # Create initial population
            self._create_initial_population()

            # Run evolution for specified generations
            for generation in range(self.config.generations):
                self.current_generation = generation

                generation_start = time.time()
                self.experiment_manager.log_generation_start(generation, len(self.population))

                # Evaluate population using Swiss tournament
                self._evaluate_generation()

                # Update Hall of Fame with best performers
                self._update_hall_of_fame()

                # Save generation results
                self._save_generation_results()

                # Create next generation (if not final)
                if generation < self.config.generations - 1:
                    self._create_next_generation()

                generation_time = time.time() - generation_start
                print(f"   Generation {generation} completed in {generation_time:.1f}s")

            # Final analysis
            total_time = time.time() - start_time
            self._create_final_analysis(total_time)

            # Return top agents
            top_agents = self.hall_of_fame.get_top_agents(10)
            return [agent.to_dict() for agent in top_agents]

        except KeyboardInterrupt:
            print(f"\n⚠️  Evolution interrupted by user")
            self._save_interrupted_state()
            return []

        except Exception as e:
            print(f"\n❌ Evolution failed: {e}")
            self.experiment_manager._log(f"Evolution failed: {e}")
            return []

    def _create_initial_population(self):
        """Create the initial population of agents"""
        print(f"\n🧬 Creating initial population ({self.config.population_size} agents)")

        # Import Claude API
        try:
            from anthropic import Anthropic
            self.claude_client = Anthropic(api_key=self.anthropic_api_key)
        except ImportError:
            raise RuntimeError("Anthropic library not installed. Run: pip install anthropic")

        # Create diverse fighting styles
        fighting_styles = [
            'aggressive', 'defensive', 'zoner', 'balanced', 'adaptive',
            'rushdown', 'counter_puncher', 'hit_and_run', 'pressure_fighter', 'patient_defender'
        ]

        created_count = 0
        attempts = 0
        max_attempts = self.config.population_size * 3  # Allow multiple attempts

        while created_count < self.config.population_size and attempts < max_attempts:
            attempts += 1

            # Select fighting style
            style = fighting_styles[created_count % len(fighting_styles)]

            # Generate agent code
            agent_code = self._generate_agent_code(style, generation=0)

            if agent_code:
                agent_id = f"gen0_agent_{created_count:03d}"

                # Validate and create agent
                if self._create_and_validate_agent(agent_id, agent_code, style, generation=0):
                    created_count += 1
                    if created_count % 5 == 0:
                        print(f"   Created {created_count}/{self.config.population_size} agents")

        print(f"✅ Initial population created: {len(self.population)} agents")

        if len(self.population) < self.config.population_size // 2:
            raise RuntimeError(f"Failed to create sufficient initial population: {len(self.population)}")

    def _generate_agent_code(self, fighting_style: str, generation: int,
                           parent_codes: List[str] = None) -> Optional[str]:
        """Generate agent code using Claude API"""
        try:
            context = PromptContext(
                fighting_style=fighting_style,
                generation=generation,
                parent_codes=parent_codes or []
            )

            prompt = self.prompt_manager.generate_agent_prompt(context)

            response = self.claude_client.messages.create(
                model=self.config.anthropic_model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            code = response.content[0].text.strip()

            # Clean up code (remove markdown if present)
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()

            return code

        except Exception as e:
            print(f"⚠️  Failed to generate agent code: {e}")
            return None

    def _create_and_validate_agent(self, agent_id: str, code: str, fighting_style: str,
                                  generation: int) -> bool:
        """Create and validate an agent"""
        # Validate code
        validation_result = self.code_validator.validate_code(code, agent_id)

        if not validation_result.is_valid:
            return False

        # Create safe agent
        success = self.agent_pool.add_agent(agent_id, validation_result.cleaned_code,
                                          self.config.timeout_seconds)

        if success:
            agent = self.agent_pool.get_agent(agent_id)
            # Add metadata
            agent.fighting_style = fighting_style
            agent.generation = generation
            agent.code = validation_result.cleaned_code

            self.population.append(agent)
            return True

        return False

    def _evaluate_generation(self):
        """Evaluate the current generation using Swiss tournament"""
        print(f"\n⚔️  Evaluating Generation {self.current_generation}")

        valid_agents = [agent for agent in self.population if agent.is_valid]

        if len(valid_agents) < 2:
            print(f"❌ Insufficient valid agents for evaluation: {len(valid_agents)}")
            return

        # Phase 1: Swiss tournament among peers
        print(f"   Phase 1: Swiss tournament ({len(valid_agents)} agents)")
        tournament = SwissTournament(valid_agents, rounds=self.config.swiss_rounds)

        def tournament_match_runner(agent1, agent2):
            return self.match_runner.run_match(agent1, agent2)

        tournament_rankings = tournament.run_tournament(tournament_match_runner)

        # Phase 2: Evaluate top performers against rule-based opponents
        print(f"   Phase 2: Rule-based evaluation")
        top_count = min(len(valid_agents) // 2, 10)  # Top half or max 10
        top_agents = [agent for agent_id, standing in tournament_rankings[:top_count]
                     for agent in valid_agents if agent.agent_id == agent_id]

        for agent in top_agents:
            rule_based_results = self.rule_based_runner.evaluate_agent_vs_rule_based(agent)

            # Combine tournament and rule-based fitness
            tournament_fitness = next(standing.avg_fitness for agent_id, standing in tournament_rankings
                                    if agent_id == agent.agent_id)
            rule_based_fitness = rule_based_results['overall']['avg_fitness']

            # Weighted combination: 30% tournament, 70% rule-based
            agent.fitness = tournament_fitness * 0.3 + rule_based_fitness * 0.7
            agent.win_rate = rule_based_results['overall']['win_rate']
            agent.avg_reward = rule_based_results['overall']['avg_fitness']

        # Phase 3: Quick evaluation for remaining agents
        remaining_agents = [agent for agent in valid_agents if agent not in top_agents]
        for agent in remaining_agents:
            # Lighter evaluation against one rule-based opponent
            if self.rule_based_opponents:
                match_result = self.match_runner.run_match(agent, self.rule_based_opponents[0])
                agent.fitness = match_result.agent1_fitness
                agent.win_rate = match_result.agent1_score
                agent.avg_reward = match_result.agent1_fitness
            else:
                agent.fitness = 0.0
                agent.win_rate = 0.0
                agent.avg_reward = 0.0

        # Sort population by fitness
        self.population.sort(key=lambda x: getattr(x, 'fitness', 0), reverse=True)

        # Print generation statistics
        if self.population:
            best_fitness = getattr(self.population[0], 'fitness', 0)
            avg_fitness = sum(getattr(agent, 'fitness', 0) for agent in self.population) / len(self.population)

            print(f"   📊 Generation {self.current_generation} Results:")
            print(f"      Best fitness: {best_fitness:.2f}")
            print(f"      Avg fitness:  {avg_fitness:.2f}")
            print(f"      Valid agents: {len(valid_agents)}/{len(self.population)}")

    def _update_hall_of_fame(self):
        """Update Hall of Fame with current generation's best agents"""
        agent_data = []

        for agent in self.population:
            if hasattr(agent, 'fitness') and agent.fitness > 0:
                data = {
                    'agent_id': agent.agent_id,
                    'fitness': agent.fitness,
                    'win_rate': getattr(agent, 'win_rate', 0.0),
                    'avg_reward': getattr(agent, 'avg_reward', 0.0),
                    'code': agent.code,
                    'fighting_style': getattr(agent, 'fighting_style', 'unknown'),
                    'tournament_stats': {},
                    'lineage': getattr(agent, 'lineage', [])
                }
                agent_data.append(data)

        self.hall_of_fame.add_agents(agent_data, self.current_generation)

    def _save_generation_results(self):
        """Save results for the current generation"""
        # Calculate generation statistics
        valid_agents = [agent for agent in self.population if agent.is_valid]
        fitness_values = [getattr(agent, 'fitness', 0) for agent in valid_agents]

        if fitness_values:
            stats = {
                'generation': self.current_generation,
                'best_fitness': max(fitness_values),
                'avg_fitness': sum(fitness_values) / len(fitness_values),
                'valid_agents': len(valid_agents),
                'total_agents': len(self.population),
                'hall_of_fame_size': len(self.hall_of_fame.agents)
            }
        else:
            stats = {
                'generation': self.current_generation,
                'best_fitness': 0.0,
                'avg_fitness': 0.0,
                'valid_agents': 0,
                'total_agents': len(self.population),
                'hall_of_fame_size': len(self.hall_of_fame.agents)
            }

        # Update experiment tracking
        self.experiment_manager.update_evolution_summary(self.current_generation, stats)
        self.experiment_manager.log_generation_complete(self.current_generation, stats)

        # Archive all agents from this generation
        for agent in self.population:
            if hasattr(agent, 'code'):
                metadata = {
                    'generation': self.current_generation,
                    'fitness': getattr(agent, 'fitness', 0.0),
                    'fighting_style': getattr(agent, 'fighting_style', 'unknown'),
                    'win_rate': getattr(agent, 'win_rate', 0.0)
                }

                self.agent_serializer.save_agent_python(
                    agent.agent_id, agent.code, metadata
                )

    def _create_next_generation(self):
        """Create the next generation through selection and evolution"""
        print(f"\n🧬 Creating Generation {self.current_generation + 1}")

        # Clear current population
        old_population = self.population.copy()
        self.population = []
        self.agent_pool = AgentPool()  # Fresh agent pool

        # Keep elite agents
        elite_count = min(self.config.elite_size, len(old_population))
        elite_agents = old_population[:elite_count]

        created_count = 0

        # Add elite agents to new generation
        for i, elite_agent in enumerate(elite_agents):
            if hasattr(elite_agent, 'code'):
                new_id = f"gen{self.current_generation + 1}_elite_{i:03d}"
                if self._create_and_validate_agent(
                    new_id, elite_agent.code,
                    getattr(elite_agent, 'fighting_style', 'unknown'),
                    self.current_generation + 1
                ):
                    created_count += 1

        # Generate new agents through mutation and crossover
        attempts = 0
        max_attempts = self.config.population_size * 3

        while created_count < self.config.population_size and attempts < max_attempts:
            attempts += 1

            if len(old_population) == 0:
                break

            new_code = None

            # Decide between mutation and crossover
            if len(old_population) >= 2 and (created_count % 3 != 0):  # 2/3 crossover, 1/3 mutation
                # Crossover
                parent1, parent2 = self._tournament_selection(old_population, 2)
                if hasattr(parent1, 'code') and hasattr(parent2, 'code'):
                    new_code = self._generate_agent_code(
                        'hybrid',
                        self.current_generation + 1,
                        [parent1.code, parent2.code]
                    )
            else:
                # Mutation
                parent = self._tournament_selection(old_population, 1)[0]
                if hasattr(parent, 'code'):
                    new_code = self._generate_agent_code(
                        getattr(parent, 'fighting_style', 'adaptive'),
                        self.current_generation + 1,
                        [parent.code]
                    )

            if new_code:
                new_id = f"gen{self.current_generation + 1}_agent_{created_count:03d}"
                if self._create_and_validate_agent(
                    new_id, new_code, 'evolved', self.current_generation + 1
                ):
                    created_count += 1

        print(f"   Created {len(self.population)} agents for next generation")

    def _tournament_selection(self, population: List[SafeAgent], count: int) -> List[SafeAgent]:
        """Select agents using tournament selection"""
        import random

        selected = []
        tournament_size = min(3, len(population))

        for _ in range(count):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda x: getattr(x, 'fitness', 0))
            selected.append(winner)

        return selected

    def _create_final_analysis(self, total_time: float):
        """Create final analysis and reports"""
        print(f"\n📊 Creating final analysis")

        # Generate comprehensive report
        report_path = self.experiment_manager.create_analysis_report()

        # Get final statistics
        hof_stats = self.hall_of_fame.get_hall_of_fame_stats()
        progress = self.experiment_manager.get_experiment_progress()

        print(f"\n🏁 Evolution Complete!")
        print(f"   Total time: {total_time:.1f} seconds")
        print(f"   Generations: {progress['current_generation'] + 1}")
        print(f"   Hall of Fame: {hof_stats['total_agents']} agents")
        print(f"   Best fitness: {hof_stats['best_fitness']:.2f}")
        print(f"   Report: {report_path}")

    def _save_interrupted_state(self):
        """Save state when evolution is interrupted"""
        self.experiment_manager._log("Evolution interrupted - saving current state")
        self._save_generation_results()
        self._create_final_analysis(0)

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Evolutionary Fighting Game AI Training")

    parser.add_argument('--population', type=int, default=15,
                       help='Population size (default: 15)')
    parser.add_argument('--generations', type=int, default=10,
                       help='Number of generations (default: 10)')
    parser.add_argument('--games-per-match', type=int, default=3,
                       help='Games per match (default: 3)')
    parser.add_argument('--experiment-name', type=str, default=None,
                       help='Experiment name (auto-generated if not provided)')
    parser.add_argument('--anthropic-key', type=str, default=None,
                       help='Anthropic API key (overrides .env file)')
    parser.add_argument('--anthropic-model', type=str, default=None,
                       help='Anthropic model name (overrides .env file)')
    parser.add_argument('--skip-env-setup', action='store_true',
                       help='Skip automatic .env file loading')

    args = parser.parse_args()

    # Setup environment configuration
    if not args.skip_env_setup:
        print("🔧 Setting up environment configuration...")
        env_config = setup_environment()

        if not env_config.get('config_valid', False):
            print("\n❌ Environment configuration failed!")
            print("💡 You can:")
            print("   1. Create/fix your .env file with ANTHROPIC_API_KEY")
            print("   2. Use --anthropic-key command line argument")
            print("   3. Set ANTHROPIC_API_KEY environment variable")
            print("   4. Use --skip-env-setup and provide key manually")
            return 1
    else:
        env_config = {}

    # Get API key (command line overrides environment)
    api_key = (args.anthropic_key or
              env_config.get('anthropic_api_key') or
              os.getenv('ANTHROPIC_API_KEY'))

    if not api_key:
        print("❌ No Anthropic API key found!")
        print("💡 Please either:")
        print("   1. Add ANTHROPIC_API_KEY to your .env file")
        print("   2. Use --anthropic-key command line argument")
        print("   3. Set ANTHROPIC_API_KEY environment variable")
        return 1

    # Get model name (command line overrides environment)
    model_name = (args.anthropic_model or
                 env_config.get('anthropic_model') or
                 "claude-3-5-sonnet-20241022")

    # Create configuration
    config = ExperimentConfig(
        population_size=args.population,
        generations=args.generations,
        games_per_match=args.games_per_match,
        swiss_rounds=max(1, math.ceil(math.log2(args.population))),
        anthropic_model=model_name
    )

    print(f"🧬 Starting Evolutionary Training")
    print(f"   Population: {config.population_size}")
    print(f"   Generations: {config.generations}")
    print(f"   Swiss Rounds: {config.swiss_rounds}")
    print(f"   Games per Match: {config.games_per_match}")
    print(f"   Model: {model_name}")
    print(f"   API Key: {api_key[:12]}...{api_key[-4:]} (masked)")

    # Run evolution
    try:
        trainer = EvolutionaryTrainer(config, api_key, args.experiment_name)
        top_agents = trainer.run_evolution()

        if top_agents:
            print(f"\n🏆 Top 3 Agents:")
            for i, agent in enumerate(top_agents[:3]):
                print(f"   {i+1}. {agent['agent_id']}: {agent['fitness']:.2f} fitness")

        return 0

    except Exception as e:
        print(f"❌ Evolution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
