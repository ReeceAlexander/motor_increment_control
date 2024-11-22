#!/usr/bin/env python3

import rospy
import os
import time

def move_motor_continuously(can_id="141", max_speed=500, step_size=1, delay=0.1):
    """
    Spins the motor continuously by incrementing its position in small steps.

    Args:
        can_id (str): CAN ID of the motor (default: "141").
        max_speed (int): Maximum speed in degrees per second (default: 500 dps).
        step_size (int): Number of degrees to increment per step (default: 1 degree).
        delay (float): Delay between commands to allow the motor to move (default: 0.1 seconds).
    """

    rospy.init_node('motor_increment_node')

    position = 0  # Start at 0 degrees
    
    while True:
        # Move the motor to the current position
        move_motor_to_position(position, max_speed, can_id)
        
        # Increment the position for the next step
        position += step_size
        
        # If the position exceeds 360, reset it to 0 (to create a continuous loop)
        if position >= 360:
            position = 0
        
        # Delay to allow the motor to move
        time.sleep(delay)

def move_motor_to_position(position_degrees, max_speed=500, can_id="141"):
    """
    Moves the motor to the specified position using the CAN protocol.

    Args:
        position_degrees (int): Target position in degrees.
        max_speed (int): Maximum speed in degrees per second (default: 500 dps).
        can_id (str): CAN ID of the motor (default: "141").
    """
    # Convert position to 0.01-degree units
    angle_control = int(position_degrees * 100)
    
    # Convert max speed to hexadecimal
    max_speed_low = max_speed & 0xFF
    max_speed_high = (max_speed >> 8) & 0xFF
    
    # Break position into 4 bytes
    angle_low = angle_control & 0xFF
    angle_byte2 = (angle_control >> 8) & 0xFF
    angle_byte3 = (angle_control >> 16) & 0xFF
    angle_high = (angle_control >> 24) & 0xFF
    
    # Construct the CAN data payload
    data = f"A4 00 {max_speed_low:02X} {max_speed_high:02X} {angle_low:02X} {angle_byte2:02X} {angle_byte3:02X} {angle_high:02X}"
    
    # Construct the cansend command
    cansend_command = f"cansend can0 {can_id}#{data.replace(' ', '')}"
    
    # Send the command using os.system
    print(f"Executing: {cansend_command}")
    os.system(cansend_command)

# Example usage
if __name__ == "__main__":
    try:
        move_motor_continuously()

    except rospy.ROSInterruptException:
        pass
