import glfw
from OpenGL.GL import *

# Инициализация GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Создаем окно с контекстом OpenGL
window = glfw.create_window(500, 500, "House", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)

# Устанавливаем цвет фона
glClearColor(1, 1, 1, 1)  # Фон


def draw_house(r, g, b, size_x, size_y):
    # Основание
    glColor3f(r, g, b)  # Серый
    glBegin(GL_QUADS)
    glVertex2f(-size_x, -size_y)  # Нижний левый угол
    glVertex2f(size_x, -size_y)  # Нижний правый угол
    glVertex2f(size_x, size_y)  # Верхний правый угол
    glVertex2f(-size_x, size_y)  # Верхний левый угол
    glEnd()


# Основной цикл рендеринга
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    red = 1
    green = 0
    blue = 1

    size_x, size_y = 0.1, 0.1

    back_r, back_g, back_b = 0, 0, 0
    trigger = True

    while True:

        glClear(GL_COLOR_BUFFER_BIT)

        if trigger:
            back_r += 0.0001
            back_g += 0.0001
            back_b += 0.0001

            red -= 0.0001
            green += 0.0001
            blue -= 0.0001

            size_x += 0.00001
            size_y += 0.00001

            if back_r >= 1:
                trigger = False

        if not trigger:
            back_r -= 0.0001
            back_g -= 0.0001
            back_b -= 0.0001

            red += 0.0001
            green -= 0.0001
            blue += 0.0001

            size_x -= 0.00001
            size_y -= 0.00001

            if back_r == 0:
                trigger = True

        glClearColor(back_r, back_g, back_b, 1)  # Фон
        draw_house(red, green, blue, size_x, size_y)

        # Обновляем окно
        glfw.swap_buffers(window)
        glfw.poll_events()

# Закрытие окна
glfw.terminate()
