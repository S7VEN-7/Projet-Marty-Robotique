# Define common style for buttons
COMMON_BUTTON_STYLE = """
    QPushButton {
        background-color: #87CEEB;  /* Sky blue color */
        color: white;
        border: 2px solid #4682B4;  /* Steel blue color */
        padding: 10px;
        border-radius: 10px;  /* Rounded corners */
    }
    QPushButton:hover {
        background-color: #4682B4;  /* Darker blue when hovered */
    }
    QPushButton:pressed {
        background-color: #87CEEB;
        border: 2px solid #87CEEB;
    }
"""



# Specific style for action buttons (Run and Reset)
BUTTON_STYLE_ACTION = COMMON_BUTTON_STYLE

# Specific style for draggable buttons
BUTTON_STYLE_DRAGGABLE = COMMON_BUTTON_STYLE

# Define the style for the drop area
DROP_AREA_STYLE =  COMMON_BUTTON_STYLE
