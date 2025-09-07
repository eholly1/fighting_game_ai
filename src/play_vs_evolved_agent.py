#!/usr/bin/env python3
"""
Play Against Evolved Agent

Allows human players to fight against evolved AI agents from the
evolutionary training system.
"""
import sys
import os
import argparse
import pygame

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'evolution'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'training'))

from game.core.game_engine import Game
from game.core import config
from game.entities.fighter import Fighter
from game.controllers.input_handler import PlayerController
from game.controllers.ai_controller import RLAIController
from evolution.agent_serialization import AgentSerializer
from evolution.safe_execution import SafeAgent

class EvolvedAgentController(RLAIController):
    """
    AI Controller that uses an evolved agent
    """

    def __init__(self, agent_path: str):
        """
        Initialize with evolved agent

        Args:
            agent_path: Path to the evolved agent file
        """
        super().__init__()
        self.agent_path = agent_path
        self.agent = None
        self.agent_info = {}

        # Load the evolved agent
        self._load_agent()

    def _load_agent(self):
        """Load the evolved agent from file"""
        try:
            # Read the agent file directly
            with open(self.agent_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract the code part (everything after "# Agent Code:")
            if "# Agent Code:" in content:
                code_start = content.find("# Agent Code:") + len("# Agent Code:")
                code = content[code_start:].strip()
            else:
                # Fallback: use everything after the docstring
                parts = content.split('"""')
                if len(parts) >= 3:
                    code = '"""'.join(parts[2:]).strip()
                else:
                    code = content

            # Extract metadata from the docstring
            agent_id = os.path.basename(self.agent_path).replace('.py', '')
            fitness = 'Unknown'
            fighting_style = 'Unknown'
            generation = 'Unknown'
            win_rate = 'Unknown'

            if '"""' in content:
                docstring = content.split('"""')[1]

                # Extract info from docstring
                for line in docstring.split('\n'):
                    if 'Agent ID:' in line:
                        agent_id = line.split('Agent ID:')[1].strip()
                    elif 'Fitness:' in line:
                        fitness_text = line.split('Fitness:')[1].strip()
                        try:
                            fitness = float(fitness_text)
                        except:
                            fitness = fitness_text
                    elif 'Fighting Style:' in line:
                        fighting_style = line.split('Fighting Style:')[1].strip()
                    elif 'Generation:' in line:
                        generation = line.split('Generation:')[1].strip()
                    elif 'Win Rate:' in line:
                        win_rate_text = line.split('Win Rate:')[1].strip().replace('%', '')
                        try:
                            win_rate = float(win_rate_text) / 100.0
                        except:
                            win_rate = win_rate_text

            # Create safe agent
            self.agent = SafeAgent(agent_id, code)

            if not self.agent.is_valid:
                raise ValueError(f"Agent failed to compile: {agent_id}")

            # Store agent info
            self.agent_info = {
                'id': agent_id,
                'fitness': fitness,
                'fighting_style': fighting_style,
                'generation': generation,
                'win_rate': win_rate
            }

            print(f"✅ Loaded evolved agent:")
            print(f"   ID: {self.agent_info['id']}")
            print(f"   Fitness: {self.agent_info['fitness']}")
            print(f"   Fighting Style: {self.agent_info['fighting_style']}")
            print(f"   Generation: {self.agent_info['generation']}")
            if isinstance(self.agent_info['win_rate'], (int, float)):
                print(f"   Win Rate: {float(self.agent_info['win_rate'])*100:.1f}%")

        except Exception as e:
            print(f"❌ Failed to load agent: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def get_action(self, state):
        """
        Get action from the evolved agent

        Args:
            state: Game state array

        Returns:
            Action integer (0-9)
        """
        try:
            if self.agent and self.agent.is_valid:
                action = self.agent.get_action(state)
                return action
            else:
                return 0  # Idle if agent is invalid

        except Exception as e:
            # Agent error - return idle action
            if not hasattr(self, '_error_count'):
                self._error_count = 0
            self._error_count += 1

            if self._error_count <= 3:  # Only print first few errors
                print(f"⚠️  Agent error: {e}")

            return 0

def list_available_agents(experiments_dir: str = "src/evolution/experiments"):
    """List all available evolved agents"""
    print(f"🔍 Available Evolved Agents:")
    print("=" * 60)

    if not os.path.exists(experiments_dir):
        print(f"❌ No experiments directory found: {experiments_dir}")
        print(f"💡 Run evolutionary training first:")
        print(f"   cd src/evolution")
        print(f"   python evolution_runner.py --population 3 --generations 1")
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

            print(f"   {len(agents)+1:2d}. Rank {rank:3s} | Fitness {fitness:6s} | {agent_file}")

            agents.append({
                'path': agent_path,
                'experiment': experiment,
                'rank': rank,
                'fitness': fitness,
                'filename': agent_file,
                'display_name': f"Rank {rank} (Fitness {fitness})"
            })

    if not agents:
        print(f"❌ No agents found in any experiments.")
        print(f"💡 Run evolutionary training first:")
        print(f"   cd src/evolution")
        print(f"   python evolution_runner.py --population 3 --generations 1")

    return agents

def select_agent_interactive(agents):
    """Let user select an agent interactively"""
    if not agents:
        return None

    print(f"\n🎯 Select an agent to fight against:")

    while True:
        try:
            choice = input(f"Enter agent number (1-{len(agents)}) or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                return None

            agent_num = int(choice)
            if 1 <= agent_num <= len(agents):
                selected = agents[agent_num - 1]
                print(f"✅ Selected: {selected['display_name']}")
                return selected['path']
            else:
                print(f"❌ Please enter a number between 1 and {len(agents)}")

        except ValueError:
            print(f"❌ Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print(f"\n👋 Cancelled")
            return None

class EvolvedAgentGame(Game):
    """
    Game class that uses an evolved agent as Player 2
    """

    def __init__(self, agent_path: str, **kwargs):
        """
        Initialize game with evolved agent

        Args:
            agent_path: Path to evolved agent file
            **kwargs: Additional arguments for Game
        """
        self.agent_path = agent_path
        self.evolved_controller = None
        super().__init__(**kwargs)

        # Load the evolved agent controller
        self.evolved_controller = EvolvedAgentController(self.agent_path)

        print(f"\n🥊 Human vs Evolved Agent Fight!")
        print(f"   Player 1 (Human) vs Player 2 (Evolved Agent)")
        print(f"\n🎮 Controls:")
        print(f"   Player 1: WASD to move, J=punch, K=kick, L=block, I=projectile")
        print(f"   ESC=quit, P=pause, R=restart")
        print(f"\n🚀 Press any key to start fighting!")

    def start_game(self, mode=None):
        """Override start_game to always use evolved agent mode"""
        # Force human vs evolved agent mode
        self.game_mode = 'human_vs_evolved_agent'
        self.state = config.GameState.FIGHTING

        # Play game start sound
        self.audio_manager.play_sound('game_start')

        # Reset projectiles and timer
        self.projectiles = []
        self.round_timer = config.ROUND_TIME_FRAMES
        self.winner = None

        # Create fighters
        self.fighter1 = Fighter(
            x=config.SCREEN_WIDTH // 4,
            y=config.STAGE_FLOOR - config.FIGHTER_HEIGHT,
            color=config.RED,
            facing_right=True
        )

        self.fighter2 = Fighter(
            x=3 * config.SCREEN_WIDTH // 4,
            y=config.STAGE_FLOOR - config.FIGHTER_HEIGHT,
            color=config.BLUE,
            facing_right=False
        )

        # Set up controllers
        self.player1_controller = PlayerController(1, self.input_handler)
        self.ai_controller = self.evolved_controller  # Use evolved agent as AI
        self.player2_controller = None

    def handle_keydown(self, key):
        """Override keydown handling for evolved agent mode"""
        if self.state == config.GameState.MENU:
            # Any key starts the fight
            self.audio_manager.play_sound('menu_confirm')
            self.start_game()
        elif self.state == config.GameState.FIGHTING:
            if key == pygame.K_ESCAPE:
                self.state = config.GameState.MENU
            elif key == pygame.K_p:
                self.toggle_pause()
            elif key == pygame.K_r:
                self.restart_fight()
        elif self.state == config.GameState.GAME_OVER:
            if key == pygame.K_r:
                self.restart_fight()
            elif key == pygame.K_ESCAPE:
                self.state = config.GameState.MENU
        elif self.state == config.GameState.PAUSED:
            if key == pygame.K_p:
                self.toggle_pause()
            elif key == pygame.K_ESCAPE:
                self.state = config.GameState.MENU

    def restart_fight(self):
        """Restart the current fight"""
        self.start_game()

    def update_fight(self):
        """Override fight update to handle evolved agent"""
        # Update fighter facing directions
        if self.fighter1.x < self.fighter2.x:
            self.fighter1.facing_right = True
            self.fighter2.facing_right = False
        else:
            self.fighter1.facing_right = False
            self.fighter2.facing_right = True

        # Handle input for human player (fighter1)
        projectile1 = self.player1_controller.update_fighter(
            self.fighter1, self.audio_manager, self.demo_recorder, self.fighter2
        )
        if projectile1:
            self.projectiles.append(projectile1)

        # Handle evolved agent (fighter2)
        projectile2 = self.ai_controller.update_fighter(self.fighter2, self.fighter1, self.audio_manager)
        if projectile2:
            self.projectiles.append(projectile2)

        # Update fighters
        self.fighter1.update()
        self.fighter2.update()

        # Update projectiles
        self.update_projectiles()

        # Update particle system
        self.particle_system.update()

        # Check for attacks hitting
        self.check_combat()

        # Check for projectile hits
        self.check_projectile_hits()

        # Check for character collisions
        self.check_character_collision()

        # Update round timer
        if self.round_timer > 0:
            self.round_timer -= 1

        # Check for game over conditions
        game_over = False

        # Check for KO
        if not self.fighter1.is_alive() or not self.fighter2.is_alive():
            game_over = True
            if not self.fighter1.is_alive():
                self.winner = "Evolved Agent"
            else:
                self.winner = "Human"

        # Check for timeout
        elif self.round_timer <= 0:
            game_over = True
            # Determine winner by health
            if self.fighter1.health > self.fighter2.health:
                self.winner = "Human"
            elif self.fighter2.health > self.fighter1.health:
                self.winner = "Evolved Agent"
            else:
                self.winner = "Draw"

        if game_over and self.state != config.GameState.GAME_OVER:
            self.audio_manager.play_sound('game_over')
            self.state = config.GameState.GAME_OVER

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Play against evolved AI agents")
    parser.add_argument('--agent', type=str, help='Path to specific agent file')
    parser.add_argument('--list', action='store_true', help='List available agents')
    parser.add_argument('--experiments-dir', type=str, default='src/evolution/experiments',
                       help='Directory containing experiments')
    parser.add_argument('--auto-select', action='store_true',
                       help='Automatically select the best available agent')

    args = parser.parse_args()

    print(f"🥊 Fighting Game - Human vs Evolved Agent")
    print("=" * 50)

    if args.list:
        list_available_agents(args.experiments_dir)
        return

    agent_path = None

    if args.agent:
        agent_path = args.agent
        if not os.path.exists(agent_path):
            print(f"❌ Agent file not found: {agent_path}")
            return
    else:
        # List available agents and let user choose
        agents = list_available_agents(args.experiments_dir)

        if not agents:
            return

        if args.auto_select:
            # Auto-select the best agent (first in list)
            agent_path = agents[0]['path']
            print(f"\n🤖 Auto-selected: {agents[0]['display_name']}")
        else:
            # Interactive selection
            agent_path = select_agent_interactive(agents)

            if not agent_path:
                print(f"👋 No agent selected. Goodbye!")
                return

    try:
        # Create and run the game with evolved agent
        print(f"\n🚀 Starting game...")
        game = EvolvedAgentGame(agent_path)
        game.run()

    except KeyboardInterrupt:
        print(f"\n👋 Game interrupted by user")
    except Exception as e:
        print(f"❌ Game failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
