# Smart Home Gesture Control IoT Project V2 - Advanced Edition

A sophisticated real-time hand gesture recognition system that controls smart home devices using advanced computer vision and IoT integration with Blynk platform.

## 🎯 Features

- **Advanced Gesture Recognition**: Recognizes complex hand poses and motion gestures
- **Static Poses**: 👌 OK, ✌️ Peace, 👍👎 Thumbs, 🤘 Rock, 🤟 Love, 🤙 Call Me, ✊ Fist, ✋ Open Hand
- **Motion Gestures**: 👋 Wave, ← Swipe Left, → Swipe Right
- **Live Camera Feed**: Uses OpenCV for real-time video processing with motion trails
- **Advanced IoT Integration**: Connected to Blynk platform with 12 virtual pins
- **Smart Home Control**: Each gesture controls different smart home devices and scenes
- **Intelligent Detection**: Multi-layer validation with gesture stability checking

## 🤚 Gesture Mapping

### Static Poses
| Gesture | Device/Action | Description |
|---------|---------------|-------------|
| 👍 Thumbs Up | Living Room Light | Toggle ON |
| 👎 Thumbs Down | Living Room Light | Turn OFF |
| 👌 OK Sign | Bedroom Light | Toggle |
| ✌️ Peace Sign | Ceiling Fan | Toggle |
| 🤘 Rock Sign | Sound System | Toggle |
| 🤟 Love Sign | Mood Lighting | Toggle |
| 🤙 Call Me | Phone Notifications | Toggle |
| ✊ Fist | All Devices | Turn OFF |
| ✋ Open Hand | All Devices | Turn ON |

### Motion Gestures
| Gesture | Action | Description |
|---------|--------|-------------|
| 👋 Wave | Welcome Mode | Activate greeting sequence |
| ← Swipe Left | Previous Scene | Switch to previous lighting scene |
| → Swipe Right | Next Scene | Switch to next lighting scene |

## 📋 Prerequisites

- Python 3.7 or higher (tested on Python 3.13)
- Webcam or camera device
- Blynk account and app
- Internet connection for Blynk IoT

## 🚀 Installation

### 1. Clone or Download Project Files

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies include:**
- opencv-python (computer vision)
- BlynkLib (IoT integration)
- numpy (numerical operations)

### 3. Set Up Blynk App

#### Download Blynk App:
- **iOS**: [App Store](https://apps.apple.com/app/blynk-iot/id808760481)
- **Android**: [Google Play](https://play.google.com/store/apps/details?id=cc.blynk)

#### Create New Project:
1. Open Blynk app and create account
2. Tap **"Create New Project"**
3. Project settings:
   - **Name**: "Smart Home Gesture Control"
   - **Hardware**: "Generic Board"
   - **Connection**: "WiFi"
4. Tap **"Create Project"**

#### Get Auth Token:
- You'll receive an **Auth Token** via email
- Or tap the **settings icon** (⚙️) in your project
- Copy the **Auth Token**

#### Add Widgets to Project:
1. **Value Display** (V0) - Current gesture code
2. **LED Indicators** (V1-V11) - Device status for each gesture
3. **Terminal** (V20) - Advanced gesture status messages

### 4. Configure the Project
1. Open `config.py`
2. Replace the auth token:
   ```python
   BLYNK_AUTH_TOKEN = "your_actual_token_here"
   ```
3. Adjust camera settings if needed (usually defaults work fine)

## 🎮 Usage

### 1. Run the Advanced Application
```bash
python main_advanced.py
```

### 2. System Startup
- **Calibration**: Keep hand out of view for 30 frames (~1 second)
- **Detection Zone**: Blue rectangle shows where to make gestures
- **Ready**: System will show "Advanced Gesture System Ready!"

### 3. Making Gestures

#### Static Poses:
- Hold gesture **steady for 1 second**
- Keep hand in blue detection zone
- Face palm toward camera
- Make clear, distinct poses

#### Motion Gestures:
- **Wave**: Move hand left-right repeatedly (3+ oscillations)
- **Swipe Left**: Move hand from right to left across screen
- **Swipe Right**: Move hand from left to right across screen

### 4. System Controls
- **'q'** - Quit application
- **'s'** - Show system status
- **'r'** - Recalibrate detection
- **'g'** - Show gesture statistics (NEW!)

### 5. Blynk App Monitoring
- **V0**: Current gesture code
- **V1-V11**: Device status LEDs
- **V20**: Gesture status messages

## 📁 Project Structure

```
Project/
├── main_advanced.py           # Advanced gesture recognition system (USE THIS)
├── main.py                    # Legacy simple system (backup)
├── advanced_gesture_detector.py  # Complex gesture detection logic
├── blynk_controller.py        # Enhanced Blynk IoT integration
├── config.py                  # Configuration with gesture mappings
├── requirements.txt           # Python dependencies
├── GESTURE_GUIDE.md          # Detailed gesture instructions
├── BLYNK_SETUP_GUIDE.md      # Comprehensive Blynk setup
└── README.md                 # This documentation
```

## 🔧 Technical Details

### Advanced Gesture Detection
- **Multi-layer Analysis**: Skin detection, shape validation, convexity analysis
- **HSV Color Space**: Better skin detection across lighting conditions
- **Motion Tracking**: 15-point position history for gesture trails
- **Convexity Defects**: Sophisticated finger counting and pose analysis
- **Gesture Classification**: Complex logic combining multiple features

### Enhanced Camera Integration
- **Larger Detection Zone**: 80% height, 90% width coverage
- **Motion Trail Visualization**: See hand movement paths
- **Adaptive Background**: Automatic calibration and noise reduction
- **Real-time Processing**: Optimized for smooth 30fps performance

### Advanced IoT Integration
- **12 Virtual Pins**: V0, V1-V11, V20 for comprehensive control
- **Smart Rate Limiting**: Prevents server overload
- **Error Recovery**: Automatic reconnection and retry logic
- **Action Types**: Toggle, on/off, momentary activation
- **Enhanced Status**: Real-time gesture and device feedback

## 🛠️ Troubleshooting

### Common Issues

#### 1. Gesture Not Detected
- **Check lighting**: Ensure good, even lighting
- **Hand position**: Keep hand in blue detection zone
- **Hold steady**: Static poses need 1 second stability
- **Recalibrate**: Press 'r' to recalibrate background

#### 2. Wrong Gesture Detected
- **Make distinct gestures**: Ensure clear hand poses
- **Check background**: Avoid cluttered or skin-colored backgrounds
- **Adjust distance**: Stay 2-4 feet from camera
- **Better lighting**: Avoid shadows and backlighting

#### 3. Motion Gestures Not Working
- **Larger movements**: Make more deliberate motions
- **Consistent direction**: Maintain steady left/right movement
- **Moderate speed**: Not too fast or too slow
- **Stay in zone**: Keep hand in detection area during motion

#### 4. Blynk Connection Issues
- **Project running**: Ensure play button is pressed in Blynk console
- **Auth token**: Verify token is correct in config.py
- **Internet**: Check internet connection
- **Virtual pins**: Confirm widgets use correct pin numbers

#### 5. Performance Issues
- **Close other apps**: Free up camera and CPU resources
- **Lower resolution**: Adjust CAMERA_WIDTH/HEIGHT in config.py
- **Reduce FPS**: Lower CAMERA_FPS if needed
- **Better hardware**: Modern multi-core processor recommended

### System Requirements
- **CPU**: Modern multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: Minimum 4GB, 8GB recommended
- **Camera**: Any USB webcam or built-in camera (720p or better)
- **OS**: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+
- **Internet**: Stable connection for Blynk IoT

## 🎨 Customization

### Adding New Gestures
1. **Define gesture logic** in `advanced_gesture_detector.py`
2. **Add gesture mapping** in `config.py` GESTURE_DEVICE_MAPPING
3. **Update Blynk pins** and add corresponding widgets
4. **Test and calibrate** new gesture recognition

### Changing Device Actions
1. **Edit gesture mappings** in `config.py`
2. **Update Blynk virtual pins** as needed
3. **Modify action types**: toggle, on, off, activate
4. **Configure Blynk widgets** for new devices

### Adjusting Detection Sensitivity
- **Gesture stability**: Modify GESTURE_STABILITY_THRESHOLD in config.py
- **Detection confidence**: Adjust skin color ranges in detector
- **Motion thresholds**: Tune swipe distance and wave frequency
- **Area limits**: Modify hand size detection ranges

## 🚀 Advanced Features

### Gesture Statistics
- Press **'g'** to view detection statistics
- See which gestures you use most
- Track system performance and accuracy

### Motion Trail Visualization
- See colored trail following your hand movement
- Helps with motion gesture debugging
- Visual feedback for gesture paths

### Multi-layer Validation
- **Skin detection** with multiple tone ranges
- **Shape analysis** for hand-like objects
- **Motion tracking** for gesture trails
- **Stability checking** to prevent false triggers

### Smart IoT Integration
- **Rate limiting** prevents server flooding
- **Error recovery** with automatic reconnection
- **Action variety** with different control types
- **Status feedback** through multiple channels

## 🔮 Future Enhancements

- **Machine Learning**: AI-powered gesture recognition
- **Voice Commands**: Combined voice and gesture control
- **Multiple Users**: Multi-person gesture recognition
- **Mobile App**: Direct smartphone control interface
- **Cloud Integration**: AWS/Google Cloud IoT integration
- **Gesture Recording**: Custom gesture training system

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

### Getting Help:
1. **Check GESTURE_GUIDE.md** for detailed gesture instructions
2. **Review BLYNK_SETUP_GUIDE.md** for IoT setup help
3. **Test components separately** using system controls
4. **Check gesture statistics** with 'g' key
5. **Verify Blynk setup** with virtual pin configuration

### Debug Information:
- **System status**: Press 's' for detailed status
- **Gesture stats**: Press 'g' for detection statistics
- **Recalibration**: Press 'r' if detection degrades
- **Console output**: Check terminal for error messages

---

## 🎉 Quick Start Summary

1. **Install**: `pip install -r requirements.txt`
2. **Setup Blynk**: Create project, get auth token, add widgets
3. **Configure**: Update `config.py` with your auth token
4. **Run**: `python main_advanced.py`
5. **Calibrate**: Keep hand out of view during startup
6. **Gesture**: Make poses in blue detection zone
7. **Control**: Watch your smart home respond to gestures!

**🏠 Welcome to the future of gesture-controlled smart homes! ✨**

---

**⚠️ Security Note**: Keep your Blynk auth token secure and never share it publicly.