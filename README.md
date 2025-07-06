# Enhanced Hand Gesture Recognition System

A comprehensive AI-powered hand gesture recognition system with profile collections, real-time tracking, and keyboard automation.

## 🌟 Features

### 🎮 Profile System
- **Racing Game Profile**: Control racing games with gestures (accelerate, brake, turn left/right, nitro, horn)
- **Video Player Profile**: Control media players (play/pause, volume, seek, fullscreen)
- **General Gaming Profile**: Common gaming controls (jump, movement, actions)
- **Custom Profiles**: Create your own gesture collections

### 🤖 AI-Powered Analysis
- Individual finger detection (up/down/bent states)
- Hand rotation tracking (360° analysis)
- Finger spacing analysis
- Distance measurements between landmarks
- Real-time stability filtering
- Complex gesture pattern matching

### ⏱️ Smart Recording System
- **3-2-1 Countdown Timer** for gesture capture
- 3-second steady recording window
- Automatic pattern averaging for stability
- Visual feedback during recording
- Template gesture quick setup

### 🔧 Advanced Features
- Profile-specific key bindings
- Gesture activation/deactivation
- File-based profile persistence
- Real-time gesture execution
- Comprehensive GUI settings panel

## 📁 Project Structure

```
gesture-recognition/
├── main.py                     # Main entry point
├── main_gesture_app.py         # Core application logic
├── gesture_profile_manager.py  # Profile management system
├── gesture_recognition.py      # Hand analysis and recognition engine
├── gesture_recorder.py         # Recording system with countdown
├── gesture_gui.py             # GUI components and settings panel
├── gesture_profiles/          # Auto-created directory for profiles
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install opencv-python mediapipe numpy pynput
```

### Installation
1. Clone or download all project files
2. Ensure all Python files are in the same directory
3. Run the application:

```bash
python main.py
```

## 🎯 How to Use

### 1. Start the Application
```bash
python main.py
```

### 2. Create a Gesture Profile
1. Press `s` to open Settings
2. Go to "📁 Profile Management" tab
3. Click "📂 Create New Profile" or use a template:
   - 🏎️ Racing Game
   - 🎥 Video Player  
   - 🎮 General Gaming

### 3. Record Gestures
1. Go to "➕ Add Gesture" tab
2. Select your profile
3. For template gestures: Click "🔴 Record" next to any template
4. For custom gestures:
   - Enter gesture name (e.g., "accelerate")
   - Enter key binding (e.g., "up", "space", "w")
   - Choose hand type (Single/Both hands)
   - Click "🔴 Start Recording"

### 4. Recording Process
1. **Get Ready**: Position your hand in camera view
2. **Countdown**: Wait for 3-2-1 countdown
3. **Record**: Hold your gesture steady for 3 seconds
4. **Save**: Gesture automatically saved to profile

### 5. Manage Gestures
1. Go to "📋 Manage Gestures" tab
2. View all gestures in current profile
3. Activate/deactivate gestures
4. Edit key bindings
5. Delete unwanted gestures

## 🎮 Example Usage Scenarios

### Racing Game Setup
1. Create "Racing Game" profile
2. Record gestures:
   - **Fist** → "up" (accelerate)
   - **Open hand** → "down" (brake)
   - **Point left** → "left" (turn left)
   - **Point right** → "right" (turn right)
   - **Thumbs up** → "space" (nitro)

### Video Player Setup
1. Create "Video Player" profile
2. Record gestures:
   - **Peace sign** → "space" (play/pause)
   - **Thumbs up** → "up" (volume up)
   - **Thumbs down** → "down" (volume down)
   - **Point right** → "right" (seek forward)
   - **OK sign** → "f" (fullscreen)

## 🔧 Key Binding Examples

- **Single keys**: `a`, `w`, `s`, `d`, `1`, `2`, `3`
- **Special keys**: `space`, `enter`, `tab`, `esc`, `backspace`
- **Arrow keys**: `up`, `down`, `left`, `right`
- **Function keys**: `f1`, `f2`, `f3`, etc.
- **Combinations**: `ctrl+c`, `alt+tab`, `shift+w`

## 📊 Technical Details

### Hand Analysis
- Uses MediaPipe for hand landmark detection
- Analyzes 21 hand landmarks per hand
- Supports both left and right hand recognition
- Real-time finger state classification

### Gesture Recognition
- Pattern-based matching system
- Confidence scoring for accuracy
- Support for 15+ built-in gestures
- Custom gesture learning capability

### Profile System
- JSON-based profile storage
- Automatic file persistence
- Profile switching without restart
- Template profiles for quick setup

## 🎯 Controls

- **`s`** - Open Settings panel
- **`q`** - Quit application
- **Mouse** - Interact with GUI settings

## 🔍 Troubleshooting

### Camera Issues
- Ensure camera is not used by other applications
- Try different camera indices (0, 1, 2)
- Check camera permissions

### Import Errors
```bash
pip install opencv-python mediapipe numpy pynput
```

### Gesture Recognition Issues
- Ensure good lighting
- Keep hand clearly visible in camera
- Re-record gestures if accuracy is low
- Check gesture activation status

## 🚀 Advanced Features

### Profile Collections
- Multiple profiles for different applications
- Quick profile switching
- Template-based setup
- Custom gesture combinations

### Recording System
- Visual countdown feedback
- Automatic pattern stabilization
- Multiple sample averaging
- Real-time recording status

### GUI Management
- Tabbed interface for organization
- Real-time gesture list updates
- Drag-and-drop profile management
- Visual feedback for all operations

## 📝 Notes

- Profiles are automatically saved in `gesture_profiles/` directory
- Each profile is stored as a JSON file
- Gestures remain active between application restarts
- Camera feed shows real-time hand analysis
- Recording requires steady hand positioning for best results

## 🎉 Getting Started Tips

1. **Start with templates** - Use Racing/Video/Gaming templates for quick setup
2. **Good lighting** - Ensure adequate lighting for hand detection
3. **Steady recording** - Hold gestures steady during 3-second recording
4. **Test gestures** - Verify gestures work before recording many
5. **Profile organization** - Create separate profiles for different applications
