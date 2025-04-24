#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Test script for the tap_space_key movement
# This script sends the tap_space_key movement data directly to the robot
import sys
import os
import threading

# Add the OpenCatPythonAPI directory to the Python path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'OpenCatPythonAPI'))

from PetoiRobot import *

def main():
    try:
        # Connect to the robot
        print("Connecting to robot...")
        

        # def listen():
        #     serialObject = Communication('/dev/cu.usbmodem56D00028531', 115200, 1)
        #     print(serialObject.Receive_data(0))
        # t = threading.Thread(
        #     target=listen,
        #     daemon=True
        # )
        # t.start()
        dog_port = Communication('/dev/cu.usbmodem56D00028531', 115200, 1)
        goodPorts = [dog_port]
        # goodPorts = {}
        # connectPort(goodPorts)
        res = send(goodPorts, ['kbalance', 1])
        attempt = 1    
        while (res == -1):
            attempt += 1
            time.sleep(0.5)
            res = send(goodPorts, ['kbalance', 1])    
            if attempt == 10:
                print("Failed to send movement") 
                closePort()
                exit(0)
        # Define the tap_space_key movement data
        # Format: [period, offset, transformSpeed, skillHeader, frameSize, ...frames]
        # Each frame has 16 joint angles (0-15) plus timing parameters
        start_pose_data = [
            1, 0, -17, 1,# Frame 1: Starting position
            0, 0, 0, 0, 0, 0, 0, 0,  # Joints 1-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45  # Joints 12-15 
        ]
        tap_space_data_r = [
            -4, 0, -17, 1,  # 4 frames, no offset, no transform speed, skill header 1
            0, 3, 1,     # Additional parameters
            
            # Frame 1: Lift
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 70, 75, 75,  # Joints 8-11
            0, -75, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
            
            # Frame 2: Press
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 12, 75, 75,  # Joints 8-11
            0, -5, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
            
            # Frame 3: Lift
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 65, 75, 75,  # Joints 8-11
            0, -68, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters  
            
            # Frame 4: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
        ]
        
        tap_space_data_l = [
            -4, 0, -17, 1,  # 4 frames, no offset, no transform speed, skill header 1
            0, 3, 1,     # Additional parameters
            
            # Frame 1: Lift
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            70, 45, 75, 75,  # Joints 8-11
            -75, 0, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
            
            # Frame 2: Press
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            12, 45, 75, 75,  # Joints 8-11
            -5, 0, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
            
            # Frame 3: Lift
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            65, 45, 75, 75,  # Joints 8-11
            -68, 0, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters  
            
            # Frame 4: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            15, 0, 0, 0,  # Timing parameters
        ]

        scoot_forward_data_r = [
            -4, 0, -17, 1,  # 4 frames, no offset, no transform speed, skill header 1
            0, 3, 3,     # start frame, end frame, and loop times# Additional parameters
            
            # Frame 1: right leg
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 80, 75,  # Joints 8-11
            0, 0, -30, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters

            # Frame 2: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters

            # Frame 3: left leg
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 80,  # Joints 8-11
            0, 0, -45, -30,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters

            # Frame 4: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters
        ]
        scoot_forward_data_l = [
            -4, 0, -17, 1,  # 4 frames, no offset, no transform speed, skill header 1
            0, 3, 3,     # start frame, end frame, and loop times# Additional parameters

            # Frame 1: left leg
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 80,  # Joints 8-11
            0, 0, -45, -30,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters


            # Frame 2: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters

            # Frame 3: right leg
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 80, 75,  # Joints 8-11
            0, 0, -30, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters

            # Frame 4: Return to start
            0, 0, 0, 0,  # Joints 0-3
            0, 0, 0, 0,  # Joints 4-7
            45, 45, 75, 75,  # Joints 8-11
            0, 0, -45, -45,  # Joints 12-15
            8, 0, 0, 0,  # Timing parameters
        ]
        # Send the movement data directly
        print("Sending start_pose_data pose...")
        res = send(goodPorts, ['K', start_pose_data, 1]) 
        print(res)
        # serialObject.Send_data(b'v')
        # print(serialObject.Receive_data(0))
        for i in range(6):
            if i % 2 == 0:
                tap = tap_space_data_r
                move = scoot_forward_data_r
            else:
                tap = tap_space_data_l
                move = scoot_forward_data_l
            res = send(goodPorts, ['K', tap, 1])
            if res == -1:
                 print("Retry")
                 time.sleep(0.5)
                 res = send(goodPorts, ['K', tap, 1])
                 if res == -1:
                      print("Connection Error")
                      closePort()
                      exit(0)
            # serialObject.Send_data(b'v')
            # print(serialObject.Receive_data(0))
            res = send(goodPorts, ['K', move, 1])            # Wait for the movement to complete 
            if res == -1:
                print("Retry")
                time.sleep(0.5)
                res = send(goodPorts, ['K', move, 1])
                if res == -1:
                    print("Connection Error")
                    closePort()
                    exit(0)
            # serialObject.Send_data(b'v')
            # print(serialObject.Receive_data(0))
        # Close the connection
        print("Closing connection...")
        closePort()
        print("Connection closed. Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            closePort()
        except:
            pass

if __name__ == "__main__":
    main() 