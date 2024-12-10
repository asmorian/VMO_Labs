from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Размер окна
width, height = 800, 600


def init():
    """Инициализация OpenGL"""
    glClearColor(0.2, 0.3, 0.4, 1)  # Установить цвет фона (темно-синий)
    glEnable(GL_DEPTH_TEST)  # Включить тест глубины


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очистить буферы
    glLoadIdentity()

    # Переместить камеру назад, чтобы сфера была видна
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    material_diffuse = [1, 1, 1, 1.0]
    material_specular = [1.0, 0, 0, 1.0]  # Блики (белый)
    material_shininess = [10.0]  # Сила бликов (чем больше, тем ярче и меньше)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

    # Чайник
    glTranslated(-2, 4.5, -10)
    glColor3f(1.0, 0, 0)
    glutSolidTeapot(0.5)

    # Сфера
    glTranslated(0, -1.5, 0)
    glColor3f(0, 1, 0)
    glutSolidSphere(0.5, 50, 50)

    # Куб
    glTranslated(0, -1, 0)
    glColor3f(0, 0, 1)
    glutSolidCube(0.5)

    # Тор
    glTranslated(0, -1.2, 0)
    glColor3f(1, 1, 0)
    glutSolidTorus(0.1, 0.5, 50, 50)

    # Конус
    glTranslated(0, -1.8, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 1, 1)
    glutSolidCone(0.3, 0.8, 20, 20)

    # Многогранник
    glRotated(90, 1, 0, 0)
    glColor3f(1, 0, 1)
    glTranslated(0, -2, 0)
    glutSolidDodecahedron()

    # Чайник (грани)
    glTranslated(3.5, 7.5, 0)
    glColor3f(1, 0, 0)
    glutWireTeapot(0.5)

    # Сфера (грани)
    glTranslated(0, -1.5, 0)
    glColor3f(0, 1, 0)
    glutWireSphere(0.5, 10, 10)

    # Куб (грани)
    glTranslated(0, -1, 0)
    glColor3f(0, 0, 1)
    glutWireCube(0.5)

    # Тор (грани)
    glTranslated(0, -1.2, 0)
    glColor3f(1, 1, 0)
    glutWireTorus(0.1, 0.5, 10, 10)

    # Конус (грани)
    glTranslated(0, -1.8, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 1, 1)
    glutWireCone(0.3, 0.8, 10, 10)

    # Многогранник (грани)
    glRotated(90, 1, 0, 0)
    glColor3f(1, 0, 1)
    glTranslated(0, -2, 0)
    glutWireDodecahedron()

    glutSwapBuffers()  # Обменять буферы


def reshape(w, h):
    """Обработчик изменения размеров окна."""
    glViewport(0, 0, w, h)  # Настроить область просмотра
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, w / h, 1, 100)  # Установить перспективу
    glMatrixMode(GL_MODELVIEW)


def main():
    """Главная функция программы."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Двойная буферизация, цвет, глубина
    glutInitWindowSize(width, height)  # Размер окна
    glutCreateWindow(b"OpenGL Sphere")  # Создать окно

    init()  # Инициализация OpenGL

    glutDisplayFunc(draw)  # Установить функцию отображения
    glutReshapeFunc(reshape)  # Установить функцию изменения размера окна
    glutMainLoop()  # Запустить главный цикл GLUT


if __name__ == "__main__":
    main()
