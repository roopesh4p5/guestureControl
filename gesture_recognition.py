#!/usr/bin/env python3
"""
Gesture Recognition Engine
Handles hand analysis, gesture recognition, and pattern matching
"""

import math
import time
import threading
from collections import deque
from typing import Dict, List, Tuple, Optional

try:
    import pynput
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("⚠️  pynput not available. Install with: pip install pynput")


class GestureRecognitionEngine:
    """Core gesture recognition and analysis engine"""
    
    def __init__(self):
        # Finger landmark indices
        self.finger_tips = [4, 8, 12, 16, 20]
        self.finger_pips = [3, 6, 10, 14, 18]
        self.finger_mcps = [2, 5, 9, 13, 17]
        
        # Gesture history for stability
        self.left_gesture_history = deque(maxlen=5)
        self.right_gesture_history = deque(maxlen=5)
        
        # Keyboard controller
        if PYNPUT_AVAILABLE:
            self.keyboard_controller = pynput.keyboard.Controller()
        else:
            self.keyboard_controller = None
        
        # Known gesture patterns
        self.gesture_patterns = {
            'fist': {'fingers': [0, 0, 0, 0, 0], 'description': 'Closed fist'},
            'open': {'fingers': [1, 1, 1, 1, 1], 'description': 'Open hand'},
            'thumbs_up': {'fingers': [1, 0, 0, 0, 0], 'description': 'Thumbs up'},
            'thumbs_down': {'fingers': [-1, 0, 0, 0, 0], 'description': 'Thumbs down'},
            'index_point': {'fingers': [0, 1, 0, 0, 0], 'description': 'Index pointing'},
            'peace': {'fingers': [0, 1, 1, 0, 0], 'description': 'Peace sign'},
            'rock': {'fingers': [0, 1, 0, 0, 1], 'description': 'Rock on'},
            'ok': {'fingers': [0, 0, 1, 1, 1], 'description': 'OK sign'},
            'three': {'fingers': [0, 1, 1, 1, 0], 'description': 'Three fingers'},
            'four': {'fingers': [0, 1, 1, 1, 1], 'description': 'Four fingers'},
            'gun': {'fingers': [1, 1, 0, 0, 0], 'description': 'Gun gesture'},
            'call_me': {'fingers': [1, 0, 0, 0, 1], 'description': 'Call me'},
            'middle_finger': {'fingers': [0, 0, 1, 0, 0], 'description': 'Middle finger'},
            'spock': {'fingers': [1, 1, 1, 0, 0], 'description': 'Vulcan salute'},
            'love': {'fingers': [0, 1, 0, 1, 1], 'description': 'I love you'},
        }
    
    def calculate_distance(self, point1, point2):
        """Calculate distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def calculate_angle(self, point1, point2, point3):
        """Calculate angle between three points"""
        a = math.sqrt((point2[0] - point3[0])**2 + (point2[1] - point3[1])**2)
        b = math.sqrt((point1[0] - point3[0])**2 + (point1[1] - point3[1])**2)
        c = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        
        try:
            angle = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
            return math.degrees(angle)
        except:
            return 0
    
    def calculate_hand_rotation(self, landmarks):
        """Calculate hand rotation using multiple reference points"""
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        
        dx = middle_mcp[0] - wrist[0]
        dy = middle_mcp[1] - wrist[1]
        primary_angle = math.degrees(math.atan2(dy, dx))
        
        index_mcp = landmarks[5]
        dx2 = index_mcp[0] - wrist[0]
        dy2 = index_mcp[1] - wrist[1]
        secondary_angle = math.degrees(math.atan2(dy2, dx2))
        
        avg_angle = (primary_angle + secondary_angle) / 2
        
        if avg_angle < 0:
            avg_angle += 360
        
        return avg_angle
    
    def analyze_finger_state(self, landmarks, finger_idx):
        """Analyze individual finger state with detailed information"""
        tip_idx = self.finger_tips[finger_idx]
        pip_idx = self.finger_pips[finger_idx]
        mcp_idx = self.finger_mcps[finger_idx]
        
        tip = landmarks[tip_idx]
        pip = landmarks[pip_idx]
        mcp = landmarks[mcp_idx]
        wrist = landmarks[0]
        
        tip_to_wrist = self.calculate_distance(tip, wrist)
        pip_to_wrist = self.calculate_distance(pip, wrist)
        mcp_to_wrist = self.calculate_distance(mcp, wrist)
        
        finger_angle = self.calculate_angle(mcp, pip, tip)
        
        if finger_idx == 0:  # Thumb special case
            if tip[0] > pip[0]:
                state = 1
                description = "Extended Right"
            elif tip[0] < pip[0]:
                state = -1
                description = "Extended Left"
            else:
                state = 0
                description = "Neutral"
        else:
            if tip[1] < pip[1]:
                if tip_to_wrist > pip_to_wrist:
                    state = 1
                    description = "Fully Extended"
                else:
                    state = 0.5
                    description = "Partially Extended"
            else:
                if tip_to_wrist < mcp_to_wrist:
                    state = 0
                    description = "Fully Bent"
                else:
                    state = -0.5
                    description = "Partially Bent"
        
        return {
            'state': state,
            'description': description,
            'angle': finger_angle,
            'tip_distance': tip_to_wrist,
            'pip_distance': pip_to_wrist,
            'mcp_distance': mcp_to_wrist
        }
    
    def analyze_finger_spacing(self, landmarks):
        """Analyze spacing between fingers"""
        spacings = []
        finger_names = ['Thumb-Index', 'Index-Middle', 'Middle-Ring', 'Ring-Pinky']
        
        for i in range(4):
            tip1 = landmarks[self.finger_tips[i]]
            tip2 = landmarks[self.finger_tips[i + 1]]
            distance = self.calculate_distance(tip1, tip2)
            
            normalized_spacing = min(distance / 0.3, 1.0)
            
            spacings.append({
                'name': finger_names[i],
                'distance': distance,
                'normalized': normalized_spacing,
                'description': 'Wide' if normalized_spacing > 0.7 else 'Normal' if normalized_spacing > 0.3 else 'Close'
            })
        
        return spacings
    
    def recognize_gesture(self, finger_states, custom_gestures=None, active_gestures=None, hand_type='single'):
        """Recognize complex gestures from finger states"""
        pattern = [1 if state > 0.5 else -1 if state < -0.5 else 0 for state in finger_states]

        # Check against known patterns first
        best_match = None
        best_score = 0

        for gesture_name, gesture_info in self.gesture_patterns.items():
            score = 0
            for i, expected in enumerate(gesture_info['fingers']):
                if pattern[i] == expected:
                    score += 1
                elif abs(pattern[i] - expected) <= 1:
                    score += 0.5

            if score > best_score:
                best_score = score
                best_match = gesture_name

        # Check against custom gestures
        if custom_gestures and active_gestures:
            custom_match = self.match_custom_gesture(pattern, custom_gestures, active_gestures, hand_type)
            if custom_match and custom_match['confidence'] > best_score / 5.0:
                return custom_match

        confidence = best_score / 5.0

        return {
            'gesture': best_match,
            'confidence': confidence,
            'pattern': pattern,
            'description': self.gesture_patterns[best_match]['description'] if best_match else 'Unknown',
            'is_custom': False
        }
    
    def match_custom_gesture(self, pattern, custom_gestures, active_gestures, hand_type='single'):
        """Match against custom recorded gestures"""
        best_match = None
        best_score = 0

        for gesture_name, gesture_data in custom_gestures.items():
            if gesture_name not in active_gestures:
                continue

            if gesture_data.get('hand_type', 'single') != hand_type:
                continue

            stored_pattern = gesture_data.get('pattern', [])
            if len(stored_pattern) != len(pattern):
                continue

            score = 0
            for i, (expected, actual) in enumerate(zip(stored_pattern, pattern)):
                if expected == actual:
                    score += 1
                elif abs(expected - actual) <= 1:
                    score += 0.5

            confidence = score / len(pattern)
            if confidence > best_score and confidence > 0.7:
                best_score = confidence
                best_match = gesture_name

        if best_match:
            return {
                'gesture': best_match,
                'confidence': best_score,
                'pattern': pattern,
                'description': custom_gestures[best_match].get('description', 'Custom gesture'),
                'is_custom': True
            }

        return None
    
    def execute_gesture_action(self, gesture_name, gesture_bindings):
        """Execute keyboard action for recognized gesture"""
        if not self.keyboard_controller or not PYNPUT_AVAILABLE:
            return

        if gesture_name in gesture_bindings:
            key_binding = gesture_bindings[gesture_name]
            try:
                if key_binding.lower() in ['space', 'enter', 'tab', 'esc', 'backspace']:
                    special_keys = {
                        'space': pynput.keyboard.Key.space,
                        'enter': pynput.keyboard.Key.enter,
                        'tab': pynput.keyboard.Key.tab,
                        'esc': pynput.keyboard.Key.esc,
                        'backspace': pynput.keyboard.Key.backspace
                    }
                    self.keyboard_controller.press(special_keys[key_binding.lower()])
                    self.keyboard_controller.release(special_keys[key_binding.lower()])
                else:
                    self.keyboard_controller.press(key_binding)
                    self.keyboard_controller.release(key_binding)

                print(f"🎮 Executed: {gesture_name} -> {key_binding}")
            except Exception as e:
                print(f"❌ Error executing gesture action: {e}")
    
    def analyze_hand(self, landmarks, hand_label, custom_gestures=None, active_gestures=None, gesture_bindings=None):
        """Analyze a single hand and return comprehensive data"""
        finger_data = []
        
        # Analyze each finger
        for i in range(5):
            finger_info = self.analyze_finger_state(landmarks, i)
            finger_data.append(finger_info)
        
        # Calculate hand rotation
        rotation = self.calculate_hand_rotation(landmarks)
        
        # Analyze finger spacing
        spacing = self.analyze_finger_spacing(landmarks)
        
        # Recognize gesture
        finger_states = [f['state'] for f in finger_data]
        gesture = self.recognize_gesture(finger_states, custom_gestures, active_gestures)
        
        # Execute gesture action if recognized
        if gesture['is_custom'] and gesture['confidence'] > 0.8 and gesture_bindings:
            self.execute_gesture_action(gesture['gesture'], gesture_bindings)
        
        return {
            'hand_label': hand_label,
            'fingers': finger_data,
            'rotation': rotation,
            'spacing': spacing,
            'gesture': gesture,
            'landmarks': landmarks
        }
