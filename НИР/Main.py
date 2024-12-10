# Интерфейс
from gui.GUI import *

# Файл с константами.
from utilities.constants import *


# Класс входной точки в программу.
class Main:
    def __init__(self):
        # Класс интерфейса.
        self.gui = GUI(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_BG)
        self.gui.run()


# Запуск приложения.
app = Main()
