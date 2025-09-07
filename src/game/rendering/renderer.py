"""
Renderer for the 2D Fighting Game
"""
import pygame
from ..core import config

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def render_game(self, fighter1, fighter2, game_state, game_engine, ai_controller=None, game_mode=None):
        """Render the complete game scene"""
        # Clear screen
        self.screen.fill(config.BLACK)

        # Draw stage
        self._draw_stage()

        # Draw fighters
        self._draw_fighter(fighter1)
        self._draw_fighter(fighter2)

        # Draw UI
        self._draw_health_bars(fighter1, fighter2)
        self._draw_timer(game_engine.round_timer)
        self._draw_debug_info(fighter1, fighter2)
        self._draw_ai_behavior_info(ai_controller, game_mode)

        # Draw game state info
        if game_state == config.GameState.GAME_OVER:
            self._draw_game_over(game_engine.winner, game_engine.round_timer)

    def _draw_stage(self):
        """Draw the fighting stage"""
        # Stage floor
        pygame.draw.rect(self.screen, config.GRAY,
                        (config.STAGE_LEFT, config.STAGE_FLOOR,
                         config.STAGE_WIDTH, config.SCREEN_HEIGHT - config.STAGE_FLOOR))

        # Stage boundaries
        pygame.draw.line(self.screen, config.WHITE,
                        (config.STAGE_LEFT, config.STAGE_FLOOR),
                        (config.STAGE_LEFT, config.STAGE_FLOOR - 20), 3)
        pygame.draw.line(self.screen, config.WHITE,
                        (config.STAGE_RIGHT, config.STAGE_FLOOR),
                        (config.STAGE_RIGHT, config.STAGE_FLOOR - 20), 3)

        # Center line
        center_x = config.SCREEN_WIDTH // 2
        pygame.draw.line(self.screen, config.LIGHT_GRAY,
                        (center_x, config.STAGE_FLOOR),
                        (center_x, config.STAGE_FLOOR - 10), 2)

    def _draw_fighter(self, fighter):
        """Draw a fighter with state-based appearance"""
        # Main body
        body_color = fighter.color

        # Modify color based on state
        if fighter.state == config.FighterState.HIT:
            # Flash yellow when hit (for both punches and kicks)
            body_color = config.YELLOW
        elif fighter.state == config.FighterState.KNOCKBACK:
            # Flash yellow when in knockback
            body_color = config.YELLOW
        elif fighter.state == config.FighterState.BLOCKING:
            # Darker when blocking
            body_color = tuple(max(0, c - 50) for c in fighter.color)

        # Draw main body
        pygame.draw.rect(self.screen, body_color, fighter.rect)

        # Draw facing direction indicator
        if fighter.facing_right:
            eye_x = fighter.x + fighter.width - 10
        else:
            eye_x = fighter.x + 5
        pygame.draw.circle(self.screen, config.WHITE,
                          (int(eye_x), int(fighter.y + 15)), 5)

        # Draw state-specific visuals
        self._draw_fighter_state_effects(fighter)

        # Draw attack hitboxes (for debugging)
        self._draw_hitboxes(fighter)

    def _draw_fighter_state_effects(self, fighter):
        """Draw visual effects based on fighter state"""
        if fighter.state == config.FighterState.PUNCHING:
            # Draw punch effect - smaller and positioned to match hitbox
            if fighter.facing_right:
                effect_x = fighter.x + fighter.width + 15
            else:
                effect_x = fighter.x - 15
            pygame.draw.circle(self.screen, config.YELLOW,
                             (int(effect_x), int(fighter.y + 42)), 12, 3)

        elif fighter.state == config.FighterState.KICKING:
            # Draw kick effect - positioned lower to match new kick height
            if fighter.facing_right:
                effect_x = fighter.x + fighter.width + 20
            else:
                effect_x = fighter.x - 20
            pygame.draw.circle(self.screen, config.YELLOW,
                             (int(effect_x), int(fighter.y + 75)), 15, 3)

        elif fighter.state == config.FighterState.BLOCKING:
            # Draw block effect
            pygame.draw.rect(self.screen, config.BLUE,
                           (fighter.x - 5, fighter.y - 5,
                            fighter.width + 10, fighter.height + 10), 3)

        elif fighter.state == config.FighterState.CHARGING:
            # Draw charging effect around fighter
            charge_color = (0, 200, 0)
            pygame.draw.rect(self.screen, charge_color,
                           (fighter.x - 3, fighter.y - 3,
                            fighter.width + 6, fighter.height + 6), 2)

        # Draw charging orb if present
        if hasattr(fighter, 'charging_orb') and fighter.charging_orb:
            fighter.charging_orb.draw(self.screen)

    def _draw_hitboxes(self, fighter):
        """Draw attack hitboxes for debugging"""
        hitbox, damage, knockback = fighter.get_attack_hitbox()
        if hitbox:
            pygame.draw.rect(self.screen, config.RED, hitbox, 2)

    def _draw_health_bars(self, fighter1, fighter2):
        """Draw health bars for both fighters"""
        bar_width = 300
        bar_height = 20
        bar_y = 30

        # Player 1 health bar (left side)
        p1_bar_x = 50
        health_ratio1 = fighter1.health / fighter1.max_health

        # Background
        pygame.draw.rect(self.screen, config.DARK_RED,
                        (p1_bar_x, bar_y, bar_width, bar_height))
        # Health
        pygame.draw.rect(self.screen, config.RED,
                        (p1_bar_x, bar_y, bar_width * health_ratio1, bar_height))
        # Border
        pygame.draw.rect(self.screen, config.WHITE,
                        (p1_bar_x, bar_y, bar_width, bar_height), 2)

        # Player 2 health bar (right side)
        p2_bar_x = config.SCREEN_WIDTH - 50 - bar_width
        health_ratio2 = fighter2.health / fighter2.max_health

        # Background
        pygame.draw.rect(self.screen, config.DARK_BLUE,
                        (p2_bar_x, bar_y, bar_width, bar_height))
        # Health
        pygame.draw.rect(self.screen, config.BLUE,
                        (p2_bar_x, bar_y, bar_width * health_ratio2, bar_height))
        # Border
        pygame.draw.rect(self.screen, config.WHITE,
                        (p2_bar_x, bar_y, bar_width, bar_height), 2)

        # Health text
        p1_text = self.small_font.render(f"P1: {fighter1.health}", True, config.WHITE)
        p2_text = self.small_font.render(f"P2: {fighter2.health}", True, config.WHITE)
        self.screen.blit(p1_text, (p1_bar_x, bar_y + bar_height + 5))
        self.screen.blit(p2_text, (p2_bar_x, bar_y + bar_height + 5))

        # Projectile cooldown bars
        self._draw_projectile_cooldowns(fighter1, fighter2, p1_bar_x, p2_bar_x, bar_y + bar_height + 30, bar_width)

    def _draw_timer(self, round_timer):
        """Draw the round timer in the center top"""
        # Convert frames to seconds
        seconds_left = max(0, round_timer // config.FPS)
        minutes = seconds_left // 60
        seconds = seconds_left % 60

        # Format timer text
        timer_text = f"{minutes}:{seconds:02d}"

        # Choose color based on time remaining
        if seconds_left <= 10:
            color = config.RED  # Red when time is almost up
        elif seconds_left <= 30:
            color = config.YELLOW  # Yellow when time is low
        else:
            color = config.WHITE  # White normally

        # Draw timer
        timer_surface = self.font.render(timer_text, True, color)
        timer_rect = timer_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 30))

        # Draw background for better visibility
        bg_rect = timer_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, config.BLACK, bg_rect)
        pygame.draw.rect(self.screen, color, bg_rect, 2)

        self.screen.blit(timer_surface, timer_rect)

    def _draw_projectile_cooldowns(self, fighter1, fighter2, p1_x, p2_x, cooldown_y, bar_width):
        """Draw projectile cooldown progress bars"""
        cooldown_height = 8

        # Player 1 projectile cooldown
        if fighter1.projectile_cooldown > 0:
            # Cooldown active - show red bar filling up
            cooldown_ratio = 1.0 - (fighter1.projectile_cooldown / config.PROJECTILE_COOLDOWN)

            # Background (empty part)
            pygame.draw.rect(self.screen, config.DARK_RED,
                           (p1_x, cooldown_y, bar_width, cooldown_height))
            # Progress (filled part)
            pygame.draw.rect(self.screen, config.RED,
                           (p1_x, cooldown_y, bar_width * cooldown_ratio, cooldown_height))
            # Border
            pygame.draw.rect(self.screen, config.WHITE,
                           (p1_x, cooldown_y, bar_width, cooldown_height), 1)

            # Cooldown text
            cooldown_text = self.small_font.render("Projectile Cooldown", True, config.WHITE)
            self.screen.blit(cooldown_text, (p1_x, cooldown_y + cooldown_height + 2))
        else:
            # Ready - show green "READY" indicator
            ready_text = self.small_font.render("Projectile Ready", True, config.GREEN)
            self.screen.blit(ready_text, (p1_x, cooldown_y))

        # Player 2 projectile cooldown
        if fighter2.projectile_cooldown > 0:
            # Cooldown active - show blue bar filling up
            cooldown_ratio = 1.0 - (fighter2.projectile_cooldown / config.PROJECTILE_COOLDOWN)

            # Background (empty part)
            pygame.draw.rect(self.screen, config.DARK_BLUE,
                           (p2_x, cooldown_y, bar_width, cooldown_height))
            # Progress (filled part)
            pygame.draw.rect(self.screen, config.BLUE,
                           (p2_x, cooldown_y, bar_width * cooldown_ratio, cooldown_height))
            # Border
            pygame.draw.rect(self.screen, config.WHITE,
                           (p2_x, cooldown_y, bar_width, cooldown_height), 1)

            # Cooldown text
            cooldown_text = self.small_font.render("Projectile Cooldown", True, config.WHITE)
            self.screen.blit(cooldown_text, (p2_x, cooldown_y + cooldown_height + 2))
        else:
            # Ready - show green "READY" indicator
            ready_text = self.small_font.render("Projectile Ready", True, config.GREEN)
            self.screen.blit(ready_text, (p2_x, cooldown_y))

    def _draw_debug_info(self, fighter1, fighter2):
        """Draw debug information"""
        debug_y = config.SCREEN_HEIGHT - 150

        # Fighter states
        p1_state_text = self.small_font.render(f"P1 State: {fighter1.state}", True, config.WHITE)
        p2_state_text = self.small_font.render(f"P2 State: {fighter2.state}", True, config.WHITE)

        self.screen.blit(p1_state_text, (20, debug_y))
        self.screen.blit(p2_state_text, (20, debug_y + 20))

        # Attack timers and hit flags
        p1_attack_text = self.small_font.render(f"P1 Attack Timer: {fighter1.attack_timer}, Has Hit: {fighter1.has_hit_this_attack}", True, config.WHITE)
        p2_attack_text = self.small_font.render(f"P2 Attack Timer: {fighter2.attack_timer}, Has Hit: {fighter2.has_hit_this_attack}", True, config.WHITE)

        self.screen.blit(p1_attack_text, (20, debug_y + 40))
        self.screen.blit(p2_attack_text, (20, debug_y + 60))

        # Hitbox information
        hitbox1, damage1, knockback1 = fighter1.get_attack_hitbox()
        hitbox2, damage2, knockback2 = fighter2.get_attack_hitbox()

        p1_hitbox_text = self.small_font.render(f"P1 Hitbox: {'Yes' if hitbox1 else 'No'}, Dmg: {damage1}", True, config.WHITE)
        p2_hitbox_text = self.small_font.render(f"P2 Hitbox: {'Yes' if hitbox2 else 'No'}, Dmg: {damage2}", True, config.WHITE)

        self.screen.blit(p1_hitbox_text, (20, debug_y + 80))
        self.screen.blit(p2_hitbox_text, (20, debug_y + 100))

        # Distance between fighters
        distance = abs(fighter1.x - fighter2.x)
        distance_text = self.small_font.render(f"Distance: {distance:.0f}", True, config.WHITE)
        self.screen.blit(distance_text, (20, debug_y + 120))

        # Collision detection debug removed for cleaner display

    def _draw_ai_behavior_info(self, ai_controller, game_mode):
        """Draw AI behavior information"""
        if game_mode == 'human_vs_ai' and ai_controller:
            # Draw new BalancedAI info
            if hasattr(ai_controller, 'personality') and hasattr(ai_controller, 'difficulty'):
                ai_info = f"{ai_controller.personality.title()} AI ({ai_controller.difficulty.title()})"
                ai_text = self.small_font.render(ai_info, True, config.CYAN)
                self.screen.blit(ai_text, (config.SCREEN_WIDTH - 250, 70))

                # Show current intent
                if hasattr(ai_controller, 'current_intent'):
                    intent_text = self.small_font.render(f"Intent: {ai_controller.current_intent.upper()}", True, config.WHITE)
                    self.screen.blit(intent_text, (config.SCREEN_WIDTH - 250, 95))
            else:
                # Fallback for old AI controllers
                ai_text = self.small_font.render("AI Opponent", True, config.CYAN)
                self.screen.blit(ai_text, (config.SCREEN_WIDTH - 250, 70))
        elif game_mode == 'human_vs_evolved_ai' and ai_controller:
            # Draw Evolved AI info
            if hasattr(ai_controller, 'agent_info'):
                fitness = ai_controller.agent_info.get('fitness', 'Unknown')
                fighting_style = ai_controller.agent_info.get('fighting_style', 'Unknown')
                ai_text = self.small_font.render(f"Evolved AI: {fighting_style} (Fitness: {fitness})", True, config.CYAN)
                self.screen.blit(ai_text, (config.SCREEN_WIDTH - 350, 70))
            else:
                ai_text = self.small_font.render("Evolved AI", True, config.CYAN)
                self.screen.blit(ai_text, (config.SCREEN_WIDTH - 250, 70))
        elif game_mode == 'human_vs_rl_ai' and ai_controller:
            # Draw RL AI info
            ai_type = "RL AI (Trained)" if hasattr(ai_controller, 'policy') and ai_controller.policy else "RL AI (Fallback)"
            ai_text = self.small_font.render(f"AI: {ai_type}", True, config.CYAN)
            self.screen.blit(ai_text, (config.SCREEN_WIDTH - 250, 70))

    def _draw_game_over(self, winner, round_timer):
        """Draw game over screen with winner and reason"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(config.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Determine winner text and color
        if winner == "Player 1":
            winner_text = "Player 1 Wins!"
            color = config.RED
        elif winner == "Player 2":
            winner_text = "Player 2 Wins!"
            color = config.BLUE
        elif winner == "Draw":
            winner_text = "Draw!"
            color = config.WHITE
        else:
            winner_text = "Game Over!"
            color = config.WHITE

        # Determine reason
        if round_timer <= 0:
            if winner == "Draw":
                reason_text = "Time's up! Equal health - it's a draw!"
            else:
                reason_text = "Time's up! Victory by health advantage!"
        else:
            reason_text = "Victory by knockout!"

        # Draw winner text
        text_surface = self.font.render(winner_text, True, color)
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(text_surface, text_rect)

        # Draw reason text
        reason_surface = self.small_font.render(reason_text, True, config.WHITE)
        reason_rect = reason_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(reason_surface, reason_rect)

        # Draw restart instruction
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, config.WHITE)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(config.BLACK)

        # Title
        title_text = self.font.render("2D Fighting Game", True, config.WHITE)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Menu fields
        field_y_start = 180
        field_spacing = 50

        # Personality field
        personality_label = "Opponent Personality:"
        personality_value = f"< {self.game_engine.personalities[self.game_engine.selected_personality]} >"

        # Highlight current field
        personality_color = config.YELLOW if self.game_engine.menu_field == 0 else config.WHITE

        personality_label_text = self.small_font.render(personality_label, True, personality_color)
        personality_value_text = self.font.render(personality_value, True, personality_color)

        # Center the label and value
        label_rect = personality_label_text.get_rect(center=(config.SCREEN_WIDTH // 2, field_y_start))
        value_rect = personality_value_text.get_rect(center=(config.SCREEN_WIDTH // 2, field_y_start + 25))

        self.screen.blit(personality_label_text, label_rect)
        self.screen.blit(personality_value_text, value_rect)

        # Difficulty field (with extra spacing)
        difficulty_y = field_y_start + field_spacing + 20  # Added 20px spacing
        difficulty_label = "Difficulty Level:"
        difficulty_value = f"< {self.game_engine.difficulties[self.game_engine.selected_difficulty]} >"

        # Highlight current field
        difficulty_color = config.YELLOW if self.game_engine.menu_field == 1 else config.WHITE

        difficulty_label_text = self.small_font.render(difficulty_label, True, difficulty_color)
        difficulty_value_text = self.font.render(difficulty_value, True, difficulty_color)

        # Center the label and value
        label_rect = difficulty_label_text.get_rect(center=(config.SCREEN_WIDTH // 2, difficulty_y))
        value_rect = difficulty_value_text.get_rect(center=(config.SCREEN_WIDTH // 2, difficulty_y + 25))

        self.screen.blit(difficulty_label_text, label_rect)
        self.screen.blit(difficulty_value_text, value_rect)

        # Instructions
        instructions_y = difficulty_y + 80
        instructions = [
            "↑↓ - Switch Fields    ←→ - Change Values",
            "SPACE - Start Fighting!    ESC - Quit"
        ]

        for i, instruction in enumerate(instructions):
            instruction_text = self.small_font.render(instruction, True, config.LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH // 2, instructions_y + i * 25))
            self.screen.blit(instruction_text, instruction_rect)

        # AI description
        selected_personality = self.game_engine.personalities[self.game_engine.selected_personality]
        selected_difficulty = self.game_engine.difficulties[self.game_engine.selected_difficulty]

        ai_title = self.font.render(f"Your Opponent: {selected_personality} AI ({selected_difficulty})", True, config.YELLOW)
        ai_title_rect = ai_title.get_rect(center=(config.SCREEN_WIDTH // 2, instructions_y + 80))
        self.screen.blit(ai_title, ai_title_rect)

        # Personality descriptions
        personality_descriptions = {
            "Aggressive": [
                "• Rushdown fighting style with constant pressure",
                "• Prefers close combat with punches and kicks",
                "• High aggression, moderate adaptation"
            ],
            "Defensive": [
                "• Turtle fighting style with reactive tactics",
                "• Focuses on blocking and counter-attacks",
                "• Low aggression, high adaptation"
            ],
            "Zoner": [
                "• Keepaway fighting style with space control",
                "• Heavy use of projectiles and positioning",
                "• Moderate aggression, prefers long range"
            ],
            "Balanced": [
                "• All-around fighting style with varied tactics",
                "• Uses all combat techniques equally",
                "• Balanced aggression and adaptation"
            ]
        }

        ai_description = personality_descriptions[selected_personality]

        for i, desc in enumerate(ai_description):
            desc_text = self.small_font.render(desc, True, config.LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(config.SCREEN_WIDTH // 2, instructions_y + 110 + i * 25))
            self.screen.blit(desc_text, desc_rect)

        # Player 1 controls
        p1_title = self.small_font.render("Player 1 (Red Fighter):", True, config.RED)
        self.screen.blit(p1_title, (50, 420))

        p1_controls = [
            "A/D - Move Left/Right",
            "W - Jump",
            "J - Punch",
            "K - Kick",
            "L - Block",
            "I - Projectile (Hold to charge)"
        ]

        for i, control in enumerate(p1_controls):
            control_text = self.small_font.render(control, True, config.WHITE)
            self.screen.blit(control_text, (70, 450 + i * 25))

        # Game controls
        game_controls_title = self.small_font.render("Game Controls:", True, config.GREEN)
        self.screen.blit(game_controls_title, (50, 600))

        game_controls = [
            "P - Pause/Unpause",
            "R - Restart (when game over)",
            "ESC - Return to menu"
        ]

        for i, control in enumerate(game_controls):
            control_text = self.small_font.render(control, True, config.WHITE)
            self.screen.blit(control_text, (70, 630 + i * 25))
