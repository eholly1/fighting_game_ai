#!/usr/bin/env python3
"""
Play Against Evolved Agent

Allows human players to fight against evolved AI agents from the
evolutionary training system.
"""
import sys
import os
import pygame
import numpy as np
from typing import Optional

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))

# Import game components
from game_engine import GameEngine
from fighter import Fighter
from agent_serialization import AgentSerializer
from safe_execution import SafeAgent

class HumanVsAgentGame:
    """
    Game mode for human vs evolved agent
    """
    
    def __init__(self, agent_path: str):
        """
        Initialize the human vs agent game
        
        Args:
            agent_path: Path to the evolved agent file
        """
        self.agent_path = agent_path
        self.agent = None
        self.game_engine = None
        
        # Load the evolved agent
        self._load_agent()
        
        # Initialize game
        self._init_game()
    
    def _load_agent(self):
        """Load the evolved agent from file"""
        try:
            # Get the directory containing the agent file
            agent_dir = os.path.dirname(self.agent_path)
            serializer = AgentSerializer(agent_dir)
            
            # Load the agent
            agent_data = serializer.load_agent_python(self.agent_path)
            
            if agent_data is None:
                raise ValueError(f"Could not load agent from {self.agent_path}")
            
            # Create safe agent
            self.agent = SafeAgent(agent_data.agent_id, agent_data.code)
            
            if not self.agent.is_valid:
                raise ValueError(f"Agent failed to compile: {agent_data.agent_id}")
            
            print(f"✅ Loaded agent: {agent_data.agent_id}")
            print(f"   Fitness: {agent_data.metadata.get('fitness', 'Unknown')}")
            print(f"   Fighting Style: {agent_data.metadata.get('fighting_style', 'Unknown')}")
            print(f"   Generation: {agent_data.metadata.get('generation', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Failed to load agent: {e}")
            sys.exit(1)
    
    def _init_game(self):
        """Initialize the game engine"""
        try:
            self.game_engine = GameEngine()
            print(f"✅ Game engine initialized")
            print(f"🎮 Controls:")
            print(f"   A/D: Move left/right")
            print(f"   W: Jump")
            print(f"   J: Punch")
            print(f"   K: Kick") 
            print(f"   L: Block")
            print(f"   I: Projectile")
            print(f"   ESC: Quit")
            print(f"   R: Restart round")
            
        except Exception as e:
            print(f"❌ Failed to initialize game: {e}")
            sys.exit(1)
    
    def _get_human_action(self, keys) -> int:
        """Convert keyboard input to game action"""
        # Check for multiple key presses and prioritize
        
        # Block + movement combinations
        if keys[pygame.K_l]:  # Block key
            if keys[pygame.K_a]:
                return 7  # move_left_block
            elif keys[pygame.K_d]:
                return 8  # move_right_block
            else:
                return 6  # block
        
        # Attack actions (highest priority)
        if keys[pygame.K_j]:
            return 4  # punch
        if keys[pygame.K_k]:
            return 5  # kick
        if keys[pygame.K_i]:
            return 9  # projectile
        
        # Movement actions
        if keys[pygame.K_w]:
            return 3  # jump
        if keys[pygame.K_a]:
            return 1  # move_left
        if keys[pygame.K_d]:
            return 2  # move_right
        
        return 0  # idle
    
    def _get_agent_action(self) -> int:
        """Get action from the evolved agent"""
        try:
            # Get game state for the agent (player 2 perspective)
            state = self.game_engine.get_state(player_fighter=self.game_engine.fighter2)
            
            # Get action from agent
            action = self.agent.get_action(state)
            
            return action
            
        except Exception as e:
            print(f"⚠️  Agent error: {e}")
            return 0  # Default to idle on error
    
    def _display_game_info(self):
        """Display game information on screen"""
        # This would be implemented with pygame text rendering
        # For now, we'll print to console periodically
        pass
    
    def _check_round_end(self) -> Optional[str]:
        """Check if the round has ended and return winner"""
        fighter1 = self.game_engine.fighter1  # Human
        fighter2 = self.game_engine.fighter2  # Agent
        
        # Check for KO
        if not fighter1.is_alive():
            return "Agent"
        elif not fighter2.is_alive():
            return "Human"
        
        # Check for timeout
        if self.game_engine.timer <= 0:
            if fighter1.health > fighter2.health:
                return "Human"
            elif fighter2.health > fighter1.health:
                return "Agent"
            else:
                return "Draw"
        
        return None
    
    def play(self):
        """Main game loop"""
        print(f"\n🥊 Starting Human vs Agent Fight!")
        print(f"   Human (Player 1) vs {self.agent.agent_id} (Player 2)")
        
        clock = pygame.time.Clock()
        running = True
        round_count = 1
        human_wins = 0
        agent_wins = 0
        draws = 0
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Restart round
                        self.game_engine.reset()
                        print(f"\n🔄 Round {round_count} restarted!")
            
            # Get input
            keys = pygame.key.get_pressed()
            human_action = self._get_human_action(keys)
            agent_action = self._get_agent_action()
            
            # Update game
            self.game_engine.update(human_action, agent_action)
            
            # Check for round end
            winner = self._check_round_end()
            if winner:
                if winner == "Human":
                    human_wins += 1
                    print(f"🏆 Round {round_count}: Human wins!")
                elif winner == "Agent":
                    agent_wins += 1
                    print(f"🤖 Round {round_count}: Agent wins!")
                else:
                    draws += 1
                    print(f"🤝 Round {round_count}: Draw!")
                
                print(f"📊 Score - Human: {human_wins}, Agent: {agent_wins}, Draws: {draws}")
                print(f"   Press R to start next round, ESC to quit")
                
                # Wait for restart or quit
                waiting = True
                while waiting and running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                waiting = False
                            elif event.key == pygame.K_r:
                                round_count += 1
                                self.game_engine.reset()
                                print(f"\n🥊 Round {round_count} starting!")
                                waiting = False
                    
                    clock.tick(60)
            
            # Render game
            self.game_engine.render()
            
            # Control frame rate
            clock.tick(60)
        
        # Final statistics
        total_rounds = human_wins + agent_wins + draws
        if total_rounds > 0:
            print(f"\n📈 Final Statistics:")
            print(f"   Total Rounds: {total_rounds}")
            print(f"   Human Wins: {human_wins} ({human_wins/total_rounds*100:.1f}%)")
            print(f"   Agent Wins: {agent_wins} ({agent_wins/total_rounds*100:.1f}%)")
            print(f"   Draws: {draws} ({draws/total_rounds*100:.1f}%)")
            
            if human_wins > agent_wins:
                print(f"🏆 Overall Winner: Human!")
            elif agent_wins > human_wins:
                print(f"🤖 Overall Winner: Agent!")
            else:
                print(f"🤝 Overall Result: Tie!")
        
        pygame.quit()

def list_available_agents(experiments_dir: str = "experiments"):
    """List all available evolved agents"""
    print(f"🔍 Available Evolved Agents:")
    print("=" * 50)
    
    if not os.path.exists(experiments_dir):
        print(f"❌ No experiments directory found: {experiments_dir}")
        return []
    
    agents = []
    
    for experiment in os.listdir(experiments_dir):
        experiment_path = os.path.join(experiments_dir, experiment)
        if not os.path.isdir(experiment_path):
            continue
        
        top_agents_dir = os.path.join(experiment_path, "top_agents")
        if not os.path.exists(top_agents_dir):
            continue
        
        print(f"\n📁 Experiment: {experiment}")
        
        agent_files = [f for f in os.listdir(top_agents_dir) if f.endswith('.py')]
        agent_files.sort()  # Sort by rank
        
        for i, agent_file in enumerate(agent_files[:5]):  # Show top 5
            agent_path = os.path.join(top_agents_dir, agent_file)
            
            # Extract info from filename
            parts = agent_file.replace('.py', '').split('_')
            rank = parts[1] if len(parts) > 1 else "?"
            fitness = parts[3] if len(parts) > 3 else "?"
            
            print(f"   {i+1}. Rank {rank}, Fitness {fitness}")
            print(f"      File: {agent_file}")
            
            agents.append({
                'path': agent_path,
                'experiment': experiment,
                'rank': rank,
                'fitness': fitness,
                'filename': agent_file
            })
    
    return agents

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Play against evolved AI agents")
    parser.add_argument('--agent', type=str, help='Path to specific agent file')
    parser.add_argument('--list', action='store_true', help='List available agents')
    parser.add_argument('--experiments-dir', type=str, default='experiments',
                       help='Directory containing experiments (default: experiments)')
    
    args = parser.parse_args()
    
    # Change to evolution directory if needed
    if os.path.basename(os.getcwd()) != 'evolution':
        if os.path.exists('src/evolution'):
            os.chdir('src/evolution')
        elif os.path.exists('evolution'):
            os.chdir('evolution')
    
    if args.list:
        agents = list_available_agents(args.experiments_dir)
        if not agents:
            print(f"❌ No agents found. Run some evolutionary training first!")
        return
    
    if args.agent:
        agent_path = args.agent
    else:
        # Try to find the best agent automatically
        agents = list_available_agents(args.experiments_dir)
        
        if not agents:
            print(f"❌ No agents found. Run some evolutionary training first!")
            print(f"💡 Try: python evolution_runner.py --population 3 --generations 1")
            return
        
        # Use the best agent (first in list)
        agent_path = agents[0]['path']
        print(f"🤖 Auto-selected best agent: {agents[0]['filename']}")
    
    if not os.path.exists(agent_path):
        print(f"❌ Agent file not found: {agent_path}")
        return
    
    try:
        # Create and run the game
        game = HumanVsAgentGame(agent_path)
        game.play()
        
    except KeyboardInterrupt:
        print(f"\n👋 Game interrupted by user")
    except Exception as e:
        print(f"❌ Game failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
