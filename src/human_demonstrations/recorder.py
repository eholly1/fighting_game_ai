"""
Human Demonstration Recorder
Records human gameplay for behavioral cloning
"""
import json
import time
import numpy as np
from datetime import datetime
import os
import pygame

class DemonstrationRecorder:
    """Records human demonstrations for behavioral cloning"""
    
    def __init__(self, save_dir='src/human_demonstrations/data'):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
        self.recording = False
        self.demonstrations = []
        self.current_episode = []
        
        # Action mapping (reverse of environment mapping)
        self.action_mapping = {
            'idle': 0,
            'move_left': 1,
            'move_right': 2,
            'jump': 3,
            'punch': 4,
            'kick': 5,
            'block': 6,
            'move_left_block': 7,
            'move_right_block': 8,
            'projectile': 9
        }
        
        print("🎬 Demonstration Recorder initialized")
        print("📁 Save directory:", save_dir)
        print("\n🎮 Recording Controls:")
        print("  F1 - Start/Stop recording")
        print("  F2 - Save demonstrations")
        print("  F3 - Clear demonstrations")
        print("  F4 - Show statistics")
    
    def handle_key_event(self, event):
        """Handle recording control keys"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                if self.recording:
                    self.stop_recording()
                else:
                    self.start_recording()
            elif event.key == pygame.K_F2:
                self.save_demonstrations()
            elif event.key == pygame.K_F3:
                self.clear_demonstrations()
            elif event.key == pygame.K_F4:
                print(self.get_stats())
    
    def start_recording(self):
        """Start recording demonstrations"""
        self.recording = True
        self.current_episode = []
        print("🔴 RECORDING STARTED - Play naturally!")
        print("   Press F1 again to stop recording")
    
    def stop_recording(self):
        """Stop recording and save current episode"""
        if self.recording and len(self.current_episode) > 0:
            self.demonstrations.append(self.current_episode.copy())
            print(f"📹 Episode recorded: {len(self.current_episode)} steps")
            print(f"📊 Total episodes: {len(self.demonstrations)}")
            print(f"📊 Total samples: {sum(len(ep) for ep in self.demonstrations)}")
        elif self.recording:
            print("📹 Recording stopped (no data recorded)")
        
        self.recording = False
        self.current_episode = []
    
    def record_step(self, state, action_name):
        """Record a single step of demonstration"""
        if not self.recording:
            return
        
        # Convert action name to action index
        action_idx = self.action_mapping.get(action_name, 0)
        
        # Store state-action pair
        demo_step = {
            'state': state.tolist() if isinstance(state, np.ndarray) else state,
            'action': action_idx,
            'action_name': action_name,
            'timestamp': time.time()
        }
        
        self.current_episode.append(demo_step)
    
    def save_demonstrations(self, filename=None):
        """Save all demonstrations to file"""
        if not self.demonstrations:
            print("❌ No demonstrations to save!")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"human_demos_{timestamp}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        # Prepare data for saving
        save_data = {
            'metadata': {
                'num_episodes': len(self.demonstrations),
                'total_steps': sum(len(ep) for ep in self.demonstrations),
                'recorded_at': datetime.now().isoformat(),
                'action_mapping': self.action_mapping,
                'state_size': len(self.demonstrations[0][0]['state']) if self.demonstrations else 0
            },
            'demonstrations': self.demonstrations
        }
        
        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"💾 Saved {len(self.demonstrations)} episodes to {filepath}")
        print(f"📊 Total steps: {save_data['metadata']['total_steps']}")
        return filepath
    
    def clear_demonstrations(self):
        """Clear all recorded demonstrations"""
        self.demonstrations = []
        self.current_episode = []
        print("🗑️ Cleared all demonstrations")
    
    def get_stats(self):
        """Get recording statistics"""
        total_steps = sum(len(ep) for ep in self.demonstrations)
        if total_steps == 0:
            return "📊 No demonstrations recorded"
        
        avg_episode_length = total_steps / len(self.demonstrations) if self.demonstrations else 0
        
        # Count action distribution
        action_counts = {}
        for episode in self.demonstrations:
            for step in episode:
                action_name = step['action_name']
                action_counts[action_name] = action_counts.get(action_name, 0) + 1
        
        stats = f"""
📊 Demonstration Statistics:
  Episodes: {len(self.demonstrations)}
  Total steps: {total_steps}
  Avg episode length: {avg_episode_length:.1f}
  Recording status: {'🔴 RECORDING' if self.recording else '⚫ STOPPED'}
  
🎮 Action Distribution:"""
        
        for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_steps) * 100
            stats += f"\n  {action}: {count} ({percentage:.1f}%)"
        
        return stats

def load_demonstrations(filepath):
    """Load demonstrations from file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"📂 Loaded demonstrations from {filepath}")
    print(f"📊 Episodes: {data['metadata']['num_episodes']}")
    print(f"📊 Total steps: {data['metadata']['total_steps']}")
    
    return data

def demonstrations_to_dataset(demonstrations_data):
    """Convert demonstrations to training dataset"""
    states = []
    actions = []
    
    for episode in demonstrations_data['demonstrations']:
        for step in episode:
            states.append(step['state'])
            actions.append(step['action'])
    
    return np.array(states, dtype=np.float32), np.array(actions, dtype=np.int64)
