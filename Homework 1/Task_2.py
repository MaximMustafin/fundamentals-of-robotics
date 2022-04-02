# Homework 1, Task 2 - Warp an image with a mouse clicking and rotate it with a perspective transformation

import cv2 as cv
import numpy as np

image = cv.imread('cards.jpg')  # reading image from directory


#  function for circle drawing 
def draw_circle(event, x, y, flags, param):
    global mouse_x, mouse_y, print_status, p
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(image, (x, y), 3, (255, 255, 0), -1)
        mouse_x, mouse_y = x, y
        p += 1
        print_status = True


global p
p = 0
f = 0
cv.imshow("img_warp", image)
cv.setMouseCallback('img_warp', draw_circle)

x1 = 0, 0
x2 = 0, 0
x3 = 0, 0
x4 = 0, 0

global print_status
print_status = False

while True:
    cv.imshow('img_warp', image)
    k = cv.waitKey(20) & 0xFF
    if p == 4 and f == 1:
        break
    if p == 1:
        x1 = mouse_x, mouse_y
        if print_status:
            print(x1)
            print_status = False
    if p == 2:
        x2 = mouse_x, mouse_y
        if print_status:
            print(x2)
            print_status = False
    if p == 3:
        x3 = mouse_x, mouse_y
        if print_status:
            print(x3)
            print_status = False
    if p == 4:
        x4 = mouse_x, mouse_y
        if print_status:
            print(x4)
            print_status = False
        f = 1

width, height = 250, 350
pts1 = np.float32([[x1], [x2], [x3], [x4]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
image_output = cv.warpPerspective(image, matrix, (width, height))

cv.imshow('image_output', image_output)
cv.waitKey(0)
