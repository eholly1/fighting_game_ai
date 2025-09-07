"""
Behavioral Cloning Trainer
Trains policies to mimic human demonstrations
"""
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from training.models import FighterPolicy
from recorder import load_demonstrations, demonstrations_to_dataset

class DemonstrationDataset(Dataset):
    """PyTorch dataset for human demonstrations"""

    def __init__(self, states, actions):
        self.states = torch.FloatTensor(states)
        self.actions = torch.LongTensor(actions)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return self.states[idx], self.actions[idx]

class BehavioralCloningTrainer:
    """Trains policies using behavioral cloning"""

    def __init__(self, state_size=26, action_size=10, hidden_size=128):
        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = hidden_size

        # Initialize policy
        self.policy = FighterPolicy(state_size, action_size, hidden_size)

        # Training parameters
        self.learning_rate = 1e-3
        self.batch_size = 64
        self.num_epochs = 100

        # Optimizer and loss
        self.optimizer = optim.Adam(self.policy.parameters(), lr=self.learning_rate)
        self.criterion = nn.CrossEntropyLoss()

        # Training history
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []

    def load_demonstrations(self, demo_filepath):
        """Load and prepare demonstration data"""
        print(f"📂 Loading demonstrations from {demo_filepath}")

        # Load demonstrations
        demo_data = load_demonstrations(demo_filepath)
        states, actions = demonstrations_to_dataset(demo_data)

        print(f"📊 Dataset: {len(states)} samples, {len(np.unique(actions))} unique actions")

        # Split into train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            states, actions, test_size=0.2, random_state=42, stratify=actions
        )

        # Create datasets and dataloaders
        self.train_dataset = DemonstrationDataset(X_train, y_train)
        self.val_dataset = DemonstrationDataset(X_val, y_val)

        self.train_loader = DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True
        )
        self.val_loader = DataLoader(
            self.val_dataset, batch_size=self.batch_size, shuffle=False
        )

        print(f"📊 Train: {len(self.train_dataset)} samples")
        print(f"📊 Validation: {len(self.val_dataset)} samples")

        # Print action distribution
        unique, counts = np.unique(actions, return_counts=True)
        print("\n🎮 Action Distribution:")
        action_names = ['idle', 'move_left', 'move_right', 'jump', 'punch', 'kick',
                       'block', 'move_left_block', 'move_right_block', 'projectile']
        for action_idx, count in zip(unique, counts):
            if action_idx < len(action_names):
                name = action_names[action_idx]
                percentage = (count / len(actions)) * 100
                print(f"  {name}: {count} ({percentage:.1f}%)")

    def train_epoch(self):
        """Train for one epoch"""
        self.policy.train()
        total_loss = 0
        correct = 0
        total = 0

        for states, actions in self.train_loader:
            # Forward pass
            action_logits, _ = self.policy(states)
            loss = self.criterion(action_logits, actions)

            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            # Statistics
            total_loss += loss.item()
            _, predicted = torch.max(action_logits.data, 1)
            total += actions.size(0)
            correct += (predicted == actions).sum().item()

        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100 * correct / total

        return avg_loss, accuracy

    def validate(self):
        """Validate the model"""
        self.policy.eval()
        total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for states, actions in self.val_loader:
                action_logits, _ = self.policy(states)
                loss = self.criterion(action_logits, actions)

                total_loss += loss.item()
                _, predicted = torch.max(action_logits.data, 1)
                total += actions.size(0)
                correct += (predicted == actions).sum().item()

        avg_loss = total_loss / len(self.val_loader)
        accuracy = 100 * correct / total

        return avg_loss, accuracy

    def train(self, num_epochs=None):
        """Train the policy using behavioral cloning"""
        if num_epochs is not None:
            self.num_epochs = num_epochs

        print(f"\n🚀 Starting behavioral cloning training for {self.num_epochs} epochs")
        print(f"📊 Batch size: {self.batch_size}, Learning rate: {self.learning_rate}")

        best_val_accuracy = 0
        best_model_state = None

        for epoch in range(self.num_epochs):
            # Train
            train_loss, train_acc = self.train_epoch()

            # Validate
            val_loss, val_acc = self.validate()

            # Store history
            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)
            self.train_accuracies.append(train_acc)
            self.val_accuracies.append(val_acc)

            # Save best model
            if val_acc > best_val_accuracy:
                best_val_accuracy = val_acc
                best_model_state = self.policy.state_dict().copy()

            # Print progress
            if (epoch + 1) % 10 == 0 or epoch == 0:
                print(f"Epoch {epoch+1:3d}/{self.num_epochs}: "
                      f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.1f}%, "
                      f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.1f}%")

        # Load best model
        if best_model_state is not None:
            self.policy.load_state_dict(best_model_state)
            print(f"\n✅ Training completed! Best validation accuracy: {best_val_accuracy:.1f}%")

        return best_val_accuracy

    def save_policy(self, filepath):
        """Save the trained policy"""
        torch.save({
            'model_state_dict': self.policy.state_dict(),
            'training_history': {
                'train_losses': self.train_losses,
                'val_losses': self.val_losses,
                'train_accuracies': self.train_accuracies,
                'val_accuracies': self.val_accuracies
            },
            'model_config': {
                'state_size': self.state_size,
                'action_size': self.action_size,
                'hidden_size': self.hidden_size
            }
        }, filepath)
        print(f"💾 Saved behavioral cloning policy to {filepath}")

    def plot_training_history(self, save_path=None):
        """Plot training history"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Loss plot
        ax1.plot(self.train_losses, label='Train Loss')
        ax1.plot(self.val_losses, label='Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.set_title('Training Loss')
        ax1.legend()
        ax1.grid(True)

        # Accuracy plot
        ax2.plot(self.train_accuracies, label='Train Accuracy')
        ax2.plot(self.val_accuracies, label='Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.set_title('Training Accuracy')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"📊 Saved training plot to {save_path}")
        else:
            plt.show()

def main():
    """Example usage"""
    # Example: Train on demonstrations
    trainer = BehavioralCloningTrainer()

    # Load demonstrations (you'll need to record some first)
    demo_file = "src/human_demonstrations/data/human_demos_example.json"
    if os.path.exists(demo_file):
        trainer.load_demonstrations(demo_file)
        trainer.train(num_epochs=50)
        trainer.save_policy("src/training/policies/behavioral_cloning_init.pth")
        trainer.plot_training_history()
    else:
        print(f"❌ Demo file not found: {demo_file}")
        print("Record some demonstrations first using the recorder!")

if __name__ == "__main__":
    main()
