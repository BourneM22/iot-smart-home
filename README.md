# Smart Home Gesture Control IoT Project

A real-time hand gesture recognition system that controls smart home devices using computer vision and IoT integration with Blynk platform.

## Features

- **Real-time Hand Gesture Detection**: Recognizes hand gestures for numbers 1-5 using MediaPipe
- **Live Camera Feed**: Uses OpenCV for real-time video processing
- **IoT Integration**: Connected to Blynk platform for remote monitoring and control
- **Smart Home Control**: Each gesture (1-5) controls a different smart home device
- **Stable Gesture Recognition**: Implements gesture stability checking to prevent false triggers

## Gesture Mapping

| Gesture | Device | Description |
|---------|--------|-------------|
| 1 finger | Device 1 | Living Room Light |
| 2 fingers | Device 2 | Bedroom Light |
| 3 fingers | Device 3 | Ceiling Fan |
| 4 fingers | Device 4 | Air Conditioner |
| 5 fingers | Device 5 | Television |

## Prerequisites

- Python 3.7 or higher
- Webcam or camera device
- Blynk account and app
- Internet connection for Blynk IoT

## Installation

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Blynk**:
   - Download the Blynk app on your smartphone
   - Create a new project
   - Get your Auth Token from project settings
   - Add the following widgets to your project:
     - Value Display (V0) - Current Gesture
     - LED widgets (V1-V5) - Device status indicators
     - Terminal (V10) - System status messages

4. **Configure the project**:
   - Open `config.py`
   - Replace `P7DzRsVE5E9scx3EwvUW0Qeg8koHZnKO` with your actual Blynk auth token
   - Adjust camera and detection settings if needed

## Usage

1. **Run the main application**:
   ```bash
   python main.py
   ```

2. **Control the system**:
   - Show hand gestures (1-5 fingers) in front of the camera
   - Each gesture will activate the corresponding device
   - Monitor device status through the Blynk app
   - Press 'q' to quit the application
   - Press 's' to show system status

3. **Blynk App Monitoring**:
   - View current gesture on V0 display
   - See device status on LED widgets (V1-V5)
   - Check system messages in terminal widget (V10)

## Project Structure

```
Project/
├── main.py                 # Main application entry point
├── gesture_detector.py     # Hand gesture detection logic
├── camera_handler.py       # Camera management and video feed
├── blynk_controller.py     # Blynk IoT integration
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md              # This documentation
```

## Technical Details

### Hand Gesture Detection
- Uses MediaPipe for hand landmark detection
- Analyzes finger positions to determine extended fingers
- Implements gesture stability checking to prevent false positives

### Camera Integration
- OpenCV-based video capture
- Threaded frame processing for smooth performance
- Configurable camera settings (resolution, FPS)

### IoT Integration
- Blynk platform for remote monitoring and control
- Virtual pins for device control and status display
- Real-time notifications and status updates

## Troubleshooting

### Common Issues

1. **Camera not working**:
   - Check if camera is connected and not used by other applications
   - Try changing `CAMERA_INDEX` in `config.py` (0, 1, 2, etc.)

2. **Blynk connection issues**:
   - Verify your auth token is correct
   - Check internet connection
   - Ensure Blynk app project is configured with correct virtual pins

3. **Gesture detection not accurate**:
   - Ensure good lighting conditions
   - Keep hand clearly visible in camera frame
   - Adjust `MIN_DETECTION_CONFIDENCE` in `config.py`

4. **Performance issues**:
   - Lower camera resolution in `config.py`
   - Reduce FPS if needed
   - Close other applications using camera/CPU

### System Requirements
- **CPU**: Modern multi-core processor recommended
- **RAM**: Minimum 4GB, 8GB recommended
- **Camera**: Any USB webcam or built-in camera
- **OS**: Windows, macOS, or Linux

## Customization

### Adding More Gestures
1. Modify `count_extended_fingers()` in `gesture_detector.py`
2. Add new virtual pins in `config.py`
3. Update device mapping in `blynk_controller.py`

### Changing Device Actions
1. Edit `trigger_device_action()` in `blynk_controller.py`
2. Update `DEVICE_NAMES` in `config.py`
3. Configure corresponding widgets in Blynk app

### Adjusting Detection Sensitivity
- Modify confidence thresholds in `config.py`
- Adjust `GESTURE_STABILITY_THRESHOLD` for gesture confirmation
- Fine-tune MediaPipe parameters in `gesture_detector.py`

## Future Enhancements

- Support for more complex gestures
- Voice command integration
- Multiple camera support
- Machine learning-based gesture recognition
- Integration with other IoT platforms
- Mobile app for direct control

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review configuration settings
3. Test individual components separately
4. Check Blynk app setup and virtual pin configuration

---

**Note**: Make sure to keep your Blynk auth token secure and never share it publicly.
