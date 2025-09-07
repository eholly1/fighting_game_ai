#!/usr/bin/env python3
"""
Launch script for the Fighting Game AI Training Dashboard
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def launch_dashboard(port=8501):
    """Launch the Streamlit dashboard"""
    if not check_dependencies():
        return
    
    print("🚀 Launching Fighting Game AI Training Dashboard...")
    print(f"🌐 Dashboard will be available at: http://localhost:{port}")
    print("📊 Loading experiment data...")
    print("\n" + "="*50)
    
    try:
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard.py", 
            "--server.port", str(port),
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Launch Fighting Game AI Training Dashboard')
    parser.add_argument('--port', type=int, default=8501, help='Port to run dashboard on')
    
    args = parser.parse_args()
    
    # Change to the training directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    launch_dashboard(args.port)
