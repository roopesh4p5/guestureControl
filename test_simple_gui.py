#!/usr/bin/env python3
"""
Test the simplified GUI interface
"""

import sys
import os
import tkinter as tk

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_profile_manager import GestureProfileManager
    from gesture_recorder import GestureRecorder, GestureRecordingSession
    from gesture_gui import GestureSettingsGUI
    
    def test_simple_gui():
        """Test the simplified GUI"""
        print("🧪 Testing simplified GUI interface...")
        
        # Create components
        profile_manager = GestureProfileManager()
        recorder = GestureRecorder()
        recording_session = GestureRecordingSession(profile_manager, recorder)
        gui = GestureSettingsGUI(profile_manager, recorder, recording_session)
        
        # Create root window
        root = tk.Tk()
        root.title("Test - Simplified GUI")
        root.geometry("800x600")
        
        gui.root = root
        
        # Open settings window
        gui.open_settings_window()
        
        print("✅ GUI opened successfully!")
        print("📋 Instructions:")
        print("1. Try creating a new profile")
        print("2. Try creating a template profile")
        print("3. Try adding a gesture (name: 'test', key: 'a')")
        print("4. Close the window when done testing")
        
        # Run the GUI
        root.mainloop()
        
        print("✅ GUI test completed!")
    
    if __name__ == "__main__":
        test_simple_gui()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
