import pyxel
import cv2
import numpy as np
import knn_related as my_knn

alto = 100
ancho = 100

prediction = 0
drawing = False
menu = True
app1_draw = False
app2_image = False
app2_image_csvmode = False
app2_image_submode = False
last_drawn_x = 0  # posición anterior del mouse
last_drawn_y = 0  # posición anterior del mouse
isDark = False

dibujo_matrix = np.zeros((alto, ancho))
image_submited = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
csv_submited = np.loadtxt("csv_img.csv", delimiter=",")


def importFile(type):
    global csv_submited, image_submited
    fileTitle = input("Por favor indique el archivo que desea importar: ")
    if type == "CSV":
        csv_submited = np.loadtxt(fileTitle, delimiter=",")
    elif type == "IMG":
        image_submited = cv2.imread(fileTitle, cv2.IMREAD_GRAYSCALE)


def drawing_in_matrix():  # dibuja en la matriz, información pura
    global last_drawn_x, last_drawn_y

    cv2.line(dibujo_matrix, (last_drawn_x, last_drawn_y), (pyxel.mouse_x, pyxel.mouse_y), 255, 13)

    last_drawn_x = pyxel.mouse_x
    last_drawn_y = pyxel.mouse_y


def drawing_state_start():
    global drawing, last_drawn_x, last_drawn_y
    drawing = True
    last_drawn_x = pyxel.mouse_x
    last_drawn_y = pyxel.mouse_y


def drawing_state_stop():
    global drawing
    drawing = False


def erase_drawing():
    global dibujo_matrix
    dibujo_matrix = np.zeros((alto, ancho))


def predict_knn(matrix, isDark):
    if matrix is None:
        print("No has importado ningun archivo, por favor importa un archivo")
        return

    preprocessed = my_knn.pre_processing(matrix, isDark)
    print("Predicción 1:", my_knn.knn_method1(preprocessed))
    print("Predicción 2:", my_knn.knn_method2(preprocessed))


def drawing_in_window():  # toma el dibujo de la matriz y lo representa en la ventana
    for y in range(ancho):
        for x in range(alto):
            if dibujo_matrix[y][x] == 255:
                pyxel.pset(x, y, 7)
            else:
                pyxel.pset(x, y, 0)


def ui_menu():
    pyxel.text(5, 10, "Select type of input: ", 7)
    pyxel.text(5, 20, "1. Live ", 7)
    pyxel.text(5, 30, "2. Submitted ", 7)


def ui_draw():
    pyxel.rect(100, 0, 200, 100, 7)
    pyxel.text(105, 10, "Digit input: ", 0)
    pyxel.text(105, 20, "To draw use LEFT CLICK ", 0)
    pyxel.text(105, 30, "To clear use SPACE ", 0)
    pyxel.text(105, 40, "To predict use P ", 0)
    pyxel.text(105, 50, "To go to MENU use M", 0)


def ui_submit():
    pyxel.text(5, 10, "Type of submsn: ", 7)
    pyxel.text(5, 20, "I. Image ", 7)
    pyxel.text(5, 30, "F. CSV ", 7)
    pyxel.text(5, 40, "To change background base color use C", 7)
    pyxel.text(5, 50, "To predict use P ", 7)
    pyxel.text(5, 60, "To go to MENU use M", 7)
    pyxel.text(5, 70, "* submit b4 running", 7)
    if app2_image_submode:
        pyxel.text(5, 80, "Mode: PNG", 8)
    if app2_image_csvmode:
        pyxel.text(5, 80, "Mode: CSV", 8)
    pyxel.text(5, 90, "Dark: " + str(isDark), 9)


class App:
    def __init__(self):
        pyxel.init(alto + 100, ancho, title="digit input :3")
        pyxel.mouse(True)  # activa el mouse
        pyxel.run(self.update, self.draw)

    def update(self):
        global drawing, menu, app1_draw, app2_image

        if pyxel.btnp(pyxel.KEY_M):
            menu = True
            app1_draw = False
            app2_image = False

        if pyxel.btnp(pyxel.KEY_Q):  # si se presiona la tecla Q
            pyxel.quit()  # se cierra el programa

        if menu:
            if pyxel.btnp(pyxel.KEY_1):
                menu = False
                app1_draw = True

            if pyxel.btnp(pyxel.KEY_2):
                menu = False
                app2_image = True

        if app1_draw:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # si se presiona el boton izquierdo del mouse

                drawing_state_start()  # se inicia el dibujo

            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # si se suelta el boton izquierdo del mouse
                drawing_state_stop()  # se detiene el dibujo

            if drawing:  # si se esta dibujando
                drawing_in_matrix()  # se dibuja en la matriz

            if pyxel.btnp(pyxel.KEY_SPACE):  # si se presiona la tecla SPACE
                erase_drawing()  # se borra el dibujo

            if pyxel.btnp(pyxel.KEY_P):  # si se presiona la tecla P
                predict_knn(dibujo_matrix, True)  # se predice el numero

        if app2_image:
            global app2_image_submode, app2_image_csvmode, isDark
            if pyxel.btnp(pyxel.KEY_I):
                app2_image_submode = True
                app2_image_csvmode = False
                importFile("IMAGE")
            if pyxel.btnp(pyxel.KEY_F):
                app2_image_csvmode = True
                app2_image_submode = False
                importFile("CSV")
            if pyxel.btnp(pyxel.KEY_C):
                isDark = not isDark
            if pyxel.btnp(pyxel.KEY_P):
                if app2_image_submode:
                    predict_knn(image_submited, isDark)
                if app2_image_csvmode:
                    predict_knn(csv_submited, isDark)

    def draw(self):
        pyxel.cls(0)
        if menu:
            ui_menu()
        if app1_draw:
            ui_draw()
            drawing_in_window()  # se dibuja en la ventana

        if app2_image:
            ui_submit()


#  ------------------------------

App()
