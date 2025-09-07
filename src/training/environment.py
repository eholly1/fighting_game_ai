"""
Fighting Game RL Environment
Wraps the game engine for RL training
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pygame
from game.core import config
from game.entities.fighter import Fighter

class FightingGameEnv:
    """RL Environment wrapper for the fighting game"""

    def __init__(self, headless=True, max_steps=3600):  # 60 seconds at 60 FPS
        self.headless = headless
        self.max_steps = max_steps
        self.current_step = 0

        # Enable training mode to disable debug outputs
        config.TRAINING_MODE = True

        # Initialize pygame (needed even in headless mode for game logic)
        pygame.init()
        if headless:
            # Create a dummy surface for headless training
            self.screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        else:
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        # Game components
        self.game_engine = None
        self.fighter1 = None  # RL agent
        self.fighter2 = None  # Opponent

        # State and action spaces
        self.state_size = 26  # Increased to include projectile charge levels
        self.action_size = 10
        self.action_mapping = {
            0: 'idle',
            1: 'move_left',
            2: 'move_right',
            3: 'jump',
            4: 'punch',
            5: 'kick',
            6: 'block',
            7: 'move_left_block',
            8: 'move_right_block',
            9: 'projectile'
        }

        # Training state
        self.last_health = [100, 100]  # [fighter1, fighter2]
        self.last_positions = [0, 0]
        self.episode_rewards = []

        # Projectile action tracking for encouraging longer holds
        self.projectile_action_count = [0, 0]  # [fighter1, fighter2] consecutive projectile actions
        self.projectile_charge_bonus = [0, 0]  # Bonus for holding projectile action

    def reset(self):
        """Reset environment for new episode"""
        self.current_step = 0

        # Create fresh fighters
        self.fighter1 = Fighter(100, config.STAGE_FLOOR - 60, config.BLUE)
        self.fighter2 = Fighter(600, config.STAGE_FLOOR - 60, config.RED)

        # Reset health and positions
        self.fighter1.health = 100
        self.fighter2.health = 100
        self.last_health = [100, 100]
        self.last_positions = [self.fighter1.x, self.fighter2.x]

        # Reset projectile tracking
        self.projectile_action_count = [0, 0]
        self.projectile_charge_bonus = [0, 0]

        return self.get_state()

    def get_state(self, player_fighter=None):
        """Convert game state to RL state vector with mirroring"""
        f1, f2 = self.fighter1, self.fighter2

        # Default to fighter1 as the player perspective
        if player_fighter is None:
            player_fighter = f1

        # Determine if we need to mirror (player is on the right)
        if player_fighter == f1:
            player, opponent = f1, f2
            mirror = False
        else:
            player, opponent = f2, f1
            mirror = False  # We'll handle mirroring in the state construction

        # If player is to the right of opponent, we need to mirror
        if player.x > opponent.x:
            mirror = True

        # Build state with consistent perspective (player on left, opponent on right)
        if mirror:
            # Mirror positions and velocities
            player_x = 1.0 - (player.x / config.STAGE_WIDTH)
            opponent_x = 1.0 - (opponent.x / config.STAGE_WIDTH)
            player_vel_x = -player.velocity_x / config.FIGHTER_SPEED
            opponent_vel_x = -opponent.velocity_x / config.FIGHTER_SPEED
            # When mirrored, relative position should be negative (opponent to left)
            relative_x = -(opponent_x - player_x)  # Flip sign for mirrored perspective
        else:
            # Normal positions
            player_x = player.x / config.STAGE_WIDTH
            opponent_x = opponent.x / config.STAGE_WIDTH
            player_vel_x = player.velocity_x / config.FIGHTER_SPEED
            opponent_vel_x = opponent.velocity_x / config.FIGHTER_SPEED
            relative_x = (opponent_x - player_x)  # opponent relative to player

        state = [
            # Player state (always "on the left" in representation)
            player_x,
            player.y / config.STAGE_HEIGHT,
            player.health / 100.0,
            player_vel_x,
            float(player.is_grounded),
            float(player.is_attacking),
            float(player.is_blocking),
            player.attack_cooldown / config.ATTACK_COOLDOWN,
            # Projectile state for player
            player.projectile_cooldown / config.PROJECTILE_COOLDOWN,
            float(player.is_charging_projectile),
            player.charging_orb.get_charge_percent() if player.charging_orb else 0.0,

            # Opponent state (always "on the right" in representation)
            opponent_x,
            opponent.y / config.STAGE_HEIGHT,
            opponent.health / 100.0,
            opponent_vel_x,
            float(opponent.is_grounded),
            float(opponent.is_attacking),
            float(opponent.is_blocking),
            opponent.attack_cooldown / config.ATTACK_COOLDOWN,
            # Projectile state for opponent
            opponent.projectile_cooldown / config.PROJECTILE_COOLDOWN,
            float(opponent.is_charging_projectile),
            opponent.charging_orb.get_charge_percent() if opponent.charging_orb else 0.0,

            # Relative information (opponent relative to player)
            abs(relative_x),  # Distance (always positive)
            relative_x,       # Relative position (positive = opponent to right)
            (opponent.y - player.y) / config.STAGE_HEIGHT,  # Height difference
            (player.health - opponent.health) / 100.0,      # Health advantage
        ]

        return np.array(state, dtype=np.float32)

    def step(self, action1, action2=None):
        """Execute one step in the environment"""
        self.current_step += 1

        # Execute actions
        self._execute_action(self.fighter1, action1)
        if action2 is not None:
            self._execute_action(self.fighter2, action2)

        # Update game physics
        self.fighter1.update()
        self.fighter2.update()

        # Check for combat
        self._check_combat()

        # Calculate rewards
        reward1 = self._calculate_reward(self.fighter1, self.fighter2)
        reward2 = self._calculate_reward(self.fighter2, self.fighter1) if action2 is not None else 0

        # Check if episode is done
        done = self._is_done()

        # Update tracking variables
        self.last_health = [self.fighter1.health, self.fighter2.health]
        self.last_positions = [self.fighter1.x, self.fighter2.x]

        # Return step results
        next_state = self.get_state()
        info = {
            'fighter1_health': self.fighter1.health,
            'fighter2_health': self.fighter2.health,
            'step': self.current_step
        }

        if action2 is not None:
            return next_state, (reward1, reward2), done, info
        else:
            return next_state, reward1, done, info

    def _execute_action(self, fighter, action):
        """Execute an action for a fighter"""
        action_name = self.action_mapping.get(action, 'idle')

        if action_name == 'move_left':
            fighter.move_left()
        elif action_name == 'move_right':
            fighter.move_right()
        elif action_name == 'jump':
            fighter.jump()
        elif action_name == 'punch':
            fighter.punch()
        elif action_name == 'kick':
            fighter.kick()
        elif action_name == 'block':
            fighter.block()
        elif action_name == 'move_left_block':
            fighter.move_left()
            fighter.block()
        elif action_name == 'move_right_block':
            fighter.move_right()
            fighter.block()
        elif action_name == 'projectile':
            # For training, simulate a quick projectile without getting stuck in charging state
            if fighter.can_charge_projectile():
                # Temporarily start charging to create projectile
                fighter.start_charging_projectile()
                if fighter.charging_orb:
                    # Give it a small charge and immediately fire
                    fighter.charging_orb.charge_time = 10  # Small charge
                    projectile = fighter.stop_charging_projectile()
                    # Projectile created but not managed in training environment
                else:
                    # If charging failed, ensure we're not stuck in charging state
                    fighter.cancel_charging_projectile()
        # 'idle' does nothing

    def _check_combat(self):
        """Check for combat interactions between fighters"""
        # Simple combat check - adapted from game engine
        hitbox1, damage1, knockback1 = self.fighter1.get_attack_hitbox()
        hitbox2, damage2, knockback2 = self.fighter2.get_attack_hitbox()

        # Fighter 1 hits Fighter 2
        if hitbox1 and hitbox1.colliderect(self.fighter2.rect) and not self.fighter1.has_hit_this_attack:
            if not self.fighter2.is_blocking:
                knockback_direction = 1 if self.fighter1.x < self.fighter2.x else -1
                self.fighter2.take_damage(damage1, knockback1, knockback_direction)
                self.fighter1.has_hit_this_attack = True

        # Fighter 2 hits Fighter 1
        if hitbox2 and hitbox2.colliderect(self.fighter1.rect) and not self.fighter2.has_hit_this_attack:
            if not self.fighter1.is_blocking:
                knockback_direction = 1 if self.fighter2.x < self.fighter1.x else -1
                self.fighter1.take_damage(damage2, knockback2, knockback_direction)
                self.fighter2.has_hit_this_attack = True

    def _calculate_reward(self, fighter, opponent):
        """Calculate reward for a fighter"""
        reward = 0

        # Health-based rewards
        health_change = fighter.health - self.last_health[0 if fighter == self.fighter1 else 1]
        opp_health_change = opponent.health - self.last_health[1 if fighter == self.fighter1 else 0]

        reward += health_change * 0.2  # Penalty for losing health (health_change is negative when damaged)
        reward -= opp_health_change * 0.2  # Reward for damaging opponent

        # Combat rewards
        if hasattr(fighter, 'has_hit_this_attack') and fighter.has_hit_this_attack:
            reward += 5.0  # Reward for landing hits

        # Projectile charging reward - logarithmic increase for longer holds
        if fighter.is_charging_projectile and fighter.charging_orb:
            charge_percent = fighter.charging_orb.get_charge_percent()
            if charge_percent > 0:
                # Logarithmic reward: log(1 + charge_percent) * 0.5
                # This gives: 0% = 0, 50% = 0.2, 100% = 0.35
                import math
                log_reward = math.log(1 + charge_percent) * 0.5
                reward += log_reward

        # Encourage engagement - small reward for being in fighting range
        distance = abs(fighter.x - opponent.x)
        if distance < 150:  # Close enough to fight
            reward += 0.1

        # Removed boundary penalty - engagement reward should handle positioning

        # Terminal rewards (handle both KO and timeout victories)
        if self._is_done():
            # Check victory conditions
            if not fighter.is_alive():
                reward -= 50  # Large penalty for losing by KO
            elif not opponent.is_alive():
                reward += 50  # Large reward for winning by KO
            elif self.current_step >= self.max_steps:
                # Timeout - determine winner by health
                if fighter.health > opponent.health:
                    reward += 50  # Win by health advantage
                elif fighter.health < opponent.health:
                    reward -= 50  # Lose by health disadvantage
                # Draw (equal health) gives no terminal reward

        return reward

    def _is_done(self):
        """Check if episode should end"""
        # Episode ends if someone dies or max steps reached
        return (not self.fighter1.is_alive() or
                not self.fighter2.is_alive() or
                self.current_step >= self.max_steps)

    def render(self):
        """Render the environment (for debugging)"""
        if not self.headless:
            self.screen.fill(config.BLACK)
            # Simple rendering - just rectangles for fighters
            pygame.draw.rect(self.screen, self.fighter1.color,
                           (self.fighter1.x, self.fighter1.y, self.fighter1.width, self.fighter1.height))
            pygame.draw.rect(self.screen, self.fighter2.color,
                           (self.fighter2.x, self.fighter2.y, self.fighter2.width, self.fighter2.height))
            pygame.display.flip()

    def close(self):
        """Clean up environment"""
        pygame.quit()
