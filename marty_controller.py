from martypy import Marty, MartyConnectException

def get_marty():
    try:
        marty = Marty("wifi", "192.168.0.104", blocking=True)  # replace with the appropriate address for your Marty
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
    elif action == "circle_dance":
        marty.circle_dance()
    elif action == "eyes":
        marty.eyes(pose_or_angle="neutral")  # or any other pose you want
    elif action == "piww":
        marty.kick()
    elif action == "arms":
        # Example angles: left_angle = 90, right_angle = -90
        marty.arms(left_angle=90, right_angle=-90, move_time=2000)  # Adjust angles and move time as needed
