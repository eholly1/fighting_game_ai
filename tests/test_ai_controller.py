import sys
import os
import pytest
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/game/controllers'))
from ai_controller import DummyAI
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/game/core'))
import config

def test_dummy_ai_initialization():
    ai = DummyAI()
    assert ai.decision_timer == 0
    assert ai.current_action == "idle"
    assert ai.action_duration == 0
    assert ai.target_distance == 150
    assert hasattr(ai, 'behavior_mode')
    assert hasattr(ai, 'is_charging_projectile')
    assert hasattr(ai, 'charge_start_distance')

def test_set_behavior_mode_changes_mode_and_prints():
    ai = DummyAI()
    with patch('builtins.print') as mock_print:
        ai.set_behavior_mode(config.AIBehavior.DEFAULT)
        mock_print.assert_called()

def test_get_behavior_name_default():
    ai = DummyAI()
    name = ai._get_behavior_name(config.AIBehavior.DEFAULT)
    assert isinstance(name, str)
    assert "Default" in name or name == "Default AI"
