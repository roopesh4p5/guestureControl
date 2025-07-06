#!/usr/bin/env python3
"""
Test script for special key bindings and combinations
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_recognition import GestureRecognitionEngine
    
    def test_special_keys():
        """Test special key recognition"""
        print("🧪 Testing Special Key Support...")
        
        engine = GestureRecognitionEngine()
        
        # Test special keys
        special_keys_to_test = [
            'space', 'enter', 'tab', 'esc', 'backspace', 'delete',
            'up', 'down', 'left', 'right', 'home', 'end',
            'shift', 'ctrl', 'alt', 'f1', 'f5', 'f12'
        ]
        
        print("✅ Supported Special Keys:")
        special_keys_dict = engine.get_special_keys()
        for key in special_keys_to_test:
            if key in special_keys_dict:
                print(f"   • {key}")
            else:
                print(f"   ❌ {key} (not supported)")
        
        print(f"\n📊 Total special keys supported: {len(special_keys_dict)}")
    
    def test_key_combinations():
        """Test key combination parsing"""
        print("\n🧪 Testing Key Combinations...")
        
        engine = GestureRecognitionEngine()
        
        # Test combinations
        test_combinations = [
            'ctrl+c',
            'ctrl+v', 
            'shift+a',
            'alt+tab',
            'ctrl+shift+z',
            'ctrl+f1',
            'shift+enter'
        ]
        
        print("✅ Supported Key Combinations:")
        for combo in test_combinations:
            print(f"   • {combo}")
            
            # Parse the combination
            parts = combo.lower().split('+')
            modifiers = parts[:-1]
            main_key = parts[-1]
            
            print(f"     Modifiers: {modifiers}, Main key: {main_key}")
    
    def test_gesture_bindings():
        """Test gesture binding scenarios"""
        print("\n🧪 Testing Gesture Binding Scenarios...")
        
        # Simulate profile data with multiple gestures using same key
        test_bindings = {
            'gesture1': 'space',
            'gesture2': 'space',  # Same key as gesture1
            'gesture3': 'ctrl+c',
            'gesture4': 'shift+a',
            'gesture5': 'f1'
        }
        
        print("✅ Test Bindings:")
        for gesture, key in test_bindings.items():
            print(f"   • {gesture} → {key}")
        
        # Check for conflicts
        key_conflicts = {}
        for gesture, key in test_bindings.items():
            if key not in key_conflicts:
                key_conflicts[key] = []
            key_conflicts[key].append(gesture)
        
        print("\n🔍 Key Binding Analysis:")
        for key, gestures in key_conflicts.items():
            if len(gestures) > 1:
                print(f"   ⚠️  Key '{key}' used by: {', '.join(gestures)}")
            else:
                print(f"   ✅ Key '{key}' used by: {gestures[0]}")
    
    def test_key_validation():
        """Test key binding validation"""
        print("\n🧪 Testing Key Validation...")
        
        engine = GestureRecognitionEngine()
        special_keys = engine.get_special_keys()
        
        test_keys = [
            'a',           # Regular key
            'space',       # Special key
            'ctrl+c',      # Combination
            'shift+f1',    # Special + combination
            'invalid+key', # Invalid combination
            'f13',         # Unsupported function key
        ]
        
        print("✅ Key Validation Results:")
        for key in test_keys:
            if '+' in key:
                parts = key.lower().split('+')
                main_key = parts[-1]
                modifiers = parts[:-1]
                
                valid_modifiers = all(mod in ['ctrl', 'shift', 'alt', 'cmd'] for mod in modifiers)
                valid_main = main_key in special_keys or len(main_key) == 1
                
                if valid_modifiers and valid_main:
                    print(f"   ✅ '{key}' - Valid combination")
                else:
                    print(f"   ❌ '{key}' - Invalid combination")
            elif key in special_keys:
                print(f"   ✅ '{key}' - Valid special key")
            elif len(key) == 1 and key.isalnum():
                print(f"   ✅ '{key}' - Valid regular key")
            else:
                print(f"   ❌ '{key}' - Invalid key")
    
    if __name__ == "__main__":
        test_special_keys()
        test_key_combinations()
        test_gesture_bindings()
        test_key_validation()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
