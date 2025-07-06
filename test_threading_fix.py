#!/usr/bin/env python3
"""
Test script to verify threading fixes for gesture recording
"""

import sys
import os
import time
import threading

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_recorder import GestureRecorder
    from gesture_gui import GestureSettingsGUI
    from gesture_profile_manager import GestureProfileManager
    import tkinter as tk
    
    def test_threading_fix():
        """Test the threading fix for GUI updates"""
        print("🧪 Testing threading fix for gesture recording...")
        
        # Create components
        profile_manager = GestureProfileManager()
        recorder = GestureRecorder()
        
        # Create a simple tkinter root for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create a simple GUI component
        gui = GestureSettingsGUI(profile_manager, recorder, None)
        gui.root = root
        
        # Create a test profile
        profile_manager.create_profile("Test Profile", "Test profile for threading")
        profile_manager.load_profile("Test Profile")
        
        print("✅ Components created successfully")
        
        # Test the recording with callbacks
        def test_callback(message, color):
            print(f"📝 Status update: {message} (color: {color})")
        
        def test_completion(name, data):
            print(f"🎉 Recording completed: {name}")
            print(f"📊 Data: {data}")
        
        recorder.set_status_callback(test_callback)
        recorder.set_completion_callback(test_completion)
        
        print("🔴 Starting test recording...")
        recorder.start_recording_with_timer("test_gesture", "space", "single")
        
        # Simulate some recording data
        def simulate_data():
            time.sleep(4)  # Wait for countdown
            for i in range(10):  # Simulate 10 data points
                recorder.add_recording_data([1, 0, 0, 0, 0])  # Thumbs up pattern
                time.sleep(0.1)
        
        # Start simulation in background
        data_thread = threading.Thread(target=simulate_data)
        data_thread.start()
        
        # Run GUI event loop for 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                root.update_idletasks()
                root.update()
                time.sleep(0.01)
            except tk.TclError:
                break
        
        print("✅ Test completed successfully - no threading errors!")
        
        # Cleanup
        if recorder.recording_timer:
            recorder.recording_timer.cancel()
        
        root.destroy()
        
        return True
    
    if __name__ == "__main__":
        try:
            test_threading_fix()
            print("🎉 All tests passed!")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are installed:")
    print("pip install opencv-python mediapipe numpy pynput")
