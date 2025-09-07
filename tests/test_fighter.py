"""
Unit tests for Fighter class
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
from game.core import config
from game.entities.fighter import Fighter

def test_fighter_creation():
    """Test fighter creation and basic properties"""
    pygame.init()
    fighter = Fighter(100, 100, config.RED)
    assert fighter.x == 100
    assert fighter.y == 100
    assert fighter.health == config.MAX_HEALTH
    assert fighter.is_alive()
    print("✓ Fighter creation test passed")

def test_fighter_movement():
    """Test fighter movement"""
    pygame.init()
    fighter = Fighter(100, config.STAGE_FLOOR - config.FIGHTER_HEIGHT, config.RED)
    
    # Test movement
    fighter.move_right()
    fighter.update()
    assert fighter.velocity_x == config.FIGHTER_SPEED
    
    fighter.move_left()
    fighter.update()
    assert fighter.velocity_x == -config.FIGHTER_SPEED
    
    print("✓ Fighter movement test passed")

def test_fighter_combat():
    """Test fighter combat"""
    pygame.init()
    fighter = Fighter(100, config.STAGE_FLOOR - config.FIGHTER_HEIGHT, config.RED)
    
    # Test attack
    fighter.punch()
    assert fighter.state == config.FighterState.PUNCHING
    assert fighter.is_attacking
    
    # Test damage
    initial_health = fighter.health
    fighter.take_damage(10)
    assert fighter.health == initial_health - 10
    
    print("✓ Fighter combat test passed")

def main():
    """Run all tests"""
    print("Running fighter tests...")
    
    try:
        test_fighter_creation()
        test_fighter_movement()
        test_fighter_combat()
        print("\n🎉 All fighter tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
