import pygame
import json, os
import time

import hid

#### Pour le moment ça ne fonctionne pas... ####
################################# PS4 CONTROLLER LIGHTBAR #################################
# def set_ps4_lightbar_color(red, green, blue):
#     # Find the PS4 controller
#     devices = hid.enumerate(1356, 2508)
#     if len(devices) == 0:
#         print("PS4 controller not found.")
#         return

#     # Open the device
#     device_info = devices[0]
#     device = hid.device()
#     device.open_path(device_info['path'])

#     # Prepare the HID report
#     report = [0x11, 0x80, 0x00, 0x00, red, green, blue, 0x00]

#     # Send the HID report to change the light bar color
#     device.write(report)

#     # Close the device
#     device.close()

# # Example: Set light bar to red
# set_ps4_lightbar_color(255, 0, 0)
# time.sleep(5)  # Keep it red for 5 seconds
# # Example: Set light bar to blue
# set_ps4_lightbar_color(0, 0, 255)
# time.sleep(5)
# set_ps4_lightbar_color(0, 255, 0)


################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
# DISPLAY_W, DISPLAY_H = 960, 570
# canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
# window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
# player = pygame.Rect(DISPLAY_W/2, DISPLAY_H/2, 60,60)
LEFT, RIGHT, UP, DOWN  = False, False, False, False
clock = pygame.time.Clock()
# color = 0
###########################################################################################

#Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

with open(os.path.join(os.path.dirname(__file__), 'ps4_keys.json')) as file:
    button_keys = json.load(file)
# 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

# START OF GAME LOOP
while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # HANDLES BUTTON PRESSES
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['left_arrow']:
                LEFT = True
                print("LEFT")
            if event.button == button_keys['right_arrow']:
                RIGHT = True
                print("RIGHT")
            if event.button == button_keys['down_arrow']:
                DOWN = True
                print("DOWN")
            if event.button == button_keys['up_arrow']:
                UP = True
                print("UP")
            if event.button == button_keys['triangle']:
                print("TRIANGLE")
            if event.button == button_keys['square']:
                print("SQUARE")
            if event.button == button_keys['circle']:
                print("CIRCLE")
            if event.button == button_keys['cross']:
                print("CROSS")
            if event.button == button_keys['L1']:
                print("L1")
            if event.button == button_keys['R1']:
                print("R1")
            if event.button == button_keys['L2']:
                print("L2")
            if event.button == button_keys['R2']:
                print("R2")


            if event.button == button_keys['share']:
                print("SHARE")

                running = False


            if event.button == button_keys['options']:
                print("OPTIONS")
            if event.button == button_keys['L3']:
                print("L3")
            if event.button == button_keys['R3']:
                print("R3")
            if event.button == button_keys['PS']:
                print("PS")
            if event.button == button_keys['touchpad']:
                print("TOUCHPAD")
            

        # HANDLES BUTTON RELEASES
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == button_keys['left_arrow']:
                LEFT = False
                print("LEFT RELEASED")
            if event.button == button_keys['right_arrow']:
                RIGHT = False
                print("RIGHT RELEASED")
            if event.button == button_keys['down_arrow']:
                DOWN = False
                print("DOWN RELEASED")
            if event.button == button_keys['up_arrow']:
                UP = False
                print("UP RELEASED")

        #HANDLES ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
            # print(analog_keys)
            # Horizontal Analog

            # L-joystick
            if abs(analog_keys[0]) > .2:
                if analog_keys[0] < -.2:
                    LEFT = True
                    print(analog_keys[0], " LEFT (L-joystick)")
                else:
                    LEFT = False

                if analog_keys[0] > .2:
                    RIGHT = True
                    print(analog_keys[0], " RIGHT (L-joystick)")
                else:
                    RIGHT = False

            # Vertical Analog
            if abs(analog_keys[1]) > .2:
                if analog_keys[1] < -.2:
                    UP = True
                    print(analog_keys[1], " UP (L-joystick)")
                else:
                    UP = False

                if analog_keys[1] > .2:
                    DOWN = True
                    print(analog_keys[1], " DOWN (L-joystick)")
                else:
                    DOWN = False
            
            # R-joystick
            if abs(analog_keys[2]) > .2:
                if analog_keys[2] < -.2:
                    LEFT = True
                    print(analog_keys[2], " LEFT (R-joystick)")
                else:
                    LEFT = False

                if analog_keys[2] > .2:
                    RIGHT = True
                    print(analog_keys[2], " RIGHT (R-joystick)")
                else:
                    RIGHT = False

            # Vertical Analog
            if abs(analog_keys[3]) > .2:
                if analog_keys[3] < -.2:
                    UP = True
                    print(analog_keys[3], " UP (R-joystick)")
                else:
                    UP = False

                if analog_keys[3] > .2:
                    DOWN = True
                    print(analog_keys[3], " DOWN (R-joystick)")
                else:
                    DOWN = False

                # Triggers
            if analog_keys[4] == 1:  # Left trigger
                # color += 2
                print("LEFT TRIGGER")
            if analog_keys[5] == 1:  # Right Trigger
                # color -= 2
                print("RIGHT TRIGGER")

    # Handle Player movement
    # if LEFT:
    #     player.x -=5 #*(-1 * analog_keys[0])
    # if RIGHT:
    #     player.x += 5 #* analog_keys[0]
    # if UP:
    #     player.y -= 5
    # if DOWN:
    #     player.y += 5

    # if color < 0:
    #     color = 0
    # elif color > 255:
    #     color = 255


################################# UPDATE WINDOW AND DISPLAY #################################
# canvas.fill((255,255,255))
# pygame.draw.rect(canvas, (0,0 + color,255), player)
# window.blit(canvas, (0,0))
clock.tick(60)
# pygame.display.update()