# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:47:50 2018

@author: Victor Rogalev
"""

import pygame,time


pygame.init()

# Set up the joystick
pygame.joystick.init()

my_joystick = None
joystick_names = []

# Enumerate joysticks
for i in range(0, pygame.joystick.get_count()):   # returns number of joysticks
    joystick_names.append(pygame.joystick.Joystick(i).get_name())

print (joystick_names)

# By default, load the first available joystick.
if (len(joystick_names) > 0):
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

print ('number of axes: ', my_joystick.get_numaxes())
print ('number of buttons: ', my_joystick.get_numbuttons())
print ('number of hats: ', my_joystick.get_numhats())

for i in range(0, my_joystick.get_numaxes()):
    print ("position of axis ", i, " :", my_joystick.get_axis(i))
    
    
for i in range(0, my_joystick.get_numbuttons()):
    print ("pressed buttons ", i, " :", my_joystick.get_button(i))
    
for i in range(0, my_joystick.get_numhats()):
    print ("hat position ", i, " :", my_joystick.get_hat(i))

done = False

motion_flag = False
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYHATMOTION:
            print("Joystick button pressed. ", event.value[0])
            new = event.value
            print (new[0])
            print (type(event.value))
            
        elif event.type == pygame.JOYAXISMOTION:
            time.sleep(0.1)
            if (event.axis == 0) and (my_joystick.get_button(4)==1):               
                if (my_joystick.get_axis(0)>0.5):
#                    
#                    while (my_joystick.get_axis(0)>0.1):
#                    time.sleep(0.05)
                    if not motion_flag:
                        print ('start moving')
                        motion_flag = True
                    else:
                        print ('keep moving')
                else:
                    if motion_flag:
                        print ('stopped')
                        motion_flag = False
            elif (event.axis == 0) and (my_joystick.get_button(4)==0) and (motion_flag):
                print ('stopped')
                motion_flag = False
                
#            print ('Axis motion ', event.axis, event.value)
#            if event.button == 0:
#                print ('stop button was pressed')
#                print (' L1 button is ', my_joystick.get_button(4))

#     A couple of joystick functions...
#    def check_axis(self, p_axis):
#        if (self.my_joystick):
#            if (p_axis &lt; self.my_joystick.get_numaxes()):
#                return self.my_joystick.get_axis(p_axis)
#
#        return 0
#
#    def check_button(self, p_button):
#        if (self.my_joystick):
#            if (p_button &lt; self.my_joystick.get_numbuttons()):
#                return self.my_joystick.get_button(p_button)
#
#        return False

#    def check_hat(self, p_hat):
#        if (self.my_joystick):
#            if (p_hat &lt; self.my_joystick.get_numhats()):
#                return self.my_joystick.get_hat(p_hat)
#
#        return (0, 0)


#g_keys = pygame.event.get()
#
#
#
#        for event in g_keys:
#            if (event.type == KEYDOWN and event.key == K_ESCAPE):
#                self.quit()
#                return
#
#            elif (event.type == QUIT):
#                self.quit()
#                return
#
#        for i in range(0, self.my_joystick.get_numaxes()):
#            if (self.my_joystick.get_axis(i)):
#                pygame.draw.circle(self.screen, (0, 0, 200), 
#                                   (20 + (i * 30), 50), 10, 0)
#            else:
#                pygame.draw.circle(self.screen, (255, 0, 0), 
#                                   (20 + (i * 30), 50), 10, 0)
#
#
#        for i in range(0, self.my_joystick.get_numbuttons()):
#            if (self.my_joystick.get_button(i)):
#                pygame.draw.circle(self.screen, (0, 0, 200), 
#                                   (20 + (i * 30), 100), 10, 0)
#            else:
#                pygame.draw.circle(self.screen, (255, 0, 0), 
#                                   (20 + (i * 30), 100), 10, 0)
#
#            self.center_text("%d" % i, 20 + (i * 30), 100, (255, 255, 255))
#
#        self.draw_text("POV Hats (%d)" % self.my_joystick.get_numhats(), 
#                       5, 125, (255, 255, 255))
#
#        for i in range(0, self.my_joystick.get_numhats()):
#            if (self.my_joystick.get_hat(i) != (0, 0)):
#                pygame.draw.circle(self.screen, (0, 0, 200), 
#                                   (20 + (i * 30), 150), 10, 0)
#            else:
#                pygame.draw.circle(self.screen, (255, 0, 0), 
#                                   (20 + (i * 30), 150), 10, 0)
#
