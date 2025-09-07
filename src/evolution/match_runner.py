#!/usr/bin/env python3
"""
Match Runner for Swiss Tournament System

Handles execution of individual matches between agents, including
safety measures and result calculation.
"""
import sys
import os
import time
import numpy as np
from typing import Tuple, Dict, Any, Optional

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))

from swiss_tournament import TournamentResult

class MatchRunner:
    """
    Executes matches between agents with safety measures and result tracking
    """

    def __init__(self, games_per_match: int = 5, timeout_seconds: int = 30):
        """
        Initialize match runner

        Args:
            games_per_match: Number of games to play per match
            timeout_seconds: Maximum time allowed per match
        """
        self.games_per_match = games_per_match
        self.timeout_seconds = timeout_seconds

        # Import training environment
        try:
            from environment import FightingGameEnv
            self.env_class = FightingGameEnv
        except ImportError as e:
            print(f"❌ Could not import training environment: {e}")
            self.env_class = None

    def run_match(self, agent1, agent2) -> TournamentResult:
        """
        Run a complete match between two agents

        Args:
            agent1: First agent (must have get_action method and agent_id attribute)
            agent2: Second agent (must have get_action method and agent_id attribute)

        Returns:
            TournamentResult with match outcome and statistics
        """
        if self.env_class is None:
            return self._create_error_result(agent1, agent2, "Environment not available")

        start_time = time.time()

        try:
            # Run multiple games
            agent1_wins = 0
            agent2_wins = 0
            agent1_total_fitness = 0.0
            agent2_total_fitness = 0.0
            games_completed = 0

            env = self.env_class(headless=True)

            for game_num in range(self.games_per_match):
                # Check timeout
                if time.time() - start_time > self.timeout_seconds:
                    print(f"⏰ Match timeout after {games_completed} games")
                    break

                # Play single game
                game_result = self._play_single_game(env, agent1, agent2, game_num)

                if game_result is None:
                    continue  # Skip failed games

                # Update match statistics
                winner, agent1_fitness, agent2_fitness = game_result

                if winner == 1:
                    agent1_wins += 1
                elif winner == 2:
                    agent2_wins += 1
                # else: draw (no winner)

                agent1_total_fitness += agent1_fitness
                agent2_total_fitness += agent2_fitness
                games_completed += 1

            env.close()

            # Calculate match scores
            if games_completed == 0:
                return self._create_error_result(agent1, agent2, "No games completed")

            # Score calculation: 1.0 for win, 0.5 for draw, 0.0 for loss
            if agent1_wins > agent2_wins:
                agent1_score, agent2_score = 1.0, 0.0
            elif agent2_wins > agent1_wins:
                agent1_score, agent2_score = 0.0, 1.0
            else:
                agent1_score, agent2_score = 0.5, 0.5  # Draw

            # Average fitness over games played
            agent1_avg_fitness = agent1_total_fitness / games_completed
            agent2_avg_fitness = agent2_total_fitness / games_completed

            return TournamentResult(
                agent1_id=agent1.agent_id,
                agent2_id=agent2.agent_id,
                agent1_score=agent1_score,
                agent2_score=agent2_score,
                agent1_fitness=agent1_avg_fitness,
                agent2_fitness=agent2_avg_fitness,
                games_played=games_completed,
                metadata={
                    'agent1_wins': agent1_wins,
                    'agent2_wins': agent2_wins,
                    'draws': games_completed - agent1_wins - agent2_wins,
                    'match_duration': time.time() - start_time
                }
            )

        except Exception as e:
            return self._create_error_result(agent1, agent2, f"Match error: {str(e)}")

    def _play_single_game(self, env, agent1, agent2, game_num: int) -> Optional[Tuple[int, float, float]]:
        """
        Play a single game between two agents

        Returns:
            Tuple of (winner, agent1_fitness, agent2_fitness) or None if game failed
            winner: 1 for agent1, 2 for agent2, 0 for draw
        """
        try:
            state = env.reset()
            agent1_total_reward = 0.0
            agent2_total_reward = 0.0

            step_count = 0
            max_steps = 3600  # 60 seconds at 60 FPS

            while step_count < max_steps:
                # Get actions from both agents with safety
                action1 = self._get_safe_action(agent1, state)

                # Get opponent state for agent2
                opponent_state = env.get_state(player_fighter=env.fighter2)
                action2 = self._get_safe_action(agent2, opponent_state)

                # Execute step
                next_state, rewards, done, info = env.step(action1, action2)

                # Accumulate rewards
                if isinstance(rewards, tuple):
                    agent1_total_reward += rewards[0]
                    agent2_total_reward += rewards[1]
                else:
                    agent1_total_reward += rewards

                if done:
                    break

                state = next_state
                step_count += 1

            # Determine winner based on health
            if env.fighter1.health > env.fighter2.health:
                winner = 1  # Agent1 wins
            elif env.fighter2.health > env.fighter1.health:
                winner = 2  # Agent2 wins
            else:
                winner = 0  # Draw

            return winner, agent1_total_reward, agent2_total_reward

        except Exception as e:
            print(f"⚠️  Game {game_num} failed: {e}")
            return None

    def _get_safe_action(self, agent, state) -> int:
        """
        Get action from agent with safety measures

        Returns:
            Valid action integer (0-9), defaults to 0 (idle) on error
        """
        try:
            # Ensure state is numpy array
            if not isinstance(state, np.ndarray):
                state = np.array(state, dtype=np.float32)

            # Get action from agent
            action = agent.get_action(state)

            # Validate action
            if not isinstance(action, (int, float, np.integer, np.floating)):
                return 0

            action = int(action)
            return max(0, min(9, action))  # Clamp to valid range

        except Exception as e:
            # Agent failed, return idle action
            if not hasattr(agent, '_error_count'):
                agent._error_count = 0
            agent._error_count += 1

            if agent._error_count <= 3:  # Only print first few errors
                print(f"⚠️  Agent {agent.agent_id} action error: {e}")

            return 0  # Idle action

    def _create_error_result(self, agent1, agent2, error_msg: str) -> TournamentResult:
        """Create a result for a failed match"""
        print(f"❌ Match failed: {agent1.agent_id} vs {agent2.agent_id} - {error_msg}")

        return TournamentResult(
            agent1_id=agent1.agent_id,
            agent2_id=agent2.agent_id,
            agent1_score=0.0,
            agent2_score=0.0,
            agent1_fitness=0.0,
            agent2_fitness=0.0,
            games_played=0,
            metadata={'error': error_msg}
        )

class RuleBasedMatchRunner(MatchRunner):
    """
    Specialized match runner for evaluating agents against rule-based opponents
    """

    def __init__(self, rule_based_opponents: list, games_per_match: int = 10):
        """
        Initialize rule-based match runner

        Args:
            rule_based_opponents: List of rule-based opponent instances
            games_per_match: Number of games per opponent
        """
        super().__init__(games_per_match)
        self.rule_based_opponents = rule_based_opponents

    def evaluate_agent_vs_rule_based(self, agent) -> Dict[str, float]:
        """
        Evaluate an agent against all rule-based opponents

        Returns:
            Dictionary with evaluation metrics
        """
        total_fitness = 0.0
        total_wins = 0
        total_games = 0

        results = {}

        for opponent in self.rule_based_opponents:
            match_result = self.run_match(agent, opponent)

            # Store individual opponent results
            opponent_name = getattr(opponent, 'difficulty', 'unknown')
            results[f'vs_{opponent_name}'] = {
                'score': match_result.agent1_score,
                'fitness': match_result.agent1_fitness,
                'games': match_result.games_played
            }

            # Accumulate totals
            total_fitness += match_result.agent1_fitness * match_result.games_played
            total_wins += match_result.agent1_score * match_result.games_played
            total_games += match_result.games_played

        # Calculate overall metrics
        results['overall'] = {
            'avg_fitness': total_fitness / total_games if total_games > 0 else 0.0,
            'win_rate': total_wins / total_games if total_games > 0 else 0.0,
            'total_games': total_games
        }

        return results

def create_rule_based_opponents():
    """Create standard set of rule-based opponents for evaluation"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))
        from models import SimplePolicy

        opponents = [
            SimplePolicy('easy'),
            SimplePolicy('medium'),
            SimplePolicy('hard')
        ]

        # Add agent_id attribute for compatibility with match runner
        for i, opponent in enumerate(opponents):
            opponent.agent_id = f"rule_based_{opponent.difficulty}"

        return opponents
    except ImportError as e:
        print(f"❌ Could not create rule-based opponents: {e}")
        return []
