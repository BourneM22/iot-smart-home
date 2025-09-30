"""
Configuration file for Smart Home Gesture Control IoT Project
"""

# Blynk Configuration
BLYNK_AUTH_TOKEN = "P7DzRsVE5E9scx3EwvUW0Qeg8koHZnKO"  # Replace with your actual token

# Camera Configuration
CAMERA_INDEX = 0  # Default camera (usually 0 for built-in camera)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Gesture Detection Configuration
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
GESTURE_STABILITY_THRESHOLD = 10  # Number of frames to confirm gesture (more stable)

# Blynk Template Information (for reference)
BLYNK_TEMPLATE_ID = "TMPL6PFxUy7MW"
BLYNK_TEMPLATE_NAME = "IOT Smart Home"
# Blynk Virtual Pins
VIRTUAL_PINS = {
    'GESTURE_DISPLAY': 0,  # V0 - Display current gesture
    'DEVICE_1': 1,         # V1 - Device 1 (Light 1)
    'DEVICE_2': 2,         # V2 - Device 2 (Light 2) 
    'DEVICE_3': 3,         # V3 - Device 3 (Fan)
    'DEVICE_4': 4,         # V4 - Device 4 (AC)
    'DEVICE_5': 5,         # V5 - Device 5 (TV)
    'TERMINAL': 10         # V10 - Terminal for status messages
}

# Device Names (for display purposes) - Legacy number mapping
DEVICE_NAMES = {
    1: "Living Room Light",
    2: "Bedroom Light", 
    3: "Ceiling Fan",
    4: "Air Conditioner",
    5: "Television"
}

# Advanced Gesture to Device Mapping
GESTURE_DEVICE_MAPPING = {
    # Static Poses
    'thumbs_up': {'device': 'Living Room Light', 'action': 'toggle', 'pin': 1},
    'thumbs_down': {'device': 'Living Room Light', 'action': 'off', 'pin': 1},
    'ok': {'device': 'Bedroom Light', 'action': 'toggle', 'pin': 2},
    'peace': {'device': 'Ceiling Fan', 'action': 'toggle', 'pin': 3},
    'rock': {'device': 'Sound System', 'action': 'toggle', 'pin': 4},
    'love': {'device': 'Mood Lighting', 'action': 'toggle', 'pin': 5},
    'call_me': {'device': 'Phone Notifications', 'action': 'toggle', 'pin': 6},
    'fist': {'device': 'All Devices', 'action': 'off', 'pin': 7},
    'open_hand': {'device': 'All Devices', 'action': 'on', 'pin': 8},
    
    # Motion Gestures
    'wave': {'device': 'Welcome Mode', 'action': 'activate', 'pin': 9},
    'swipe_left': {'device': 'Previous Scene', 'action': 'activate', 'pin': 10},
    'swipe_right': {'device': 'Next Scene', 'action': 'activate', 'pin': 11},
}

# Gesture Categories
STATIC_GESTURES = ['thumbs_up', 'thumbs_down', 'ok', 'peace', 'rock', 'love', 'call_me', 'fist', 'open_hand', 'crossed']
MOTION_GESTURES = ['wave', 'swipe_left', 'swipe_right']
