import random
import time
from marty_controller import get_marty, perform_action


def hexcolor(color: str) -> int:
    try:
        color_value = int(color, 16)
    except ValueError:
        raise ValueError("Invalid hex color format")

    if 0x300000 < color_value <= 0x339999:
        return 1
    elif 0x340000 < color_value <= 0x390000:
        return 2
    elif 0x3a0000 < color_value <= 0x3fffff:
        return 3
    elif 0x900000 < color_value <= 0xa50000:
        return 4
    elif color_value > 0xab0000:
        return 5
    else:
        return 0

def get_color_sensor_hex(marty, add_on_or_side: str) -> str:
    if marty is None:
        return "000000"  #

    hex_color = marty.get_color_sensor_hex(add_on_or_side)
    return hex_color

def get_color_reading(marty, add_on_or_side: str) -> str:
    hex_color = get_color_sensor_hex(marty, add_on_or_side)
    return hex_color

def print_grid(action_table):
    grid = [[' ' for _ in range(3)] for _ in range(3)]
    for entry in action_table:
        x, y = entry["position"]
        color = entry.get("color", "Unknown")
        if isinstance(color, int):
            color_str = str(color)
        else:
            color_str = color

        grid[2 - x][y] = color_str[0].upper()

    print("   | 0 | 1 | 2 ")
    print("---|---|---|---")
    for i in range(2, -1, -1):
        print(f" {i} | {' | '.join(grid[i])}")

def trouver_trajectoire(start_x, start_y):
    action_table = []

    marty = get_marty()

    color_hex = get_color_reading(marty, "left")
    color_category = hexcolor(color_hex)

    position_record = {
        "position": (start_x, start_y),
        "action": "start",
        "color": color_category
    }
    action_table.append(position_record)

    # Set the initial position
    x, y = start_x, start_y
    actions_map = {
        (0, 0): [
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1)  # Move up
        ],
        (0, 1): [
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1) , # Move up
            ("tourner a gauche", -1, 0),  # Move left
            ("reculer", 0, -1),  # Move down
        ],
        (0, 2): [
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1) , # Move up
            ("tourner a droite", 1, 0),  # Move right
        ],
        (1, 0): [
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1)  # Move up
        ],
        (1, 1): [
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
        ],
        (1, 2): [
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
        ],
        (2, 0): [
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a gauche", -1, 0),  # Move left
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("avancer", 0, 1) , # Move up
            ("tourner a gauche", -1, 0),  # Move left
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1)  # Move up
        ],
        (2, 1): [
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1)  # Move up
        ],
        (2, 2): [
            ("avancer", 0, 1),  # Move up
            ("avancer", 0, 1),  # Move up
            ("tourner a droite", 1, 0),  # Move right
            ("tourner a droite", 1, 0),  # Move right
            ("reculer", 0, -1),  # Move down
            ("reculer", 0, -1),  # Move down
            ("tourner a gauche", -1, 0),  # Move left
            ("avancer", 0, 1)  # Move up
        ],
    }


    actions_sequence = actions_map.get((x, y), [])


    for action, dx, dy in actions_sequence:
        # Perform the action

        time.sleep(5)


        perform_action(action, marty)


        x += dx
        y += dy


        x = max(0, min(x, 2))
        y = max(0, min(y, 2))


        color = None
        for entry in action_table:
            if entry["position"] == (x, y):
                color = entry["color"]
                break


        if color is None:
            color_hex = get_color_reading(marty, "left")
            color = hexcolor(color_hex)


        position_record = {
            "position": (x, y),
            "action": action,
            "color": color
        }
        action_table.append(position_record)

    return action_table


if __name__ == "__main__":

    start_x = int(input("Enter the starting x-coordinate (0, 1, or 2): "))
    start_y = int(input("Enter the starting y-coordinate (0, 1, or 2): "))


    action_table = trouver_trajectoire(start_x, start_y)


    print("Position | Action | Color Category")
    for entry in action_table:
        print(f"{entry['position']} | {entry['action']} | {entry['color']}")


    print("\nGrid representation of color categories:")
    print_grid(action_table)
