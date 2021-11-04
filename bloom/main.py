# Alunos: Leandro Pontes Berleze e Otávio Thomas Bertucini
import sys
import timeit
import numpy as np
import cv2
import math

INPUT_IMAGE = './corrida.bmp'
THRESHOLD = 0.65

STD_DEVIATION = 2

def bright_pass(original, gray):

    result = original.copy()

    for y in range(0, gray.shape[0]):
        for x in range(0, gray.shape[1]):
            if(gray[y][x][0] <= THRESHOLD):
                result[y][x] = [0, 0, 0]

    return result


def box_blur(original, brighten):

    original = original.copy()
    brighten = brighten.copy()
    brighten_sum = np.zeros(brighten.shape)

    window_size = [5, 15, 25, 35]

    for size in window_size:

        blured = cv2.boxFilter(brighten, ddepth=-1, ksize=(size, size))

        brighten_sum = brighten_sum + blured

    output = np.zeros(original.shape)
    output = cv2.normalize((0.65 * original) + (0.25 * brighten_sum), output, 0, 255, cv2.NORM_MINMAX)

    return output

def gaussian_blur(original, brighten):
    #Refêrencia: https://www.w3.org/TR/SVG11/filters.html#feGaussianBlurElement
    original = original.copy()
    brighten = brighten.copy()
    
    deviation = math.floor(STD_DEVIATION * 3 * math.sqrt(2*math.pi) / 4 + 0.5)

    if(deviation % 2 == 0):
        blured = cv2.boxFilter(brighten, ddepth=-1, ksize=(deviation, deviation))
        blured = cv2.boxFilter(blured, ddepth=-1, ksize=(deviation, deviation))
        blured = cv2.boxFilter(blured, ddepth=-1, ksize=(deviation + 1, deviation + 1))

    else:
        blured = cv2.boxFilter(brighten, ddepth=-1, ksize=(deviation, deviation))
        blured = cv2.boxFilter(blured, ddepth=-1, ksize=(deviation, deviation))
        blured = cv2.boxFilter(blured, ddepth=-1, ksize=(deviation, deviation))
            

    output = np.zeros(original.shape)
    output = cv2.normalize((0.65 * original) + (0.25 * blured), output, 0, 255, cv2.NORM_MINMAX)

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

    output = gaussian_blur(img, brighted)

    cv2.imwrite('output.png', output)


main()
