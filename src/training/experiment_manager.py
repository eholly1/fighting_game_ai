"""
Experiment Manager for Fighting Game RL Training
Handles structured logging, evaluation, and experiment organization
"""
import os
import json
import time
import numpy as np
from datetime import datetime
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple

from environment import FightingGameEnv
from models import SimplePolicy


class ExperimentManager:
    """Manages training experiments with structured logging and evaluation"""

    def __init__(self, experiment_name: str, config: Dict = None):
        self.experiment_name = experiment_name
        self.config = config or {}

        # Setup directories
        self.base_dir = "experiments"
        self.experiment_dir = os.path.join(self.base_dir, experiment_name)
        self.logs_dir = os.path.join(self.experiment_dir, "logs")
        self.policies_dir = os.path.join(self.experiment_dir, "policies")
        self.plots_dir = os.path.join(self.experiment_dir, "plots")

        self._create_directories()

        # Metrics storage
        self.metrics_file = os.path.join(self.logs_dir, "metrics.jsonl")
        self.config_file = os.path.join(self.experiment_dir, "config.json")

        # Evaluation settings (from config)
        self.eval_games = config.get('training', {}).get('eval_games', 50)
        self.eval_interval = config.get('training', {}).get('eval_interval', 5000)

        # Running metrics
        self.episode_count = 0
        self.step_count = 0
        self.start_time = time.time()

        # Save config
        self._save_config()

        print(f"📁 Experiment: {experiment_name}")
        print(f"📂 Directory: {self.experiment_dir}")

    def _create_directories(self):
        """Create experiment directory structure"""
        for directory in [self.experiment_dir, self.logs_dir, self.policies_dir, self.plots_dir]:
            os.makedirs(directory, exist_ok=True)

    def _save_config(self):
        """Save experiment configuration"""
        config_data = {
            "experiment_name": self.experiment_name,
            "created_at": datetime.now().isoformat(),
            "config": self.config
        }

        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    def log_training_step(self, episode: int, step: int, metrics: Dict):
        """Log metrics from a training step"""
        self.episode_count = episode
        self.step_count = step

        log_entry = {
            "type": "training",
            "experiment": self.experiment_name,
            "episode": episode,
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "elapsed_time": time.time() - self.start_time,
            "metrics": metrics
        }

        # Append to JSONL file
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def log_evaluation(self, episode: int, step: int, eval_results: Dict):
        """Log evaluation results"""
        log_entry = {
            "type": "evaluation",
            "experiment": self.experiment_name,
            "episode": episode,
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "elapsed_time": time.time() - self.start_time,
            "results": eval_results
        }

        # Append to JSONL file
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Print summary
        win_rate = eval_results.get('win_rate', 0)
        avg_length = eval_results.get('avg_game_length', 0)
        engagement = eval_results.get('engagement_score', 0)

        print(f"📊 Evaluation @ Step {step}:")
        print(f"   Win Rate: {win_rate:.1%}")
        print(f"   Avg Game Length: {avg_length:.1f}")
        print(f"   Engagement Score: {engagement:.2f}")

    def evaluate_policy(self, policy, opponent_type: str = "rule_based") -> Dict:
        """Evaluate policy against specified opponent"""
        print(f"🎯 Evaluating policy against {opponent_type}...")

        env = FightingGameEnv(headless=True)

        # Create opponent policy once (not every step!)
        if opponent_type == "rule_based":
            opponent_policy = SimplePolicy('medium')
        else:
            opponent_policy = None

        # Results tracking
        wins = 0
        game_lengths = []
        action_counts = defaultdict(int)
        total_actions = 0

        # Behavioral metrics
        distances = []
        combat_time = 0
        total_time = 0

        for game in range(self.eval_games):
            state = env.reset()
            game_length = 0
            game_distances = []

            while True:
                # Get AI action
                action = policy.get_action(state, deterministic=True)
                action_counts[action] += 1
                total_actions += 1

                # Get opponent action (from opponent's perspective)
                if opponent_type == "rule_based":
                    opponent_state = env.get_state(player_fighter=env.fighter2)
                    opponent_action = opponent_policy.get_action(opponent_state)
                else:
                    opponent_action = 0  # idle

                # Step environment
                next_state, reward, done, info = env.step(action, opponent_action)

                # Track behavioral metrics
                fighter1_x = env.fighter1.x
                fighter2_x = env.fighter2.x
                distance = abs(fighter1_x - fighter2_x)
                game_distances.append(distance)

                if distance < 150:  # Combat range
                    combat_time += 1
                total_time += 1

                game_length += 1
                state = next_state

                if done:
                    # Check who won (handle both KO and timeout victories)
                    if env.fighter1.is_alive() and not env.fighter2.is_alive():
                        # AI wins by KO
                        wins += 1
                    elif env.fighter1.is_alive() and env.fighter2.is_alive():
                        # Timeout - check health advantage
                        if env.fighter1.health > env.fighter2.health:
                            wins += 1  # AI wins by health advantage
                        # If fighter2 has more health or equal health, AI loses/draws (no win counted)

                    game_lengths.append(game_length)
                    distances.extend(game_distances)
                    break

        env.close()

        # Calculate metrics
        win_rate = wins / self.eval_games
        avg_game_length = np.mean(game_lengths)
        avg_distance = np.mean(distances)
        engagement_score = combat_time / total_time if total_time > 0 else 0

        # Action distribution
        action_distribution = {}
        for action_idx, count in action_counts.items():
            action_distribution[action_idx] = count / total_actions

        results = {
            "win_rate": win_rate,
            "wins": wins,
            "total_games": self.eval_games,
            "avg_game_length": avg_game_length,
            "avg_distance_from_opponent": avg_distance,
            "engagement_score": engagement_score,
            "action_distribution": action_distribution,
            "opponent_type": opponent_type
        }

        return results

    def save_policy(self, policy, suffix: str = "checkpoint"):
        """Save policy with experiment organization"""
        import torch

        filename = f"policy_{suffix}_step_{self.step_count}.pth"
        filepath = os.path.join(self.policies_dir, filename)

        torch.save({
            'model_state_dict': policy.state_dict(),
            'experiment': self.experiment_name,
            'episode': self.episode_count,
            'step': self.step_count,
            'timestamp': datetime.now().isoformat()
        }, filepath)

        print(f"💾 Saved policy: {filename}")
        return filepath

    def should_evaluate(self) -> bool:
        """Check if it's time for evaluation"""
        # Check if we've crossed an evaluation interval since last evaluation
        if not hasattr(self, 'last_eval_step'):
            self.last_eval_step = 0

        current_interval = self.step_count // self.eval_interval
        last_interval = self.last_eval_step // self.eval_interval

        should_eval = current_interval > last_interval and self.step_count > 0

        if should_eval:
            self.last_eval_step = self.step_count
            print(f"🎯 Evaluation triggered: step={self.step_count}, interval={current_interval}")

        return should_eval

    def get_experiment_summary(self) -> Dict:
        """Get summary of experiment progress"""
        if not os.path.exists(self.metrics_file):
            return {"status": "no_data"}

        # Read all metrics
        training_metrics = []
        evaluation_metrics = []

        with open(self.metrics_file, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry["type"] == "training":
                    training_metrics.append(entry)
                elif entry["type"] == "evaluation":
                    evaluation_metrics.append(entry)

        summary = {
            "experiment_name": self.experiment_name,
            "status": "active" if len(training_metrics) > 0 else "completed",
            "total_episodes": len(training_metrics),
            "total_steps": self.step_count,
            "evaluations": len(evaluation_metrics),
            "latest_win_rate": evaluation_metrics[-1]["results"]["win_rate"] if evaluation_metrics else None,
            "elapsed_time": time.time() - self.start_time
        }

        return summary

    @staticmethod
    def list_experiments() -> List[str]:
        """List all available experiments"""
        base_dir = "experiments"
        if not os.path.exists(base_dir):
            return []

        experiments = []
        for item in os.listdir(base_dir):
            exp_dir = os.path.join(base_dir, item)
            if os.path.isdir(exp_dir) and os.path.exists(os.path.join(exp_dir, "config.json")):
                experiments.append(item)

        return sorted(experiments)

    @staticmethod
    def load_experiment_data(experiment_name: str) -> Dict:
        """Load all data for an experiment"""
        exp_dir = os.path.join("experiments", experiment_name)
        metrics_file = os.path.join(exp_dir, "logs", "metrics.jsonl")
        config_file = os.path.join(exp_dir, "config.json")

        if not os.path.exists(metrics_file):
            return {"error": "No metrics found"}

        # Load config
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Load metrics
        training_data = []
        evaluation_data = []

        with open(metrics_file, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry["type"] == "training":
                    training_data.append(entry)
                elif entry["type"] == "evaluation":
                    evaluation_data.append(entry)

        return {
            "config": config,
            "training_data": training_data,
            "evaluation_data": evaluation_data
        }
