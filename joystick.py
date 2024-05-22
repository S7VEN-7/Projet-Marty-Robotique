import pygame
import json, os
import connexion

class JoystickController ():
    def __init__(self):
        pygame.init()
        self.running = True
        self.LEFT, self.RIGHT, self.UP, self.DOWN  = False, False, False, False
        self.clock = pygame.time.Clock()

        # Initialize controller
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        with open(os.path.join(os.path.dirname(__file__), './game_controller/ps4_keys.json')) as file:
            button_keys = json.load(file)

        self.joystick_keys = []
        for key in button_keys:
            self.joystick_keys.append(key)

        # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }


    def run(self):
        # START OF GAME LOOP
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # BUTTON PRESSES
                self.handle_button_presses(event)

                # ANALOG INPUTS
                self.handle_analog_inputs(event)


    def handle_button_presses(self, event):
        # BUTTON PRESSES
        if event.type == pygame.JOYBUTTONDOWN:
            print(self.joystick_keys[event.button])
            if self.joystick_keys[event.button] == "cross":
                self.joystick_rumble(0.65, 1, 250)
                connexion.marty.celebrate()
            elif self.joystick_keys[event.button] == "circle":
                self.joystick_rumble(0, 1, 250)
            elif self.joystick_keys[event.button] == "triangle":
                self.joystick_rumble(0.65, 1, 250)
            elif self.joystick_keys[event.button] == "square":
                self.joystick_rumble(0.65, 0, 250)
            elif self.joystick_keys[event.button] == "share":
                self.running = False


    def handle_analog_inputs(self, event):
        # ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION:
            self.analog_keys[event.axis] = event.value
            # L-joystick
            # Horizontal Analog
            if abs(self.analog_keys[0]) > .2:
                if self.analog_keys[0] < -.2:
                    self.LEFT = True
                    print(self.analog_keys[0], " LEFT (L-joystick)")
                else:
                    self.LEFT = False

                if self.analog_keys[0] > .2:
                    self.RIGHT = True
                    print(self.analog_keys[0], " RIGHT (L-joystick)")
                else:
                    self.RIGHT = False

            # Vertical Analog
            if abs(self.analog_keys[1]) > .2:
                if self.analog_keys[1] < -.2:
                    self.UP = True
                    print(self.analog_keys[1], " UP (L-joystick)")
                else:
                    self.UP = False

                if self.analog_keys[1] > .2:
                    self.DOWN = True
                    print(self.analog_keys[1], " DOWN (L-joystick)")
                else:
                    self.DOWN = False
            
            # R-joystick
            # Horizontal Analog
            if abs(self.analog_keys[2]) > .2:
                if self.analog_keys[2] < -.2:
                    self.LEFT = True
                    print(self.analog_keys[2], " LEFT (R-joystick)")
                else:
                    self.LEFT = False

                if self.analog_keys[2] > .2:
                    self.RIGHT = True
                    print(self.analog_keys[2], " RIGHT (R-joystick)")
                else:
                    self.RIGHT = False

            # Vertical Analog
            if abs(self.analog_keys[3]) > .2:
                if self.analog_keys[3] < -.2:
                    self.UP = True
                    print(self.analog_keys[3], " UP (R-joystick)")
                else:
                    self.UP = False

                if self.analog_keys[3] > .2:
                    self.DOWN = True
                    print(self.analog_keys[3], " DOWN (R-joystick)")
                else:
                    self.DOWN = False

                # Triggers
            if self.analog_keys[4] == 1:  # Left trigger
                # color += 2
                print("LEFT TRIGGER")
            if self.analog_keys[5] == 1:  # Right Trigger
                # color -= 2
                print("RIGHT TRIGGER")


    def joystick_rumble(self, low, high, duration):
        # RUMBLE THE CONTROLLER
        self.joystick.rumble(low, high, duration)
        

############################################################################

# Run the controller

controller = JoystickController()
controller.run()

################################# LIGHTBAR #################################
# import time
# import hid
# #Pour le moment ça ne fonctionne pas...

# def set_ps4_lightbar_color(red, green, blue):
#     # Find the PS4 controller
#     devices = hid.enumerate(1356, 2508)
#     if len(devices) == 0:
#         print("PS4 controller not found.")
#     return

# # Open the device
# device_info = devices[0]
# device = hid.device()
# device.open_path(device_info['path'])

# # Prepare the HID report
# report = [0x11, 0x80, 0x00, 0x00, red, green, blue, 0x00]

# # Send the HID report to change the light bar color
# device.write(report)

# # Close the device
# device.close()

# # Example: Set light bar to red
# set_ps4_lightbar_color(255, 0, 0)
# time.sleep(5) # Keep it red for 5 seconds

# # Example: Set light bar to blue
# set_ps4_lightbar_color(0, 0, 255)
# time.sleep(5)
# set_ps4_lightbar_color(0, 255, 0)

############################################################################