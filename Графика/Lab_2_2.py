import random
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sympy import false

# Размер окна
width, height = 800, 600

pos = 0

move_trigger = 0
rotate_trigger = 0
water_height = 0
is_moved = False
is_rotated = False

# Позиция и угол вращения чайника
teapot_pos_y = 0.0  # Начальная позиция по оси Y
teapot_rotation = 0.0  # Начальный угол вращения

particles = [{"x": 0.0, "y": 0.0, "z": 0.0, "speed": random.uniform(0.02, 0.05)} for _ in range(100)]


def draw_water_particles():
    set_material("blue")  # Цвет воды
    glPointSize(5.0)  # Размер частиц

    glBegin(GL_POINTS)
    for p in particles:
        # Рисуем частицу
        glVertex3f(p["x"], p["y"], p["z"])

        # Обновляем положение частицы
        p["y"] -= p["speed"]  # Двигается вниз

        # Если частица упала слишком низко, сбрасываем её вверх
        if p["y"] < -1.0:
            p["x"] = random.uniform(-0.05, 0.05)
            p["y"] = 0.8
            p["z"] = random.uniform(-0.05, 0.05)
    glEnd()


def update():
    global teapot_pos_y, teapot_rotation
    global move_trigger
    global rotate_trigger
    global is_moved
    global is_rotated

    # Сдвиг
    if not is_moved:
        if move_trigger == 0:
            teapot_pos_y += 0.0009
            if teapot_pos_y >= 2:
                move_trigger = 1
                is_moved = True
        elif move_trigger and teapot_pos_y >= -0.5:
            teapot_pos_y -= 0.0009
            if teapot_pos_y <= 0:
                move_trigger = 1

    # Вращение
    if is_moved and not is_rotated:
        if rotate_trigger == 0:
            teapot_rotation += 0.015
            if teapot_rotation >= 40.0:
                rotate_trigger = 1
                is_rotated = True
        else:
            teapot_rotation -= 0.015
            if teapot_rotation <= 0.0:
                rotate_trigger = 0
                is_moved = False

    # Перерисовываем сцену
    glutPostRedisplay()


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
    global water_height
    global is_rotated

    # Чайник
    glEnable(GL_TEXTURE_2D)  # Включить текстурирование
    glBindTexture(GL_TEXTURE_2D, teapot_texture)

    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)

    set_material("white")

    # Сохраняем матрицу перед трансформацией чайника
    glPushMatrix()
    glTranslatef(-1 + teapot_pos_y, teapot_pos_y, -3)  # Поднимаем чайник по оси Y
    glRotatef(15, -1.0, 0.0, 0.0)  # Вращаем вокруг оси Y
    glRotatef(teapot_rotation, 0.0, 0.0, -1.0)  # Вращаем вокруг оси Y

    glRotatef(30.0, 1.0, 0.0, 0.0)
    glRotatef(20.0, 0.0, -1.0, 0.0)
    glutSolidTeapot(1)
    glPopMatrix()  # Восстанавливаем матрицу

    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)

    # Стол
    glPushMatrix()
    set_material("grey")
    glPushMatrix()  # Сохраняем матрицу для стола
    glTranslatef(0, -6, -5.5)
    glRotatef(20.0, 1, -1.0, 0.0)
    glEnable(GL_TEXTURE_2D)
    draw_textured_cube(10)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    # Чашка
    glPushMatrix()
    set_material("blue")
    glTranslatef(2, 0, -1)  # Смещаем вверх по оси Y для стола
    glRotatef(100, 1.0, 0.0, 0.0)  # Поворачиваем чашку
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 1, 20, 20)  # Корпус чашки

    # Ручка чашки
    glRotatef(90, 1.0, 1.0, 0.0)
    glRotatef(45, 1.0, -1.0, 1.0)
    glTranslatef(0.25, 0.7, 0.0)
    glutSolidTorus(0.05, 0.3, 30, 30)
    glPopMatrix()

    # "Чай"
    glPushMatrix()
    set_material("white")
    glTranslatef(2.02, -1, -1.2)  # Смещаем вверх по оси Y для стола
    glRotatef(-82, 1.0, 0.0, 0.0)  # Поворачиваем чашку
    glutSolidCylinder(0.49, 0.1 + water_height, 20, 20)
    glPopMatrix()

    if is_rotated:
        glPushMatrix()
        glTranslatef(1.9, 0.22, -1)
        draw_water_particles()
        glPopMatrix()
        if water_height < 0.9:
            water_height += 0.0003
        else:
            is_rotated = False

    glPopMatrix()  # Восстанавливаем матрицу для чашки


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
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Table and tea")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(update)  # Добавляем функцию для обновления сцены
    glutMainLoop()


if __name__ == "__main__":
    main()
