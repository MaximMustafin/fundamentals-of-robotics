# Homework 2, Task 2 - Create a bird's eye view video from a fixed camera using perspective transformation and
# save it to a file

import numpy as np
import cv2 as cv

video = cv.VideoCapture('Highway_Driving.mp4')
fourcc = cv.VideoWriter_fourcc(*'XVID')
path = 'transformed_video.avi'
video_writer = cv.VideoWriter(path, fourcc, 25.0, (1280, 720))
video.set(cv.CAP_PROP_POS_MSEC, 3737000)
success, first_frame = video.read()

width = int(first_frame.shape[1])
height = int(first_frame.shape[0])
dim = (width, height)


def draw_circle(event, x, y, flags, param):
    global mouse_x, mouse_y, print_status, p
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(first_frame, (x, y), 3, (255, 255, 0), -1)
        mouse_x, mouse_y = x, y
        p += 1
        print_status = True


global p
p = 0
f = 0
cv.imshow('first_frame', first_frame)
cv.setMouseCallback('first_frame', draw_circle)

x1 = 0, 0
x2 = 0, 0
x3 = 0, 0
x4 = 0, 0

global print_status
print_status = False

while True:
    cv.imshow('first_frame', first_frame)
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

pts1 = np.float32([[x1], [x2], [x3], [x4]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv.getPerspectiveTransform(pts1, pts2)

while video.isOpened():
    ret, frame = video.read()
    if ret:
        frame = cv.warpPerspective(frame, matrix, (width, height))

        cv.imshow('video', frame)
        video_writer.write(frame)
        key = cv.waitKey(27)

        if key == 27:
            break

    else:
        break

video.release()
cv.destroyAllWindows()
