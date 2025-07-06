#!/usr/bin/env python3
"""
Test script for both-hand gesture recognition
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_recognition import GestureRecognitionEngine
    
    def test_both_hands_recognition():
        """Test both-hand gesture recognition"""
        print("🧪 Testing Both-Hand Gesture Recognition...")
        
        engine = GestureRecognitionEngine()
        
        # Test data: simulate finger states
        # Left hand: 1 finger up (index finger)
        left_finger_states = [0, 1, 0, 0, 0]  # thumb, index, middle, ring, pinky
        
        # Right hand: 5 fingers up (all fingers)
        right_finger_states = [1, 1, 1, 1, 1]  # all fingers up
        
        # Expected: 6 total fingers (1 + 5)
        
        # Create test custom gestures
        custom_gestures = {
            'six': {
                'pattern': [6, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],  # 6 total, left pattern, right pattern
                'hand_type': 'both',
                'description': 'Number six with both hands'
            },
            'seven': {
                'pattern': [7, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],  # 7 total
                'hand_type': 'both',
                'description': 'Number seven with both hands'
            }
        }
        
        active_gestures = {'six', 'seven'}
        
        # Test recognition
        result = engine.recognize_both_hands_gesture(
            left_finger_states, right_finger_states, custom_gestures, active_gestures
        )
        
        print(f"Left hand fingers: {left_finger_states} (1 finger up)")
        print(f"Right hand fingers: {right_finger_states} (5 fingers up)")
        print(f"Expected total: 6 fingers")
        print(f"Recognition result: {result}")
        
        if result:
            print(f"✅ Recognized: {result['gesture']}")
            print(f"✅ Confidence: {result['confidence']:.2f}")
            print(f"✅ Total fingers: {result.get('total_fingers', 'N/A')}")
        else:
            print("❌ No gesture recognized")
        
        # Test another combination
        print("\n" + "="*50)
        print("Testing 7 fingers (2 left + 5 right)...")
        
        left_finger_states_2 = [0, 1, 1, 0, 0]  # 2 fingers up
        right_finger_states_2 = [1, 1, 1, 1, 1]  # 5 fingers up
        
        result2 = engine.recognize_both_hands_gesture(
            left_finger_states_2, right_finger_states_2, custom_gestures, active_gestures
        )
        
        print(f"Left hand fingers: {left_finger_states_2} (2 fingers up)")
        print(f"Right hand fingers: {right_finger_states_2} (5 fingers up)")
        print(f"Expected total: 7 fingers")
        print(f"Recognition result: {result2}")
        
        if result2:
            print(f"✅ Recognized: {result2['gesture']}")
            print(f"✅ Confidence: {result2['confidence']:.2f}")
            print(f"✅ Total fingers: {result2.get('total_fingers', 'N/A')}")
        else:
            print("❌ No gesture recognized")
    
    def test_pattern_creation():
        """Test how patterns are created for both-hand gestures"""
        print("\n🔍 Testing Pattern Creation...")
        
        # Simulate different finger combinations
        test_cases = [
            ([1, 0, 0, 0, 0], [1, 1, 1, 1, 1], 6),  # 1 + 5 = 6
            ([1, 1, 0, 0, 0], [1, 1, 1, 1, 1], 7),  # 2 + 5 = 7
            ([1, 1, 1, 0, 0], [1, 1, 1, 1, 1], 8),  # 3 + 5 = 8
            ([1, 1, 1, 1, 0], [1, 1, 1, 1, 1], 9),  # 4 + 5 = 9
            ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1], 10), # 5 + 5 = 10
        ]
        
        for left, right, expected_total in test_cases:
            left_pattern = [1 if state > 0.5 else 0 for state in left]
            right_pattern = [1 if state > 0.5 else 0 for state in right]
            total_fingers = sum(left_pattern) + sum(right_pattern)
            combined_pattern = [total_fingers] + left_pattern + right_pattern
            
            print(f"Left: {left} -> Right: {right} -> Total: {total_fingers} (expected: {expected_total})")
            print(f"Combined pattern: {combined_pattern}")
            print()
    
    if __name__ == "__main__":
        test_both_hands_recognition()
        test_pattern_creation()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
