"""
Input handler for human players
"""
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../core')))
import config

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()

    def update(self, events):
        """Update input state based on pygame events"""
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()

        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.keys_pressed.add(key_name)
                self.keys_just_pressed.add(key_name)
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.keys_pressed.discard(key_name)
                self.keys_just_released.add(key_name)

    def is_key_pressed(self, key: str) -> bool:
        """Check if key is currently pressed"""
        return key in self.keys_pressed

    def is_key_just_pressed(self, key: str) -> bool:
        """Check if key was just pressed this frame"""
        return key in self.keys_just_pressed

    def is_key_just_released(self, key: str) -> bool:
        """Check if key was just released this frame"""
        return key in self.keys_just_released

class PlayerController:
    def __init__(self, player_id: int, input_handler: InputHandler):
        self.player_id = player_id
        self.input_handler = input_handler

        # Get control scheme based on player ID
        if player_id == 1:
            self.controls = config.PLAYER1_CONTROLS
        else:
            self.controls = config.PLAYER2_CONTROLS

    def update_fighter(self, fighter, audio_manager=None, demo_recorder=None, opponent=None):
        """Update fighter based on input"""
        # Determine current action for recording
        current_action = self._get_current_action()

        # Record demonstration if recorder is provided
        if demo_recorder and opponent:
            # Get state from RL AI controller format (with mirroring)
            from .ai_controller import RLAIController
            temp_controller = RLAIController()
            state = temp_controller.get_state_vector(fighter, opponent)
            demo_recorder.record_step(state, current_action)
        # Movement
        left_pressed = self.input_handler.is_key_pressed(self.controls['left'])
        right_pressed = self.input_handler.is_key_pressed(self.controls['right'])

        if left_pressed and not right_pressed:
            fighter.move_left(audio_manager)
        elif right_pressed and not left_pressed:
            fighter.move_right(audio_manager)
        else:
            fighter.stop_moving()

        # Jump
        if self.input_handler.is_key_just_pressed(self.controls['jump']):
            fighter.jump(audio_manager)

        # Attacks
        if self.input_handler.is_key_just_pressed(self.controls['punch']):
            fighter.punch(audio_manager)

        if self.input_handler.is_key_just_pressed(self.controls['kick']):
            fighter.kick(audio_manager)

        # Block
        if self.input_handler.is_key_pressed(self.controls['block']):
            fighter.block()
        elif self.input_handler.is_key_just_released(self.controls['block']):
            fighter.stop_blocking()

        # Projectile - charge while held, fire when released
        if self.input_handler.is_key_pressed(self.controls['projectile']):
            if not fighter.is_charging_projectile:
                fighter.start_charging_projectile()
        elif self.input_handler.is_key_just_released(self.controls['projectile']):
            if fighter.is_charging_projectile:
                projectile = fighter.stop_charging_projectile(audio_manager)
                if projectile:
                    return projectile  # Return projectile to be added to game

        return None

    def _get_current_action(self):
        """Determine the current action based on input state"""
        # Check for complex actions first
        left_pressed = self.input_handler.is_key_pressed(self.controls['left'])
        right_pressed = self.input_handler.is_key_pressed(self.controls['right'])
        block_pressed = self.input_handler.is_key_pressed(self.controls['block'])

        # Movement + block combinations
        if left_pressed and block_pressed:
            return 'move_left_block'
        elif right_pressed and block_pressed:
            return 'move_right_block'

        # Single actions (prioritize attacks and special actions)
        if self.input_handler.is_key_pressed(self.controls['projectile']):
            return 'projectile'
        elif self.input_handler.is_key_just_pressed(self.controls['punch']):
            return 'punch'
        elif self.input_handler.is_key_just_pressed(self.controls['kick']):
            return 'kick'
        elif block_pressed:
            return 'block'
        elif self.input_handler.is_key_just_pressed(self.controls['jump']):
            return 'jump'
        elif left_pressed:
            return 'move_left'
        elif right_pressed:
            return 'move_right'
        else:
            return 'idle'
