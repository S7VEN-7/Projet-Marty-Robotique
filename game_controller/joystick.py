import inputs

pads = inputs.devices.gamepads

if len(pads) == 0:
    raise Exception("Aucune manette de jeu n'est connectée !")

while True:
    events = inputs.get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)