#!/usr/bin/env python3
"""
Simple runner script for evolutionary training

This script provides an easy way to run evolutionary training with
automatic environment setup and sensible defaults.
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from env_config import setup_environment, create_sample_env_file
from evolution_runner import main as evolution_main

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if .env file exists
    env_file_exists = os.path.exists('.env') or os.path.exists('../.env') or os.path.exists('../../.env')
    
    if not env_file_exists:
        print("⚠️  No .env file found!")
        print("💡 Would you like me to create a sample .env file? (y/n): ", end="")
        
        try:
            response = input().lower().strip()
            if response in ['y', 'yes']:
                success = create_sample_env_file()
                if success:
                    print("\n✅ Sample .env file created!")
                    print("📝 Please edit the .env file with your actual Anthropic API key")
                    print("   Then run this script again.")
                    return False
                else:
                    print("❌ Failed to create .env file")
                    return False
            else:
                print("📝 Please create a .env file with your Anthropic API key")
                print("   Example content:")
                print("   ANTHROPIC_API_KEY=sk-ant-your-key-here")
                print("   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022")
                return False
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return False
    
    # Test environment setup
    env_config = setup_environment()
    
    if not env_config.get('config_valid', False):
        print("❌ Environment configuration is invalid!")
        print("💡 Please check your .env file and ensure ANTHROPIC_API_KEY is set correctly")
        return False
    
    print("✅ All prerequisites met!")
    return True

def run_quick_test():
    """Run a quick test evolution"""
    print("\n🧪 Running quick test evolution...")
    print("   Population: 3 agents")
    print("   Generations: 1")
    print("   Games per match: 1")
    
    # Override sys.argv for the test
    original_argv = sys.argv.copy()
    sys.argv = [
        'evolution_runner.py',
        '--population', '3',
        '--generations', '1', 
        '--games-per-match', '1',
        '--experiment-name', 'quick_test'
    ]
    
    try:
        result = evolution_main()
        sys.argv = original_argv
        return result == 0
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        sys.argv = original_argv
        return False

def run_small_evolution():
    """Run a small evolution for testing"""
    print("\n🧬 Running small evolution...")
    print("   Population: 8 agents")
    print("   Generations: 3")
    print("   Games per match: 2")
    
    original_argv = sys.argv.copy()
    sys.argv = [
        'evolution_runner.py',
        '--population', '8',
        '--generations', '3',
        '--games-per-match', '2',
        '--experiment-name', 'small_evolution'
    ]
    
    try:
        result = evolution_main()
        sys.argv = original_argv
        return result == 0
    except Exception as e:
        print(f"❌ Small evolution failed: {e}")
        sys.argv = original_argv
        return False

def run_full_evolution():
    """Run a full evolution"""
    print("\n🚀 Running full evolution...")
    print("   Population: 15 agents")
    print("   Generations: 10")
    print("   Games per match: 3")
    
    original_argv = sys.argv.copy()
    sys.argv = [
        'evolution_runner.py',
        '--population', '15',
        '--generations', '10',
        '--games-per-match', '3'
    ]
    
    try:
        result = evolution_main()
        sys.argv = original_argv
        return result == 0
    except Exception as e:
        print(f"❌ Full evolution failed: {e}")
        sys.argv = original_argv
        return False

def interactive_menu():
    """Interactive menu for running evolution"""
    print("\n🎮 Evolutionary Training Menu")
    print("=" * 40)
    print("1. Quick test (3 agents, 1 generation)")
    print("2. Small evolution (8 agents, 3 generations)")
    print("3. Full evolution (15 agents, 10 generations)")
    print("4. Custom parameters")
    print("5. Exit")
    
    while True:
        try:
            print("\n🔢 Choose an option (1-5): ", end="")
            choice = input().strip()
            
            if choice == '1':
                success = run_quick_test()
                if success:
                    print("✅ Quick test completed successfully!")
                else:
                    print("❌ Quick test failed")
                break
                
            elif choice == '2':
                success = run_small_evolution()
                if success:
                    print("✅ Small evolution completed successfully!")
                else:
                    print("❌ Small evolution failed")
                break
                
            elif choice == '3':
                success = run_full_evolution()
                if success:
                    print("✅ Full evolution completed successfully!")
                else:
                    print("❌ Full evolution failed")
                break
                
            elif choice == '4':
                print("\n📝 Custom Parameters:")
                try:
                    pop = input("Population size (default 15): ").strip() or "15"
                    gen = input("Generations (default 10): ").strip() or "10"
                    games = input("Games per match (default 3): ").strip() or "3"
                    name = input("Experiment name (optional): ").strip() or None
                    
                    original_argv = sys.argv.copy()
                    sys.argv = ['evolution_runner.py', '--population', pop, '--generations', gen, '--games-per-match', games]
                    if name:
                        sys.argv.extend(['--experiment-name', name])
                    
                    result = evolution_main()
                    sys.argv = original_argv
                    
                    if result == 0:
                        print("✅ Custom evolution completed successfully!")
                    else:
                        print("❌ Custom evolution failed")
                    break
                    
                except KeyboardInterrupt:
                    print("\n👋 Cancelled")
                    continue
                    
            elif choice == '5':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def main():
    """Main function"""
    print("🧬 Evolutionary Fighting Game AI Training")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # If command line arguments provided, run directly
    if len(sys.argv) > 1:
        # Pass through to evolution_runner
        return evolution_main()
    
    # Otherwise, show interactive menu
    interactive_menu()
    return 0

if __name__ == "__main__":
    sys.exit(main())
