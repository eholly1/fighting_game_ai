
import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the audio module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/game/audio'))
from audio_manager import AudioManager

@pytest.fixture
def audio_manager():
    # Patch pygame.mixer to avoid actual audio playback
    with patch('audio_manager.pygame.mixer') as mock_mixer:
        yield AudioManager()

def test_initialization_loads_all_sounds(audio_manager):
    assert hasattr(audio_manager, 'sounds')
    assert isinstance(audio_manager.sounds, dict)

def test_play_valid_sound(audio_manager):
    audio_manager.sounds['punch'] = MagicMock()
    audio_manager.play_sound('punch')
    audio_manager.sounds['punch'].play.assert_called_once()

def test_play_missing_sound_logs_warning(audio_manager, capsys):
    audio_manager.play_sound('missing_sound')
    captured = capsys.readouterr()
    assert 'Sound not available' in captured.out or 'not found' in captured.out

def test_cleanup_releases_resources(audio_manager):
    with patch('audio_manager.pygame.mixer.quit') as mock_quit:
        audio_manager.cleanup()
        mock_quit.assert_called_once()
