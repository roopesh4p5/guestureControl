#!/usr/bin/env python3
"""
Enhanced Hand Gesture Recognition System
Main entry point for the comprehensive gesture recognition application

Features:
- Profile-based gesture collections (Racing, Video Control, Gaming)
- 3-2-1 countdown timer for gesture recording
- Real-time hand tracking and gesture recognition
- Key binding assignment for gestures
- Automatic file persistence for gesture profiles
- GUI settings panel for easy management

Usage:
    python main.py

Controls:
    - Press 's' to open Settings panel
    - Press 'q' to quit application
"""

import sys
import os
import traceback

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import our main application
    from main_gesture_app import ComprehensiveHandGestureAnalyzer
    
    def main():
        """Main entry point for the gesture recognition system"""
        print("🚀 Starting Enhanced Hand Gesture Recognition System...")
        print("=" * 60)
        
        try:
            # Create and run the application
            app = ComprehensiveHandGestureAnalyzer()
            app.run()
            
        except KeyboardInterrupt:
            print("\n🛑 Application interrupted by user")
        except Exception as e:
            print(f"❌ Application error: {e}")
            traceback.print_exc()
        finally:
            print("\n👋 Gesture Recognition System closed")
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print("❌ Import Error: Missing required modules")
    print(f"Error details: {e}")
    print("\n📦 Please install required dependencies:")
    print("pip install opencv-python mediapipe numpy pynput")
    print("\nRequired modules:")
    print("- opencv-python (for camera and image processing)")
    print("- mediapipe (for hand landmark detection)")
    print("- numpy (for numerical operations)")
    print("- pynput (for keyboard automation)")
    sys.exit(1)

except Exception as e:
    print(f"❌ Startup Error: {e}")
    traceback.print_exc()
    sys.exit(1)
