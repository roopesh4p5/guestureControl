#!/usr/bin/env python3
"""
Main Gesture Recognition Application
Integrates all components for comprehensive hand gesture recognition
"""

import cv2
import mediapipe as mp
import numpy as np
import traceback
from collections import deque

# Import our custom modules
from gesture_profile_manager import GestureProfileManager
from gesture_recognition import GestureRecognitionEngine
from gesture_recorder import GestureRecorder, GestureRecordingSession
from gesture_gui import GestureSettingsGUI


class ComprehensiveHandGestureAnalyzer:
    """Main application class that integrates all gesture recognition components"""
    
    def __init__(self):
        print("🤖 Enhanced Comprehensive Hand Gesture Analyzer with Profile Collections")
        
        # Initialize core components
        self.profile_manager = GestureProfileManager()
        self.recognition_engine = GestureRecognitionEngine()
        self.gesture_recorder = GestureRecorder()
        self.recording_session = GestureRecordingSession(self.profile_manager, self.gesture_recorder)
        self.gui = GestureSettingsGUI(self.profile_manager, self.gesture_recorder, self.recording_session)
        
        # MediaPipe setup for both hands with better configuration
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
            model_complexity=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Hand data storage
        self.left_hand_data = None
        self.right_hand_data = None
        self.both_hands_gesture_data = None
        
        print("✅ Analyzer initialized with Profile Collections!")
        self.print_controls()
    
    def print_controls(self):
        """Print control information"""
        print("\n🤖 ENHANCED AI GESTURE RECOGNITION FEATURES:")
        print("=" * 60)
        print("📊 ANALYSIS FEATURES:")
        print("   • Individual finger detection (up/down/bent)")
        print("   • Hand rotation angles (360° tracking)")
        print("   • Finger spacing analysis")
        print("   • Distance measurements")
        print("   • Complex gesture recognition")
        print("   • Real-time stability filtering")
        print("   • Timer-based gesture recording")
        print("   • Profile-based gesture collections")
        print("\n🎮 PROFILE SYSTEM:")
        print("   • Create gesture profiles (Racing, Video Control, etc.)")
        print("   • Save/Load gesture collections")
        print("   • Profile-specific key bindings")
        print("   • File-based storage")
        print("\n📱 CONTROLS:")
        print("   • Left hand: Top-left corner")
        print("   • Right hand: Top-right corner")
        print("   • Press 's' to open Settings")
        print("   • Press 'p' to open Profile Selector")
        print("   • Press 'q' to quit")
        print("=" * 60)
    
    def setup_camera(self):
        """Setup camera with optimal settings"""
        print("🔍 Setting up camera...")

        for camera_index in [0, 1, 2]:
            try:
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"✅ Camera found at index {camera_index}")
                        break
                    else:
                        cap.release()
                        continue
                cap.release()
            except Exception as e:
                print(f"⚠️  Camera index {camera_index} failed: {e}")
                continue
        else:
            print("❌ No working camera found!")
            return None

        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception as e:
            print(f"⚠️  Camera configuration warning: {e}")

        return cap
    
    def analyze_hands_for_recording(self, frame):
        """Analyze both hands for recording purposes"""
        if self.gesture_recorder.is_recording():
            # Check if we're recording a both-hand gesture
            if hasattr(self.gesture_recorder, 'recording_hand_type') and self.gesture_recorder.recording_hand_type == 'both':
                # For both-hand recording, we need both hands
                if self.left_hand_data and self.right_hand_data:
                    left_finger_states = [finger['state'] for finger in self.left_hand_data['fingers']]
                    right_finger_states = [finger['state'] for finger in self.right_hand_data['fingers']]

                    # Combine patterns for both-hand recording
                    left_pattern = [1 if state > 0.5 else 0 for state in left_finger_states]
                    right_pattern = [1 if state > 0.5 else 0 for state in right_finger_states]
                    total_fingers = sum(left_pattern) + sum(right_pattern)
                    combined_pattern = [total_fingers] + left_pattern + right_pattern

                    self.gesture_recorder.add_recording_data(combined_pattern)
            else:
                # Single hand recording
                if self.left_hand_data:
                    finger_states = [finger['state'] for finger in self.left_hand_data['fingers']]
                    self.gesture_recorder.add_recording_data(finger_states)
                elif self.right_hand_data:
                    finger_states = [finger['state'] for finger in self.right_hand_data['fingers']]
                    self.gesture_recorder.add_recording_data(finger_states)

    def analyze_both_hands_gesture(self, profile_data, custom_gestures, active_gestures, gesture_bindings):
        """Analyze both hands together for combined gestures"""
        if not self.left_hand_data or not self.right_hand_data:
            return

        left_finger_states = [finger['state'] for finger in self.left_hand_data['fingers']]
        right_finger_states = [finger['state'] for finger in self.right_hand_data['fingers']]

        # Recognize both-hand gesture
        both_hands_gesture = self.recognition_engine.recognize_both_hands_gesture(
            left_finger_states, right_finger_states, custom_gestures, active_gestures
        )

        # Execute if recognized
        if both_hands_gesture and both_hands_gesture['confidence'] > 0.7:
            self.recognition_engine.execute_gesture_action(both_hands_gesture['gesture'], gesture_bindings)

            # Store for display
            self.both_hands_gesture_data = both_hands_gesture
    
    def display_info(self, frame):
        """Display hand information on frame"""
        height, width = frame.shape[:2]
        
        # Display left hand info
        if self.left_hand_data:
            self.draw_hand_info(frame, self.left_hand_data, 10, 30, "LEFT")
        
        # Display right hand info
        if self.right_hand_data:
            self.draw_hand_info(frame, self.right_hand_data, width - 300, 30, "RIGHT")
        
        # Display recording status
        if self.gesture_recorder.is_recording():
            cv2.putText(frame, "🔴 RECORDING", (width//2 - 100, height - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif self.gesture_recorder.is_countdown_active():
            status = self.gesture_recorder.get_recording_status()
            if status['status'] == 'countdown':
                cv2.putText(frame, f"⏰ {status['countdown']}", (width//2 - 50, height - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 165, 255), 3)
        
        # Display current profile
        if self.profile_manager.current_profile:
            cv2.putText(frame, f"Profile: {self.profile_manager.current_profile}", 
                       (10, height - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display active gestures count
        profile_data = self.profile_manager.get_current_profile_data()
        if profile_data:
            active_count = len(profile_data.get('active_gestures', []))
            total_count = len(profile_data.get('gestures', {}))
            cv2.putText(frame, f"Gestures: {active_count}/{total_count} active",
                       (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display both-hand gesture info
        if hasattr(self, 'both_hands_gesture_data') and self.both_hands_gesture_data:
            both_gesture = self.both_hands_gesture_data
            cv2.putText(frame, f"Both Hands: {both_gesture['gesture']} ({both_gesture.get('total_fingers', 0)} fingers)",
                       (width//2 - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            cv2.putText(frame, f"Confidence: {both_gesture['confidence']:.2f}",
                       (width//2 - 150, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
    
    def draw_hand_info(self, frame, hand_data, x, y, side):
        """Draw hand information on frame"""
        # Hand label
        cv2.putText(frame, f"{side} HAND", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Gesture info
        gesture = hand_data['gesture']
        gesture_text = f"Gesture: {gesture['gesture'] or 'None'}"
        cv2.putText(frame, gesture_text, (x, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Confidence
        confidence_text = f"Confidence: {gesture['confidence']:.2f}"
        cv2.putText(frame, confidence_text, (x, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Rotation
        rotation_text = f"Rotation: {hand_data['rotation']:.1f}°"
        cv2.putText(frame, rotation_text, (x, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Finger states
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        for i, finger in enumerate(hand_data['fingers']):
            state_text = f"{finger_names[i]}: {finger['description']}"
            cv2.putText(frame, state_text, (x, y + 85 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    def run(self):
        """Main execution loop"""
        # Initialize GUI
        self.gui.initialize_root()
        
        cap = self.setup_camera()
        if not cap:
            return

        print("🎮 Gesture Recognition Active!")
        print("📋 Press 's' to open Settings")
        print("🎯 Press 'p' to open Profile Selector")
        print("🔴 Press 'q' to quit")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process with MediaPipe
                results = self.hands.process(rgb_frame)
                
                # Reset hand data
                self.left_hand_data = None
                self.right_hand_data = None
                self.both_hands_gesture_data = None
                
                if results.multi_hand_landmarks and results.multi_handedness:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        # Get hand label
                        hand_label = handedness.classification[0].label
                        
                        # Extract landmarks
                        landmarks = []
                        for lm in hand_landmarks.landmark:
                            landmarks.append([lm.x, lm.y])
                        
                        # Get current profile data for gesture recognition
                        profile_data = self.profile_manager.get_current_profile_data()
                        if profile_data:
                            custom_gestures = profile_data.get('gestures', {})
                            active_gestures = set(profile_data.get('active_gestures', []))
                            gesture_bindings = profile_data.get('bindings', {})

                            # Debug: Occasionally show what profile is active (every 5 seconds)
                            if hasattr(self, 'debug_timer'):
                                self.debug_timer += 1
                            else:
                                self.debug_timer = 0

                            if self.debug_timer % 150 == 0 and len(active_gestures) > 0:  # Every ~5 seconds at 30fps
                                print(f"🎯 Active Profile: {self.profile_manager.current_profile}")
                                print(f"🎯 Active Gestures: {list(active_gestures)}")
                        else:
                            custom_gestures = {}
                            active_gestures = set()
                            gesture_bindings = {}
                        
                        # Analyze hand
                        hand_data = self.recognition_engine.analyze_hand(
                            landmarks, hand_label, custom_gestures, active_gestures, gesture_bindings
                        )
                        
                        if hand_label == "Left":
                            self.left_hand_data = hand_data
                        else:
                            self.right_hand_data = hand_data
                        
                        # Draw landmarks
                        self.mp_drawing.draw_landmarks(
                            frame, hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style()
                        )
                
                # Analyze hands for recording
                self.analyze_hands_for_recording(frame)

                # Check for both-hand gestures if both hands are detected
                if self.left_hand_data and self.right_hand_data:
                    self.analyze_both_hands_gesture(profile_data, custom_gestures, active_gestures, gesture_bindings)

                # Display information
                self.display_info(frame)
                
                # Show frame
                cv2.imshow('Enhanced Gesture Recognition', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.gui.open_settings_window()
                elif key == ord('p'):
                    self.gui.open_profile_selector()
                
                # Update GUI (with error handling)
                try:
                    self.gui.update_tkinter()
                except Exception as e:
                    # Don't let GUI errors crash the main loop
                    pass

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
        finally:
            # Cleanup
            if self.gesture_recorder.recording_timer:
                self.gesture_recorder.recording_timer.cancel()
            
            cap.release()
            cv2.destroyAllWindows()
            self.gui.cleanup()


# Main execution
if __name__ == "__main__":
    try:
        analyzer = ComprehensiveHandGestureAnalyzer()
        analyzer.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        traceback.print_exc()
