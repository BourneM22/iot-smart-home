# Setup Instructions for Smart Home Gesture Control

## Step-by-Step Setup Guide

### 1. Environment Setup

**Install Python Dependencies:**
```bash
# Navigate to project directory
cd "/Users/bourne/College/Semester 1/IOT/Project"

# Install required packages
pip install -r requirements.txt
```

### 2. Blynk App Configuration

**Download and Setup Blynk App:**

1. **Download Blynk App**:
   - iOS: App Store
   - Android: Google Play Store

2. **Create New Project**:
   - Open Blynk app
   - Tap "Create New Project"
   - Choose "Generic Board" as hardware
   - Select "WiFi" as connection type
   - Tap "Create Project"

3. **Get Auth Token**:
   - You'll receive an auth token via email
   - Or go to Project Settings (nut icon) → Auth Token
   - Copy this token for later use

4. **Add Widgets to Project**:

   **Widget 1: Value Display (Current Gesture)**
   - Drag "Value Display" widget to canvas
   - Tap to configure
   - Set Virtual Pin to V0
   - Label: "Current Gesture"
   - Reading Frequency: 1 sec

   **Widget 2-6: LED Indicators (Device Status)**
   - Drag 5 "LED" widgets to canvas
   - Configure each LED:
     - LED 1: Virtual Pin V1, Label "Living Room Light"
     - LED 2: Virtual Pin V2, Label "Bedroom Light"  
     - LED 3: Virtual Pin V3, Label "Ceiling Fan"
     - LED 4: Virtual Pin V4, Label "Air Conditioner"
     - LED 5: Virtual Pin V5, Label "Television"

   **Widget 7: Terminal (System Messages)**
   - Drag "Terminal" widget to canvas
   - Set Virtual Pin to V10
   - Label: "System Status"

5. **Save Project**:
   - Tap the play button (▶) to start the project

### 3. Project Configuration

**Update Configuration File:**

1. Open `config.py` in a text editor
2. Replace `P7DzRsVE5E9scx3EwvUW0Qeg8koHZnKO` with your actual auth token:
   ```python
   BLYNK_AUTH_TOKEN = "your_actual_token_here"
   ```
3. Save the file

### 4. Hardware Setup

**Camera Setup:**
- Ensure your camera/webcam is connected
- Test camera with any camera app to verify it works
- Note the camera index (usually 0 for built-in camera)

### 5. Running the Application

**Start the System:**
```bash
python main.py
```

**Expected Output:**
```
Starting Smart Home Gesture Control System...
Camera Info: {'width': 640, 'height': 480, 'fps': 30, 'backend': 'AVFoundation'}
System ready! Show hand gestures (1-5) to control devices.
Press 'q' to quit, 's' to show status
```

### 6. Testing the System

**Test Gestures:**
1. Show 1 finger → Should activate Device 1 (Living Room Light)
2. Show 2 fingers → Should activate Device 2 (Bedroom Light)
3. Show 3 fingers → Should activate Device 3 (Ceiling Fan)
4. Show 4 fingers → Should activate Device 4 (Air Conditioner)
5. Show 5 fingers → Should activate Device 5 (Television)

**Check Blynk App:**
- Value Display should show current gesture number
- Corresponding LED should light up
- Terminal should show system messages

### 7. Troubleshooting Setup Issues

**Camera Issues:**
```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

**Blynk Connection Issues:**
- Verify auth token is correct
- Check internet connection
- Ensure Blynk project is running (play button pressed)

**Import Errors:**
```bash
# Check if packages are installed
pip list | grep -E "(opencv|mediapipe|blynk)"
```

### 8. Advanced Configuration

**Camera Settings (config.py):**
```python
CAMERA_INDEX = 0        # Change if using external camera
CAMERA_WIDTH = 640      # Adjust resolution
CAMERA_HEIGHT = 480
CAMERA_FPS = 30         # Adjust frame rate
```

**Detection Settings:**
```python
MIN_DETECTION_CONFIDENCE = 0.7  # Lower for easier detection
MIN_TRACKING_CONFIDENCE = 0.5   # Lower for easier tracking
GESTURE_STABILITY_THRESHOLD = 5  # Frames to confirm gesture
```

### 9. Running in Background (Optional)

**For continuous operation:**
```bash
# Run with nohup (Linux/Mac)
nohup python main.py > gesture_log.txt 2>&1 &

# Or use screen (Linux/Mac)
screen -S gesture_control
python main.py
# Ctrl+A, D to detach
```

### 10. Verification Checklist

- [ ] Python dependencies installed
- [ ] Blynk app configured with correct widgets
- [ ] Auth token updated in config.py
- [ ] Camera working and accessible
- [ ] Internet connection available
- [ ] Application starts without errors
- [ ] Gestures detected and displayed
- [ ] Blynk app shows updates
- [ ] All 5 gestures working correctly

## Quick Start Commands

```bash
# Complete setup in one go
cd "/Users/bourne/College/Semester 1/IOT/Project"
pip install -r requirements.txt
# Edit config.py with your auth token
python main.py
```

## Support

If you encounter issues:
1. Check each step carefully
2. Verify all requirements are met
3. Test components individually
4. Check error messages in terminal
5. Verify Blynk app configuration matches the setup
