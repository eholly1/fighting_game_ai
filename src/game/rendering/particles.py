"""
Particle system for visual effects
"""
import pygame
import random
import math
from ..core import config

class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, size, lifetime):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.2

    def update(self):
        """Update particle position and lifetime"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity  # Apply gravity
        self.velocity_x *= 0.98  # Air resistance
        self.lifetime -= 1

        # Fade out as lifetime decreases
        fade_ratio = self.lifetime / self.max_lifetime
        self.size = max(1, int(self.size * fade_ratio))

    def is_alive(self):
        """Check if particle should still be rendered"""
        return self.lifetime > 0

    def draw(self, screen):
        """Draw the particle"""
        if self.is_alive():
            # Fade alpha based on lifetime
            fade_ratio = self.lifetime / self.max_lifetime
            alpha = int(255 * fade_ratio)

            # Create surface with alpha for fading
            particle_surface = pygame.Surface((self.size * 2, self.size * 2))
            particle_surface.set_alpha(alpha)

            # Draw particle as circle
            pygame.draw.circle(particle_surface, self.color,
                             (self.size, self.size), self.size)

            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_hit_effect(self, x, y, attack_type="punch"):
        """Add particles for a successful hit"""
        num_particles = 10 if attack_type == "kick" else 7

        for _ in range(num_particles):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)  # Increased speed
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - random.uniform(1, 3)  # Slight upward bias

            # Hit effect colors (red/orange for damage)
            colors = [config.RED, config.ORANGE, config.YELLOW]
            color = random.choice(colors)

            # Bigger particles for more impact
            size = random.randint(5, 10) if attack_type == "kick" else random.randint(4, 8)
            lifetime = random.randint(25, 45)  # Longer lasting

            particle = Particle(x, y, velocity_x, velocity_y, color, size, lifetime)
            self.particles.append(particle)

    def add_block_effect(self, x, y):
        """Add particles for a blocked attack"""
        num_particles = 6

        for _ in range(num_particles):
            # Particles spread outward from block point
            angle = random.uniform(-math.pi/3, math.pi/3)  # Forward spread
            speed = random.uniform(1, 4)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - random.uniform(0, 2)

            # Block effect colors (blue/cyan for defense)
            colors = [config.BLUE, config.CYAN, config.WHITE]
            color = random.choice(colors)

            size = random.randint(2, 4)
            lifetime = random.randint(15, 25)

            particle = Particle(x, y, velocity_x, velocity_y, color, size, lifetime)
            self.particles.append(particle)

    def add_knockback_effect(self, x, y, knockback_direction=1):
        """Add particles for knockback effect with sideways burst"""
        num_particles = 15

        for _ in range(num_particles):
            # Create a sideways burst in the knockback direction
            # Angle range: -45 to +45 degrees from horizontal
            base_angle = 0 if knockback_direction > 0 else math.pi  # Right or left
            angle_variation = random.uniform(-math.pi/4, math.pi/4)  # ±45 degrees
            angle = base_angle + angle_variation

            speed = random.uniform(5, 12)  # Higher speed for dramatic effect
            velocity_x = math.cos(angle) * speed * knockback_direction
            velocity_y = math.sin(angle) * speed - random.uniform(1, 3)  # Slight upward bias

            # Knockback effect colors (bright and energetic)
            colors = [config.YELLOW, config.ORANGE, config.WHITE]
            color = random.choice(colors)

            size = random.randint(6, 12)  # Bigger particles
            lifetime = random.randint(30, 50)  # Longer lasting

            particle = Particle(x, y, velocity_x, velocity_y, color, size, lifetime)
            self.particles.append(particle)

    def update(self):
        """Update all particles and remove dead ones"""
        # Update all particles
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()
