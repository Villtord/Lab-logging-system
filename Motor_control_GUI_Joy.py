#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 23:12:15 2018

@author: villtord
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal,QTimer,QThread
from Simple_UI_3 import Ui_MainWindow
import send_motor
import time

import pygame

global com_port_name, get_pos, motor_stop, move_abs
global offset_steps, offset_mm, steps_per_mm
global position_LEED, position_EXCH, position_PASS

com_port_name = 'COM3'

get_pos = bytearray ([1,6,1,0,0,0,0,0])
motor_stop = bytearray ([1,3,0,0,0,0,0,0,4])
move_abs = bytearray ([1,4,0,0])
move_rel = bytearray ([1,4,1,0])
roll_speed = 300
roll_right = bytearray ([1,1,0,0])
roll_left = bytearray ([1,2,0,0])

offset_steps = -716948
offset_mm   = 245
steps_per_mm = 16026.45

position_LEED = 244
position_EXCH = 75
position_PASS = 10

def convert (value,flag):
    
    global offset_steps, offset_mm, steps_per_mm

    if flag == True:                #make convertion from mm to microsteps

        result = int (offset_steps + (offset_mm-value)*steps_per_mm)
    
    else:                           #make convertion from microsteps to mm
        
        result = offset_mm - (value-offset_steps)/steps_per_mm
    
    return result


class update_position(QThread):
    
    global get_pos, com_port_name
    
    new_value_trigger = pyqtSignal(float)
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()        
        print ("get_value initializeed")

    def update_position (self):
        
        self.check = get_pos
        try:
            self.position = int (send_motor.send_command(com_port_name, self.check)) # in microsteps
            self.position_mm = convert(self.position, False)
            self.new_value_trigger.emit(self.position_mm)
        except:
            print ('can not get the position')
            pass
        
class joystick_control_class(QThread):
    
    global get_pos, com_port_name
    
    joystick_trigger = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()
    
        pygame.init()
        
        pygame.joystick.init()
        
        self.my_joystick = None
        self.joystick_names = []
        
        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):   # returns number of joysticks
             self.joystick_names.append(pygame.joystick.Joystick(i).get_name())
        
        print ( self.joystick_names)
        
        # By default, load the first available joystick.
        if (len( self.joystick_names) > 0):
             self.my_joystick = pygame.joystick.Joystick(0)
             self.my_joystick.init()        
        print ("joystick control initializeed")
#        print ('number of axes: ',  self.my_joystick.get_numaxes())
#        print ('number of buttons: ',  self.my_joystick.get_numbuttons())
#        print ('number of hats: ',  self.my_joystick.get_numhats())

    def start (self):
        done = False
        motion_flag = False
        # -------- Main Program Loop -----------
        while done == False:
            time.sleep(0.05)
            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                
                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed. ", event.button)
                    if event.button == 0:
                        print ('stop button was pressed')
                        self.joystick_trigger.emit('stop')
                    elif (event.button == 2) and ((self.my_joystick.get_button(4)==1) or (self.my_joystick.get_button(5)==1)):
                        print ('LEED')
                        self.joystick_trigger.emit ('LEED')
                    elif (event.button == 3) and ((self.my_joystick.get_button(4)==1) or (self.my_joystick.get_button(5)==1)):
                        print ('EXCH')
                        self.joystick_trigger.emit ('EXCH')
                    elif (event.button == 1) and ((self.my_joystick.get_button(4)==1) or (self.my_joystick.get_button(5)==1)):
                        print ('PASS')
                        self.joystick_trigger.emit ('PASS')
                    
                elif event.type == pygame.JOYHATMOTION:
                    if (event.value[0] == 1) and ((self.my_joystick.get_button(4)==1) or (self.my_joystick.get_button(5)==1)):
                        print ('shifting right')
                        self.joystick_trigger.emit ('shift_right')
                    elif (event.value[0] == -1) and ((self.my_joystick.get_button(4)==1) or (self.my_joystick.get_button(5)==1)):
                        print ('shifting left')
                        self.joystick_trigger.emit ('shift_left')
                        
                if event.type == pygame.JOYBUTTONUP and ((event.button == 4) or (event.button == 5)):
                    print("Joystick safety button UNpressed. ", event.button)
                    if (abs(self.my_joystick.get_axis(4))>0.8):
                        print ('stop button was pressed')
                        motion_flag = False
                        self.joystick_trigger.emit('stop')
                
                
                elif event.type == pygame.JOYAXISMOTION:
                    time.sleep(0.1)
                    
                    if (event.axis == 4) and (self.my_joystick.get_button(4) == 1) and (self.my_joystick.get_button(5) == 1):               
                        if (self.my_joystick.get_axis(4)>0.8):
                            if not motion_flag:
                                print ('start moving right')
                                motion_flag = True
                                self.joystick_trigger.emit('move_right')
                            else:
                                print ('keep moving right')
                        elif (self.my_joystick.get_axis(4)<-0.8):
                            if not motion_flag:
                                print ('start moving left')
                                motion_flag = True
                                self.joystick_trigger.emit('move_left')
                            else:
                                print ('keep moving left')
                        else:
                            if motion_flag:
                                print ('stopped')
                                motion_flag = False
                                self.joystick_trigger.emit('stop')
                    elif (event.axis == 4) and (motion_flag) and ((self.my_joystick.get_button(4) == 0) or (self.my_joystick.get_button(5) == 0)):
                        print ('stopped')
                        motion_flag = False
                        self.joystick_trigger.emit('stop')
        
    def stop (self):
        
        self.my_joystick.quit() 



class ExampleApp(QWidget, Ui_MainWindow):
    
    global com_port_name, get_pos, motor_stop, move_abs, roll_right, roll_left
    global position_LEED, position_EXCH, position_PASS
            
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        """ Start monitoring the current position and connect all signals"""

        self.update_thread = update_position()
        
        self.pushButton.clicked.connect(lambda: self.move_motor(self.lineEdit.text()))
        self.pushButton_1.clicked.connect(self.joystick_operation)
        self.pushButton_2.clicked.connect(self.stop_motor)
        self.pushButton_3.clicked.connect(lambda: self.shift_motor(1,self.lineEdit_3.text()))   # L shift
        self.pushButton_4.clicked.connect(lambda: self.shift_motor(-1,self.lineEdit_3.text()))  # R shift
        self.pushButton_5.clicked.connect(lambda: self.move_motor(self.lineEdit_4.text()))      # LEED
        self.pushButton_6.clicked.connect(lambda: self.move_motor(self.lineEdit_5.text()))      # EXCH
        self.pushButton_7.clicked.connect(lambda: self.move_motor(self.lineEdit_6.text()))      # PASS
        
        self.start()
        
        """ Show the LEED, EXCH and PASS positions """
        self.lineEdit_4.setText(str(position_LEED))
        self.lineEdit_5.setText(str(position_EXCH))
        self.lineEdit_6.setText(str(position_PASS))
        
    def start (self):
            
        self.update_thread.new_value_trigger.connect(self.update_position_label)
        
        self.timer_x = QTimer(self)
        self.timer_x.timeout.connect(self.update_thread.update_position)        
        self.timer_x.start(1000)
        
    def stop_motor(self):
        
        self.command = motor_stop                                            # construct command
        send_motor.send_command(com_port_name, self.command)                   # senf command
        
    def update_position_label (self, value):
        
        self.position_mm = value
        self.lineEdit_2.setText("{:1.1f}".format(self.position_mm))
            
    def roll_motor (self, value):
        
        if (float (value) >= 0):
            print ('rolling right ', value)
            self.command = roll_right+roll_speed.to_bytes(4, byteorder='big',signed=True)        
            send_motor.send_command(com_port_name, self.command)
        else:
            print ('rolling left ', value)
            self.command = roll_left+roll_speed.to_bytes(4, byteorder='big',signed=True)         
            send_motor.send_command(com_port_name, self.command)
            
    def move_motor (self, value):
        
        if (float (value) <= 265) & (float (value) >= 0):
            self.lineEdit.setText(value)
            self.value = convert (float(value), True)
            print ('moving to ', self.value)
            self.command = move_abs + (self.value).to_bytes(4, byteorder='big',signed=True)        
            send_motor.send_command(com_port_name, self.command)

    def shift_motor(self, flag, value):
        
        self.shift=float(value)
        if (self.shift <= 50) & (self.shift >= 0):
            if flag == -1:
                self.shift = (-1)*self.shift
            self.new_value = float(self.lineEdit_2.text())+self.shift
            self.lineEdit.setText(str(self.new_value))
            print (self.new_value)
            self.shift_steps = convert (self.new_value, True)
            print (self.shift_steps)
            self.command = move_abs + (self.shift_steps).to_bytes(4, byteorder='big',signed=True)
            send_motor.send_command(com_port_name, self.command)
    

    def joystick_operation(self):
        
        if self.pushButton_1.isChecked():
            self.pushButton_1.setText("Disable Joystick")
            self.joystick_monitor = joystick_control_class()
            self.joystick_monitor.joystick_trigger.connect (self.joystick_processing)
            
            self.joystick_monitor.start()
        else:
            print ("not checked")
            self.pushButton_1.setText("Enable Joystick")
            self.joystick_monitor.stop()
            
    def joystick_processing(self, parameter):
        
        self.joystick_command = parameter
        
        if self.joystick_command == 'stop':
            self.stop_motor()
        elif self.joystick_command == 'shift_left':
            self.shift_motor(1,self.lineEdit_3.text())
        elif self.joystick_command == 'shift_right':
            self.shift_motor(-1,self.lineEdit_3.text())
        elif self.joystick_command == 'LEED':
            self.move_motor(self.lineEdit_4.text())
        elif self.joystick_command == 'EXCH':
            self.move_motor(self.lineEdit_5.text())
        elif self.joystick_command == 'PASS':
            self.move_motor(self.lineEdit_6.text())
        elif self.joystick_command == 'move_right':
            self.roll_motor(1)
        elif self.joystick_command == 'move_left':
            self.roll_motor(-1)
            
    def __del__ (self):
        
        self.stop_motor()
        self.update_thread.quit()
        self.timer_x.stop()
        self.timer_x.deleteLater()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.setWindowTitle("Motor control")
    form.show()                         # Show the form
    sys.exit(app.exec_())
    app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function