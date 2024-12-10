from tkinter import *
from utilities.constants import *

class ColoredButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=FLAT,  # Remove button relief
            highlightthickness=0,  # Remove highlight
            padx=7,  # Add horizontal padding
            pady=7,  # Add vertical padding
            font=("Arial Bold", 10),  # Set font
            foreground="black",  # Text color
            background=BUTTON_COLOR,  # Background color
            cursor="hand2"  # Hover cursor

        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    # Наведение курсора на кнопку.
    def on_hover(self, event):
        self.config(background="#addbff")

    # Отведение курсора от кнопки.
    def on_leave(self, event):
        self.config(background="lightblue")
