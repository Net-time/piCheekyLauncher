#!/usr/bin/python
# piCheekyLauncher V1.0, check repository on github for more information
#  Requirements:
#   * A Dream Cheeky Thunder USB Missile Launcher "original v2"
#   * Python 2.6+
#   * A Raspberry Pi
#   * Python PyUSB Support and its dependencies
#     sudo apt-get update
#     sudo apt-get install libusb-dev
#
#   # May work on Windows, Mac and Linux
############################################################################

import sys
import platform
import time
#import re
#import base64
import usb.core
import usb.util

# Protocol command bytes
FIRE    = 0x10
STOP    = 0x20
#[direction], Byte to read for limit switch, switch "on" bit value , command to send.
direction_list = [["down", 0, 64, 0x02],["up", 0, 128, 0x01],
                  ["left", 1, 4, 0x04],["right", 1, 8, 0x08]]

DEVICE = None
#DEVICE_TYPE = None

def usage():
    print "Usage: python piCheekyLauncher.py [command] [value]"
    print ""
    print "     up     - move up    <value> milliseconds"
    print "     down   - move down  <value> milliseconds"
    print "     right  - move right <value> milliseconds"
    print "     left   - move left  <value> milliseconds"
    print "     fire   - fire <value> times (between 1-3)"
    print "     charge - precharge for faster fire of shot 1"
    print "     center - park at center position"

def setup_usb():
    global DEVICE 
#    global DEVICE_TYPE
    DEVICE = usb.core.find(idVendor=0x1941, idProduct=0x8021)
    if DEVICE is None:
        raise ValueError('Missile device ID 1941:8021 not found, use lsusb to list your devices')
    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    
    DEVICE.set_configuration()

def send_cmd(cmd):
    DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])
    
def send_move(cmd, duration_ms):
    send_cmd(direction_list[cmd][3])
    StopTime = time.time()+ duration_ms / 1000.0
    while StopTime >= time.time():
        # Read switch states and check if limit switch comes on
        ret = DEVICE.read(0x81,8, 100)
        if ret[direction_list[cmd][1]]&direction_list[cmd][2] != 0:
            print 'Limit reached' 
            break   
    send_cmd(STOP)

def run_command(command, value):   
    command = command.lower()    
    # Check if command is a direction
    for x in range(0,len(direction_list)):
        try:
            cmd_no = x
            pos = direction_list[x].index(command)
            break
        except:
            cmd_no = -1
            pass
    if cmd_no != -1 :
        send_move( cmd_no,value)
    elif command == "center":
        # Move to bottom-left
        print command
        send_move(0, 2300)
        send_move(3, 20000)
        send_move(1, 1100)
        send_move(2, 9000)
    elif command == "fire" or command == "charge":
        if value < 1 or value > 3:
            value = 1
        ret = DEVICE.read(0x81,8, 100)
        for i in range(value):
            send_cmd(FIRE)
            while ret[1]&128 == 0:
                ret = DEVICE.read(0x81,8, 100)
            if command == "fire":
                while ret[1]&128 != 0:
                    ret = DEVICE.read(0x81,8, 100)
            send_cmd(STOP)
    else:
        print "%s unkown command" % command

def main(args):
    if len(args) < 2:
        usage()
        sys.exit(1)
    setup_usb()
    # Process any passed commands or command_sets
    command = args[1]
    value = 0
    if len(args) > 2:
        value = int(args[2])
    run_command(command, value)

if __name__ == '__main__':
    main(sys.argv)
