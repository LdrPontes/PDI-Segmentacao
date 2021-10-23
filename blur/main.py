import sys
import timeit
import numpy as np
import cv2
import math

INPUT_IMAGE = './Exemplos/b01.bmp'
WINDOW_SIZE_X = 15
WINDOW_SIZE_Y = 11

'''
1 = INGẼNUO
2 = SEPARÁVEL
3 = IMAGEM INTEGRAL
'''
METHOD = 2

def dumb_window_mean(window):

    mean = []

    for c in range(0, 3):
        total = 0
        for x in range(0, WINDOW_SIZE_X):
            for y in range(0, WINDOW_SIZE_Y):
                try:
                    total += window[y][x][c]
                except:
                    pass
        channel_mean = total / (WINDOW_SIZE_Y * WINDOW_SIZE_X)
        mean.append(channel_mean)

    return mean


def dumb(img):

    initial_x = math.floor(WINDOW_SIZE_X / 2)
    initial_y = math.floor(WINDOW_SIZE_Y / 2)

    blured = np.zeros(img.shape)

    for x in range(initial_x, img.shape[1] - initial_x):
        for y in range(initial_y, img.shape[0] - initial_y):
            
            mean = dumb_window_mean(img[y-initial_y:y+initial_y, x-initial_x:x+initial_x])

            for channel, value in enumerate(mean):
                blured[y][x][channel] = value

    return blured[WINDOW_SIZE_Y:img.shape[0]-WINDOW_SIZE_Y, WINDOW_SIZE_X:img.shape[1]-WINDOW_SIZE_X]

def splitable_mean(window, window_size):
    mean = []
    
    for c in range(0, 3):
        total = 0
        for i in range(0, window_size):
            try:
                total += window[i][c]
            except Exception as e:
                print(e)
                pass
        channel_mean = total / window_size
        mean.append(channel_mean)
    
    return mean

def splitable(img):
    initial_x = math.floor(WINDOW_SIZE_X / 2)
    initial_y = math.floor(WINDOW_SIZE_Y / 2)
    
    blured_horizontal = np.zeros(img.shape)
    blured = np.zeros(img.shape)

    for y in range(initial_y, img.shape[0]):
        for x in range(initial_x, img.shape[1] - initial_x):
            window = img[y, x-initial_x:x+initial_x + 1]
            mean = splitable_mean(window, WINDOW_SIZE_X)
            
            for channel, value in enumerate(mean):
                blured_horizontal[y][x][channel] = value
        
    for x in range(initial_x, blured_horizontal.shape[1]):  
        for y in range(initial_y, blured_horizontal.shape[0] - initial_y):
            window = blured_horizontal[y-initial_y:y+initial_y + 1, x]
            mean = splitable_mean(window, WINDOW_SIZE_Y)
                        
            for channel, value in enumerate(mean):
                blured[y][x][channel] = value
    
    return blured[WINDOW_SIZE_Y:img.shape[0]-WINDOW_SIZE_Y, WINDOW_SIZE_X:img.shape[1]-WINDOW_SIZE_X]
            

def integral(img):

    return img


def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.astype(np.float32)

    blured = None
    if(METHOD == 1):
        blured = dumb(img.copy())
    elif(METHOD == 2):
        blured = splitable(img.copy())
    elif(METHOD == 3):
        blured = integral(img.copy())
    cv2.imwrite('out.bmp', blured)


main()
