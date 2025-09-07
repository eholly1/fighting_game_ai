"""
Training script for Fighting Game RL agents with ExperimentManager
"""
import os
import time
import yaml
import argparse
import numpy as np
import torch
import matplotlib.pyplot as plt
from collections import deque

from environment import FightingGameEnv
from models import FighterPolicy, PPOTrainer, RandomPolicy, SimplePolicy
from experiment_manager import ExperimentManager

class ExperimentTrainer:
    """Enhanced trainer with experiment management and structured logging"""

    def __init__(self, experiment_name: str, config_path: str = None):
        # Load configuration
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default configuration
            self.config = self._get_default_config()

        # Initialize experiment manager
        self.experiment_manager = ExperimentManager(experiment_name, self.config)

        # Extract training parameters
        training_config = self.config.get('training', {})
        self.batch_size = int(training_config.get('batch_size', 2048))
        self.learning_rate = float(training_config.get('learning_rate', 3e-4))
        self.gamma = float(training_config.get('gamma', 0.99))
        self.gae_lambda = float(training_config.get('gae_lambda', 0.95))
        self.total_steps = int(training_config.get('total_steps', 100000))

        print(f"🚀 Initialized trainer for experiment: {experiment_name}")
        print(f"📋 Total steps: {self.total_steps}")
        print(f"🎯 Batch size: {self.batch_size}")

    def _get_default_config(self):
        """Get default configuration if no config file provided"""
        return {
            'training': {
                'total_steps': 100000,
                'batch_size': 2048,
                'learning_rate': 3e-4,
                'gamma': 0.99,
                'gae_lambda': 0.95,
                'eval_interval': 5000,
                'init_from_bc': True
            },
            'environment': {
                'max_episode_steps': 2048,
                'headless': True
            },
            'opponents': {
                'types': ['rule_based'],
                'difficulty': 'medium'
            }
        }

    def train(self):
        """Main training method with experiment management"""
        print(f"\n=== Starting Training ===")

        # Initialize environment and policy
        env_config = self.config.get('environment', {})
        env = FightingGameEnv(headless=env_config.get('headless', True))
        policy = FighterPolicy()

        # Initialize opponent policy once (not every step!)
        opponent_config = self.config.get('opponents', {})
        difficulty = opponent_config.get('difficulty', 'medium')
        self.opponent_policy = SimplePolicy(difficulty)

        # Try to initialize from behavioral cloning policy
        training_config = self.config.get('training', {})
        if training_config.get('init_from_bc', False):
            bc_policy_path = training_config.get('bc_policy_path', 'easy_behavioral_cloning.pth')
            if os.path.exists(bc_policy_path):
                print(f"🧠 Initializing from behavioral cloning policy: {bc_policy_path}")
                try:
                    checkpoint = torch.load(bc_policy_path, map_location='cpu')
                    policy.load_state_dict(checkpoint['model_state_dict'])
                    print("✅ Successfully loaded BC initialization!")
                except Exception as e:
                    print(f"⚠️ Failed to load BC policy: {e}, starting from scratch")
            else:
                print(f"⚠️ BC policy not found: {bc_policy_path}, starting from scratch")

        trainer = PPOTrainer(policy, lr=self.learning_rate)

        # Initial evaluation at step 0 (baseline)
        print("🎯 Running initial evaluation (baseline)...")
        self.experiment_manager.step_count = 0
        initial_eval = self.experiment_manager.evaluate_policy(policy)
        self.experiment_manager.log_evaluation(0, 0, initial_eval)
        self.experiment_manager.save_policy(policy, 'initial')

        # Training loop
        episode_rewards = deque(maxlen=100)
        episode_lengths = deque(maxlen=100)
        best_reward = -float('inf')

        step = 0
        episode = 0

        print(f"🔄 Starting training loop: target steps = {self.total_steps}")

        while step < self.total_steps:
            print(f"📊 Episode {episode}, Step {step}/{self.total_steps}")
            # Collect batch of experience
            batch_data = self._collect_batch(env, policy, self.batch_size)

            if batch_data is None:
                continue

            states, actions, rewards, log_probs, values, dones = batch_data

            # Calculate returns and advantages
            returns, advantages = self._calculate_gae(rewards, values, dones)

            # Update policy
            trainer.update(states, actions, log_probs, returns, advantages)

            step += len(states)
            episode += 1

            # Track statistics
            episode_reward = np.sum(rewards)
            episode_rewards.append(episode_reward)
            episode_lengths.append(len(rewards))

            # Logging every 10 episodes
            if episode % 10 == 0 and episode > 0:
                avg_reward = np.mean(episode_rewards)
                avg_length = np.mean(episode_lengths)
                stats = trainer.get_stats()

                # Log to experiment manager
                training_metrics = {
                    'avg_reward': avg_reward,
                    'avg_length': avg_length,
                    'policy_loss': stats.get('policy_loss', 0),
                    'value_loss': stats.get('value_loss', 0),
                    'episode_reward': episode_reward
                }

                self.experiment_manager.log_training_step(episode, step, training_metrics)

                print(f"Episode {episode}, Step {step}")
                print(f"  Avg Reward: {avg_reward:.2f}")
                print(f"  Avg Length: {avg_length:.1f}")
                print(f"  Policy Loss: {stats.get('policy_loss', 0):.4f}")
                print(f"  Value Loss: {stats.get('value_loss', 0):.4f}")

                # Save best model
                if avg_reward > best_reward:
                    best_reward = avg_reward
                    self.experiment_manager.save_policy(policy, 'best')

            # Periodic evaluation (update step count first)
            self.experiment_manager.step_count = step
            if self.experiment_manager.should_evaluate():
                print(f"🎯 Running evaluation at step {step}...")
                eval_results = self.experiment_manager.evaluate_policy(policy)
                self.experiment_manager.log_evaluation(episode, step, eval_results)

                # Save checkpoint
                self.experiment_manager.save_policy(policy, f'step_{step}')

        # Save final policy
        self.experiment_manager.save_policy(policy, 'final')
        env.close()

        print(f"✅ Completed training!")
        return policy

    def _collect_batch(self, env, policy, batch_size):
        """Collect a batch of experience"""
        states, actions, rewards, log_probs, values, dones = [], [], [], [], [], []

        state = env.reset()
        episode_steps = 0
        max_episode_steps = self.config.get('environment', {}).get('max_episode_steps', 2048)

        while len(states) < batch_size:
            # Get action from policy
            action, log_prob, value = policy.get_action_and_value(state)

            # Get opponent action (from opponent's perspective)
            opponent_state = env.get_state(player_fighter=env.fighter2)
            opponent_action = self._get_opponent_action(opponent_state)

            # Step environment
            next_state, reward, done, info = env.step(action.item(), opponent_action)

            # Extract reward for player 1 (the RL agent) if it's a tuple
            if isinstance(reward, tuple):
                reward = reward[0]  # First player reward

            # Store experience
            states.append(state)
            actions.append(action.item())
            rewards.append(reward)
            log_probs.append(log_prob.item())
            values.append(value.item())
            dones.append(done)

            state = next_state
            episode_steps += 1

            if done or episode_steps > max_episode_steps:
                state = env.reset()
                episode_steps = 0

        return states, actions, rewards, log_probs, values, dones

    def _get_opponent_action(self, state):
        """Get action for opponent based on configuration"""
        # Use the persistent opponent policy (not a new instance every step!)
        return self.opponent_policy.get_action(state)

    def _calculate_gae(self, rewards, values, dones):
        """Calculate Generalized Advantage Estimation"""
        returns = []
        advantages = []

        gae = 0
        next_value = 0

        for i in reversed(range(len(rewards))):
            if i == len(rewards) - 1:
                next_non_terminal = 1.0 - dones[i]
                next_value = 0
            else:
                next_non_terminal = 1.0 - dones[i]
                next_value = values[i + 1]

            delta = rewards[i] + self.gamma * next_value * next_non_terminal - values[i]
            gae = delta + self.gamma * self.gae_lambda * next_non_terminal * gae

            advantages.insert(0, gae)
            returns.insert(0, gae + values[i])

        return returns, advantages

def main():
    """Main training function with experiment management"""
    parser = argparse.ArgumentParser(description='Fighting Game RL Training with Experiments')
    parser.add_argument('--experiment', type=str, required=False,
                       help='Experiment name')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to config file (YAML)')
    parser.add_argument('--list', action='store_true',
                       help='List all experiments')

    args = parser.parse_args()

    if args.list:
        experiments = ExperimentManager.list_experiments()
        print("📋 Available experiments:")
        for exp in experiments:
            print(f"  - {exp}")
        return

    if not args.experiment:
        print("❌ Error: --experiment is required when not using --list")
        parser.print_help()
        return

    print("🚀 Fighting Game RL Training with Experiment Management")
    print("=" * 60)

    try:
        # Initialize trainer with experiment management
        trainer = ExperimentTrainer(args.experiment, args.config)

        # Start training
        policy = trainer.train()

        # Print summary
        summary = trainer.experiment_manager.get_experiment_summary()
        print(f"\n📊 Training Summary:")
        if 'experiment_name' in summary:
            print(f"   Experiment: {summary['experiment_name']}")
            print(f"   Episodes: {summary['total_episodes']}")
            print(f"   Steps: {summary['total_steps']}")
            print(f"   Evaluations: {summary['evaluations']}")
            if summary.get('latest_win_rate'):
                print(f"   Final Win Rate: {summary['latest_win_rate']:.1%}")
        else:
            print(f"   Status: {summary.get('status', 'unknown')}")
            print(f"   Experiment: {trainer.experiment_manager.experiment_name}")

    except KeyboardInterrupt:
        print(f"\n⚠️ Training interrupted")
    except Exception as e:
        print(f"❌ Training failed: {e}")
        raise

if __name__ == "__main__":
    main()
