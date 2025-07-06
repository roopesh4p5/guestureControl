#!/usr/bin/env python3
"""
Test script to verify profile isolation and proper switching
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_profile_manager import GestureProfileManager
    
    def create_test_profiles_with_different_gestures():
        """Create test profiles with clearly different gestures"""
        print("🧪 Creating test profiles with different gestures...")
        
        manager = GestureProfileManager()
        
        # Profile 1: Numbers (1-5)
        if manager.create_profile("Numbers", "Number gestures 1-5"):
            profile_data = manager.load_profile("Numbers")
            if profile_data:
                profile_data['gestures'] = {
                    'one': {'pattern': [0, 1, 0, 0, 0], 'hand_type': 'single'},
                    'two': {'pattern': [0, 1, 1, 0, 0], 'hand_type': 'single'},
                    'three': {'pattern': [0, 1, 1, 1, 0], 'hand_type': 'single'},
                    'four': {'pattern': [0, 1, 1, 1, 1], 'hand_type': 'single'},
                    'five': {'pattern': [1, 1, 1, 1, 1], 'hand_type': 'single'}
                }
                profile_data['bindings'] = {
                    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'
                }
                profile_data['active_gestures'] = ['one', 'two', 'three', 'four', 'five']
                manager.save_profile("Numbers", profile_data)
                print("✅ Created Numbers profile with gestures: one, two, three, four, five")
        
        # Profile 2: Gaming (WASD)
        if manager.create_profile("Gaming", "Gaming controls WASD"):
            profile_data = manager.load_profile("Gaming")
            if profile_data:
                profile_data['gestures'] = {
                    'forward': {'pattern': [1, 0, 0, 0, 0], 'hand_type': 'single'},
                    'backward': {'pattern': [1, 1, 1, 1, 1], 'hand_type': 'single'},
                    'left': {'pattern': [0, 1, 0, 0, 0], 'hand_type': 'single'},
                    'right': {'pattern': [0, 0, 1, 0, 0], 'hand_type': 'single'}
                }
                profile_data['bindings'] = {
                    'forward': 'w', 'backward': 's', 'left': 'a', 'right': 'd'
                }
                profile_data['active_gestures'] = ['forward', 'backward', 'left', 'right']
                manager.save_profile("Gaming", profile_data)
                print("✅ Created Gaming profile with gestures: forward, backward, left, right")
        
        # Profile 3: Media (play/pause controls)
        if manager.create_profile("Media", "Media player controls"):
            profile_data = manager.load_profile("Media")
            if profile_data:
                profile_data['gestures'] = {
                    'play_pause': {'pattern': [0, 1, 1, 0, 0], 'hand_type': 'single'},
                    'volume_up': {'pattern': [1, 0, 0, 0, 0], 'hand_type': 'single'},
                    'volume_down': {'pattern': [1, 0, 0, 0, 1], 'hand_type': 'single'}
                }
                profile_data['bindings'] = {
                    'play_pause': 'space', 'volume_up': 'up', 'volume_down': 'down'
                }
                profile_data['active_gestures'] = ['play_pause', 'volume_up', 'volume_down']
                manager.save_profile("Media", profile_data)
                print("✅ Created Media profile with gestures: play_pause, volume_up, volume_down")
        
        return manager
    
    def test_profile_switching():
        """Test switching between profiles and verify isolation"""
        print("\n🧪 Testing Profile Switching and Isolation...")
        
        manager = create_test_profiles_with_different_gestures()
        
        # Test switching between profiles
        profiles_to_test = ["Numbers", "Gaming", "Media"]
        
        for profile_name in profiles_to_test:
            print(f"\n🔄 Switching to profile: {profile_name}")
            
            # Clear current profile first
            manager.clear_current_profile()
            
            # Load the profile
            if manager.load_profile(profile_name):
                # Get profile data
                profile_data = manager.get_current_profile_data()
                if profile_data:
                    gestures = profile_data.get('gestures', {})
                    bindings = profile_data.get('bindings', {})
                    active = profile_data.get('active_gestures', [])
                    
                    print(f"   ✅ Loaded successfully")
                    print(f"   📊 Gestures: {list(gestures.keys())}")
                    print(f"   🔗 Bindings: {bindings}")
                    print(f"   ⚡ Active: {active}")
                    
                    # Verify no cross-contamination
                    expected_gestures = {
                        "Numbers": ['one', 'two', 'three', 'four', 'five'],
                        "Gaming": ['forward', 'backward', 'left', 'right'],
                        "Media": ['play_pause', 'volume_up', 'volume_down']
                    }
                    
                    expected = set(expected_gestures[profile_name])
                    actual = set(gestures.keys())
                    
                    if expected == actual:
                        print(f"   ✅ Profile isolation verified - only expected gestures present")
                    else:
                        print(f"   ❌ Profile contamination detected!")
                        print(f"      Expected: {expected}")
                        print(f"      Actual: {actual}")
                        print(f"      Extra: {actual - expected}")
                        print(f"      Missing: {expected - actual}")
                else:
                    print(f"   ❌ Failed to get profile data")
            else:
                print(f"   ❌ Failed to load profile")
    
    def test_profile_data_integrity():
        """Test that profile data remains intact after switching"""
        print("\n🧪 Testing Profile Data Integrity...")
        
        manager = create_test_profiles_with_different_gestures()
        
        # Load each profile multiple times and verify consistency
        for i in range(3):
            print(f"\n🔄 Iteration {i+1}:")
            
            for profile_name in ["Numbers", "Gaming", "Media"]:
                manager.clear_current_profile()
                manager.load_profile(profile_name)
                
                profile_data = manager.get_current_profile_data()
                if profile_data:
                    gesture_count = len(profile_data.get('gestures', {}))
                    binding_count = len(profile_data.get('bindings', {}))
                    active_count = len(profile_data.get('active_gestures', []))
                    
                    print(f"   {profile_name}: {gesture_count} gestures, {binding_count} bindings, {active_count} active")
                    
                    # Verify counts match expected
                    expected_counts = {"Numbers": 5, "Gaming": 4, "Media": 3}
                    if gesture_count == expected_counts[profile_name]:
                        print(f"     ✅ Gesture count correct")
                    else:
                        print(f"     ❌ Gesture count mismatch: expected {expected_counts[profile_name]}, got {gesture_count}")
    
    def test_current_profile_tracking():
        """Test that current profile tracking works correctly"""
        print("\n🧪 Testing Current Profile Tracking...")
        
        manager = create_test_profiles_with_different_gestures()
        
        # Test initial state
        print(f"Initial current profile: {manager.current_profile}")
        
        # Test loading profiles
        for profile_name in ["Numbers", "Gaming", "Media"]:
            manager.load_profile(profile_name)
            current = manager.current_profile
            print(f"After loading {profile_name}: current = {current}")
            
            if current == profile_name:
                print(f"   ✅ Current profile tracking correct")
            else:
                print(f"   ❌ Current profile tracking incorrect")
        
        # Test clearing
        manager.clear_current_profile()
        print(f"After clearing: current = {manager.current_profile}")
        
        if manager.current_profile is None:
            print("   ✅ Profile clearing works correctly")
        else:
            print("   ❌ Profile clearing failed")
    
    if __name__ == "__main__":
        test_profile_switching()
        test_profile_data_integrity()
        test_current_profile_tracking()
        
        print("\n🎉 Profile isolation testing completed!")
        print("Each profile should now contain only its own gestures.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
