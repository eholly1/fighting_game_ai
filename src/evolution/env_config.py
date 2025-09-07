#!/usr/bin/env python3
"""
Environment Configuration for Evolutionary Training

Handles loading environment variables from .env file and provides
configuration management for the evolutionary training system.
"""
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

def load_environment():
    """
    Load environment variables from .env file
    
    Searches for .env file in current directory and parent directories
    """
    try:
        from dotenv import load_dotenv
        
        # Find .env file - check current directory and parent directories
        current_dir = Path.cwd()
        env_file = None
        
        # Check current directory first
        if (current_dir / '.env').exists():
            env_file = current_dir / '.env'
        else:
            # Check parent directories up to 3 levels
            for parent in current_dir.parents[:3]:
                if (parent / '.env').exists():
                    env_file = parent / '.env'
                    break
        
        if env_file:
            load_dotenv(env_file)
            print(f"✅ Loaded environment from: {env_file}")
            return True
        else:
            print("⚠️  No .env file found in current or parent directories")
            return False
            
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Failed to load .env file: {e}")
        return False

def get_anthropic_config() -> Dict[str, Optional[str]]:
    """
    Get Anthropic API configuration from environment variables
    
    Returns:
        Dictionary with api_key and model configuration
    """
    config = {
        'api_key': None,
        'model': None
    }
    
    # Try different environment variable names for API key
    api_key_vars = [
        'ANTHROPIC_API_KEY',
        'ANTHROPIC_KEY', 
        'CLAUDE_API_KEY',
        'CLAUDE_KEY'
    ]
    
    for var_name in api_key_vars:
        api_key = os.getenv(var_name)
        if api_key:
            config['api_key'] = api_key
            print(f"✅ Found Anthropic API key in {var_name}")
            break
    
    # Try different environment variable names for model
    model_vars = [
        'ANTHROPIC_MODEL',
        'CLAUDE_MODEL',
        'ANTHROPIC_MODEL_NAME',
        'CLAUDE_MODEL_NAME'
    ]
    
    for var_name in model_vars:
        model = os.getenv(var_name)
        if model:
            config['model'] = model
            print(f"✅ Found Anthropic model in {var_name}: {model}")
            break
    
    # Default model if not specified
    if not config['model']:
        config['model'] = "claude-3-5-sonnet-20241022"
        print(f"📝 Using default model: {config['model']}")
    
    return config

def validate_anthropic_config(config: Dict[str, Optional[str]]) -> bool:
    """
    Validate Anthropic configuration
    
    Args:
        config: Configuration dictionary from get_anthropic_config()
        
    Returns:
        True if configuration is valid, False otherwise
    """
    if not config['api_key']:
        print("❌ Anthropic API key not found!")
        print("   Please set one of these environment variables:")
        print("   - ANTHROPIC_API_KEY")
        print("   - ANTHROPIC_KEY")
        print("   - CLAUDE_API_KEY")
        print("   - CLAUDE_KEY")
        return False
    
    # Basic API key format validation
    api_key = config['api_key']
    if not api_key.startswith('sk-ant-'):
        print("⚠️  API key format may be incorrect (should start with 'sk-ant-')")
        print("   Proceeding anyway...")
    
    if len(api_key) < 20:
        print("⚠️  API key seems too short")
        print("   Proceeding anyway...")
    
    print(f"✅ Anthropic configuration validated")
    print(f"   API Key: {api_key[:12]}...{api_key[-4:]} (masked)")
    print(f"   Model: {config['model']}")
    
    return True

def setup_environment() -> Dict[str, Any]:
    """
    Complete environment setup for evolutionary training
    
    Returns:
        Configuration dictionary with all necessary settings
    """
    print("🔧 Setting up environment for evolutionary training")
    print("-" * 50)
    
    # Load .env file
    env_loaded = load_environment()
    
    # Get Anthropic configuration
    anthropic_config = get_anthropic_config()
    
    # Validate configuration
    config_valid = validate_anthropic_config(anthropic_config)
    
    if not config_valid:
        print("\n❌ Environment setup failed!")
        print("   Please check your .env file and API key configuration")
        return {}
    
    # Create complete configuration
    config = {
        'anthropic_api_key': anthropic_config['api_key'],
        'anthropic_model': anthropic_config['model'],
        'env_file_loaded': env_loaded,
        'config_valid': config_valid
    }
    
    print(f"\n✅ Environment setup complete!")
    return config

def create_sample_env_file(filepath: str = ".env") -> bool:
    """
    Create a sample .env file with template configuration
    
    Args:
        filepath: Path where to create the .env file
        
    Returns:
        True if file was created successfully
    """
    sample_content = """# Evolutionary Training Environment Configuration
# Copy this file to .env and fill in your actual values

# Anthropic API Configuration
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Alternative variable names (use any one of these for API key):
# ANTHROPIC_KEY=sk-ant-your-api-key-here
# CLAUDE_API_KEY=sk-ant-your-api-key-here
# CLAUDE_KEY=sk-ant-your-api-key-here

# Alternative variable names for model:
# CLAUDE_MODEL=claude-3-5-sonnet-20241022
# ANTHROPIC_MODEL_NAME=claude-3-5-sonnet-20241022
# CLAUDE_MODEL_NAME=claude-3-5-sonnet-20241022

# Optional: Training Configuration Overrides
# EVOLUTION_POPULATION_SIZE=20
# EVOLUTION_GENERATIONS=50
# EVOLUTION_GAMES_PER_MATCH=5
"""
    
    try:
        with open(filepath, 'w') as f:
            f.write(sample_content)
        
        print(f"✅ Created sample .env file: {filepath}")
        print("   Please edit this file with your actual API key")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_environment_setup():
    """Test the environment setup functionality"""
    print("🧪 Testing Environment Setup")
    print("=" * 50)
    
    # Test 1: Load environment
    print("\n1. Testing environment loading...")
    env_loaded = load_environment()
    
    # Test 2: Get configuration
    print("\n2. Testing configuration retrieval...")
    config = get_anthropic_config()
    
    # Test 3: Validate configuration
    print("\n3. Testing configuration validation...")
    if config['api_key']:
        valid = validate_anthropic_config(config)
        print(f"   Configuration valid: {valid}")
    else:
        print("   No API key found - this is expected if .env is not set up")
    
    # Test 4: Complete setup
    print("\n4. Testing complete setup...")
    full_config = setup_environment()
    
    success = len(full_config) > 0
    print(f"\n📊 Environment setup test: {'✅ PASS' if success else '❌ FAIL'}")
    
    if not success:
        print("\n💡 To fix this:")
        print("   1. Create a .env file in your project root")
        print("   2. Add: ANTHROPIC_API_KEY=your_actual_key_here")
        print("   3. Optionally add: ANTHROPIC_MODEL=claude-3-5-sonnet-20241022")
    
    return success

if __name__ == "__main__":
    # If run directly, test the environment setup
    if len(sys.argv) > 1 and sys.argv[1] == "create-sample":
        # Create sample .env file
        create_sample_env_file()
    else:
        # Test environment setup
        test_environment_setup()
