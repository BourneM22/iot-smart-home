import BlynkLib as blynklib
import time
from typing import Optional, Callable

class BlynkController:
    """
    Robust Blynk IoT controller for smart home gesture control
    """
    
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.blynk = None
        self.current_gesture = 0
        self.last_update_time = 0
        self.min_update_interval = 1.0  # Minimum 1 second between updates
        
        # Virtual pins for different devices/actions
        self.GESTURE_DISPLAY_PIN = 0  # V0 - Display current gesture
        self.DEVICE_1_PIN = 1         # V1 - Device 1 (Light 1)
        self.DEVICE_2_PIN = 2         # V2 - Device 2 (Light 2)
        self.DEVICE_3_PIN = 3         # V3 - Device 3 (Fan)
        self.DEVICE_4_PIN = 4         # V4 - Device 4 (AC)
        self.DEVICE_5_PIN = 5         # V5 - Device 5 (TV)
        
        self.connect_to_blynk()
    
    def connect_to_blynk(self):
        """Connect to Blynk with error handling"""
        # Try only one reliable server to avoid connection issues
        server = "sgp1.blynk.cloud"
        
        try:
            print(f"🔄 Connecting to Blynk server: {server}")
            self.blynk = blynklib.Blynk(self.auth_token, server=server, port=80)
            print(f"✅ Connected to Blynk server: {server}")
            self.setup_handlers()
        except Exception as e:
            print(f"❌ Failed to connect to Blynk: {e}")
            print("⚠️  Running in offline mode - gestures will be detected but not sent to Blynk")
            self.blynk = None
    
    def setup_handlers(self):
        """Setup Blynk event handlers"""
        if not self.blynk:
            return
            
        try:
            @self.blynk.handle_event('write V0')
            def write_handler(pin, value):
                print(f"📥 Received from Blynk V{pin}: {value}")
            
            @self.blynk.handle_event('read V0')
            def read_handler(pin):
                self.safe_virtual_write(pin, self.current_gesture)
        except Exception as e:
            print(f"❌ Failed to setup Blynk handlers: {e}")
    
    def safe_virtual_write(self, pin, value, retry_count=2):
        """Safely write to virtual pin with error handling and retries"""
        if not self.blynk:
            return False
        
        for attempt in range(retry_count + 1):
            try:
                self.blynk.virtual_write(pin, value)
                return True
            except Exception as e:
                if attempt < retry_count:
                    print(f"⚠️  Retry {attempt + 1} for V{pin}={value}")
                    time.sleep(0.2)
                else:
                    print(f"❌ Failed to write V{pin}={value} after {retry_count + 1} attempts: {e}")
                    return False
        return False
    
    def update_gesture(self, gesture_number: Optional[int]):
        """Update the current gesture and trigger corresponding actions"""
        if gesture_number is None:
            return
            
        # Rate limiting to prevent flooding Blynk
        current_time = time.time()
        if current_time - self.last_update_time < self.min_update_interval:
            return
            
        if gesture_number != self.current_gesture:
            self.current_gesture = gesture_number
            self.last_update_time = current_time
            
            print(f"🎯 Gesture {gesture_number} detected!")
            
            if self.blynk:
                # Send gesture to Blynk display
                success = self.safe_virtual_write(self.GESTURE_DISPLAY_PIN, gesture_number)
                if success:
                    print(f"📱 Sent gesture {gesture_number} to Blynk display")
                
                # Trigger device actions
                self.trigger_device_action(gesture_number)
            else:
                print("📱 Offline mode - gesture detected but not sent to Blynk")
    
    def trigger_device_action(self, gesture_number: int):
        """Trigger specific device actions based on gesture number"""
        if not self.blynk:
            return
            
        device_pins = {
            1: self.DEVICE_1_PIN,  # Gesture 1 -> Device 1
            2: self.DEVICE_2_PIN,  # Gesture 2 -> Device 2
            3: self.DEVICE_3_PIN,  # Gesture 3 -> Device 3
            4: self.DEVICE_4_PIN,  # Gesture 4 -> Device 4
            5: self.DEVICE_5_PIN,  # Gesture 5 -> Device 5
        }
        
        print(f"📱 Updating Blynk devices for gesture {gesture_number}")
        
        # Turn off all devices first
        for pin in device_pins.values():
            self.safe_virtual_write(pin, 0)
            time.sleep(0.1)  # Small delay between writes
        
        # Turn on the selected device
        if gesture_number in device_pins:
            success = self.safe_virtual_write(device_pins[gesture_number], 1)
            if success:
                print(f"✅ Device {gesture_number} activated in Blynk")
                
                # Send status message to terminal
                try:
                    from config import DEVICE_NAMES
                    device_name = DEVICE_NAMES.get(gesture_number, f"Device {gesture_number}")
                    status_msg = f"✅ {device_name} activated by gesture {gesture_number}!"
                    self.safe_virtual_write(10, status_msg)  # V10 for terminal
                    print(f"📱 Status sent: {status_msg}")
                except Exception as e:
                    print(f"❌ Failed to send status message: {e}")
    
    def run(self):
        """Run Blynk connection (non-blocking)"""
        if not self.blynk:
            return
            
        try:
            self.blynk.run()
        except Exception as e:
            print(f"❌ Blynk run error: {e}")
            # Try to reconnect if connection is lost
            if "connection" in str(e).lower() or "broken" in str(e).lower():
                print("🔄 Attempting to reconnect to Blynk...")
                self.connect_to_blynk()
    
    def send_status(self, status_message: str):
        """Send status message to Blynk terminal"""
        if self.blynk:
            success = self.safe_virtual_write(10, status_message)
            if success:
                print(f"📱 Status sent to Blynk: {status_message}")
    
    def is_connected(self) -> bool:
        """Check if Blynk is connected"""
        if not self.blynk:
            return False
        try:
            return self.blynk.state == blynklib.CONNECTED
        except:
            return False
    
    def get_status(self) -> str:
        """Get current Blynk connection status"""
        if not self.blynk:
            return "Offline"
        try:
            if self.blynk.state == blynklib.CONNECTED:
                return "Connected"
            else:
                return "Disconnected"
        except:
            return "Error"