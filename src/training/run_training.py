#!/usr/bin/env python3
"""
Run script for Fighting Game RL Training
Usage: python run_training.py [options]
"""
import argparse
import os
import sys
import time
import torch

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from train import SelfPlayTrainer
from environment import FightingGameEnv
from models import FighterPolicy, RandomPolicy, SimplePolicy

def test_environment():
    """Test that the environment works correctly"""
    print("Testing environment...")

    try:
        env = FightingGameEnv(headless=True)
        state = env.reset()
        print(f"Initial state shape: {state.shape}")
        print(f"State range: [{state.min():.3f}, {state.max():.3f}]")

        # Test a few steps
        for i in range(5):
            action_idx = i % len(env.action_mapping)
            action_name = env.action_mapping[action_idx]
            action2 = 0  # idle
            print(f"About to step with action {action_idx} ({action_name})")
            next_state, reward, done, info = env.step(action_idx, action2)
            print(f"Step {i}: action={action_name}, reward={reward}, done={done}")

            if done:
                state = env.reset()
            else:
                state = next_state

        env.close()
        print("Environment test passed!")
        return True

    except Exception as e:
        print(f"Environment test failed: {e}")
        return False

def test_models():
    """Test that the models work correctly"""
    print("Testing models...")

    try:
        # Test policy
        policy = FighterPolicy()
        dummy_state = torch.randn(1, 20)

        action_logits, value = policy(dummy_state)
        print(f"Policy output shapes: logits={action_logits.shape}, value={value.shape}")

        action = policy.get_action(dummy_state.numpy()[0])
        print(f"Sample action: {action}")

        # Test random policy
        random_policy = RandomPolicy()
        random_action = random_policy.get_action(dummy_state.numpy()[0])
        print(f"Random action: {random_action}")

        # Test simple policy
        simple_policy = SimplePolicy('medium')
        simple_action = simple_policy.get_action(dummy_state.numpy()[0])
        print(f"Simple policy action: {simple_action}")

        print("Models test passed!")
        return True

    except Exception as e:
        print(f"Models test failed: {e}")
        return False

def run_quick_training(difficulty='easy', steps=1000):
    """Run a quick training session for testing"""
    print(f"Running quick training for {difficulty} ({steps} steps)...")

    trainer = SelfPlayTrainer()

    # Override training steps for quick test
    trainer.difficulty_configs[difficulty]['training_steps'] = steps
    trainer.difficulty_configs[difficulty]['eval_interval'] = steps // 2

    try:
        # Initialize from behavioral cloning if available
        policy = trainer.train_difficulty_level(difficulty, init_from_bc=True)
        print("Quick training completed successfully!")
        return True
    except Exception as e:
        print(f"Quick training failed: {e}")
        return False

def run_full_training(difficulties=None):
    """Run full training for specified difficulties"""
    if difficulties is None:
        difficulties = ['easy', 'medium', 'hard']

    print(f"Starting full training for: {difficulties}")

    trainer = SelfPlayTrainer()

    for difficulty in difficulties:
        print(f"\n{'='*50}")
        print(f"Training {difficulty.upper()} AI")
        print(f"{'='*50}")

        start_time = time.time()

        try:
            policy = trainer.train_difficulty_level(difficulty)
            end_time = time.time()

            print(f"\n✅ Completed {difficulty} training in {end_time - start_time:.1f} seconds")

        except KeyboardInterrupt:
            print(f"\n⚠️  Training interrupted during {difficulty} level")
            break
        except Exception as e:
            print(f"\n❌ Error training {difficulty}: {e}")
            continue

    print(f"\n🎉 Training completed!")
    print(f"📁 Policies saved in: {trainer.save_dir}")

def list_saved_policies():
    """List all saved policies"""
    policies_dir = 'policies'

    if not os.path.exists(policies_dir):
        print("No policies directory found")
        return

    policy_files = [f for f in os.listdir(policies_dir) if f.endswith('.pth')]

    if not policy_files:
        print("No saved policies found")
        return

    print("Saved policies:")
    for policy_file in sorted(policy_files):
        filepath = os.path.join(policies_dir, policy_file)
        size = os.path.getsize(filepath) / 1024  # KB
        mtime = time.ctime(os.path.getmtime(filepath))
        print(f"  {policy_file} ({size:.1f} KB, {mtime})")

def main():
    parser = argparse.ArgumentParser(description='Fighting Game RL Training')
    parser.add_argument('--mode', choices=['test', 'quick', 'full', 'list'],
                       default='full', help='Training mode')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'],
                       help='Specific difficulty to train (for quick mode)')
    parser.add_argument('--steps', type=int, default=1000,
                       help='Number of steps for quick training')
    parser.add_argument('--difficulties', nargs='+',
                       choices=['easy', 'medium', 'hard'],
                       help='Difficulties to train (for full mode)')

    args = parser.parse_args()

    print("Fighting Game RL Training")
    print("=" * 40)
    print(f"Mode: {args.mode}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print()

    if args.mode == 'test':
        print("Running tests...")
        env_ok = test_environment()
        models_ok = test_models()

        if env_ok and models_ok:
            print("\n✅ All tests passed! Ready for training.")
        else:
            print("\n❌ Some tests failed. Check the errors above.")
            sys.exit(1)

    elif args.mode == 'quick':
        difficulty = args.difficulty or 'easy'
        success = run_quick_training(difficulty, args.steps)
        if not success:
            sys.exit(1)

    elif args.mode == 'full':
        run_full_training(args.difficulties)

    elif args.mode == 'list':
        list_saved_policies()

if __name__ == "__main__":
    main()
