#!/usr/bin/env python3
"""
Train RL policies using behavioral cloning initialization
"""
import os
import sys
import argparse
import glob

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from behavioral_cloning import BehavioralCloningTrainer
# from training.train import SelfPlayTrainer  # Skip RL for now

def find_latest_demo_file(demo_dir='data'):
    """Find the most recent demonstration file"""
    pattern = os.path.join(demo_dir, 'human_demos_*.json')
    demo_files = glob.glob(pattern)

    if not demo_files:
        return None

    # Sort by modification time, newest first
    demo_files.sort(key=os.path.getmtime, reverse=True)
    return demo_files[0]

def train_with_behavioral_cloning(demo_file, difficulty='easy', bc_epochs=50, rl_steps=50000):
    """Train a policy using behavioral cloning + RL fine-tuning"""

    print("🎯 Training with Behavioral Cloning + RL Fine-tuning")
    print("=" * 60)

    # Step 1: Behavioral Cloning Pre-training
    print("\n📚 Step 1: Behavioral Cloning Pre-training")
    print("-" * 40)

    bc_trainer = BehavioralCloningTrainer()
    bc_trainer.load_demonstrations(demo_file)

    print(f"🚀 Training for {bc_epochs} epochs...")
    best_accuracy = bc_trainer.train(num_epochs=bc_epochs)

    # Save the behavioral cloning policy
    bc_policy_path = f"../training/policies/{difficulty}_behavioral_cloning.pth"
    bc_trainer.save_policy(bc_policy_path)

    print(f"✅ Behavioral cloning completed with {best_accuracy:.1f}% accuracy")

    # Step 2: RL Fine-tuning (if requested)
    if rl_steps > 0:
        print(f"\n🎮 Step 2: RL Fine-tuning ({rl_steps} steps)")
        print("-" * 40)
        print("⚠️  RL fine-tuning not implemented yet - skipping for now")
        # TODO: Implement RL fine-tuning starting from BC policy

    print("\n🎉 Training pipeline completed!")
    print(f"📁 Behavioral cloning policy saved to: {bc_policy_path}")
    if rl_steps > 0:
        print(f"📁 RL fine-tuned policy saved to: src/training/policies/{difficulty}_final.pth")

def main():
    parser = argparse.ArgumentParser(description='Train policies from human demonstrations')
    parser.add_argument('--demo-file', type=str, help='Path to demonstration file (auto-detect if not provided)')
    parser.add_argument('--difficulty', type=str, default='easy', choices=['easy', 'medium', 'hard'],
                       help='Difficulty level to train')
    parser.add_argument('--bc-epochs', type=int, default=50,
                       help='Number of behavioral cloning epochs')
    parser.add_argument('--rl-steps', type=int, default=0,
                       help='Number of RL fine-tuning steps (0 to skip RL)')
    parser.add_argument('--bc-only', action='store_true',
                       help='Only do behavioral cloning, skip RL fine-tuning')

    args = parser.parse_args()

    # Find demonstration file
    if args.demo_file:
        demo_file = args.demo_file
    else:
        demo_file = find_latest_demo_file()

    if not demo_file or not os.path.exists(demo_file):
        print("❌ No demonstration file found!")
        print("\n📝 To record demonstrations:")
        print("1. Run the game: python src/main.py")
        print("2. Start a fight against AI")
        print("3. Press F1 to start recording")
        print("4. Play for 5+ minutes")
        print("5. Press F1 to stop recording")
        print("6. Press F2 to save demonstrations")
        return

    print(f"📂 Using demonstration file: {demo_file}")

    # Set RL steps
    if args.bc_only:
        rl_steps = 0
    else:
        rl_steps = args.rl_steps

    # Train
    train_with_behavioral_cloning(
        demo_file=demo_file,
        difficulty=args.difficulty,
        bc_epochs=args.bc_epochs,
        rl_steps=rl_steps
    )

if __name__ == "__main__":
    main()
