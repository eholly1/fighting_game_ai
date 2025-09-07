"""
Main entry point for the 2D Fighting Game
"""
import argparse
from game.core.game_engine import Game

def main():
    """Main function to start the game"""
    parser = argparse.ArgumentParser(description='2D Fighting Game')
    parser.add_argument('--record_demonstrations', action='store_true',
                       help='Automatically start recording demonstrations')

    args = parser.parse_args()

    print("Starting 2D Fighting Game...")
    print("Controls:")
    print("Player 1: WASD to move, J to punch, K to kick, L to block, I to charge projectile")
    print("Player 2: Arrow keys to move, Numpad 1 to punch, Numpad 2 to kick, Numpad 0 to block")
    print("ESC to quit, P to pause, R to restart (when game over)")

    if args.record_demonstrations:
        print("\n🎬 DEMONSTRATION RECORDING MODE")
        print("Recording will start automatically when you begin fighting!")
        print("Press F2 to save, F3 to clear, F4 for stats")

    game = Game(record_demonstrations=args.record_demonstrations)
    game.run()

if __name__ == "__main__":
    main()
