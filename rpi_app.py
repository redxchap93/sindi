#!/usr/bin/env python3
"""
Simple Raspberry Pi Robot Controller
"""

import sys
import time
import logging
from typing import Optional

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    RPI_AVAILABLE = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('robot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SimpleRobot:
    """Simple robot controller for Raspberry Pi"""
    
    def __init__(self, left_motor_pin: int = 18, right_motor_pin: int = 19):
        """
        Initialize the robot with motor pins
        
        Args:
            left_motor_pin (int): GPIO pin for left motor
            right_motor_pin (int): GPIO pin for right motor
        """
        self.left_motor_pin = left_motor_pin
        self.right_motor_pin = right_motor_pin
        self.is_initialized = False
        
        if not RPI_AVAILABLE:
            logger.warning("RPi.GPIO not available. Simulation mode enabled.")
            return
            
        try:
            # Set up GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.left_motor_pin, GPIO.OUT)
            GPIO.setup(self.right_motor_pin, GPIO.OUT)
            
            # Set up PWM
            self.left_pwm = GPIO.PWM(self.left_motor_pin, 1000)
            self.right_pwm = GPIO.PWM(self.right_motor_pin, 1000)
            
            # Start PWM with 0% duty cycle (motors off)
            self.left_pwm.start(0)
            self.right_pwm.start(0)
            
            self.is_initialized = True
            logger.info("Robot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize robot: {e}")
            raise

    def move_forward(self, speed: float = 50.0) -> None:
        """
        Move robot forward
        
        Args:
            speed (float): Speed percentage (0-100)
        """
        if not self.is_initialized:
            logger.warning("Robot not initialized. Cannot move forward.")
            return
            
        try:
            speed = max(0, min(100, speed))
            self.left_pwm.ChangeDutyCycle(speed)
            self.right_pwm.ChangeDutyCycle(speed)
            logger.info(f"Moving forward at {speed}% speed")
        except Exception as e:
            logger.error(f"Error moving forward: {e}")

    def move_backward(self, speed: float = 50.0) -> None:
        """
        Move robot backward
        
        Args:
            speed (float): Speed percentage (0-100)
        """
        if not self.is_initialized:
            logger.warning("Robot not initialized. Cannot move backward.")
            return
            
        try:
            speed = max(0, min(100, speed))
            # For simplicity, we'll use the same pins but with reversed logic
            # In a real implementation, you'd need direction control
            self.left_pwm.ChangeDutyCycle(speed)
            self.right_pwm.ChangeDutyCycle(speed)
            logger.info(f"Moving backward at {speed}% speed")
        except Exception as e:
            logger.error(f"Error moving backward: {e}")

    def turn_left(self, speed: float = 50.0) -> None:
        """
        Turn robot left
        
        Args:
            speed (float): Speed percentage (0-100)
        """
        if not self.is_initialized:
            logger.warning("Robot not initialized. Cannot turn left.")
            return
            
        try:
            speed = max(0, min(100, speed))
            self.left_pwm.ChangeDutyCycle(0)  # Stop left motor
            self.right_pwm.ChangeDutyCycle(speed)  # Run right motor
            logger.info(f"Turning left at {speed}% speed")
        except Exception as e:
            logger.error(f"Error turning left: {e}")

    def turn_right(self, speed: float = 50.0) -> None:
        """
        Turn robot right
        
        Args:
            speed (float): Speed percentage (0-100)
        """
        if not self.is_initialized:
            logger.warning("Robot not initialized. Cannot turn right.")
            return
            
        try:
            speed = max(0, min(100, speed))
            self.left_pwm.ChangeDutyCycle(speed)  # Run left motor
            self.right_pwm.ChangeDutyCycle(0)  # Stop right motor
            logger.info(f"Turning right at {speed}% speed")
        except Exception as e:
            logger.error(f"Error turning right: {e}")

    def stop(self) -> None:
        """Stop all robot movement"""
        if not self.is_initialized:
            logger.warning("Robot not initialized. Cannot stop.")
            return
            
        try:
            self.left_pwm.ChangeDutyCycle(0)
            self.right_pwm.ChangeDutyCycle(0)
            logger.info("Robot stopped")
        except Exception as e:
            logger.error(f"Error stopping robot: {e}")

    def cleanup(self) -> None:
        """Clean up GPIO resources"""
        if not self.is_initialized:
            return
            
        try:
            self.stop()
            self.left_pwm.stop()
            self.right_pwm.stop()
            GPIO.cleanup()
            logger.info("GPIO cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main() -> None:
    """Main function to demonstrate robot functionality"""
    logger.info("Starting Simple Robot Controller")
    
    # Create robot instance
    try:
        robot = SimpleRobot()
    except Exception as e:
        logger.error(f"Failed to create robot: {e}")
        return
    
    # Demonstrate robot movement if GPIO is available
    if RPI_AVAILABLE:
        try:
            # Test movements
            robot.move_forward(30)
            time.sleep(2)
            
            robot.turn_left(40)
            time.sleep(1)
            
            robot.move_forward(20)
            time.sleep(1)
            
            robot.turn_right(30)
            time.sleep(1)
            
            robot.stop()
            time.sleep(1)
            
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        except Exception as e:
            logger.error(f"Error during robot demonstration: {e}")
        finally:
            robot.cleanup()
    else:
        # Simulation mode
        logger.info("Running in simulation mode - no actual GPIO control")
        logger.info("Robot would move forward, turn, and stop if GPIO was available")

if __name__ == "__main__":
    main()