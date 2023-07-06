import pyxel
import cv2
import numpy as np
import knn_related as my_knn


alto = 100
ancho = 100

prediction = 0
drawing = False
last_drawn_x = 0  # posición anterior del mouse
last_drawn_y = 0  # posición anterior del mouse
dibujo_matrix = np.zeros((alto, ancho))


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


def predict_knn_pix():
    global dibujo_matrix

    print("Predicción 1:", my_knn.knn_method1(dibujo_matrix))
    print("Predicción 2:", my_knn.knn_method2(dibujo_matrix))


def drawing_in_window():  # toma el dibujo de la matriz y lo representa en la ventana
    for y in range(ancho):
        for x in range(alto):
            if dibujo_matrix[y][x] == 255:
                pyxel.pset(x, y, 7)
            else:
                pyxel.pset(x, y, 0)


def inter_apearance():
    global prediction
    pyxel.rect(100, 0, 200, 100, 7)
    pyxel.text(105, 10, "Digit input: ", 0)
    pyxel.text(105, 20, "To draw use LEFT CLICK ", 0)
    pyxel.text(105, 30, "To clear use SPACE ", 0)
    pyxel.text(105, 40, "To predict use P ", 0)
    pyxel.text(105, 50, "To quit use Q ", 0)
    pyxel.text(105, 60, "Prediction: " + str(prediction), 0)


class App:
    def __init__(self):
        pyxel.init(alto + 100, ancho, title="digit input :3")
        pyxel.mouse(True)  # activa el mouse
        pyxel.run(self.update, self.draw)

    def update(self):
        global drawing

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # si se presiona el boton izquierdo del mouse

            drawing_state_start()  # se inicia el dibujo

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # si se suelta el boton izquierdo del mouse
            drawing_state_stop()  # se detiene el dibujo

        if drawing:  # si se esta dibujando
            drawing_in_matrix()  # se dibuja en la matriz

        if pyxel.btnp(pyxel.KEY_Q):  # si se presiona la tecla Q
            pyxel.quit()  # se cierra el programa

        if pyxel.btnp(pyxel.KEY_SPACE):  # si se presiona la tecla SPACE
            erase_drawing()  # se borra el dibujo

        if pyxel.btnp(pyxel.KEY_P):  # si se presiona la tecla P
            predict_knn_pix()  # se predice el numero

    def draw(self):
        pyxel.cls(0)

        drawing_in_window()  # se dibuja en la ventana
        inter_apearance()


#  ------------------------------

App()
