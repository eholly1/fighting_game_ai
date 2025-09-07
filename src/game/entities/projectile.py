"""
Projectile entity for the fighting game
"""
import pygame
from ..core import config

class Projectile:
    """Projectile that can be fired by fighters"""

    def __init__(self, x, y, direction, damage, owner, charge_percent=0.0):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.damage = damage
        self.owner = owner  # Reference to the fighter who fired it
        self.charge_percent = charge_percent  # How charged this projectile was

        # Movement
        self.velocity_x = config.PROJECTILE_SPEED * direction
        self.velocity_y = 0

        # Visual properties - size based on charge level
        min_size = 6  # Minimum projectile size
        max_size = config.PROJECTILE_SIZE  # Maximum projectile size
        self.size = int(min_size + (max_size - min_size) * charge_percent)
        self.color = config.GREEN

        # State
        self.active = True
        self.has_hit = False

        # Create rect for collision detection
        self.rect = pygame.Rect(x - self.size, y - self.size, self.size * 2, self.size * 2)

    def update(self):
        """Update projectile position and state"""
        if not self.active:
            return

        # Move projectile
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Update collision rect
        self.rect.x = self.x - self.size
        self.rect.y = self.y - self.size

        # Check if projectile is off screen
        if (self.x < config.STAGE_LEFT - 50 or
            self.x > config.STAGE_RIGHT + 50 or
            self.y > config.STAGE_FLOOR + 50):
            self.active = False

    def draw(self, screen):
        """Draw the projectile"""
        if not self.active:
            return

        # Draw main projectile as a glowing orb
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

        # Draw inner glow
        inner_color = tuple(min(255, c + 100) for c in self.color)
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.size // 2)

        # Draw collision rect for debugging
        # pygame.draw.rect(screen, config.RED, self.rect, 1)

    def check_collision(self, fighter):
        """Check if projectile collides with a fighter"""
        if not self.active or self.has_hit or fighter == self.owner:
            return False

        return self.rect.colliderect(fighter.rect)

    def hit_target(self):
        """Mark projectile as having hit a target"""
        self.has_hit = True
        self.active = False


class ChargingOrb:
    """Visual effect for charging projectile"""

    def __init__(self, fighter):
        self.fighter = fighter
        self.charge_time = 0
        self.max_charge = config.PROJECTILE_CHARGE_TIME

    def update(self):
        """Update charging orb"""
        self.charge_time += 1

        # Position orb in front of fighter
        if self.fighter.facing_right:
            self.x = self.fighter.x + self.fighter.width + 20
        else:
            self.x = self.fighter.x - 20

        self.y = self.fighter.y + self.fighter.height // 2

    def draw(self, screen):
        """Draw charging orb with increasing intensity"""
        if self.charge_time <= 0:
            return

        # Calculate charge percentage
        charge_percent = min(1.0, self.charge_time / self.max_charge)

        # Size grows with charge
        base_size = 8
        max_size = 16
        size = int(base_size + (max_size - base_size) * charge_percent)

        # Color intensity increases with charge
        green_intensity = int(100 + 155 * charge_percent)
        color = (0, green_intensity, 0)

        # Draw outer glow
        glow_size = size + 4
        glow_color = (0, green_intensity // 2, 0)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), glow_size)

        # Draw main orb
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

        # Draw inner bright spot
        inner_color = (100, 255, 100)
        inner_size = max(2, size // 3)
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), inner_size)

        # Add pulsing effect when fully charged
        if charge_percent >= 1.0:
            pulse = abs(pygame.time.get_ticks() % 500 - 250) / 250.0
            pulse_size = size + int(4 * pulse)
            pulse_color = (50, 255, 50)
            pygame.draw.circle(screen, pulse_color, (int(self.x), int(self.y)), pulse_size, 2)

    def get_charge_percent(self):
        """Get current charge percentage"""
        return min(1.0, self.charge_time / self.max_charge)

    def get_damage(self):
        """Calculate damage based on charge level"""
        charge_percent = self.get_charge_percent()
        min_damage = config.PROJECTILE_MIN_DAMAGE
        max_damage = config.PROJECTILE_MAX_DAMAGE
        return int(min_damage + (max_damage - min_damage) * charge_percent)
