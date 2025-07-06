@echo off
echo ========================================
echo Enhanced Hand Gesture Recognition System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import cv2, mediapipe, numpy, pynput" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.
echo Starting Gesture Recognition System...
echo Press 's' in the camera window to open Settings
echo Press 'q' in the camera window to quit
echo.

REM Run the main application
python main.py

echo.
echo Application closed.
pause
