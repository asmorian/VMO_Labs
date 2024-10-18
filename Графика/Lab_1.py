import glfw
from OpenGL.GL import *

# Инициализация GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Создаем окно с контекстом OpenGL
window = glfw.create_window(1920, 1080, "House", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)

# Устанавливаем цвет фона
glClearColor(1, 1, 1, 1)  # Фон


def draw_house():
    # Основание
    glColor3f(0.7, 0.7, 0.7)  # Серый
    glBegin(GL_QUADS)
    glVertex2f(-0.3, -0.5)  # Нижний левый угол
    glVertex2f(0.3, -0.5)  # Нижний правый угол
    glVertex2f(0.3, 0.2)  # Верхний правый угол
    glVertex2f(-0.3, 0.2)  # Верхний левый угол
    glEnd()

    # Крыша
    glColor3f(0.0, 0.8, 0.5)  # Зелёный с голубым
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.4, 0.2)  # Левый край крыши
    glVertex2f(0.4, 0.2)  # Правый край крыши
    glVertex2f(0.0, 0.7)  # Вершина крыши
    glEnd()

    glColor3f(0.0, 1, 0.6)  # Зелёный с голубым
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.37, 0.216)  # Левый край крыши
    glVertex2f(0.37, 0.216)  # Правый край крыши
    glVertex2f(0.0, 0.68)  # Вершина крыши
    glEnd()

    # Рама
    glColor3f(0.2, 0.2, 0.2)  # Тёмно-серый
    glBegin(GL_QUADS)
    glVertex2f(-0.12, -0.27)  # Нижний левый угол
    glVertex2f(0.12, -0.27)  # Нижний правый угол
    glVertex2f(0.12, 0.02)  # Верхний правый угол
    glVertex2f(-0.12, 0.02)  # Верхний левый угол
    glEnd()

    # Окошко
    glColor3f(1, 1, 0)  # Жёлтый
    glBegin(GL_QUADS)
    glVertex2f(-0.1, -0.25)  # Нижний левый угол
    glVertex2f(0.1, -0.25)  # Нижний правый угол
    glVertex2f(0.1, 0.0)  # Верхний правый угол
    glVertex2f(-0.1, 0.0)  # Верхний левый угол
    glEnd()

    # Перекладина одна
    glColor3f(0.2, 0.2, 0.2)  # Тёмно-серый
    glLineWidth(7.0)
    glBegin(GL_LINES)
    glVertex2f(-0.12, -0.125)  # Лево
    glVertex2f(0.12, -0.125)  # Право
    glEnd()

    # Перекладина вторая
    glColor3f(0.2, 0.2, 0.2)  # Тёмно-серый
    glLineWidth(7.0)
    glBegin(GL_LINES)
    glVertex2f(0, 0)  # Лево
    glVertex2f(0, -0.25)  # Право
    glEnd()


# Основной цикл рендеринга
while not glfw.window_should_close(window):
    # Очищаем экран
    glClear(GL_COLOR_BUFFER_BIT)

    # Вызываем функцию для рисования домика
    draw_house()

    # Обновляем окно
    glfw.swap_buffers(window)
    glfw.poll_events()

# Закрытие окна
glfw.terminate()
