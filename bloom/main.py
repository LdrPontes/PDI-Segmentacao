import sys
import timeit
import numpy as np
import cv2
import math

INPUT_IMAGE = './corrida.bmp'
THRESHOLD = 0.65


def bright_pass(original, gray):

    result = original.copy()

    for y in range(0, gray.shape[0]):
        for x in range(0, gray.shape[1]):
            if(gray[y][x][0] <= THRESHOLD):
                result[y][x] = [0, 0, 0]

    return result


def box_blur(original, brighted):

    original = original.copy()
    brighted = brighted.copy()
    brighted_sum = np.zeros(brighted.shape)

    window_size = [5, 15, 25, 35]
    # window_size = [20]
    for size in window_size:

        blured = cv2.boxFilter(brighted, ddepth=-1, ksize=(size, size))

        brighted_sum = brighted_sum + blured

    output = np.zeros(original.shape)
    output = cv2.normalize((0.65 * original) + (0.30 * brighted_sum), output, 0, 255, cv2.NORM_MINMAX)

    return output


def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = gray.reshape((gray.shape[0], gray.shape[1], 1))
    gray = gray / 255

    brighted = bright_pass(img, gray)

    output = box_blur(img, brighted)

    cv2.imwrite('output.png', output)


main()
