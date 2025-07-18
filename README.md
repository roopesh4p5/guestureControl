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
- **Single-hand gestures**: Traditional one-hand recognition
- **Both-hand gestures**: Combined two-hand recognition (perfect for numbers 6-10)
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

### 2. Create or Select a Profile
1. Press `s` to open Settings
2. **Step 1**: Select or create a profile:
   - Use dropdown to select existing profile
   - Click "📂 New Profile" for custom profile
   - Click template buttons for quick setup:
     - 🏎️ Racing (accelerate, brake, turn, nitro, horn)
     - 🎥 Video (play/pause, volume, seek, fullscreen)
     - 🎮 Gaming (jump, movement, actions)

### 3. Add Gestures One by One
1. **Step 2**: In the "Add Gestures" section:
   - Enter gesture name (e.g., "accelerate", "left_turn")
   - Enter key binding (e.g., "up", "a", "space")
   - Click "🔴 Record Gesture"

### 4. Recording Process (Automatic)
1. **3-2-1 Countdown**: Get ready and position your hand
2. **Record**: Hold your gesture steady for 3 seconds
3. **Auto-Save**: Gesture automatically saved and activated
4. **Next Gesture**: Form clears, ready for next gesture

### 5. Build Your Collection & Activate Profile
- Repeat step 3-4 for each gesture you want
- Each gesture is added to your profile
- Click "💾 Save Profile" when done adding gestures
- Click "🎮 Activate Profile" to use all gestures

### 6. Switch Between Profiles (Press 'p')
- Press 'p' in camera window to open **fast Profile Selector**
- See all profiles with gesture counts and descriptions
- **📂 Load**: Instantly load and activate profile
- **🗑️ Delete**: Remove profile with confirmation
- **Fast Loading**: Optimized for quick profile switching

## 🎮 Example Usage Scenarios

### Racing Game Setup (Step by Step)
1. Press `s` to open Settings
2. Click "🏎️ Racing" template button
3. Add gestures one by one:
   - Name: "accelerate", Key: "w", Record: **Fist gesture**
   - Name: "brake", Key: "s", Record: **Open hand**
   - Name: "left", Key: "a", Record: **Point left**
   - Name: "right", Key: "d", Record: **Point right**
4. Click "💾 Save Profile" then "🎮 Activate Profile"
5. Done! Racing profile active with W/A/S/D controls

### Number Profile Setup (1-10 with Both Hands)
1. Press `s` to open Settings
2. Click "📂 New Profile" and name it "Numbers"
3. Add single-hand gestures (1-5):
   - Name: "one", Key: "1", Type: "single", Record: **1 finger**
   - Name: "two", Key: "2", Type: "single", Record: **2 fingers**
   - Name: "three", Key: "3", Type: "single", Record: **3 fingers**
   - Name: "four", Key: "4", Type: "single", Record: **4 fingers**
   - Name: "five", Key: "5", Type: "single", Record: **5 fingers**
4. Add both-hand gestures (6-10):
   - Name: "six", Key: "6", Type: "both", Record: **5 right + 1 left**
   - Name: "seven", Key: "7", Type: "both", Record: **5 right + 2 left**
   - Name: "eight", Key: "8", Type: "both", Record: **5 right + 3 left**
   - Name: "nine", Key: "9", Type: "both", Record: **5 right + 4 left**
   - Name: "ten", Key: "0", Type: "both", Record: **5 right + 5 left**
5. Save and activate profile - now you have 1-10 number recognition!

### Using Your Racing Profile
1. Press `p` to open Profile Selector
2. Select "Racing Game" profile
3. Click "✅ Activate Selected"
4. All 4 gestures now control your racing game!

### Video Player Setup (Step by Step)
1. Press `s` to open Settings
2. Click "🎥 Video" template button
3. Add gestures one by one:
   - Name: "play_pause", Key: "space", Record: **Peace sign**
   - Name: "volume_up", Key: "up", Record: **Thumbs up**
   - Name: "volume_down", Key: "down", Record: **Thumbs down**
   - Name: "seek_forward", Key: "right", Record: **Point right**
   - Name: "fullscreen", Key: "f", Record: **OK sign**
4. Done! Profile ready to use

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

- **`s`** - Open Settings panel (create/edit profiles and gestures)
- **`p`** - Open Profile Selector (switch between profiles)
- **`q`** - Quit application
- **Mouse** - Interact with GUI windows

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

### Threading/GUI Issues
- If you see "RuntimeError: main thread is not in main loop":
  - This has been fixed in the latest version
  - Restart the application if the error persists
  - The recording system now uses thread-safe GUI updates

### Recording Issues
- If recording countdown stops unexpectedly:
  - Check console for error messages
  - Ensure camera is working properly
  - Try closing and reopening the settings window

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
