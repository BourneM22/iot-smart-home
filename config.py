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

# Device Names (for display purposes)
DEVICE_NAMES = {
    1: "Living Room Light",
    2: "Bedroom Light", 
    3: "Ceiling Fan",
    4: "Air Conditioner",
    5: "Television"
}
