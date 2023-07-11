import cv2
import numpy as np
from sklearn import datasets


digitos = datasets.load_digits()
data = digitos.data
target = digitos.target
images = digitos.images


# promedio del dataset

mean_digits = np.zeros((10, 8, 8))

for i in range(10):
    mean_digits[i] = np.mean(images[target == i], axis=0)


def pre_processing(mat, isDark=False):  # función que recibe una imagen y establece que el max valor sea 16 y minimo 0

    # contours, hierarchy = cv2.findContours(mat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # x, y, w, h = cv2.boundingRect(contours)
    #
    newMat = cv2.resize(mat, (8, 8))

    if(not isDark):
        i = 0
        while i < 8:
            j = 0
            while j < 8:
                newMat[i][j] = 255 - newMat[i][j]
                j = j + 1
            i = i + 1

    i = 0

    while i < 8:
        j = 0
        while j < 8:
            if(newMat[i][j]>16):
                newMat[i][j] = newMat[i][j] * 16 // 255
            j = j + 1
        i = i + 1

    return newMat


def distancia_euclideana(mat1, mat2):
    return np.sqrt(np.sum(np.square(mat1-mat2)))


def knn_method1(preprocessed):  # method using original dataset


    distancias = []

    for i in images:
        dist = distancia_euclideana(preprocessed, i)
        distancias.append(dist)

    # ---- temp info ------------------------------------------------------
    distancias_sorted_temp = distancias.copy()
    distancias_sorted_temp.sort()
    # --------------------------------------------------------------------

    distancias_sorted = distancias_sorted_temp[:3]

    closest = []

    for item in distancias_sorted:
        if item in distancias:
            closest.append(target[distancias.index(item)])

    return closest


def knn_method2(preprocessed):  # method using mean dataset

    distancias = []

    for img in mean_digits:
        dist = distancia_euclideana(preprocessed, img)
        distancias.append(dist)

    # ---- temp info ------------------------------------------------------
    dist_copy = distancias.copy()
    dist_copy.sort()
    # ---- temp info ------------------------------------------------------

    temp_closest = dist_copy[:3]

    closest = []

    for item in temp_closest:
        if item in distancias:
            closest.append(distancias.index(item))

    return closest

