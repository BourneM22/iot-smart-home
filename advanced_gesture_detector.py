#!/usr/bin/env python3
"""
Advanced Gesture Detection System
Recognizes complex hand poses and motion gestures
"""

import cv2
import numpy as np
import time
from typing import Optional, Tuple, List
from collections import deque
import math

class AdvancedGestureDetector:
    """
    Advanced gesture detector for complex hand poses and motion gestures
    """
    
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.kernel = np.ones((5, 5), np.uint8)
        self.calibrated = False
        self.calibration_frames = 0
        
        # Motion tracking
        self.hand_positions = deque(maxlen=15)  # Track last 15 positions
        self.gesture_history = deque(maxlen=10)  # Track last 10 gestures
        
        # Gesture definitions
        self.gesture_names = {
            'ok': '👌 OK Sign',
            'peace': '✌️ Peace Sign', 
            'thumbs_up': '👍 Thumbs Up',
            'thumbs_down': '👎 Thumbs Down',
            'rock': '🤘 Rock Sign',
            'love': '🤟 Love Sign',
            'crossed': '🤞 Fingers Crossed',
            'call_me': '🤙 Call Me',
            'wave': '👋 Wave',
            'swipe_left': '← Swipe Left',
            'swipe_right': '→ Swipe Right',
            'fist': '✊ Fist',
            'open_hand': '✋ Open Hand'
        }
        
        # Motion thresholds
        self.min_motion_distance = 80
        self.wave_frequency_threshold = 3
        
    def calibrate(self, frame):
        """Calibrate background subtractor"""
        if self.calibration_frames < 30:
            self.bg_subtractor.apply(frame)
            self.calibration_frames += 1
            return False
        else:
            self.calibrated = True
            return True
    
    def detect_gesture(self, frame) -> Tuple[Optional[str], np.ndarray]:
        """
        Detect complex gestures in frame
        Returns: (gesture_name, annotated_frame)
        """
        annotated_frame = frame.copy()
        
        if not self.calibrated:
            if not self.calibrate(frame):
                cv2.putText(annotated_frame, "Calibrating... Keep hand out of view", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                return None, annotated_frame
        
        # Focus on detection zone
        h, w = frame.shape[:2]
        roi = frame[0:int(h*0.8), int(w*0.1):int(w*0.9)]  # Larger detection area
        
        # Enhanced skin detection
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Multiple skin tone ranges for better detection
        mask1 = cv2.inRange(hsv, np.array([0, 30, 80]), np.array([17, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([160, 30, 80]), np.array([179, 255, 255]))
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Advanced noise reduction
        kernel_small = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        gesture_name = None
        
        if contours:
            # Find the best hand contour
            hand_contour = self._find_best_hand_contour(contours)
            
            if hand_contour is not None:
                # Adjust coordinates back to full frame
                offset_x = int(w*0.1)
                offset_y = 0
                adjusted_contour = hand_contour + [offset_x, offset_y]
                
                # Draw hand contour
                cv2.drawContours(annotated_frame, [adjusted_contour], -1, (0, 255, 0), 2)
                
                # Get hand center for motion tracking
                M = cv2.moments(hand_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + offset_x
                    cy = int(M["m01"] / M["m00"]) + offset_y
                    hand_center = (cx, cy)
                    
                    # Track hand position
                    self.hand_positions.append((hand_center, time.time()))
                    
                    # Draw hand center
                    cv2.circle(annotated_frame, hand_center, 8, (255, 0, 255), -1)
                    
                    # Detect static pose
                    static_gesture = self._detect_static_pose(hand_contour, annotated_frame, offset_x, offset_y)
                    
                    # Detect motion gesture
                    motion_gesture = self._detect_motion_gesture()
                    
                    # Prioritize motion gestures over static poses
                    gesture_name = motion_gesture if motion_gesture else static_gesture
                    
                    # Add gesture info to frame
                    if gesture_name:
                        gesture_display = self.gesture_names.get(gesture_name, gesture_name)
                        cv2.putText(annotated_frame, f"Gesture: {gesture_display}", 
                                   (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Show detection area
        cv2.rectangle(annotated_frame, (int(w*0.1), 0), (int(w*0.9), int(h*0.8)), (255, 0, 0), 2)
        cv2.putText(annotated_frame, "Detection Zone", (int(w*0.1), 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        # Draw motion trail
        self._draw_motion_trail(annotated_frame)
        
        return gesture_name, annotated_frame
    
    def _find_best_hand_contour(self, contours) -> Optional[np.ndarray]:
        """Find the best contour that represents a hand"""
        valid_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Hand-sized area
            if 2000 < area < 25000:
                # Check shape characteristics
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # Hands are not too circular or too elongated
                    if 0.1 < circularity < 0.9:
                        # Check aspect ratio
                        x, y, w, h = cv2.boundingRect(contour)
                        aspect_ratio = float(w) / h
                        
                        # Reasonable aspect ratio for hands
                        if 0.3 < aspect_ratio < 3.0:
                            valid_contours.append((contour, area))
        
        if valid_contours:
            # Return the largest valid contour
            return max(valid_contours, key=lambda x: x[1])[0]
        
        return None
    
    def _detect_static_pose(self, contour, frame, offset_x, offset_y) -> Optional[str]:
        """Detect static hand poses"""
        area = cv2.contourArea(contour)
        
        # Calculate convex hull and defects
        hull = cv2.convexHull(contour, returnPoints=False)
        
        if len(hull) > 3:
            try:
                defects = cv2.convexityDefects(contour, hull)
                
                if defects is not None:
                    # Analyze hand shape characteristics
                    finger_count, defect_depths = self._analyze_convexity_defects(contour, defects, frame, offset_x, offset_y)
                    
                    # Get bounding rectangle for orientation analysis
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h
                    
                    # Calculate solidity
                    hull_area = cv2.contourArea(cv2.convexHull(contour))
                    solidity = area / hull_area if hull_area > 0 else 0
                    
                    # Gesture classification based on multiple features
                    return self._classify_static_gesture(finger_count, defect_depths, area, aspect_ratio, solidity, contour)
                    
            except cv2.error:
                pass
        
        return None
    
    def _analyze_convexity_defects(self, contour, defects, frame, offset_x, offset_y) -> Tuple[int, List[float]]:
        """Analyze convexity defects to understand hand shape"""
        finger_count = 0
        defect_depths = []
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            
            # Calculate triangle sides
            a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            
            if b > 0 and c > 0:
                # Calculate angle using cosine rule
                angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
                
                # Depth of defect
                depth = d / 256.0
                defect_depths.append(depth)
                
                # Count as finger if angle is acute and depth is significant
                if angle <= np.pi/2 and depth > 20:
                    finger_count += 1
                    
                    # Draw defect points for debugging
                    cv2.circle(frame, (far[0] + offset_x, far[1] + offset_y), 5, (255, 0, 0), -1)
        
        return finger_count, defect_depths
    
    def _classify_static_gesture(self, finger_count, defect_depths, area, aspect_ratio, solidity, contour) -> Optional[str]:
        """Classify static gesture based on hand features"""
        
        # Very compact hand (fist)
        if solidity > 0.85 and len(defect_depths) <= 1:
            return 'fist'
        
        # Very open hand
        if solidity < 0.65 and finger_count >= 3:
            return 'open_hand'
        
        # OK sign: circular shape with hole in middle
        if len(defect_depths) >= 1 and max(defect_depths) > 30 and solidity < 0.8:
            if 0.7 < aspect_ratio < 1.3:  # Roughly square
                return 'ok'
        
        # Peace sign: two extended fingers
        if finger_count == 1 and len(defect_depths) >= 1:  # One gap between two fingers
            if aspect_ratio > 1.2:  # Taller than wide
                return 'peace'
        
        # Thumbs up/down: elongated shape with thumb
        if finger_count <= 1 and aspect_ratio > 1.5:
            # Use contour orientation to determine up vs down
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                # Simple heuristic: if the hand is more towards top, it's thumbs up
                centroid_y = moments["m01"] / moments["m00"]
                _, y, _, h = cv2.boundingRect(contour)
                
                if centroid_y < y + h * 0.4:  # Centroid in upper part
                    return 'thumbs_up'
                elif centroid_y > y + h * 0.6:  # Centroid in lower part
                    return 'thumbs_down'
        
        # Rock sign: extended pinky and index
        if finger_count == 2 and len(defect_depths) >= 2:
            if 1.0 < aspect_ratio < 2.0:
                return 'rock'
        
        # Love sign: three fingers (index, middle, pinky)
        if finger_count == 2 and len(defect_depths) >= 2:
            if solidity < 0.7:
                return 'love'
        
        # Call me: thumb and pinky extended
        if finger_count == 1 and aspect_ratio > 1.8:
            return 'call_me'
        
        # Fingers crossed: overlapping fingers
        if finger_count == 1 and solidity > 0.75:
            return 'crossed'
        
        return None
    
    def _detect_motion_gesture(self) -> Optional[str]:
        """Detect motion-based gestures"""
        if len(self.hand_positions) < 5:
            return None
        
        # Get recent positions
        recent_positions = list(self.hand_positions)[-10:]
        
        # Wave detection: oscillating motion
        if self._detect_wave_motion(recent_positions):
            return 'wave'
        
        # Swipe detection: consistent horizontal movement
        swipe = self._detect_swipe_motion(recent_positions)
        if swipe:
            return swipe
        
        return None
    
    def _detect_wave_motion(self, positions) -> bool:
        """Detect waving motion (oscillating horizontal movement)"""
        if len(positions) < 8:
            return False
        
        # Extract x coordinates and times
        x_coords = [pos[0][0] for pos in positions]
        times = [pos[1] for pos in positions]
        
        # Check for oscillation in x direction
        direction_changes = 0
        for i in range(1, len(x_coords) - 1):
            if (x_coords[i] - x_coords[i-1]) * (x_coords[i+1] - x_coords[i]) < 0:
                direction_changes += 1
        
        # Wave should have multiple direction changes
        return direction_changes >= self.wave_frequency_threshold
    
    def _detect_swipe_motion(self, positions) -> Optional[str]:
        """Detect swipe left/right gestures"""
        if len(positions) < 5:
            return None
        
        # Calculate total displacement
        start_pos = positions[0][0]
        end_pos = positions[-1][0]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Check if movement is primarily horizontal
        if abs(dx) > abs(dy) * 2 and abs(dx) > self.min_motion_distance:
            # Check if movement is consistent (not too much back and forth)
            x_coords = [pos[0][0] for pos in positions]
            
            if dx > 0:  # Moving right
                # Check if generally moving right
                increasing = sum(1 for i in range(1, len(x_coords)) if x_coords[i] > x_coords[i-1])
                if increasing > len(x_coords) * 0.6:
                    return 'swipe_right'
            else:  # Moving left
                # Check if generally moving left
                decreasing = sum(1 for i in range(1, len(x_coords)) if x_coords[i] < x_coords[i-1])
                if decreasing > len(x_coords) * 0.6:
                    return 'swipe_left'
        
        return None
    
    def _draw_motion_trail(self, frame):
        """Draw motion trail of hand movement"""
        if len(self.hand_positions) < 2:
            return
        
        # Draw trail
        points = [pos[0] for pos in self.hand_positions]
        
        for i in range(1, len(points)):
            # Fade trail color based on age
            alpha = i / len(points)
            color = (int(255 * alpha), int(100 * alpha), int(255 * alpha))
            thickness = max(1, int(3 * alpha))
            
            cv2.line(frame, points[i-1], points[i], color, thickness)
    
    def get_gesture_info(self, gesture_name: str) -> dict:
        """Get detailed information about a gesture"""
        if not gesture_name:
            return {}
        
        gesture_info = {
            'name': gesture_name,
            'display_name': self.gesture_names.get(gesture_name, gesture_name),
            'type': 'motion' if gesture_name in ['wave', 'swipe_left', 'swipe_right'] else 'static'
        }
        
        return gesture_info
