#!/bin/bash

echo "========================================"
echo "Enhanced Hand Gesture Recognition System"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from your package manager"
    exit 1
fi

echo "Python 3 found!"
echo

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import cv2, mediapipe, numpy, pynput" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "You may need to install pip first:"
        echo "sudo apt-get install python3-pip  # Ubuntu/Debian"
        echo "brew install python3  # macOS with Homebrew"
        exit 1
    fi
fi

echo "Dependencies OK!"
echo
echo "Starting Gesture Recognition System..."
echo "Press 's' in the camera window to open Settings"
echo "Press 'q' in the camera window to quit"
echo

# Run the main application
python3 main.py

echo
echo "Application closed."
