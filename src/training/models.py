"""
Neural Network Models for Fighting Game RL
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class FighterPolicy(nn.Module):
    """Policy network for fighting game AI"""

    def __init__(self, state_size=26, action_size=10, hidden_size=128):
        super(FighterPolicy, self).__init__()

        self.state_size = state_size
        self.action_size = action_size

        # Policy network
        self.policy_net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size)
        )

        # Value network (for actor-critic)
        self.value_net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, state):
        """Forward pass - returns action logits and value"""
        action_logits = self.policy_net(state)
        value = self.value_net(state)
        return action_logits, value

    def get_action(self, state, deterministic=False):
        """Get action from state"""
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state)

        if len(state.shape) == 1:
            state = state.unsqueeze(0)

        with torch.no_grad():
            action_logits, _ = self.forward(state)
            action_probs = F.softmax(action_logits, dim=-1)

            if deterministic:
                action = torch.argmax(action_probs, dim=-1)
            else:
                action = torch.multinomial(action_probs, 1).squeeze(-1)

            return action.item() if action.numel() == 1 else action.cpu().numpy()

    def get_action_and_value(self, state):
        """Get action, log probability, and value"""
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state)

        action_logits, value = self.forward(state)
        action_probs = F.softmax(action_logits, dim=-1)
        action_dist = torch.distributions.Categorical(action_probs)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)

        return action, log_prob, value.squeeze(-1)

class PPOTrainer:
    """PPO (Proximal Policy Optimization) trainer"""

    def __init__(self, policy, lr=3e-4, eps_clip=0.2, value_coef=0.5, entropy_coef=0.01):
        self.policy = policy
        self.optimizer = torch.optim.Adam(policy.parameters(), lr=lr)

        self.eps_clip = eps_clip
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef

        # Training statistics
        self.training_stats = {
            'policy_loss': [],
            'value_loss': [],
            'entropy_loss': [],
            'total_loss': []
        }

    def update(self, states, actions, old_log_probs, returns, advantages):
        """Update policy using PPO"""
        # Convert to tensors
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        old_log_probs = torch.FloatTensor(old_log_probs)
        returns = torch.FloatTensor(returns)
        advantages = torch.FloatTensor(advantages)

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Multiple epochs of updates
        for _ in range(4):  # PPO typically does multiple epochs
            # Get current policy outputs
            action_logits, values = self.policy(states)
            action_probs = F.softmax(action_logits, dim=-1)
            action_dist = torch.distributions.Categorical(action_probs)

            new_log_probs = action_dist.log_prob(actions)
            entropy = action_dist.entropy().mean()

            # Calculate ratio for PPO
            ratio = torch.exp(new_log_probs - old_log_probs)

            # Calculate surrogate losses
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            policy_loss = -torch.min(surr1, surr2).mean()

            # Value loss
            value_loss = F.mse_loss(values.squeeze(-1), returns)

            # Total loss
            total_loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy

            # Update
            self.optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.optimizer.step()

            # Store stats
            self.training_stats['policy_loss'].append(policy_loss.item())
            self.training_stats['value_loss'].append(value_loss.item())
            self.training_stats['entropy_loss'].append(entropy.item())
            self.training_stats['total_loss'].append(total_loss.item())

    def get_stats(self):
        """Get recent training statistics"""
        if not self.training_stats['total_loss']:
            return {}

        return {
            'policy_loss': np.mean(self.training_stats['policy_loss'][-10:]),
            'value_loss': np.mean(self.training_stats['value_loss'][-10:]),
            'entropy': np.mean(self.training_stats['entropy_loss'][-10:]),
            'total_loss': np.mean(self.training_stats['total_loss'][-10:])
        }

class RandomPolicy:
    """Random policy for baseline/opponent"""

    def __init__(self, action_size=10):
        self.action_size = action_size

    def get_action(self, state, deterministic=False):
        """Return random action"""
        return np.random.randint(0, self.action_size)

class SimplePolicy:
    """Simple rule-based policy for training opponents"""

    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.action_size = 9

        # Difficulty parameters (balanced for training)
        if difficulty == 'easy':
            self.reaction_delay = 0.3
            self.mistake_rate = 0.3
            self.aggression = 0.4  # Moderate increase from 0.3
        elif difficulty == 'medium':
            self.reaction_delay = 0.15
            self.mistake_rate = 0.15
            self.aggression = 0.6  # Moderate increase from 0.5
        else:  # hard
            self.reaction_delay = 0.05
            self.mistake_rate = 0.05
            self.aggression = 0.8  # Moderate increase from 0.7

        self.last_action_time = 0

    def get_action(self, state, deterministic=False):
        """Get action based on simple rules"""
        # Add reaction delay
        self.last_action_time += 1
        if self.last_action_time < self.reaction_delay * 60:  # Convert to frames
            return 0  # idle

        # Random mistakes
        if np.random.random() < self.mistake_rate:
            return np.random.randint(0, self.action_size)

        # Simple strategy based on state
        # state[22] is distance, state[25] is health advantage
        distance = state[22]  # Already normalized (0-1)
        health_advantage = state[25]

        # Close range - attack or block
        if distance < 0.15:  # Close
            if np.random.random() < self.aggression:
                return np.random.choice([4, 5])  # punch or kick
            else:
                return 6  # block

        # Medium range - move in, attack, or projectile
        elif distance < 0.3:
            if np.random.random() < self.aggression * 0.8:  # Slightly less aggressive
                return np.random.choice([4, 5])  # attack
            elif np.random.random() < 0.2:  # 20% chance for projectile
                return 9  # projectile
            else:
                # Move towards opponent
                if state[23] > 0:  # opponent is to the right
                    return 2  # move right (towards opponent)
                else:
                    return 1  # move left (towards opponent)

        # Far range - move in or projectile
        else:
            if np.random.random() < 0.3:  # 30% chance for projectile at far range
                return 9  # projectile
            elif state[23] > 0:  # opponent is to the right
                return 2  # move right (towards opponent)
            else:
                return 1  # move left (towards opponent)

        return 0  # idle as fallback
