#!/usr/bin/env python3
"""
Advanced Smart Home Gesture Control IoT Project
Complex gesture recognition with static poses and motion gestures
"""

import cv2
import numpy as np
import time
import threading
from typing import Optional, Tuple
from config import *
from advanced_gesture_detector import AdvancedGestureDetector
from blynk_controller import BlynkController

class AdvancedSmartHomeGestureControl:
    """
    Advanced Smart Home Gesture Control with complex gesture recognition
    """
    
    def __init__(self):
        print("🏠 Initializing Advanced Smart Home Gesture Control...")
        print("🎯 Supporting complex gestures: 👌👋✌️👍👎🤘🤟🤞🤙✊✋")
        print("🔄 Motion gestures: Wave, Swipe Left/Right")
        
        self.gesture_detector = AdvancedGestureDetector()
        self.blynk_controller = None
        
        # Initialize Blynk
        try:
            self.blynk_controller = BlynkController(BLYNK_AUTH_TOKEN)
        except Exception as e:
            print(f"⚠️  Blynk initialization failed: {e}")
            print("📱 Running in offline mode - gestures will be detected but not sent to Blynk")
        
        self.running = False
        self.last_gesture = None
        self.gesture_stable_count = 0
        self.gesture_stats = {}
        
        # Initialize gesture statistics
        for gesture in STATIC_GESTURES + MOTION_GESTURES:
            self.gesture_stats[gesture] = 0
        
    def start(self):
        """Start the advanced gesture control system"""
        print("🚀 Starting Advanced Smart Home Gesture Control System...")
        
        # Initialize camera
        cap = cv2.VideoCapture(CAMERA_INDEX)
        
        if not cap.isOpened():
            print("❌ Cannot open camera")
            return False
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
        print(f"📹 Camera: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
        
        self.running = True
        
        # Start Blynk thread if available
        if self.blynk_controller and hasattr(self.blynk_controller, 'blynk') and self.blynk_controller.blynk:
            blynk_thread = threading.Thread(target=self._run_blynk)
            blynk_thread.daemon = True
            blynk_thread.start()
            print("📱 Advanced Blynk integration active")
        else:
            print("📱 Running in offline mode")
        
        # Main loop
        self._main_loop(cap)
        
        cap.release()
        cv2.destroyAllWindows()
        return True
    
    def _run_blynk(self):
        """Run Blynk in separate thread"""
        while self.running and self.blynk_controller and hasattr(self.blynk_controller, 'blynk') and self.blynk_controller.blynk:
            try:
                self.blynk_controller.run()
                time.sleep(0.01)
            except Exception as e:
                print(f"Blynk error: {e}")
                time.sleep(1)
    
    def _main_loop(self, cap):
        """Main processing loop for advanced gesture detection"""
        print("👋 Advanced Gesture System Ready!")
        print("📋 Supported Gestures:")
        print("   Static: 👌 OK, ✌️ Peace, 👍👎 Thumbs, 🤘 Rock, 🤟 Love, 🤙 Call Me, ✊ Fist, ✋ Open Hand")
        print("   Motion: 👋 Wave, ← Swipe Left, → Swipe Right")
        print("   Controls: 'q' quit, 's' status, 'r' recalibrate, 'g' gesture stats")
        
        frame_count = 0
        
        while self.running:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            frame_count += 1
            
            # Mirror effect for natural interaction
            frame = cv2.flip(frame, 1)
            
            # Detect advanced gestures
            gesture_name, annotated_frame = self.gesture_detector.detect_gesture(frame)
            
            # Process gesture with stability
            self._process_advanced_gesture(gesture_name)
            
            # Add system info
            self._add_advanced_system_info(annotated_frame, frame_count)
            
            # Show frame
            cv2.imshow('Advanced Smart Home Gesture Control', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self._show_status()
            elif key == ord('r'):
                # Reset calibration
                self.gesture_detector.calibrated = False
                self.gesture_detector.calibration_frames = 0
                print("🔄 Recalibrating advanced gesture detection...")
            elif key == ord('g'):
                self._show_gesture_stats()
        
        self.running = False
    
    def _process_advanced_gesture(self, gesture_name):
        """Process detected advanced gesture with stability checking"""
        if gesture_name == self.last_gesture:
            self.gesture_stable_count += 1
        else:
            self.gesture_stable_count = 0
            self.last_gesture = gesture_name
        
        # Different stability requirements for different gesture types
        stability_threshold = GESTURE_STABILITY_THRESHOLD
        
        # Motion gestures need less stability (they're transient)
        if gesture_name in MOTION_GESTURES:
            stability_threshold = max(3, GESTURE_STABILITY_THRESHOLD // 3)
        
        # Trigger action if gesture is stable
        if (self.gesture_stable_count >= stability_threshold and gesture_name is not None):
            
            # Update statistics
            if gesture_name in self.gesture_stats:
                self.gesture_stats[gesture_name] += 1
            
            # Get gesture info
            gesture_info = self.gesture_detector.get_gesture_info(gesture_name)
            display_name = gesture_info.get('display_name', gesture_name)
            gesture_type = gesture_info.get('type', 'unknown')
            
            print(f"🎯 {gesture_type.title()} Gesture: {display_name}")
            
            # Send to Blynk if available
            if self.blynk_controller and hasattr(self.blynk_controller, 'update_gesture'):
                try:
                    self.blynk_controller.update_gesture(gesture_name)
                except Exception as e:
                    print(f"Blynk update error: {e}")
            
            # Show device action
            if gesture_name in GESTURE_DEVICE_MAPPING:
                device_info = GESTURE_DEVICE_MAPPING[gesture_name]
                print(f"🏠 Action: {device_info['device']} - {device_info['action']}")
            
            self.gesture_stable_count = 0  # Reset
    
    def _add_advanced_system_info(self, frame, frame_count):
        """Add advanced system information to frame"""
        h, w = frame.shape[:2]
        
        # Instructions
        if self.gesture_detector.calibrated:
            cv2.putText(frame, "Show complex gestures to control smart home", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Blynk status
        if self.blynk_controller and hasattr(self.blynk_controller, 'blynk') and self.blynk_controller.blynk:
            try:
                status = "Connected" if self.blynk_controller.is_connected() else "Connecting..."
                color = (0, 255, 0) if self.blynk_controller.is_connected() else (0, 255, 255)
            except:
                status = "Error"
                color = (0, 0, 255)
        else:
            status = "Offline Mode"
            color = (128, 128, 128)
        
        cv2.putText(frame, f"Blynk: {status}", (10, h - 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Current active gesture
        if (self.blynk_controller and hasattr(self.blynk_controller, 'current_gesture') and 
            self.blynk_controller.current_gesture):
            gesture_display = self.gesture_detector.gesture_names.get(
                self.blynk_controller.current_gesture, 
                self.blynk_controller.current_gesture
            )
            cv2.putText(frame, f"Active: {gesture_display}", (10, h - 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Gesture type indicator
        if self.last_gesture:
            gesture_type = "Motion" if self.last_gesture in MOTION_GESTURES else "Static"
            cv2.putText(frame, f"Type: {gesture_type}", (10, h - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Controls
        cv2.putText(frame, "Controls: 'q' quit, 's' status, 'r' recalibrate, 'g' stats", (10, h - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def _show_status(self):
        """Show advanced system status"""
        print("\n📊 Advanced System Status:")
        print("=" * 40)
        print(f"📹 Camera: Active")
        print(f"🤖 Gesture Detection: {'Calibrated' if self.gesture_detector.calibrated else 'Calibrating'}")
        print(f"🎯 Supported Gestures: {len(STATIC_GESTURES + MOTION_GESTURES)}")
        print(f"   - Static Poses: {len(STATIC_GESTURES)}")
        print(f"   - Motion Gestures: {len(MOTION_GESTURES)}")
        
        if self.blynk_controller:
            if hasattr(self.blynk_controller, 'blynk') and self.blynk_controller.blynk:
                try:
                    connected = self.blynk_controller.is_connected()
                    print(f"📱 Blynk: {'Connected' if connected else 'Disconnected'}")
                    if hasattr(self.blynk_controller, 'current_gesture'):
                        current = self.blynk_controller.current_gesture
                        if current:
                            display_name = self.gesture_detector.gesture_names.get(current, current)
                            print(f"🎯 Current Gesture: {display_name}")
                except:
                    print("📱 Blynk: Error checking status")
            else:
                print("📱 Blynk: Offline mode")
        else:
            print("📱 Blynk: Not initialized")
        
        print(f"🔄 Gesture Stability: {self.gesture_stable_count}/{GESTURE_STABILITY_THRESHOLD}")
        print("=" * 40)
    
    def _show_gesture_stats(self):
        """Show gesture detection statistics"""
        print("\n📈 Gesture Detection Statistics:")
        print("=" * 35)
        
        total_detections = sum(self.gesture_stats.values())
        if total_detections == 0:
            print("No gestures detected yet")
            return
        
        print(f"Total Detections: {total_detections}")
        print("\nStatic Gestures:")
        for gesture in STATIC_GESTURES:
            count = self.gesture_stats.get(gesture, 0)
            if count > 0:
                percentage = (count / total_detections) * 100
                display_name = self.gesture_detector.gesture_names.get(gesture, gesture)
                print(f"  {display_name}: {count} ({percentage:.1f}%)")
        
        print("\nMotion Gestures:")
        for gesture in MOTION_GESTURES:
            count = self.gesture_stats.get(gesture, 0)
            if count > 0:
                percentage = (count / total_detections) * 100
                display_name = self.gesture_detector.gesture_names.get(gesture, gesture)
                print(f"  {display_name}: {count} ({percentage:.1f}%)")
        
        print("=" * 35)

def main():
    """Main function"""
    print("🏠 Advanced Smart Home Gesture Control")
    print("=" * 50)
    print("🎯 Complex gesture recognition system")
    print("📱 Advanced Blynk IoT integration")
    print("🤖 Static poses + Motion gestures")
    print()
    
    try:
        system = AdvancedSmartHomeGestureControl()
        system.start()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure your camera is available")

if __name__ == "__main__":
    main()
