#!/usr/bin/env python3
"""
Setup script for Enhanced Hand Gesture Recognition System
Installs required dependencies and verifies installation
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("🔧 Installing required dependencies...")
    print("=" * 50)
    
    try:
        # Install packages from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt file not found!")
        return False

def verify_installation():
    """Verify that all required modules can be imported"""
    print("\n🔍 Verifying installation...")
    print("=" * 50)
    
    required_modules = [
        ("cv2", "opencv-python"),
        ("mediapipe", "mediapipe"),
        ("numpy", "numpy"),
        ("pynput", "pynput")
    ]
    
    all_good = True
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - FAILED")
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    print("🚀 Enhanced Hand Gesture Recognition System - Setup")
    print("=" * 60)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        print("Please ensure you have all project files in the same directory.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Some modules failed to install properly.")
        print("Please try installing manually:")
        print("pip install opencv-python mediapipe numpy pynput")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 60)
    print("You can now run the application with:")
    print("python main.py")
    print("\nControls:")
    print("- Press 's' to open Settings")
    print("- Press 'q' to quit")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
