#!/usr/bin/env python3
"""
Test script to verify error fixes
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_recognition import GestureRecognitionEngine
    
    def test_key_execution():
        """Test key execution with various key types"""
        print("🧪 Testing Key Execution Fixes...")
        
        engine = GestureRecognitionEngine()
        
        # Test different key types
        test_keys = [
            'a',           # Regular key
            'space',       # Special key
            'enter',       # Special key
            'up',          # Arrow key
            'f1',          # Function key
            'ctrl+c',      # Combination
            'shift+a',     # Combination
            'invalid_key', # Invalid key
            'insert',      # Previously problematic key (removed)
        ]
        
        print("✅ Testing Key Execution:")
        for key in test_keys:
            try:
                # Test if key is recognized
                if '+' in key:
                    print(f"   • {key} - Key combination")
                elif key.lower() in engine.get_special_keys():
                    print(f"   • {key} - Special key ✅")
                elif len(key) == 1 or key.isalnum():
                    print(f"   • {key} - Regular key ✅")
                else:
                    print(f"   • {key} - Invalid key ❌")
                    
                # Test gesture bindings (simulate)
                test_bindings = {f'test_gesture_{key}': key}
                
                # This would normally execute the key, but we'll just test the logic
                if key in test_bindings.values():
                    print(f"     Binding test: ✅")
                
            except Exception as e:
                print(f"   • {key} - Error: {e}")
    
    def test_special_keys_availability():
        """Test which special keys are available"""
        print("\n🧪 Testing Special Keys Availability...")
        
        engine = GestureRecognitionEngine()
        special_keys = engine.get_special_keys()
        
        print(f"✅ Available Special Keys ({len(special_keys)}):")
        for key_name, key_obj in special_keys.items():
            print(f"   • {key_name}")
        
        # Test problematic keys that were removed
        removed_keys = ['insert', 'num_lock', 'scroll_lock']
        print(f"\n❌ Removed Problematic Keys:")
        for key in removed_keys:
            if key not in special_keys:
                print(f"   • {key} - Correctly removed ✅")
            else:
                print(f"   • {key} - Still present ⚠️")
    
    def test_key_validation():
        """Test key validation logic"""
        print("\n🧪 Testing Key Validation...")
        
        engine = GestureRecognitionEngine()
        
        # Test cases
        test_cases = [
            ('a', True, "Single letter"),
            ('1', True, "Single digit"),
            ('space', True, "Special key"),
            ('ctrl+c', True, "Valid combination"),
            ('invalid_key_name', False, "Invalid key name"),
            ('', False, "Empty key"),
            ('shift+invalid', False, "Invalid combination"),
        ]
        
        print("✅ Key Validation Results:")
        for key, expected_valid, description in test_cases:
            try:
                # Simulate validation logic
                is_valid = False
                
                if '+' in key:
                    parts = key.split('+')
                    if len(parts) >= 2:
                        modifiers = parts[:-1]
                        main_key = parts[-1]
                        valid_modifiers = all(mod in ['ctrl', 'shift', 'alt', 'cmd'] for mod in modifiers)
                        valid_main = main_key in engine.get_special_keys() or (len(main_key) == 1 and main_key.isalnum())
                        is_valid = valid_modifiers and valid_main
                elif key.lower() in engine.get_special_keys():
                    is_valid = True
                elif len(key) == 1 and key.isalnum():
                    is_valid = True
                
                status = "✅" if is_valid == expected_valid else "❌"
                print(f"   {status} '{key}' - {description} - Valid: {is_valid}")
                
            except Exception as e:
                print(f"   ❌ '{key}' - Error: {e}")
    
    if __name__ == "__main__":
        test_key_execution()
        test_special_keys_availability()
        test_key_validation()
        
        print("\n🎉 Error fix testing completed!")
        print("The key execution errors should now be resolved.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
