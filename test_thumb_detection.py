#!/usr/bin/env python3
"""
Test script to verify thumb detection fix for left vs right hands
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_recognition import GestureRecognitionEngine
    
    def test_thumb_detection():
        """Test thumb detection for both hands"""
        print("🧪 Testing Thumb Detection for Left vs Right Hands...")
        
        engine = GestureRecognitionEngine()
        
        # Simulate landmark data for testing
        # MediaPipe hand landmarks: 0=wrist, 1-4=thumb, 5-8=index, etc.
        
        # Test case 1: Left hand with thumb extended right (should be detected as extended)
        print("\n🤚 Testing LEFT HAND (thumb extended right):")
        left_hand_landmarks = [
            [0.5, 0.5],    # 0: wrist
            [0.45, 0.45],  # 1: thumb CMC
            [0.4, 0.4],    # 2: thumb MCP  
            [0.35, 0.35],  # 3: thumb IP (PIP for thumb)
            [0.3, 0.3],    # 4: thumb tip (extended right - lower x value)
            # ... other fingers (simplified)
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # index
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # middle  
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # ring
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # pinky
        ]
        
        # Analyze left hand thumb
        thumb_result = engine.analyze_finger_state(left_hand_landmarks, 0, "Right")  # MediaPipe "Right" = actual left hand
        print(f"   Result: {thumb_result['description']}")
        print(f"   State: {thumb_result['state']}")
        print(f"   Expected: Extended (Left Hand) with state = 1")
        
        # Test case 2: Right hand with thumb extended left (should be detected as extended)  
        print("\n👋 Testing RIGHT HAND (thumb extended left):")
        right_hand_landmarks = [
            [0.5, 0.5],    # 0: wrist
            [0.55, 0.45],  # 1: thumb CMC
            [0.6, 0.4],    # 2: thumb MCP
            [0.65, 0.35],  # 3: thumb IP (PIP for thumb)
            [0.7, 0.3],    # 4: thumb tip (extended left - higher x value)
            # ... other fingers (simplified)
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # index
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # middle
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # ring
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],  # pinky
        ]
        
        # Analyze right hand thumb
        thumb_result = engine.analyze_finger_state(right_hand_landmarks, 0, "Left")  # MediaPipe "Left" = actual right hand
        print(f"   Result: {thumb_result['description']}")
        print(f"   State: {thumb_result['state']}")
        print(f"   Expected: Extended (Right Hand) with state = 1")
        
        # Test case 3: Left hand with thumb bent inward
        print("\n🤚 Testing LEFT HAND (thumb bent inward):")
        left_hand_bent = [
            [0.5, 0.5],    # 0: wrist
            [0.45, 0.45],  # 1: thumb CMC
            [0.4, 0.4],    # 2: thumb MCP
            [0.35, 0.35],  # 3: thumb IP
            [0.4, 0.3],    # 4: thumb tip (bent inward - higher x value)
            # ... other fingers
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
        ]
        
        thumb_result = engine.analyze_finger_state(left_hand_bent, 0, "Right")
        print(f"   Result: {thumb_result['description']}")
        print(f"   State: {thumb_result['state']}")
        print(f"   Expected: Bent Inward (Left Hand) with state = -1")
        
        # Test case 4: Right hand with thumb bent inward
        print("\n👋 Testing RIGHT HAND (thumb bent inward):")
        right_hand_bent = [
            [0.5, 0.5],    # 0: wrist
            [0.55, 0.45],  # 1: thumb CMC
            [0.6, 0.4],    # 2: thumb MCP
            [0.65, 0.35],  # 3: thumb IP
            [0.6, 0.3],    # 4: thumb tip (bent inward - lower x value)
            # ... other fingers
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
            [0.5, 0.3], [0.5, 0.25], [0.5, 0.2], [0.5, 0.15],
        ]
        
        thumb_result = engine.analyze_finger_state(right_hand_bent, 0, "Left")
        print(f"   Result: {thumb_result['description']}")
        print(f"   State: {thumb_result['state']}")
        print(f"   Expected: Bent Inward (Right Hand) with state = -1")
    
    def test_open_hand_gesture():
        """Test open hand gesture recognition for both hands"""
        print("\n🧪 Testing Open Hand Gesture Recognition...")
        
        engine = GestureRecognitionEngine()
        
        # Test open hand for left hand (all fingers extended)
        print("\n🖐️ Testing LEFT HAND - Open Hand:")
        left_open_landmarks = [
            [0.5, 0.5],    # wrist
            [0.45, 0.45], [0.4, 0.4], [0.35, 0.35], [0.3, 0.3],    # thumb extended right
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # index extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # middle extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # ring extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # pinky extended up
        ]
        
        # Analyze all fingers
        finger_states = []
        for i in range(5):
            finger_result = engine.analyze_finger_state(left_open_landmarks, i, "Right")
            finger_states.append(finger_result['state'])
            print(f"   Finger {i}: {finger_result['description']} (state: {finger_result['state']})")
        
        print(f"   Overall pattern: {finger_states}")
        print(f"   Expected: All fingers should have positive states (extended)")
        
        # Test open hand for right hand
        print("\n🖐️ Testing RIGHT HAND - Open Hand:")
        right_open_landmarks = [
            [0.5, 0.5],    # wrist
            [0.55, 0.45], [0.6, 0.4], [0.65, 0.35], [0.7, 0.3],    # thumb extended left
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # index extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # middle extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # ring extended up
            [0.5, 0.4], [0.5, 0.3], [0.5, 0.2], [0.5, 0.1],        # pinky extended up
        ]
        
        finger_states = []
        for i in range(5):
            finger_result = engine.analyze_finger_state(right_open_landmarks, i, "Left")
            finger_states.append(finger_result['state'])
            print(f"   Finger {i}: {finger_result['description']} (state: {finger_result['state']})")
        
        print(f"   Overall pattern: {finger_states}")
        print(f"   Expected: All fingers should have positive states (extended)")
    
    def explain_mediapipe_hand_labels():
        """Explain MediaPipe hand labeling"""
        print("\n📚 MediaPipe Hand Labeling Explanation:")
        print("=" * 50)
        print("MediaPipe uses camera perspective (mirrored view):")
        print("• MediaPipe 'Left' hand = Your RIGHT hand in real life")
        print("• MediaPipe 'Right' hand = Your LEFT hand in real life")
        print("")
        print("Thumb extension directions:")
        print("• Left hand (real): Thumb extends RIGHT (positive X)")
        print("• Right hand (real): Thumb extends LEFT (negative X)")
        print("")
        print("The fix accounts for this mirroring in thumb detection.")
    
    if __name__ == "__main__":
        explain_mediapipe_hand_labels()
        test_thumb_detection()
        test_open_hand_gesture()
        
        print("\n🎉 Thumb detection testing completed!")
        print("Both hands should now correctly detect 'open' gesture when thumb is properly extended.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available")
