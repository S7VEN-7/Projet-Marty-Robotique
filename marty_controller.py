from martypy import Marty, MartyConnectException

def get_marty():
    try:
        marty = Marty("wifi", "192.168.0.107", blocking=True)  # replace with the appropriate address for your Marty
        return marty
    except MartyConnectException as e:
        print(f"Failed to connect to Marty: {e}")
        return None

def perform_action(action, marty):
    print(f"Performing action for {action}")
    if action == "avancer":
        marty.walk(num_steps=2)
    elif action == "reculer":
        marty.walk(num_steps=2, step_length=-25)
    elif action == "tourner a droite":
        marty.sidestep("right", 2)
    elif action == "tourner a gauche":
        marty.sidestep("left", 2)
    elif action == "demi_droite":
        marty.walk(4, 'auto', -13, 30, 2000)
    elif action == "demi_gauche":
        marty.walk(4, 'auto', 13, 30, 2000)