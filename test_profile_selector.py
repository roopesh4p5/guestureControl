#!/usr/bin/env python3
"""
Test script for the simplified profile selector
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
    
    def create_test_profiles():
        """Create some test profiles for testing"""
        print("🧪 Creating test profiles...")
        
        manager = GestureProfileManager()
        
        # Create test profiles
        test_profiles = [
            {
                'name': 'Racing Game',
                'description': 'Profile for racing games',
                'gestures': {
                    'accelerate': {'pattern': [1, 0, 0, 0, 0], 'hand_type': 'single'},
                    'brake': {'pattern': [1, 1, 1, 1, 1], 'hand_type': 'single'},
                    'left': {'pattern': [0, 1, 0, 0, 0], 'hand_type': 'single'},
                    'right': {'pattern': [0, 0, 1, 0, 0], 'hand_type': 'single'}
                },
                'bindings': {
                    'accelerate': 'w',
                    'brake': 's', 
                    'left': 'a',
                    'right': 'd'
                }
            },
            {
                'name': 'Numbers',
                'description': 'Number recognition 1-10',
                'gestures': {
                    'one': {'pattern': [0, 1, 0, 0, 0], 'hand_type': 'single'},
                    'two': {'pattern': [0, 1, 1, 0, 0], 'hand_type': 'single'},
                    'three': {'pattern': [0, 1, 1, 1, 0], 'hand_type': 'single'},
                    'six': {'pattern': [6, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1], 'hand_type': 'both'},
                    'ten': {'pattern': [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'hand_type': 'both'}
                },
                'bindings': {
                    'one': '1',
                    'two': '2',
                    'three': '3',
                    'six': '6',
                    'ten': '0'
                }
            },
            {
                'name': 'Video Player',
                'description': 'Media player controls',
                'gestures': {
                    'play_pause': {'pattern': [0, 1, 1, 0, 0], 'hand_type': 'single'},
                    'volume_up': {'pattern': [1, 0, 0, 0, 0], 'hand_type': 'single'},
                    'volume_down': {'pattern': [1, 0, 0, 0, 1], 'hand_type': 'single'}
                },
                'bindings': {
                    'play_pause': 'space',
                    'volume_up': 'up',
                    'volume_down': 'down'
                }
            }
        ]
        
        for profile_info in test_profiles:
            # Create profile
            if manager.create_profile(profile_info['name'], profile_info['description']):
                # Load and populate with test data
                profile_data = manager.load_profile(profile_info['name'])
                if profile_data:
                    profile_data['gestures'] = profile_info['gestures']
                    profile_data['bindings'] = profile_info['bindings']
                    profile_data['active_gestures'] = list(profile_info['gestures'].keys())
                    manager.save_profile(profile_info['name'], profile_data)
                    print(f"✅ Created test profile: {profile_info['name']}")
        
        print(f"📁 Created {len(test_profiles)} test profiles")
        return manager
    
    def test_profile_selector_gui():
        """Test the profile selector GUI"""
        print("🧪 Testing Profile Selector GUI...")
        
        # Create test profiles
        manager = create_test_profiles()
        
        # Create GUI components
        recorder = GestureRecorder()
        recording_session = GestureRecordingSession(manager, recorder)
        gui = GestureSettingsGUI(manager, recorder, recording_session)
        
        # Create root window
        root = tk.Tk()
        root.title("Test - Profile Selector")
        root.geometry("300x200")
        
        gui.root = root
        
        # Create test button to open profile selector
        test_button = tk.Button(root, text="Press 'p' to Open Profile Selector\n(or click this button)",
                               command=gui.open_profile_selector,
                               font=('Arial', 12))
        test_button.pack(expand=True)
        
        # Bind 'p' key
        root.bind('<KeyPress-p>', lambda e: gui.open_profile_selector())
        root.focus_set()
        
        print("✅ GUI opened successfully!")
        print("📋 Instructions:")
        print("1. Press 'p' key or click the button to open Profile Selector")
        print("2. Try loading different profiles")
        print("3. Try deleting a profile")
        print("4. Check loading speed and responsiveness")
        print("5. Close windows when done testing")
        
        # Run the GUI
        root.mainloop()
        
        print("✅ Profile selector test completed!")
    
    def test_profile_loading_speed():
        """Test profile loading speed"""
        print("\n🧪 Testing Profile Loading Speed...")
        
        import time
        
        manager = create_test_profiles()
        
        # Test basic info loading
        start_time = time.time()
        basic_info = manager.get_all_profiles_basic_info()
        basic_time = time.time() - start_time
        
        print(f"⚡ Basic info loading: {basic_time:.4f} seconds")
        print(f"📊 Profiles found: {len(basic_info)}")
        
        for name, info in basic_info.items():
            print(f"   • {name}: {info.get('gesture_count', 0)} gestures")
        
        # Test full profile loading
        start_time = time.time()
        for profile_name in manager.get_profile_names():
            manager.load_profile(profile_name)
        full_time = time.time() - start_time
        
        print(f"⚡ Full profile loading: {full_time:.4f} seconds")
        print(f"📈 Speed improvement: {(full_time/basic_time):.1f}x slower for full load")
    
    if __name__ == "__main__":
        test_profile_loading_speed()
        test_profile_selector_gui()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
