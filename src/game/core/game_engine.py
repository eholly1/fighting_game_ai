"""
Main game logic and state management
"""
import pygame
from . import config
from ..entities.fighter import Fighter
from ..controllers.input_handler import InputHandler, PlayerController
from ..controllers.ai_controller import DummyAI, RLAIController
from ..rendering.renderer import Renderer
from ..rendering.particles import ParticleSystem
from ..audio.audio_manager import AudioManager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from human_demonstrations.recorder import DemonstrationRecorder

class Game:
    def __init__(self, record_demonstrations=False):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("2D Fighting Game")
        self.clock = pygame.time.Clock()

        # Game state
        self.state = config.GameState.MENU
        self.running = True
        self.auto_record = record_demonstrations

        # Input handling
        self.input_handler = InputHandler()

        # Rendering
        self.renderer = Renderer(self.screen)
        self.renderer.game_engine = self  # Pass reference for menu rendering
        self.particle_system = ParticleSystem()

        # Audio
        self.audio_manager = AudioManager()

        # Human demonstration recording
        self.demo_recorder = DemonstrationRecorder()

        # Game objects (initialized when starting a fight)
        self.fighter1 = None
        self.fighter2 = None
        self.projectiles = []  # List of active projectiles
        self.player1_controller = None
        self.player2_controller = None
        self.ai_controller = None
        self.ai_controller2 = None  # For AI vs AI mode

        # Game mode
        self.game_mode = None  # 'human_vs_ai', 'human_vs_human', 'human_vs_rl_ai', 'ai_vs_ai'

        # Menu state
        self.menu_field = 0  # 0 = personality, 1 = difficulty
        self.selected_personality = 0  # Index in personality list
        self.selected_difficulty = 0   # Index in difficulty list
        self.personalities = ["Aggressive", "Defensive"]
        self.difficulties = ["Easy", "Medium", "Hard"]

        # Round timer
        self.round_timer = config.ROUND_TIME_FRAMES  # Timer in frames
        self.winner = None  # Track who won the round

    def run(self):
        """Main game loop"""
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.render()
            self.clock.tick(config.FPS)

        pygame.quit()

    def _load_evolved_agent(self):
        """Load the best evolved agent from experiments"""
        try:
            # Import the evolved agent controller
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from play_vs_evolved_agent import EvolvedAgentController

            # Find the best agent
            experiments_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'evolution', 'experiments')

            if not os.path.exists(experiments_dir):
                print("❌ No evolved agents found. Using rule-based AI instead.")
                return DummyAI()

            best_agent_path = None
            best_fitness = -1

            # Search for the best agent
            for experiment in os.listdir(experiments_dir):
                experiment_path = os.path.join(experiments_dir, experiment)
                if not os.path.isdir(experiment_path):
                    continue

                top_agents_dir = os.path.join(experiment_path, "top_agents")
                if not os.path.exists(top_agents_dir):
                    continue

                for agent_file in os.listdir(top_agents_dir):
                    if agent_file.endswith('.py') and 'rank_001' in agent_file:
                        # Extract fitness from filename
                        try:
                            parts = agent_file.split('_')
                            fitness_idx = parts.index('fitness') + 1
                            if fitness_idx < len(parts):
                                fitness = float(parts[fitness_idx])
                                if fitness > best_fitness:
                                    best_fitness = fitness
                                    best_agent_path = os.path.join(top_agents_dir, agent_file)
                        except (ValueError, IndexError):
                            continue

            if best_agent_path:
                print(f"🤖 Loading evolved agent (fitness: {best_fitness})")
                return EvolvedAgentController(best_agent_path)
            else:
                print("❌ No evolved agents found. Using rule-based AI instead.")
                return DummyAI()

        except Exception as e:
            print(f"❌ Failed to load evolved agent: {e}")
            print("Using rule-based AI instead.")
            return DummyAI()

    def handle_events(self, events):
        """Handle pygame events"""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            # Handle demonstration recording events
            self.demo_recorder.handle_key_event(event)

        # Update input handler
        self.input_handler.update(events)

    def handle_keydown(self, key):
        """Handle key press events"""
        if self.state == config.GameState.MENU:
            if key == pygame.K_SPACE:
                self.audio_manager.play_sound('menu_confirm')
                # Get selected personality and difficulty
                personality = self.personalities[self.selected_personality].lower()
                difficulty = self.difficulties[self.selected_difficulty].lower()
                self.start_game('human_vs_ai', personality, difficulty)
            elif key == pygame.K_ESCAPE:
                self.running = False
            elif key == pygame.K_UP:
                self.audio_manager.play_sound('menu_move')
                self.menu_field = (self.menu_field - 1) % 2  # Switch between fields
            elif key == pygame.K_DOWN:
                self.audio_manager.play_sound('menu_move')
                self.menu_field = (self.menu_field + 1) % 2  # Switch between fields
            elif key == pygame.K_LEFT:
                self.audio_manager.play_sound('menu_move')
                if self.menu_field == 0:  # Personality field
                    self.selected_personality = (self.selected_personality - 1) % len(self.personalities)
                else:  # Difficulty field
                    self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
            elif key == pygame.K_RIGHT:
                self.audio_manager.play_sound('menu_move')
                if self.menu_field == 0:  # Personality field
                    self.selected_personality = (self.selected_personality + 1) % len(self.personalities)
                else:  # Difficulty field
                    self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)

        elif self.state == config.GameState.FIGHTING:
            if key == pygame.K_ESCAPE:
                # Auto-save recording if it was running
                if self.auto_record and self.demo_recorder.recording:
                    self.demo_recorder.stop_recording()
                    saved_file = self.demo_recorder.save_demonstrations()
                    if saved_file:
                        print(f"💾 Auto-saved demonstrations to: {saved_file}")
                        print(f"📊 {self.demo_recorder.get_stats()}")
                    print("🎬 Recording stopped (returned to menu)")
                self.state = config.GameState.MENU
            elif key == pygame.K_p:
                self.toggle_pause()
            elif key == pygame.K_c:
                # Debug: Cancel any stuck charging states
                if self.fighter1.is_charging_projectile:
                    print("DEBUG: Manually cancelling Fighter 1 charging")
                    self.fighter1.cancel_charging_projectile()
                if self.fighter2.is_charging_projectile:
                    print("DEBUG: Manually cancelling Fighter 2 charging")
                    self.fighter2.cancel_charging_projectile()


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

    def start_game(self, mode, personality="aggressive", difficulty="easy"):
        """Start a new game with the specified mode, personality, and difficulty"""
        self.game_mode = mode
        self.selected_ai_personality = personality
        self.selected_ai_difficulty = difficulty
        self.state = config.GameState.FIGHTING

        # Auto-start recording if enabled
        if self.auto_record:
            self.demo_recorder.start_recording()
            print("🎬 Auto-started demonstration recording!")

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

        # Create AI with selected personality and difficulty
        from game.controllers.ai_controller import BalancedAI
        self.ai_controller = BalancedAI(personality, difficulty)
        self.ai_controller.game_engine = self  # Give AI access to game engine for projectile detection
        self.player2_controller = None

        print(f"🥊 Started Human vs {personality.title()} AI ({difficulty.title()} Difficulty)!")
        print(f"🧠 AI Intent: {self.ai_controller.current_intent.upper()}")
        print(f"⚔️ AI Style: {personality.title()} with fluid movement")
        print(f"🎯 AI Range Preference: {self.ai_controller.preferred_range}")
        print(f"🎮 Watch for AI tactical announcements during the fight!")

    def restart_fight(self):
        """Restart the current fight"""
        if self.game_mode:
            personality = getattr(self, 'selected_ai_personality', 'aggressive')
            difficulty = getattr(self, 'selected_ai_difficulty', 'easy')
            self.start_game(self.game_mode, personality, difficulty)

    def toggle_pause(self):
        """Toggle pause state"""
        if self.state == config.GameState.FIGHTING:
            self.state = config.GameState.PAUSED
        elif self.state == config.GameState.PAUSED:
            self.state = config.GameState.FIGHTING

    def update(self):
        """Update game logic"""
        if self.state == config.GameState.FIGHTING:
            self.update_fight()
        # Menu and other states don't need updates

    def update_fight(self):
        """Update fighting game logic"""
        # Update fighter facing directions
        if self.fighter1.x < self.fighter2.x:
            self.fighter1.facing_right = True
            self.fighter2.facing_right = False
        else:
            self.fighter1.facing_right = False
            self.fighter2.facing_right = True

        # Handle input/AI and collect projectiles
        # Fighter 1 is human controlled
        projectile1 = self.player1_controller.update_fighter(
            self.fighter1, self.audio_manager, self.demo_recorder, self.fighter2
        )
        if projectile1:
            self.projectiles.append(projectile1)

        # Fighter 2 is Balanced AI controlled
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
                self.winner = "Player 2"
            else:
                self.winner = "Player 1"

        # Check for timeout
        elif self.round_timer <= 0:
            game_over = True
            # Determine winner by health
            if self.fighter1.health > self.fighter2.health:
                self.winner = "Player 1"
            elif self.fighter2.health > self.fighter1.health:
                self.winner = "Player 2"
            else:
                self.winner = "Draw"

        if game_over and self.state != config.GameState.GAME_OVER:
            # Auto-save recording if it was running
            if self.auto_record and self.demo_recorder.recording:
                self.demo_recorder.stop_recording()
                # Auto-save demonstrations
                saved_file = self.demo_recorder.save_demonstrations()
                if saved_file:
                    print(f"💾 Auto-saved demonstrations to: {saved_file}")
                    print(f"📊 {self.demo_recorder.get_stats()}")
                print("🎬 Recording stopped (game over)")

            self.audio_manager.play_sound('game_over')
            self.state = config.GameState.GAME_OVER

    def check_combat(self):
        """Check for combat interactions between fighters"""
        # Check if fighter1 hits fighter2
        hitbox1, damage1, knockback1 = self.fighter1.get_attack_hitbox()
        if hitbox1 and hitbox1.colliderect(self.fighter2.rect) and not self.fighter1.has_hit_this_attack:
            print(f"\n=== P1 HIT DETECTED ===")
            print(f"P1 State: {self.fighter1.state}")
            print(f"P1 Position: ({self.fighter1.x:.1f}, {self.fighter1.y:.1f})")
            print(f"P2 Position: ({self.fighter2.x:.1f}, {self.fighter2.y:.1f})")
            print(f"P2 Is Blocking: {self.fighter2.is_blocking}")
            print(f"Distance: {abs(self.fighter1.x - self.fighter2.x):.1f}")

            # Check blocking logic
            facing_check = self.fighter1.facing_right != (self.fighter1.x < self.fighter2.x)
            print(f"Facing check (should be False for hit): {facing_check}")

            if not self.fighter2.is_blocking or facing_check:
                print(f">>> HIT CONFIRMED! Damage: {damage1}, Knockback: {knockback1} <<<")

                # Calculate knockback direction based on attacker position relative to defender
                knockback_direction = 1 if self.fighter1.x < self.fighter2.x else -1
                print(f"DEBUG: About to apply knockback - force: {knockback1}, direction: {knockback_direction}")

                self.fighter2.take_damage(damage1, knockback1, knockback_direction)
                self.fighter1.has_hit_this_attack = True

                # Add particle effects
                hit_x = self.fighter2.x + self.fighter2.width // 2
                hit_y = self.fighter2.y + self.fighter2.height // 2
                attack_type = "kick" if self.fighter1.state == config.FighterState.KICKING else "punch"
                self.particle_system.add_hit_effect(hit_x, hit_y, attack_type)

                # Play hit sound
                if attack_type == "kick":
                    self.audio_manager.play_sound('kick_hit')
                    if knockback1 > 0:
                        self.audio_manager.play_sound('knockback', 0.7)  # Quieter knockback sound
                else:
                    self.audio_manager.play_sound('punch_hit')

                # Add knockback effect for kicks
                if knockback1 > 0:
                    self.particle_system.add_knockback_effect(hit_x, hit_y, knockback_direction)
            else:
                print(f">>> HIT BLOCKED! Taking reduced damage: {int(damage1 * config.BLOCK_REDUCTION)} <<<")
                # Blocked attacks still deal reduced damage but no knockback or state change
                self.fighter2.take_blocked_damage(damage1)
                self.fighter1.has_hit_this_attack = True

                # Add block particle effect
                block_x = self.fighter2.x + (self.fighter2.width // 2)
                block_y = self.fighter2.y + (self.fighter2.height // 2)
                self.particle_system.add_block_effect(block_x, block_y)

                # Play block sound only once per attack
                if not self.fighter1.has_played_block_sound:
                    self.audio_manager.play_sound('block')
                    self.fighter1.has_played_block_sound = True

            print(f"========================\n")

        # Check if fighter2 hits fighter1
        hitbox2, damage2, knockback2 = self.fighter2.get_attack_hitbox()
        if hitbox2 and hitbox2.colliderect(self.fighter1.rect) and not self.fighter2.has_hit_this_attack:
            print(f"\n=== P2 HIT DETECTED ===")
            print(f"P2 State: {self.fighter2.state}")
            print(f"P2 Position: ({self.fighter2.x:.1f}, {self.fighter2.y:.1f})")
            print(f"P1 Position: ({self.fighter1.x:.1f}, {self.fighter1.y:.1f})")
            print(f"P1 Is Blocking: {self.fighter1.is_blocking}")
            print(f"Distance: {abs(self.fighter1.x - self.fighter2.x):.1f}")

            # Check blocking logic
            facing_check = self.fighter2.facing_right != (self.fighter2.x < self.fighter1.x)
            print(f"Facing check (should be False for hit): {facing_check}")

            if not self.fighter1.is_blocking or facing_check:
                print(f">>> HIT CONFIRMED! Damage: {damage2}, Knockback: {knockback2} <<<")

                # Calculate knockback direction based on attacker position relative to defender
                knockback_direction = 1 if self.fighter2.x < self.fighter1.x else -1

                self.fighter1.take_damage(damage2, knockback2, knockback_direction)
                self.fighter2.has_hit_this_attack = True

                # Add particle effects
                hit_x = self.fighter1.x + self.fighter1.width // 2
                hit_y = self.fighter1.y + self.fighter1.height // 2
                attack_type = "kick" if self.fighter2.state == config.FighterState.KICKING else "punch"
                self.particle_system.add_hit_effect(hit_x, hit_y, attack_type)

                # Play hit sound
                if attack_type == "kick":
                    self.audio_manager.play_sound('kick_hit')
                    if knockback2 > 0:
                        self.audio_manager.play_sound('knockback', 0.7)  # Quieter knockback sound
                else:
                    self.audio_manager.play_sound('punch_hit')

                # Add knockback effect for kicks
                if knockback2 > 0:
                    self.particle_system.add_knockback_effect(hit_x, hit_y, knockback_direction)
            else:
                print(f">>> HIT BLOCKED! Taking reduced damage: {int(damage2 * config.BLOCK_REDUCTION)} <<<")
                # Blocked attacks still deal reduced damage but no knockback or state change
                self.fighter1.take_blocked_damage(damage2)
                self.fighter2.has_hit_this_attack = True

                # Add block particle effect
                block_x = self.fighter1.x + (self.fighter1.width // 2)
                block_y = self.fighter1.y + (self.fighter1.height // 2)
                self.particle_system.add_block_effect(block_x, block_y)

                # Play block sound only once per attack
                if not self.fighter2.has_played_block_sound:
                    self.audio_manager.play_sound('block')
                    self.fighter2.has_played_block_sound = True

            print(f"========================\n")

    def update_projectiles(self):
        """Update all projectiles and remove inactive ones"""
        for projectile in self.projectiles[:]:  # Copy list to avoid modification during iteration
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)

    def check_projectile_hits(self):
        """Check for projectile collisions with fighters"""
        for projectile in self.projectiles[:]:  # Copy list to avoid modification during iteration
            # Check collision with fighter1
            if projectile.check_collision(self.fighter1):
                print(f"Projectile hit Fighter 1! Damage: {projectile.damage}")
                self.fighter1.take_damage(projectile.damage)
                projectile.hit_target()

                # Add hit effect
                hit_x = self.fighter1.x + self.fighter1.width // 2
                hit_y = self.fighter1.y + self.fighter1.height // 2
                self.particle_system.add_hit_effect(hit_x, hit_y, "projectile")

                # Play hit sound
                self.audio_manager.play_sound('punch_hit')  # Use punch hit sound for now

                self.projectiles.remove(projectile)
                continue

            # Check collision with fighter2
            if projectile.check_collision(self.fighter2):
                print(f"Projectile hit Fighter 2! Damage: {projectile.damage}")
                self.fighter2.take_damage(projectile.damage)
                projectile.hit_target()

                # Add hit effect
                hit_x = self.fighter2.x + self.fighter2.width // 2
                hit_y = self.fighter2.y + self.fighter2.height // 2
                self.particle_system.add_hit_effect(hit_x, hit_y, "projectile")

                # Play hit sound
                self.audio_manager.play_sound('punch_hit')  # Use punch hit sound for now

                self.projectiles.remove(projectile)

    def check_character_collision(self):
        """Check for character-to-character collision and handle pushing"""
        # Check if fighters are overlapping
        if self.fighter1.rect.colliderect(self.fighter2.rect):
            # Determine who is moving into whom
            fighter1_center = self.fighter1.x + self.fighter1.width // 2
            fighter2_center = self.fighter2.x + self.fighter2.width // 2

            # Determine push directions
            if fighter1_center < fighter2_center:
                # Fighter1 is on the left, Fighter2 is on the right
                push_f1_left = -1
                push_f2_right = 1
            else:
                # Fighter1 is on the right, Fighter2 is on the left
                push_f1_left = 1
                push_f2_right = -1

            # Try to push both fighters apart
            f1_pushed = False
            f2_pushed = False

            # Only push if the fighter can be pushed (not blocking, not in special states)
            if self.fighter1.can_be_pushed():
                f1_pushed = self.fighter1.push(push_f1_left)

            if self.fighter2.can_be_pushed():
                f2_pushed = self.fighter2.push(push_f2_right)

            # If neither could be pushed, separate them manually to prevent overlap
            if not f1_pushed and not f2_pushed:
                # Both fighters are blocking or can't be pushed - force separation
                separation_distance = 2
                if fighter1_center < fighter2_center:
                    # Move fighter1 left, fighter2 right
                    self.fighter1.x = max(config.STAGE_LEFT, self.fighter1.x - separation_distance)
                    self.fighter2.x = min(config.STAGE_RIGHT - self.fighter2.width, self.fighter2.x + separation_distance)
                else:
                    # Move fighter1 right, fighter2 left
                    self.fighter1.x = min(config.STAGE_RIGHT - self.fighter1.width, self.fighter1.x + separation_distance)
                    self.fighter2.x = max(config.STAGE_LEFT, self.fighter2.x - separation_distance)

                # Update rects after manual separation
                self.fighter1.rect.x = self.fighter1.x
                self.fighter2.rect.x = self.fighter2.x

            elif not f1_pushed and f2_pushed:
                # Fighter1 couldn't be pushed but Fighter2 was pushed
                # This means Fighter1 is blocking - stop Fighter1 from advancing
                if fighter1_center < fighter2_center:
                    # Fighter1 is trying to move right into Fighter2
                    self.fighter1.x = self.fighter2.x - self.fighter1.width - 1
                else:
                    # Fighter1 is trying to move left into Fighter2
                    self.fighter1.x = self.fighter2.x + self.fighter2.width + 1
                self.fighter1.rect.x = self.fighter1.x
                # Don't stop velocity if fighter is in knockback state
                if self.fighter1.state != config.FighterState.KNOCKBACK:
                    print(f"DEBUG COLLISION: Stopping F1 velocity (was {self.fighter1.velocity_x})")
                    self.fighter1.velocity_x = 0  # Stop horizontal movement
                else:
                    print(f"DEBUG COLLISION: F1 in knockback, preserving velocity {self.fighter1.velocity_x}")

            elif f1_pushed and not f2_pushed:
                # Fighter2 couldn't be pushed but Fighter1 was pushed
                # This means Fighter2 is blocking - stop Fighter2 from advancing
                if fighter2_center < fighter1_center:
                    # Fighter2 is trying to move right into Fighter1
                    self.fighter2.x = self.fighter1.x - self.fighter2.width - 1
                else:
                    # Fighter2 is trying to move left into Fighter1
                    self.fighter2.x = self.fighter1.x + self.fighter1.width + 1
                self.fighter2.rect.x = self.fighter2.x
                # Don't stop velocity if fighter is in knockback state
                if self.fighter2.state != config.FighterState.KNOCKBACK:
                    print(f"DEBUG COLLISION: Stopping F2 velocity (was {self.fighter2.velocity_x})")
                    self.fighter2.velocity_x = 0  # Stop horizontal movement
                else:
                    print(f"DEBUG COLLISION: F2 in knockback, preserving velocity {self.fighter2.velocity_x}")

    def render(self):
        """Render the current game state"""
        if self.state == config.GameState.MENU:
            self.renderer.draw_menu()

        elif self.state in [config.GameState.FIGHTING, config.GameState.GAME_OVER, config.GameState.PAUSED]:
            self.renderer.render_game(self.fighter1, self.fighter2, self.state, self, self.ai_controller, self.game_mode)

            # Draw projectiles
            for projectile in self.projectiles:
                projectile.draw(self.screen)

            # Draw particles on top of everything
            self.particle_system.draw(self.screen)

            if self.state == config.GameState.PAUSED:
                # Draw pause overlay
                pause_text = pygame.font.Font(None, 48).render("PAUSED", True, config.WHITE)
                pause_rect = pause_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, pause_rect)

        pygame.display.flip()
