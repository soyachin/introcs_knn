import cv2
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt

digitos = datasets.load_digits()
data = digitos.data
target = digitos.target
images = digitos.images


# promedio del dataset

mean_digits = np.zeros((10, 8, 8))

for i in range(10):
    mean_digits[i] = np.mean(images[target == i], axis=0)


def pre_processing(mat):  # función que recibe una imagen y establece que el max valor sea 16 y minimo 0
    mat = cv2.resize(mat, (8, 8))

    i = 0

    while i < 8:
        j = 0
        while j < 8:
            mat[i][j] = 255 - mat[i][j]
            j = j + 1
        i = i + 1

    i = 0

    while i < 8:
        j = 0
        while j < 8:
            mat[i][j] = mat[i][j] * 16 / 255
            j = j + 1
        i = i + 1

    return mat


def distancia_euclideana(mat1, mat2):
    return np.sqrt(np.sum((mat1 - mat2) ** 2))


def closest_euc(img_to_predict, data_used, neighbors=3):  # ta mal
    distancias = []

    for i in data_used:
        dist = distancia_euclideana(img_to_predict, i)
        distancias.append(dist)

    # también se puede realizar con argsort
    distancias.sort(reverse=True)
    closest = distancias[:neighbors]

    return closest  # returns a list


def knn_method1(img_to_predict):  # method using original dataset

    preprocessed = pre_processing(img_to_predict)

    distancias = []

    for i in images:
        dist = distancia_euclideana(preprocessed, i)
        distancias.append(dist)

    # también se puede realizar con argsort
    distancias.sort(reverse=True)
    closest = distancias[:3]

    return closest


def knn_method2(img_to_predict):  # method using mean dataset
    preprocessed = pre_processing(img_to_predict)
    distancias = []

    for img in mean_digits:
        dist = distancia_euclideana(preprocessed, img)
        distancias.append(dist)

    distancias.sort(reverse=True)
    closest = distancias[:3]

    return closest



