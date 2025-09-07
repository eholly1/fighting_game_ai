import sys
import os
import pytest
from unittest.mock import MagicMock, patch
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/game/controllers'))
from input_handler import InputHandler

class DummyEvent:
    def __init__(self, type, key):
        self.type = type
        self.key = key

@pytest.fixture
def input_handler():
    return InputHandler()

def test_initialization(input_handler):
    assert isinstance(input_handler.keys_pressed, set)
    assert isinstance(input_handler.keys_just_pressed, set)
    assert isinstance(input_handler.keys_just_released, set)

def test_is_key_pressed(input_handler):
    input_handler.keys_pressed.add('a')
    assert input_handler.is_key_pressed('a')
    assert not input_handler.is_key_pressed('b')

def test_is_key_just_pressed(input_handler):
    input_handler.keys_just_pressed.add('a')
    assert input_handler.is_key_just_pressed('a')
    assert not input_handler.is_key_just_pressed('b')

def test_is_key_just_released(input_handler):
    input_handler.keys_just_released.add('a')
    assert input_handler.is_key_just_released('a')
    assert not input_handler.is_key_just_released('b')
