#!/usr/bin/env python3
"""
Smart Home Gesture Control IoT Project
Clean main file with OpenCV-only gesture detection
"""

import cv2
import numpy as np
import time
import threading
from typing import Optional, Tuple
from config import *
from blynk_controller import BlynkController

class SimpleGestureDetector:
    """Simple gesture detector using OpenCV contours"""
    
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.kernel = np.ones((5, 5), np.uint8)
        self.calibrated = False
        self.calibration_frames = 0
        
    def calibrate(self, frame):
        """Calibrate background subtractor"""
        if self.calibration_frames < 30:  # Calibrate for 30 frames
            self.bg_subtractor.apply(frame)
            self.calibration_frames += 1
            return False
        else:
            self.calibrated = True
            return True
    
    def detect_gesture(self, frame) -> Tuple[Optional[int], np.ndarray]:
        """Detect gesture using improved hand detection"""
        annotated_frame = frame.copy()
        
        if not self.calibrated:
            if not self.calibrate(frame):
                cv2.putText(annotated_frame, "Calibrating... Keep hand out of view", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                return None, annotated_frame
        
        # Focus on upper portion of frame (where hands usually are)
        h, w = frame.shape[:2]
        roi = frame[0:int(h*0.7), int(w*0.2):int(w*0.8)]  # Top 70%, middle 60%
        
        # Convert to HSV for better skin detection
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # More restrictive skin color range
        lower_skin = np.array([0, 30, 80], dtype=np.uint8)
        upper_skin = np.array([17, 255, 255], dtype=np.uint8)
        
        # Create mask
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # More aggressive noise reduction
        kernel_small = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        gesture_number = None
        
        if contours:
            # Filter contours by area and shape
            valid_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                # Much stricter area limits for hand detection
                if 3000 < area < 15000:  # Hand-sized objects only
                    # Check if contour is roughly hand-shaped
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        # Hands are not too circular (0.1 to 0.8)
                        if 0.1 < circularity < 0.8:
                            valid_contours.append(contour)
            
            if valid_contours:
                # Use the largest valid contour
                largest_contour = max(valid_contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                # Adjust contour coordinates back to full frame
                offset_x = int(w*0.2)
                offset_y = 0
                adjusted_contour = largest_contour + [offset_x, offset_y]
                
                # Draw contour on full frame
                cv2.drawContours(annotated_frame, [adjusted_contour], -1, (0, 255, 0), 2)
                
                # More sophisticated gesture recognition
                hull = cv2.convexHull(largest_contour)
                hull_area = cv2.contourArea(hull)
                
                if hull_area > 0:
                    solidity = area / hull_area
                    
                    # Count convexity defects (fingers)
                    hull_indices = cv2.convexHull(largest_contour, returnPoints=False)
                    if len(hull_indices) > 3:
                        defects = cv2.convexityDefects(largest_contour, hull_indices)
                        finger_count = 0
                        
                        if defects is not None:
                            for i in range(defects.shape[0]):
                                s, e, f, d = defects[i, 0]
                                start = tuple(largest_contour[s][0])
                                end = tuple(largest_contour[e][0])
                                far = tuple(largest_contour[f][0])
                                
                                # Calculate angle
                                a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                                b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                                c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                                
                                if b > 0 and c > 0:
                                    angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
                                    
                                    # Count as finger if angle is acute and defect is deep enough
                                    if angle <= np.pi/2 and d > 1000:
                                        finger_count += 1
                        
                        # Add 1 for thumb (simple heuristic)
                        gesture_number = min(finger_count + 1, 5)
                        
                        # Fallback to area-based if finger counting fails
                        if gesture_number == 0 or gesture_number > 5:
                            if area < 5000:
                                gesture_number = 1
                            elif area < 7000:
                                gesture_number = 2
                            elif area < 9000:
                                gesture_number = 3
                            elif area < 11000:
                                gesture_number = 4
                            else:
                                gesture_number = 5
                    
                    # Only show gesture if confidence is high
                    if gesture_number and 1 <= gesture_number <= 5:
                        # Additional validation: check solidity
                        if solidity > 0.5:  # Hand should have reasonable solidity
                            device_name = DEVICE_NAMES.get(gesture_number, f"Device {gesture_number}")
                            cv2.putText(annotated_frame, f"Gesture: {gesture_number} - {device_name}", 
                                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            
                            # Debug info
                            cv2.putText(annotated_frame, f"Area: {int(area)}, Solidity: {solidity:.2f}", 
                                       (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                        else:
                            gesture_number = None
        
        # Show detection area
        cv2.rectangle(annotated_frame, (int(w*0.2), 0), (int(w*0.8), int(h*0.7)), (255, 0, 0), 2)
        cv2.putText(annotated_frame, "Detection Zone", (int(w*0.2), 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        return gesture_number, annotated_frame

class SmartHomeGestureControl:
    """Main application class"""
    
    def __init__(self):
        print("🏠 Initializing Smart Home Gesture Control...")
        
        self.gesture_detector = SimpleGestureDetector()
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
        
    def start(self):
        """Start the system"""
        print("🚀 Starting Smart Home Gesture Control System...")
        
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
            print("📱 Blynk integration active")
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
        """Main processing loop - SINGLE CAMERA WINDOW ONLY"""
        print("👋 System ready! Show hand gestures (1-5) to control devices")
        print("📋 Instructions:")
        print("   - Keep hand out of view during calibration")
        print("   - Show clear gestures with 1-5 fingers")
        print("   - Press 'q' to quit, 's' for status")
        
        frame_count = 0
        
        while self.running:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            frame_count += 1
            
            # Mirror effect for natural interaction
            frame = cv2.flip(frame, 1)
            
            # Detect gesture - SINGLE DETECTION, NO EXTRA WINDOWS
            gesture_number, annotated_frame = self.gesture_detector.detect_gesture(frame)
            
            # Process gesture with stability
            self._process_gesture(gesture_number)
            
            # Add system info
            self._add_system_info(annotated_frame, frame_count)
            
            # Show ONLY ONE window
            cv2.imshow('Smart Home Gesture Control', annotated_frame)
            
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
                print("🔄 Recalibrating...")
        
        self.running = False
    
    def _process_gesture(self, gesture_number):
        """Process detected gesture with stability checking"""
        if gesture_number == self.last_gesture:
            self.gesture_stable_count += 1
        else:
            self.gesture_stable_count = 0
            self.last_gesture = gesture_number
        
        # Trigger action if gesture is stable
        if (self.gesture_stable_count >= GESTURE_STABILITY_THRESHOLD and 
            gesture_number is not None):
            
            device_name = DEVICE_NAMES.get(gesture_number, f"Device {gesture_number}")
            print(f"🎯 Gesture {gesture_number} detected - {device_name}")
            
            # Send to Blynk if available
            if self.blynk_controller and hasattr(self.blynk_controller, 'update_gesture'):
                try:
                    self.blynk_controller.update_gesture(gesture_number)
                except Exception as e:
                    print(f"Blynk update error: {e}")
            
            self.gesture_stable_count = 0  # Reset
    
    def _add_system_info(self, frame, frame_count):
        """Add system information to frame"""
        h, w = frame.shape[:2]
        
        # Instructions
        if self.gesture_detector.calibrated:
            cv2.putText(frame, "Show 1-5 fingers to control devices", (10, 30), 
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
        
        cv2.putText(frame, f"Blynk: {status}", (10, h - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Current active device
        if (self.blynk_controller and hasattr(self.blynk_controller, 'current_gesture') and 
            self.blynk_controller.current_gesture > 0):
            device = DEVICE_NAMES.get(self.blynk_controller.current_gesture, "Unknown")
            cv2.putText(frame, f"Active: {device}", (10, h - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Controls
        cv2.putText(frame, "Press 'q' to quit, 's' for status, 'r' to recalibrate", (10, h - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def _show_status(self):
        """Show system status"""
        print("\n📊 System Status:")
        print("=" * 30)
        print(f"📹 Camera: Active")
        print(f"🤖 Gesture Detection: {'Calibrated' if self.gesture_detector.calibrated else 'Calibrating'}")
        
        if self.blynk_controller:
            if hasattr(self.blynk_controller, 'blynk') and self.blynk_controller.blynk:
                try:
                    connected = self.blynk_controller.is_connected()
                    print(f"📱 Blynk: {'Connected' if connected else 'Disconnected'}")
                    if hasattr(self.blynk_controller, 'current_gesture'):
                        print(f"🎯 Current Gesture: {self.blynk_controller.current_gesture}")
                        if self.blynk_controller.current_gesture > 0:
                            device = DEVICE_NAMES.get(self.blynk_controller.current_gesture, "Unknown")
                            print(f"🏠 Active Device: {device}")
                except:
                    print("📱 Blynk: Error checking status")
            else:
                print("📱 Blynk: Offline mode")
        else:
            print("📱 Blynk: Not initialized")
        
        print(f"🔄 Gesture Stability: {self.gesture_stable_count}/{GESTURE_STABILITY_THRESHOLD}")
        print("=" * 30)

def main():
    """Main function"""
    print("🏠 Smart Home Gesture Control")
    print("=" * 40)
    print("🎯 OpenCV-based gesture detection")
    print("📱 Blynk IoT integration")
    print()
    
    try:
        system = SmartHomeGestureControl()
        system.start()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure your camera is available")

if __name__ == "__main__":
    main()