"""
Fighter class for the 2D Fighting Game
"""
import pygame
from ..core import config
from typing import Tuple

class Fighter:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], facing_right: bool = True):
        # Position and movement
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.facing_right = facing_right

        # Fighter properties
        self.width = config.FIGHTER_WIDTH
        self.height = config.FIGHTER_HEIGHT
        self.color = color
        self.health = config.MAX_HEALTH
        self.max_health = config.MAX_HEALTH

        # State management
        self.state = config.FighterState.IDLE
        self.state_timer = 0
        self.is_grounded = True

        # Combat properties
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.is_attacking = False
        self.is_blocking = False
        self.hit_timer = 0
        self.has_hit_this_attack = False  # Prevent multiple hits per attack
        self.has_played_block_sound = False  # Prevent multiple block sounds per attack
        self.knockback_timer = 0  # Timer for knockback state

        # Recovery delay timers
        self.attack_to_block_delay = 0  # Delay after attack before can block
        self.block_to_attack_delay = 0  # Delay after block before can attack
        self.block_timer = 0  # Timer for minimum block duration
        self.block_button_held = False  # Track if block button is currently held

        # Projectile state
        self.projectile_cooldown = 0
        self.charging_orb = None
        self.is_charging_projectile = False

        # Create rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Attack hitboxes
        self.punch_hitbox = None
        self.kick_hitbox = None

    def update(self):
        """Update fighter state and physics"""
        self.state_timer += 1

        # Debug knockback state
        if self.state == config.FighterState.KNOCKBACK and not config.TRAINING_MODE:
            print(f"DEBUG UPDATE: In knockback state - velocity_x: {self.velocity_x}, timer: {self.knockback_timer}")

        # Update timers
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
        if self.attack_to_block_delay > 0:
            self.attack_to_block_delay -= 1
        if self.block_to_attack_delay > 0:
            self.block_to_attack_delay -= 1
        if self.block_timer > 0:
            self.block_timer -= 1
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        # Update charging orb
        if self.charging_orb:
            self.charging_orb.update()

        # Apply gravity
        if not self.is_grounded:
            self.velocity_y += config.GRAVITY
            if self.velocity_y > config.MAX_FALL_SPEED:
                self.velocity_y = config.MAX_FALL_SPEED

        # Update position
        if self.state == config.FighterState.KNOCKBACK and self.velocity_x != 0 and not config.TRAINING_MODE:
            print(f"DEBUG UPDATE: Knockback fighter moving - velocity_x: {self.velocity_x}, new_x: {self.x + self.velocity_x}")
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Ground collision
        if self.y >= config.STAGE_FLOOR - self.height:
            self.y = config.STAGE_FLOOR - self.height
            self.velocity_y = 0
            # Check if just landed (was airborne, now grounded)
            if not self.is_grounded:
                # Just landed - play land sound
                if hasattr(self, 'audio_manager') and self.audio_manager:
                    self.audio_manager.play_sound('land')
            self.is_grounded = True
            if self.state == config.FighterState.JUMPING:
                self.state = config.FighterState.IDLE
        else:
            self.is_grounded = False

        # Stage boundaries
        if self.x < config.STAGE_LEFT:
            if self.state == config.FighterState.KNOCKBACK and not config.TRAINING_MODE:
                print(f"DEBUG BOUNDARY: Knockback fighter hit left boundary, x was {self.x}")
            self.x = config.STAGE_LEFT
        elif self.x > config.STAGE_RIGHT - self.width:
            if self.state == config.FighterState.KNOCKBACK and not config.TRAINING_MODE:
                print(f"DEBUG BOUNDARY: Knockback fighter hit right boundary, x was {self.x}")
            self.x = config.STAGE_RIGHT - self.width

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y

        # Update attack hitboxes
        self._update_hitboxes()

        # Handle state transitions
        self._handle_state_transitions()

    def _update_hitboxes(self):
        """Update attack hitboxes based on current state"""
        self.punch_hitbox = None
        self.kick_hitbox = None

        if self.state == config.FighterState.PUNCHING and self.attack_timer > 0:
            # Punch hitbox in front of fighter - shorter range and height
            hitbox_x = self.x + self.width if self.facing_right else self.x - config.PUNCH_RANGE
            self.punch_hitbox = pygame.Rect(
                hitbox_x, self.y + 30, config.PUNCH_RANGE, 25
            )

        elif self.state == config.FighterState.KICKING and self.attack_timer > 0:
            # Kick hitbox in front of fighter - lower height, shorter vertical range
            hitbox_x = self.x + self.width if self.facing_right else self.x - config.KICK_RANGE
            self.kick_hitbox = pygame.Rect(
                hitbox_x, self.y + 60, config.KICK_RANGE, 30
            )

    def _handle_state_transitions(self):
        """Handle automatic state transitions"""
        # Attack state transitions
        if self.state == config.FighterState.PUNCHING:
            if self.attack_timer <= 0:
                # Play miss sound if attack didn't hit anything
                if not self.has_hit_this_attack and hasattr(self, 'audio_manager') and self.audio_manager:
                    self.audio_manager.play_sound('punch_miss')
                self.state = config.FighterState.IDLE
                self.is_attacking = False
                self.has_hit_this_attack = False  # Reset hit flag when attack ends
        elif self.state == config.FighterState.KICKING:
            if self.attack_timer <= 0:
                # Play miss sound if attack didn't hit anything
                if not self.has_hit_this_attack and hasattr(self, 'audio_manager') and self.audio_manager:
                    self.audio_manager.play_sound('kick_miss')
                self.state = config.FighterState.IDLE
                self.is_attacking = False
                self.has_hit_this_attack = False  # Reset hit flag when attack ends

        # Hit state transition
        if self.state == config.FighterState.HIT:
            if self.hit_timer <= 0:
                self.state = config.FighterState.IDLE
                self.has_hit_this_attack = False  # Reset hit flag when exiting hit state

        # Knockback state transition
        if self.state == config.FighterState.KNOCKBACK:
            if self.knockback_timer <= 0 and self.is_grounded:
                self.state = config.FighterState.IDLE
                self.has_hit_this_attack = False  # Reset hit flag when exiting knockback state

        # Block state transition - automatically exit blocking when minimum duration expires
        # and block button is not being held
        if self.state == config.FighterState.BLOCKING:
            if self.block_timer <= 0 and not self.block_button_held:
                self.state = config.FighterState.IDLE
                self.is_blocking = False
                self.block_to_attack_delay = config.BLOCK_TO_ATTACK_DELAY

        # Charging state - handled by input system, but clean up if needed
        if self.state == config.FighterState.CHARGING and not self.is_charging_projectile:
            self.state = config.FighterState.IDLE
            self.charging_orb = None

        # Safety check: if charging flag is set but not in charging state, clean up
        if self.is_charging_projectile and self.state != config.FighterState.CHARGING:
            if not config.TRAINING_MODE:
                print(f"DEBUG: Cleaning up stuck charging state (state: {self.state})")
            self.cancel_charging_projectile()

    def move_left(self, audio_manager=None):
        """Move fighter left"""
        if self.can_move():
            self.velocity_x = -config.FIGHTER_SPEED
            self.facing_right = False
            if self.is_grounded and self.state == config.FighterState.IDLE:
                self.state = config.FighterState.WALKING
                # Play footstep sound when starting to walk
                if audio_manager:
                    audio_manager.play_sound('footstep', 0.5)  # Quieter footsteps

    def move_right(self, audio_manager=None):
        """Move fighter right"""
        if self.can_move():
            self.velocity_x = config.FIGHTER_SPEED
            self.facing_right = True
            if self.is_grounded and self.state == config.FighterState.IDLE:
                self.state = config.FighterState.WALKING
                # Play footstep sound when starting to walk
                if audio_manager:
                    audio_manager.play_sound('footstep', 0.5)  # Quieter footsteps

    def jump(self, audio_manager=None):
        """Make fighter jump"""
        if self.is_grounded and self.can_move():
            self.velocity_y = -config.JUMP_STRENGTH
            self.is_grounded = False
            self.state = config.FighterState.JUMPING
            # Play jump sound
            if audio_manager:
                audio_manager.play_sound('jump')

    def punch(self, audio_manager=None):
        """Execute punch attack"""
        if self.can_attack():
            if not config.TRAINING_MODE:
                print(f"DEBUG: Fighter starting punch attack - can_attack: {self.can_attack()}")
            self.state = config.FighterState.PUNCHING
            self.attack_timer = config.ATTACK_DURATION
            self.attack_cooldown = config.ATTACK_COOLDOWN
            self.attack_to_block_delay = config.ATTACK_TO_BLOCK_DELAY  # Set delay before can block
            self.is_attacking = True
            self.has_hit_this_attack = False  # Reset hit flag for new attack
            self.has_played_block_sound = False  # Reset block sound flag for new attack
            self.velocity_x = 0
            self.audio_manager = audio_manager  # Store for miss sound later
        else:
            if not config.TRAINING_MODE:
                print(f"DEBUG: Punch blocked - can_attack: {self.can_attack()}, state: {self.state}, grounded: {self.is_grounded}, cooldown: {self.attack_cooldown}")

    def kick(self, audio_manager=None):
        """Execute kick attack"""
        if self.can_attack():
            if not config.TRAINING_MODE:
                print(f"DEBUG: Fighter starting kick attack - can_attack: {self.can_attack()}")
            self.state = config.FighterState.KICKING
            self.attack_timer = config.ATTACK_DURATION
            self.attack_cooldown = config.ATTACK_COOLDOWN
            self.attack_to_block_delay = config.ATTACK_TO_BLOCK_DELAY  # Set delay before can block
            self.is_attacking = True
            self.has_hit_this_attack = False  # Reset hit flag for new attack
            self.has_played_block_sound = False  # Reset block sound flag for new attack
            self.velocity_x = 0
            self.audio_manager = audio_manager  # Store for miss sound later
        else:
            if not config.TRAINING_MODE:
                print(f"DEBUG: Kick blocked - can_attack: {self.can_attack()}, state: {self.state}, grounded: {self.is_grounded}, cooldown: {self.attack_cooldown}")

    def start_charging_projectile(self):
        """Start charging a projectile"""
        if self.can_charge_projectile():
            from .projectile import ChargingOrb
            self.state = config.FighterState.CHARGING
            self.is_charging_projectile = True
            self.charging_orb = ChargingOrb(self)
            self.velocity_x = 0

    def stop_charging_projectile(self, audio_manager=None):
        """Stop charging and fire projectile"""
        if self.state == config.FighterState.CHARGING and self.charging_orb:
            from .projectile import Projectile

            # Calculate projectile spawn position
            if self.facing_right:
                proj_x = self.x + self.width + 10
            else:
                proj_x = self.x - 10
            proj_y = self.y + self.height // 2

            # Get damage and charge level
            damage = self.charging_orb.get_damage()
            charge_percent = self.charging_orb.get_charge_percent()
            direction = 1 if self.facing_right else -1

            # Create projectile with charge level for visual consistency
            projectile = Projectile(proj_x, proj_y, direction, damage, self, charge_percent)

            # Clean up charging state
            self.state = config.FighterState.IDLE
            self.is_charging_projectile = False
            self.charging_orb = None
            self.projectile_cooldown = config.PROJECTILE_COOLDOWN

            return projectile
        return None

    def cancel_charging_projectile(self):
        """Cancel charging without firing"""
        if self.state == config.FighterState.CHARGING:
            self.state = config.FighterState.IDLE
            self.is_charging_projectile = False
            self.charging_orb = None

    def can_charge_projectile(self) -> bool:
        """Check if fighter can start charging a projectile"""
        return (self.projectile_cooldown <= 0 and
                self.state not in [
                    config.FighterState.PUNCHING,
                    config.FighterState.KICKING,
                    config.FighterState.CHARGING,
                    config.FighterState.HIT,
                    config.FighterState.KNOCKBACK,
                    config.FighterState.BLOCKING
                ])

    def block(self):
        """Enter blocking state"""
        self.block_button_held = True  # Mark block button as held
        # Can't block while charging projectile
        if self.is_charging_projectile:
            return
        if self.can_move() and self.attack_to_block_delay <= 0:
            self.state = config.FighterState.BLOCKING
            self.is_blocking = True
            self.block_timer = config.MINIMUM_BLOCK_DURATION  # Set minimum block duration
            self.velocity_x = 0

    def stop_blocking(self):
        """Exit blocking state"""
        self.block_button_held = False  # Mark block button as released
        if self.state == config.FighterState.BLOCKING and self.block_timer <= 0:
            self.state = config.FighterState.IDLE
            self.is_blocking = False
            self.block_to_attack_delay = config.BLOCK_TO_ATTACK_DELAY  # Set delay before can attack

    def stop_moving(self):
        """Stop horizontal movement"""
        if self.state == config.FighterState.WALKING:
            self.state = config.FighterState.IDLE
        self.velocity_x = 0
        # Safety reset: ensure hit flag is cleared when not attacking
        if self.state not in [config.FighterState.PUNCHING, config.FighterState.KICKING]:
            self.has_hit_this_attack = False

    def take_damage(self, damage: int, knockback_force: float = 0, knockback_direction: int = 0):
        """Take damage and enter hit state"""
        # Cancel charging if taking damage
        if self.is_charging_projectile:
            self.cancel_charging_projectile()

        if self.is_blocking:
            damage = int(damage * config.BLOCK_REDUCTION)

        self.health -= damage
        if self.health < 0:
            self.health = 0

        # Apply knockback
        if knockback_force > 0:
            # Enter knockback state with upward and horizontal force
            if not config.TRAINING_MODE:
                print(f"DEBUG KNOCKBACK: Entering knockback state")
            self.state = config.FighterState.KNOCKBACK
            self.knockback_timer = config.KNOCKBACK_DURATION
            self.is_blocking = False

            # Apply horizontal knockback in the specified direction
            self.velocity_x = knockback_force * knockback_direction
            if not config.TRAINING_MODE:
                print(f"DEBUG KNOCKBACK: force={knockback_force}, direction={knockback_direction}, velocity_x={self.velocity_x}, state={self.state}")

            # Apply upward force (launch into air)
            self.velocity_y = -config.KICK_UPWARD_FORCE
            self.is_grounded = False
        else:
            # Regular hit without knockback
            self.state = config.FighterState.HIT
            self.hit_timer = 20
            self.is_blocking = False

    def take_blocked_damage(self, damage: int):
        """Take reduced damage while blocking without changing state"""
        # Cancel charging if taking damage
        if self.is_charging_projectile:
            self.cancel_charging_projectile()

        # Apply block damage reduction
        blocked_damage = int(damage * config.BLOCK_REDUCTION)
        self.health -= blocked_damage
        if self.health < 0:
            self.health = 0

        # Don't change state or stop blocking - just take the damage

    def can_move(self) -> bool:
        """Check if fighter can move"""
        return self.state not in [
            config.FighterState.PUNCHING,
            config.FighterState.KICKING,
            config.FighterState.CHARGING,
            config.FighterState.HIT,
            config.FighterState.KNOCKBACK,
            config.FighterState.BLOCKING
        ]

    def can_attack(self) -> bool:
        """Check if fighter can attack"""
        return (self.attack_cooldown <= 0 and
                self.block_to_attack_delay <= 0 and
                self.state not in [
                    config.FighterState.PUNCHING,
                    config.FighterState.KICKING,
                    config.FighterState.CHARGING,  # Can't attack while charging
                    config.FighterState.HIT,
                    config.FighterState.KNOCKBACK
                ])

    def get_attack_hitbox(self):
        """Get current attack hitbox if any"""
        if self.punch_hitbox:
            return self.punch_hitbox, config.PUNCH_DAMAGE, config.PUNCH_KNOCKBACK
        elif self.kick_hitbox:
            return self.kick_hitbox, config.KICK_DAMAGE, config.KICK_KNOCKBACK
        return None, 0, 0

    def is_alive(self) -> bool:
        """Check if fighter is still alive"""
        return self.health > 0

    def get_debug_info(self) -> str:
        """Get debug information about fighter state"""
        return f"State: {self.state}, Attack Timer: {self.attack_timer}, Has Hit: {self.has_hit_this_attack}, Cooldown: {self.attack_cooldown}"

    def can_be_pushed(self) -> bool:
        """Check if fighter can be pushed by collision"""
        # Can't be pushed if blocking, in knockback, or being hit
        return not (self.is_blocking or
                   self.state in [config.FighterState.KNOCKBACK, config.FighterState.HIT])

    def push(self, push_direction: int):
        """Push fighter in the given direction if possible"""
        if not self.can_be_pushed():
            return False

        # Check if there's room to be pushed (not at stage edge)
        new_x = self.x + (config.PUSH_FORCE * push_direction)

        # Check stage boundaries with threshold
        left_boundary = config.STAGE_LEFT + config.PUSH_DISTANCE_THRESHOLD
        right_boundary = config.STAGE_RIGHT - self.width - config.PUSH_DISTANCE_THRESHOLD

        if new_x >= left_boundary and new_x <= right_boundary:
            self.x = new_x
            return True

        return False
