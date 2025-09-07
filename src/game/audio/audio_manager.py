"""
Audio Manager for 2D Fighting Game
Handles loading and playing sound effects and music
"""
import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../core')))
import config

class AudioManager:
    def __init__(self):
        """Initialize the audio manager"""
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Audio storage
        self.sounds = {}
        self.music_playing = False
        
        # Volume settings
        self.master_volume = config.MASTER_VOLUME
        self.sfx_volume = config.SFX_VOLUME
        self.music_volume = config.MUSIC_VOLUME
        
        # Load all audio files
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound effects"""
        # Define sound file paths relative to the audio directory
        sound_files = {
            # Combat sounds
            'punch_hit': 'sfx/punch_hit.wav',
            'punch_miss': 'sfx/punch_miss.wav',
            'kick_hit': 'sfx/kick_hit.wav',
            'kick_miss': 'sfx/kick_miss.wav',
            'block': 'sfx/block.wav',
            'knockback': 'sfx/knockback.wav',
            
            # Movement sounds
            'jump': 'sfx/jump.wav',
            'land': 'sfx/land.wav',
            'footstep': 'sfx/footstep.wav',
            
            # UI sounds
            'menu_select': 'sfx/menu_select.wav',
            'menu_confirm': 'sfx/menu_confirm.wav',
            'game_start': 'sfx/game_start.wav',
            'game_over': 'sfx/game_over.wav',
            
            # Special effects
            'health_low': 'sfx/health_low.wav',
            'victory': 'sfx/victory.wav'
        }
        
        # Get the directory where this file is located
        audio_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load each sound file
        for sound_name, file_path in sound_files.items():
            full_path = os.path.join(audio_dir, file_path)
            try:
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    sound.set_volume(self.sfx_volume * self.master_volume)
                    self.sounds[sound_name] = sound
                    print(f"Loaded sound: {sound_name}")
                else:
                    print(f"Sound file not found: {full_path}")
                    # Create a silent placeholder
                    self.sounds[sound_name] = None
            except pygame.error as e:
                print(f"Error loading sound {sound_name}: {e}")
                self.sounds[sound_name] = None
    
    def play_sound(self, sound_name, volume_modifier=1.0):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                sound = self.sounds[sound_name]
                # Temporarily adjust volume
                original_volume = sound.get_volume()
                sound.set_volume(original_volume * volume_modifier)
                sound.play()
                # Restore original volume
                sound.set_volume(original_volume)
            except pygame.error as e:
                print(f"Error playing sound {sound_name}: {e}")
        else:
            print(f"Sound not available: {sound_name}")
    
    def play_music(self, music_file, loop=-1):
        """Play background music"""
        audio_dir = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(audio_dir, 'music', music_file)
        
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(loop)
                self.music_playing = True
                print(f"Playing music: {music_file}")
            else:
                print(f"Music file not found: {music_path}")
        except pygame.error as e:
            print(f"Error playing music {music_file}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def _update_volumes(self):
        """Update all sound volumes"""
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.sfx_volume * self.master_volume)
        
        if self.music_playing:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def cleanup(self):
        """Clean up audio resources"""
        pygame.mixer.quit()
