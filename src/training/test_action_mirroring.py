#!/usr/bin/env python3
"""
Test script to verify action mirroring is working correctly in the training environment
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from training.environment import FightingGameEnv

def test_action_mirroring():
    """Test that action mirroring works correctly"""
    print("🧪 Testing Action Mirroring in Training Environment")
    print("=" * 60)

    # Create environment
    env = FightingGameEnv(headless=True)

    # Test case 1: Fighter1 on left, Fighter2 on right (normal positioning)
    print("\n📍 Test 1: Normal positioning (Fighter1 left, Fighter2 right)")
    env.reset()

    # Ensure normal positioning
    env.fighter1.x = 200  # Left side
    env.fighter2.x = 600  # Right side

    print(f"   Fighter1 position: {env.fighter1.x}")
    print(f"   Fighter2 position: {env.fighter2.x}")

    # Test move_right action for fighter1 (should move right, toward fighter2)
    initial_x1 = env.fighter1.x
    env._execute_action_with_mirroring(env.fighter1, env.fighter2, 2)  # move_right
    env.fighter1.update()

    if env.fighter1.x > initial_x1:
        print("   ✅ Fighter1 move_right: CORRECT (moved right toward opponent)")
    else:
        print("   ❌ Fighter1 move_right: FAILED (did not move right)")

    # Test case 2: Fighter1 on right, Fighter2 on left (mirrored positioning)
    print("\n📍 Test 2: Mirrored positioning (Fighter1 right, Fighter2 left)")
    env.reset()

    # Force mirrored positioning
    env.fighter1.x = 600  # Right side
    env.fighter2.x = 200  # Left side

    print(f"   Fighter1 position: {env.fighter1.x}")
    print(f"   Fighter2 position: {env.fighter2.x}")

    # Test move_right action for fighter1 (should be mirrored to move_left, toward fighter2)
    initial_x1 = env.fighter1.x
    env._execute_action_with_mirroring(env.fighter1, env.fighter2, 2)  # move_right (should be mirrored)
    env.fighter1.update()

    if env.fighter1.x < initial_x1:
        print("   ✅ Fighter1 move_right (mirrored): CORRECT (moved left toward opponent)")
    else:
        print("   ❌ Fighter1 move_right (mirrored): FAILED (did not move toward opponent)")

    # Test case 3: Verify mirroring logic directly
    print("\n🔄 Test 3: Direct mirroring logic")

    mirror_tests = [
        ('move_left', 'move_right'),
        ('move_right', 'move_left'),
        ('move_left_block', 'move_right_block'),
        ('move_right_block', 'move_left_block'),
        ('punch', 'punch'),  # Should not change
        ('kick', 'kick'),    # Should not change
        ('block', 'block'),  # Should not change
        ('jump', 'jump'),    # Should not change
        ('projectile', 'projectile'),  # Should not change
        ('idle', 'idle'),    # Should not change
    ]

    all_passed = True
    for original, expected in mirror_tests:
        mirrored = env._mirror_action(original)
        if mirrored == expected:
            print(f"   ✅ {original} -> {mirrored}")
        else:
            print(f"   ❌ {original} -> {mirrored} (expected {expected})")
            all_passed = False

    # Test case 4: State mirroring consistency
    print("\n🎯 Test 4: State mirroring consistency")
    env.reset()

    # Position fighter1 on right
    env.fighter1.x = 600
    env.fighter2.x = 200

    # Get state for fighter1 (should be mirrored)
    state = env.get_state(player_fighter=env.fighter1)
    relative_pos = state[23]  # relative position

    if relative_pos < 0:  # Opponent should appear to the left in mirrored state
        print("   ✅ State mirroring: CORRECT (opponent appears to left)")
    else:
        print("   ❌ State mirroring: FAILED (opponent does not appear to left)")
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Action mirroring is working correctly.")
        print("   Evolutionary training should now work properly!")
    else:
        print("❌ SOME TESTS FAILED! Action mirroring needs more work.")

    env.close()
    return all_passed

if __name__ == "__main__":
    test_action_mirroring()
