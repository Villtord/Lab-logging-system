# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:23:57 2018

@author: ARPES
"""

def send_command (com_name, command):

    import serial.tools.list_ports
    
    """ Open COM-port and send/read the command"""
    ser = serial.Serial(com_name,                   
                         baudrate=57600,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=0.2)
    
    """Write a command(s) to pressure controller and read the reply """
    try:
        command = command + (sum(command) % 256).to_bytes(1,byteorder='big', signed=False)  # add checksum to command
    except:
        print ('command ready')
        pass
    
    try:
        ser.write(command)
        read_str = ser.readall()
        " from manual - bytes 5,6,7,8 give the value"
        read_str = int.from_bytes(read_str[4:8], byteorder='big', signed=True)               
    except:
        pass    
    
    ser.close()
    try:
#        read_str = '10000'
        return read_str
    except:
        pass        