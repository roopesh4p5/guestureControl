#!/usr/bin/env python3
"""
Gesture Recorder
Handles gesture recording with countdown timer and data capture
"""

import threading
import time
from typing import List, Callable, Optional


class GestureRecorder:
    """Handles gesture recording with timer-based capture"""
    
    def __init__(self):
        self.recording_gesture = False
        self.recording_data = []
        self.recording_name = ""
        self.recording_key_binding = ""
        self.recording_hand_type = "single"
        self.recording_countdown = 0
        self.recording_timer = None
        
        # Callbacks for UI updates
        self.status_callback = None
        self.completion_callback = None
    
    def set_status_callback(self, callback: Callable[[str, str], None]):
        """Set callback for status updates (message, color)"""
        self.status_callback = callback
    
    def set_completion_callback(self, callback: Callable[[str, dict], None]):
        """Set callback for recording completion (gesture_name, gesture_data)"""
        self.completion_callback = callback
    
    def start_recording_with_timer(self, gesture_name: str, key_binding: str, hand_type: str = 'single'):
        """Start recording with countdown timer"""
        self.recording_name = gesture_name
        self.recording_key_binding = key_binding
        self.recording_hand_type = hand_type
        self.recording_countdown = 3
        self.recording_data = []
        
        print(f"🔴 Starting recording for '{gesture_name}' in...")
        if self.status_callback:
            self.status_callback("Get ready to record...", 'orange')
        
        self.countdown_timer()
    
    def countdown_timer(self):
        """Countdown timer for recording"""
        if self.recording_countdown > 0:
            message = f"Recording in {self.recording_countdown}..."
            print(f"⏰ {self.recording_countdown}...")
            
            if self.status_callback:
                self.status_callback(message, 'orange')
            
            self.recording_countdown -= 1
            # Schedule next countdown
            self.recording_timer = threading.Timer(1.0, self.countdown_timer)
            self.recording_timer.start()
        else:
            message = "🔴 Recording NOW! Hold your gesture steady..."
            print(message)
            
            if self.status_callback:
                self.status_callback(message, 'red')
            
            self.recording_gesture = True
            # Stop recording after 3 seconds
            self.recording_timer = threading.Timer(3.0, self.stop_recording_auto)
            self.recording_timer.start()
    
    def stop_recording_auto(self):
        """Automatically stop recording after timer"""
        if self.recording_gesture:
            self.recording_gesture = False
            self.finish_recording()
    
    def stop_recording_manual(self):
        """Manually stop recording"""
        if self.recording_timer:
            self.recording_timer.cancel()
        
        if self.recording_gesture:
            self.recording_gesture = False
            self.finish_recording()
    
    def add_recording_data(self, finger_states: List[float]):
        """Add finger state data during recording"""
        if self.recording_gesture:
            self.recording_data.append(finger_states.copy())
    
    def finish_recording(self):
        """Finish recording and save the gesture"""
        if not self.recording_data:
            message = "❌ No gesture data captured!"
            print(message)
            if self.status_callback:
                self.status_callback(message, 'red')
            return False

        # Average the recorded patterns for stability
        avg_pattern = []
        for i in range(5):  # 5 fingers
            finger_values = [pattern[i] for pattern in self.recording_data if len(pattern) > i]
            if finger_values:
                avg_value = sum(finger_values) / len(finger_values)
                avg_pattern.append(1 if avg_value > 0.5 else -1 if avg_value < -0.5 else 0)
            else:
                avg_pattern.append(0)

        # Create gesture data
        gesture_data = {
            'pattern': avg_pattern,
            'hand_type': self.recording_hand_type,
            'description': f"Custom gesture: {self.recording_name}",
            'recorded_samples': len(self.recording_data),
            'key_binding': self.recording_key_binding
        }

        success_message = f"✅ Gesture '{self.recording_name}' saved successfully!"
        print(success_message)
        print(f"🔗 Key binding: {self.recording_key_binding}")
        print(f"📊 Pattern: {avg_pattern}")
        
        if self.status_callback:
            self.status_callback(success_message, 'green')
        
        if self.completion_callback:
            self.completion_callback(self.recording_name, gesture_data)

        return True
    
    def cancel_recording(self):
        """Cancel current recording"""
        if self.recording_timer:
            self.recording_timer.cancel()
        
        self.recording_gesture = False
        self.recording_data = []
        
        message = "❌ Recording cancelled"
        print(message)
        if self.status_callback:
            self.status_callback(message, 'orange')
    
    def is_recording(self):
        """Check if currently recording"""
        return self.recording_gesture
    
    def is_countdown_active(self):
        """Check if countdown is active"""
        return self.recording_countdown > 0 or (self.recording_timer and self.recording_timer.is_alive())
    
    def get_recording_status(self):
        """Get current recording status"""
        if self.recording_gesture:
            return {
                'status': 'recording',
                'message': 'Recording gesture...',
                'samples_captured': len(self.recording_data)
            }
        elif self.recording_countdown > 0:
            return {
                'status': 'countdown',
                'message': f'Recording in {self.recording_countdown}...',
                'countdown': self.recording_countdown
            }
        else:
            return {
                'status': 'idle',
                'message': 'Ready to record',
                'samples_captured': 0
            }


class GestureRecordingSession:
    """Manages a complete gesture recording session for a profile"""
    
    def __init__(self, profile_manager, gesture_recorder):
        self.profile_manager = profile_manager
        self.recorder = gesture_recorder
        self.current_profile = None
        self.recorded_gestures = {}
        
        # Set up recorder callbacks
        self.recorder.set_completion_callback(self.on_gesture_recorded)
    
    def start_session(self, profile_name: str):
        """Start a recording session for a profile"""
        profile_data = self.profile_manager.load_profile(profile_name)
        if not profile_data:
            return False
        
        self.current_profile = profile_name
        self.recorded_gestures = {}
        print(f"🎬 Started recording session for profile: {profile_name}")
        return True
    
    def record_gesture(self, gesture_name: str, key_binding: str, hand_type: str = 'single'):
        """Record a single gesture"""
        if not self.current_profile:
            print("❌ No active recording session")
            return False
        
        self.recorder.start_recording_with_timer(gesture_name, key_binding, hand_type)
        return True
    
    def on_gesture_recorded(self, gesture_name: str, gesture_data: dict):
        """Handle completed gesture recording"""
        self.recorded_gestures[gesture_name] = gesture_data
        
        # Save to current profile
        if self.current_profile:
            profile_data = self.profile_manager.get_current_profile_data()
            if profile_data:
                # Add gesture to profile
                profile_data['gestures'][gesture_name] = {
                    'pattern': gesture_data['pattern'],
                    'hand_type': gesture_data['hand_type'],
                    'description': gesture_data['description'],
                    'recorded_samples': gesture_data['recorded_samples']
                }
                
                # Add key binding
                profile_data['bindings'][gesture_name] = gesture_data['key_binding']
                
                # Activate the gesture
                if gesture_name not in profile_data['active_gestures']:
                    profile_data['active_gestures'].append(gesture_name)
                
                # Save profile
                self.profile_manager.save_profile(self.current_profile, profile_data)
                print(f"💾 Saved gesture '{gesture_name}' to profile '{self.current_profile}'")
    
    def end_session(self):
        """End the recording session"""
        if self.current_profile:
            print(f"🏁 Ended recording session for profile: {self.current_profile}")
            print(f"📊 Recorded {len(self.recorded_gestures)} gestures")
            
            self.current_profile = None
            self.recorded_gestures = {}
    
    def get_session_status(self):
        """Get current session status"""
        return {
            'active': self.current_profile is not None,
            'profile': self.current_profile,
            'recorded_count': len(self.recorded_gestures),
            'recorded_gestures': list(self.recorded_gestures.keys()),
            'recording_status': self.recorder.get_recording_status()
        }
