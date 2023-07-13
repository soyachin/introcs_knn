import pyxel
import cv2
import numpy as np
import knn_related as my_knn  # importa el archivo knn_related.py
from statistics import mode

# Se define el tamaño del canvas (app_live_drawing)
alto = 100
ancho = 100

# Se declaran variables para el funcionamiento del programa (estados y posición del mouse)

drawing_state = False  # ¿Se está dibujando?

main_menu = True  # ¿Se está en el menú principal?
app_live_drawing = False
app_submit = False
app_submit_CSVMODE = False
app_submit_PNGMODE = False

last_drawn_x = 0  # posición anterior del mouse
last_drawn_y = 0  # posición anterior del mouse
isDark = False

# Se crea una matriz que almacena el dibujo
dibujo_matrix = np.zeros((alto, ancho))

# Se lee la información de los archivos csv e imágenes
image_submited = None


def importFile(type):  # Se pasa un string que indica el tipo de archivo que se quiere importar
    global image_submited
    fileTitle = input("Por favor indique el archivo que desea importar: ")
    if type == "IMG":
        image_submited = cv2.imread(fileTitle, cv2.IMREAD_GRAYSCALE)


def drawing_in_matrix():  # Se altera la información de la matriz que almacena el dibujo
    global last_drawn_x, last_drawn_y

    # Se dibuja una linea entre la posición anterior del mouse y la posición actual, color y grosor
    cv2.line(dibujo_matrix, (last_drawn_x, last_drawn_y), (pyxel.mouse_x, pyxel.mouse_y), 255, 13)
    # Recordar que el dibujo es fluido porque se actualiza constantemente

    # Se actualiza la posición anterior del mouse
    last_drawn_x = pyxel.mouse_x
    last_drawn_y = pyxel.mouse_y


def drawing_state_start():
    global drawing_state, last_drawn_x, last_drawn_y
    drawing_state = True
    last_drawn_x = pyxel.mouse_x
    last_drawn_y = pyxel.mouse_y


def drawing_state_stop():
    global drawing_state
    drawing_state = False


def erase_drawing():
    global dibujo_matrix
    dibujo_matrix = np.zeros((alto, ancho))


def predict_knn(matrix, isDark):
    if matrix is None:
        print("No has importado ningun archivo, por favor importa un archivo")
        return

    preprocessed = my_knn.pre_processing(matrix, isDark)

    method1_result = my_knn.knn_method1(preprocessed)
    method2_result = my_knn.knn_method2(preprocessed)

    print("\nTargets:")
    print("Metodo 1:", method1_result)
    print("Metodo 2:", method2_result, "\n")

    print("Soy la inteliencia artificial, y he detectado que el digito ingresado corresponde al número:",
          mode(method1_result))
    print("Soy la inteliencia artificial versión 2, y he detectado que el digito ingresado corresponde al número:",
          mode(method2_result))


def show_drawing_pyxel():  # toma el dibujo de la matriz y lo representa en la ventana
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
    pyxel.text(5, 30, "To change background base color use C", 7)
    pyxel.text(5, 40, "To predict use P ", 7)
    pyxel.text(5, 50, "To go to MENU use M", 7)
    pyxel.text(5, 60, "* submit b4 running", 7)
    if app_submit_PNGMODE:
        pyxel.text(5, 70, "Mode: IMAGE", 8)
    pyxel.text(5, 80, "Dark: " + str(isDark), 9)


class App:
    # Las funciones __init__, update y draw son funciones que deben ser definidas. Leer la documentación de Pyxel
    def __init__(self):  # Se inicializa la ventana
        pyxel.init(alto + 100, ancho, title="Proyecto final")
        pyxel.mouse(True)  # activa el mouse
        pyxel.run(self.update, self.draw)

    # La función update() es la encargada de actualizar la lógica del programa,
    # basándose en el uso de teclas (inputs) del usuario
    def update(self):
        global drawing_state, main_menu, app_live_drawing, app_submit

        if pyxel.btnp(pyxel.KEY_M):
            main_menu = True
            app_live_drawing = False
            app_submit = False

        if pyxel.btnp(pyxel.KEY_Q):  # si se presiona la tecla Q
            pyxel.quit()  # se cierra el programa

        if main_menu:
            if pyxel.btnp(pyxel.KEY_1):
                main_menu = False
                app_live_drawing = True

            if pyxel.btnp(pyxel.KEY_2):
                main_menu = False
                app_submit = True

        if app_live_drawing:
            # Diccionario: revisar documentación de Pyxel
            # .btnp = Button Pressed
            # .btnr = Button Released
            # .KEY_SPACE = Tecla espacio y así ...
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # si se presiona el boton izquierdo del mouse

                drawing_state_start()  # se inicia el dibujo

            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # si se suelta el boton izquierdo del mouse
                drawing_state_stop()  # se detiene el dibujo

            if drawing_state:  # si se esta dibujando
                drawing_in_matrix()  # se dibuja en la matriz

            if pyxel.btnp(pyxel.KEY_SPACE):  # si se presiona la tecla SPACE
                erase_drawing()  # se borra el dibujo

            if pyxel.btnp(pyxel.KEY_P):  # si se presiona la tecla P
                predict_knn(dibujo_matrix, True)  # se predice el numero, el True es porque se debe invertir el color

        if app_submit:
            global app_submit_PNGMODE, app_submit_CSVMODE, isDark
            if pyxel.btnp(pyxel.KEY_I):
                app_submit_PNGMODE = True
                importFile("IMG")
            if pyxel.btnp(pyxel.KEY_C):
                isDark = not isDark
            if pyxel.btnp(pyxel.KEY_P):
                if app_submit_PNGMODE:
                    predict_knn(image_submited, isDark)

    # La función draw() es la encargada de dibujar (mostrar) en la ventana
    def draw(self):
        pyxel.cls(0)
        if main_menu:
            ui_menu()  # Se definen funciones para dibujar en la ventana para cada caso específico
        if app_live_drawing:
            ui_draw()
            show_drawing_pyxel()  # Con esta función se toma la matriz de dibujo y se muestra en la ventana de pyxel.
            # Si no se implementa esta función, no se verá el dibujo en la ventana (pero sí se guardará en la matriz)

        if app_submit:
            ui_submit()


#  ------------------------------

App()
