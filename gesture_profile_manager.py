#!/usr/bin/env python3
"""
Gesture Profile Manager
Handles creation, loading, saving, and management of gesture profiles
"""

import json
import os
import time
from typing import Dict, List, Optional


class GestureProfileManager:
    """Manages gesture profiles and collections"""
    
    def __init__(self):
        self.profiles_dir = "gesture_profiles"
        self.current_profile = None
        self.profiles = {}
        self.ensure_profiles_directory()
        self.load_all_profiles()
    
    def ensure_profiles_directory(self):
        """Create profiles directory if it doesn't exist"""
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            print(f"📁 Created profiles directory: {self.profiles_dir}")
    
    def create_profile(self, name: str, description: str = ""):
        """Create a new gesture profile"""
        profile = {
            'name': name,
            'description': description,
            'gestures': {},
            'bindings': {},
            'active_gestures': [],
            'created_at': time.time(),
            'modified_at': time.time()
        }
        
        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.profiles_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(profile, f, indent=2)
            
            self.profiles[name] = {
                'data': profile,
                'filepath': filepath
            }
            
            print(f"✅ Created profile: {name}")
            return True
        except Exception as e:
            print(f"❌ Error creating profile: {e}")
            return False
    
    def load_profile(self, name: str):
        """Load a specific profile and clear any previous profile data"""
        if name in self.profiles:
            try:
                # Clear current profile first to avoid mixing data
                self.current_profile = None

                # Load fresh data from file
                with open(self.profiles[name]['filepath'], 'r') as f:
                    profile_data = json.load(f)

                # Update cache with fresh data
                self.profiles[name]['data'] = profile_data

                # Set as current profile only after successful load
                self.current_profile = name

                print(f"✅ Loaded profile: {name}")
                print(f"📊 Profile contains {len(profile_data.get('gestures', {}))} gestures")

                return profile_data
            except Exception as e:
                print(f"❌ Error loading profile: {e}")
                self.current_profile = None
                return None
        return None
    
    def save_profile(self, name: str, profile_data: dict):
        """Save profile data"""
        if name in self.profiles:
            try:
                profile_data['modified_at'] = time.time()
                
                with open(self.profiles[name]['filepath'], 'w') as f:
                    json.dump(profile_data, f, indent=2)
                
                self.profiles[name]['data'] = profile_data
                print(f"✅ Saved profile: {name}")
                return True
            except Exception as e:
                print(f"❌ Error saving profile: {e}")
                return False
        return False
    
    def load_all_profiles(self):
        """Load all available profiles with basic info for fast access"""
        self.profiles = {}

        if not os.path.exists(self.profiles_dir):
            return

        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        profile_data = json.load(f)

                    profile_name = profile_data.get('name', filename[:-5])

                    # Store full data and basic info for quick access
                    self.profiles[profile_name] = {
                        'data': profile_data,
                        'filepath': filepath,
                        'basic_info': {
                            'name': profile_name,
                            'gesture_count': len(profile_data.get('gestures', {})),
                            'description': profile_data.get('description', ''),
                            'created_at': profile_data.get('created_at', 0),
                            'modified_at': profile_data.get('modified_at', 0)
                        }
                    }
                except Exception as e:
                    print(f"⚠️  Error loading profile {filename}: {e}")

        print(f"📁 Loaded {len(self.profiles)} profiles")
    
    def delete_profile(self, name: str):
        """Delete a profile"""
        if name in self.profiles:
            try:
                os.remove(self.profiles[name]['filepath'])
                del self.profiles[name]
                
                if self.current_profile == name:
                    self.current_profile = None
                
                print(f"🗑️  Deleted profile: {name}")
                return True
            except Exception as e:
                print(f"❌ Error deleting profile: {e}")
                return False
        return False
    
    def get_profile_names(self):
        """Get list of all profile names"""
        return list(self.profiles.keys())
    
    def get_current_profile_data(self, force_reload=False):
        """Get current profile data"""
        if self.current_profile and self.current_profile in self.profiles:
            # Force reload from file to ensure we have the latest data
            if force_reload:
                try:
                    with open(self.profiles[self.current_profile]['filepath'], 'r') as f:
                        fresh_data = json.load(f)
                    self.profiles[self.current_profile]['data'] = fresh_data
                    return fresh_data
                except Exception as e:
                    print(f"Warning: Could not reload profile data: {e}")

            return self.profiles[self.current_profile]['data']
        return None

    def reload_current_profile_from_disk(self):
        """Force reload current profile from disk to ensure fresh data"""
        if self.current_profile:
            print(f"🔄 Reloading profile '{self.current_profile}' from disk...")
            return self.get_current_profile_data(force_reload=True)
        return None
    
    def create_template_profile(self, template_name: str):
        """Create template profiles with predefined gesture structures"""
        templates = {
            "Racing Game": {
                "description": "Profile for racing games with directional controls",
                "template_gestures": {
                    "accelerate": {"key": "up", "description": "Accelerate"},
                    "brake": {"key": "down", "description": "Brake/Reverse"},
                    "turn_left": {"key": "left", "description": "Turn Left"},
                    "turn_right": {"key": "right", "description": "Turn Right"},
                    "nitro": {"key": "space", "description": "Nitro Boost"},
                    "horn": {"key": "h", "description": "Horn"}
                }
            },
            "Video Player": {
                "description": "Profile for video player controls",
                "template_gestures": {
                    "play_pause": {"key": "space", "description": "Play/Pause"},
                    "volume_up": {"key": "up", "description": "Volume Up"},
                    "volume_down": {"key": "down", "description": "Volume Down"},
                    "seek_forward": {"key": "right", "description": "Seek Forward"},
                    "seek_backward": {"key": "left", "description": "Seek Backward"},
                    "fullscreen": {"key": "f", "description": "Toggle Fullscreen"}
                }
            },
            "General Gaming": {
                "description": "General gaming profile with common controls",
                "template_gestures": {
                    "jump": {"key": "space", "description": "Jump"},
                    "move_forward": {"key": "w", "description": "Move Forward"},
                    "move_backward": {"key": "s", "description": "Move Backward"},
                    "move_left": {"key": "a", "description": "Move Left"},
                    "move_right": {"key": "d", "description": "Move Right"},
                    "action": {"key": "e", "description": "Action/Interact"}
                }
            }
        }
        
        if template_name not in templates:
            return False
        
        template = templates[template_name]
        
        # Create the profile
        if self.create_profile(template_name, template["description"]):
            # Add template gesture placeholders
            profile_data = self.get_current_profile_data()
            if profile_data:
                profile_data['template_gestures'] = template["template_gestures"]
                self.save_profile(template_name, profile_data)
            return True
        
        return False
    
    def get_template_gestures(self, profile_name: str):
        """Get template gestures for a profile"""
        if profile_name in self.profiles:
            profile_data = self.profiles[profile_name]['data']
            return profile_data.get('template_gestures', {})
        return {}

    def get_profile_basic_info(self, profile_name: str):
        """Get basic profile info without loading full data"""
        if profile_name in self.profiles:
            return self.profiles[profile_name].get('basic_info', {})
        return {}

    def get_all_profiles_basic_info(self):
        """Get basic info for all profiles"""
        basic_info = {}
        for profile_name, profile_info in self.profiles.items():
            basic_info[profile_name] = profile_info.get('basic_info', {})
        return basic_info

    def clear_current_profile(self):
        """Clear current profile to ensure clean state"""
        self.current_profile = None
        print("🧹 Cleared current profile")

    def get_profile_gestures_only(self, profile_name: str):
        """Get only the gestures for a specific profile (for debugging)"""
        if profile_name in self.profiles:
            profile_data = self.profiles[profile_name]['data']
            gestures = profile_data.get('gestures', {})
            bindings = profile_data.get('bindings', {})
            active = profile_data.get('active_gestures', [])

            print(f"🔍 Profile '{profile_name}' debug info:")
            print(f"   Gestures: {list(gestures.keys())}")
            print(f"   Bindings: {bindings}")
            print(f"   Active: {active}")

            return {
                'gestures': gestures,
                'bindings': bindings,
                'active_gestures': active
            }
        return None
