from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Размер окна
width, height = 800, 600


def load_texture(image_path):
    img = Image.open(image_path)
    img_data = img.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
    width, height = img.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id


def draw_textured_cube(size):
    half_size = size / 2.0

    # Включаем текстурирование
    glBindTexture(GL_TEXTURE_2D, table_texture)

    glBegin(GL_QUADS)

    # Передняя грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, half_size)

    # Задняя грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, -half_size)

    # Верхняя грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, half_size)

    # Нижняя грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, -half_size, half_size)

    # Правая грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(half_size, -half_size, half_size)

    # Левая грань
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size, half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, -half_size, half_size)

    glEnd()


def draw_teapot():
    # Чайник
    # Текстурированный чайник
    glEnable(GL_TEXTURE_2D)  # Включить текстурирование
    glBindTexture(GL_TEXTURE_2D, teapot_texture)  # Привязать текстуру

    # Включить автоматическую генерацию текстурных координат
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)

    set_material("white")  # Настройка материала
    glPushMatrix()
    glTranslatef(-2, 1, -3)
    glRotatef(30.0, 1.0, 0.0, 0.0)
    glRotatef(20.0, 0.0, -1.0, 0.0)
    glutSolidTeapot(1)  # Рисуем чайник

    # Отключить автоматическую генерацию текстурных координат
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)

    # Стол
    set_material("grey")
    glTranslatef(1.5, -4.75, 0)
    glEnable(GL_TEXTURE_2D)
    draw_textured_cube(8)
    glDisable(GL_TEXTURE_2D)

    # Чашка
    # Корпус
    set_material("blue")
    glTranslatef(2.0, 5.5, 1.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 1, 20, 20)

    # Ручка
    glRotatef(90, 1.0, 1.0, 0.0)
    glRotatef(45, 1.0, -1.0, 1.0)
    glTranslatef(0.25, 0.7, 0.0)
    glutSolidTorus(0.05, 0.3, 30, 30)


def set_material(color=None, light_mode=None):
    # Настройки материала
    material_diffuse = [0.8, 0.5, 0.3, 1.0]  # Оранжевый цвет

    match color:
        case "orange":
            material_diffuse = [0.8, 0.5, 0.3, 1.0]
        case "blue":
            material_diffuse = [0, 0, 1, 1.0]
        case "red":
            material_diffuse = [1, 0, 0, 1.0]
        case "green":
            material_diffuse = [0, 1, 0, 1.0]
        case "grey":
            material_diffuse = [0.5, 0.5, 0.5, 1.0]

    match light_mode:
        case None:
            material_specular = [1.0, 1.0, 1.0, 1.0]  # Блики (белый)
            material_shininess = [100.0]  # Сила бликов (чем больше, тем ярче и меньше)
        case 1:
            material_specular = [1.0, 0, 0, 1.0]  # Блики (белый)
            material_shininess = [10.0]  # Сила бликов (чем больше, тем ярче и меньше)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)


def init():
    """Инициализация OpenGL."""
    glClearColor(0.2, 0.3, 0.4, 1)  # Цвет фона
    glEnable(GL_DEPTH_TEST)  # Включить тест глубины
    glEnable(GL_LIGHTING)  # Включить освещение
    glEnable(GL_LIGHT0)  # Включить источник света 0

    # Настройки источника света
    light_position = [1.0, 1.0, 1.0, 0.0]  # Позиция света (направленный свет)
    light_diffuse = [1, 0.8, 0.8, 1.0]  # Диффузное освещение (белый цвет)
    light_specular = [1.0, 1.0, 1.0, 1.0]  # Спекулярное освещение (белые блики)
    light_ambient = [0.2, 0.2, 0.2, 1.0]  # Фоновое освещение (мягкий серый цвет)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])

    global table_texture
    global teapot_texture
    table_texture = load_texture("images.jpg")
    teapot_texture = load_texture("teapot.jpg")


def display():
    """Функция отображения."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очистить буферы
    glLoadIdentity()

    # Расположить камеру
    gluLookAt(0.0, 0.0, 5.0,  # Позиция камеры
              0.0, 0.0, 0.0,  # Точка, куда смотрит камера
              0.0, 1.0, 0.0)  # Вектор "вверх"

    # Нарисовать объект
    draw_teapot()

    glutSwapBuffers()  # Обменять буферы


def reshape(w, h):
    """Обработчик изменения размеров окна."""
    if h == 0:
        h = 1
    aspect = w / h  # Соотношение сторон окна

    glViewport(0, 0, w, h)  # Установить область просмотра
    glMatrixMode(GL_PROJECTION)  # Перейти в режим проекционной матрицы
    glLoadIdentity()
    gluPerspective(45, aspect, 1.0, 100.0)  # Настроить перспективу
    glMatrixMode(GL_MODELVIEW)  # Вернуться в режим матрицы вида модели


def main():
    """Главная функция программы."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Двойная буферизация, цвет, глубина
    glutInitWindowSize(width, height)  # Размер окна
    glutCreateWindow(b"Table and tea")  # Создать окно

    init()  # Инициализация OpenGL

    glutDisplayFunc(display)  # Установить функцию отображения
    glutReshapeFunc(reshape)  # Установить функцию изменения размера окна
    glutMainLoop()  # Запустить главный цикл GLUT


if __name__ == "__main__":
    main()
