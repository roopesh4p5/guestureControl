#!/usr/bin/env python3
"""
Debug script to test gesture recognition issue
"""

import sys
import os
import json

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_profile_manager import GestureProfileManager
    
    def debug_profile_data():
        """Debug profile data to see what's stored"""
        print("🔍 Debugging Profile Data...")
        
        # Create profile manager
        manager = GestureProfileManager()
        
        # List all profiles
        profiles = manager.get_profile_names()
        print(f"📁 Available profiles: {profiles}")
        
        for profile_name in profiles:
            print(f"\n📋 Profile: {profile_name}")
            
            # Load profile
            profile_data = manager.load_profile(profile_name)
            if profile_data:
                gestures = profile_data.get('gestures', {})
                bindings = profile_data.get('bindings', {})
                active_gestures = profile_data.get('active_gestures', [])
                
                print(f"   Total gestures: {len(gestures)}")
                print(f"   Active gestures: {len(active_gestures)} - {active_gestures}")
                print(f"   Bindings: {bindings}")
                
                # Check each gesture
                for gesture_name, gesture_data in gestures.items():
                    is_active = gesture_name in active_gestures
                    key_binding = bindings.get(gesture_name, "No binding")
                    pattern = gesture_data.get('pattern', [])
                    
                    print(f"     • {gesture_name}: {key_binding} - {'✅ Active' if is_active else '❌ Inactive'} - Pattern: {pattern}")
                
                # Also check the raw file
                print(f"\n📄 Raw file content for {profile_name}:")
                try:
                    filepath = manager.profiles[profile_name]['filepath']
                    with open(filepath, 'r') as f:
                        raw_data = json.load(f)
                    
                    print(f"   File active_gestures: {raw_data.get('active_gestures', [])}")
                    print(f"   File gestures count: {len(raw_data.get('gestures', {}))}")
                    print(f"   File bindings count: {len(raw_data.get('bindings', {}))}")
                    
                except Exception as e:
                    print(f"   Error reading file: {e}")
            else:
                print(f"   ❌ Could not load profile data")
    
    def test_gesture_matching():
        """Test gesture matching logic"""
        print("\n🧪 Testing Gesture Matching...")
        
        from gesture_recognition import GestureRecognitionEngine
        
        engine = GestureRecognitionEngine()
        
        # Create test data
        custom_gestures = {
            'test1': {'pattern': [1, 0, 0, 0, 0], 'hand_type': 'single'},
            'test2': {'pattern': [0, 1, 0, 0, 0], 'hand_type': 'single'},
            'test3': {'pattern': [0, 0, 1, 0, 0], 'hand_type': 'single'}
        }
        
        active_gestures = {'test1', 'test2', 'test3'}
        
        # Test pattern that should match test1
        test_pattern = [1, 0, 0, 0, 0]
        
        result = engine.match_custom_gesture(test_pattern, custom_gestures, active_gestures)
        
        print(f"Test pattern: {test_pattern}")
        print(f"Custom gestures: {list(custom_gestures.keys())}")
        print(f"Active gestures: {list(active_gestures)}")
        print(f"Match result: {result}")
    
    if __name__ == "__main__":
        debug_profile_data()
        test_gesture_matching()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
