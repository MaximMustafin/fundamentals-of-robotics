# Homework 1, Task 3 - Record a video from a webcam with OpenCV and save it to the disk with mp4 compression

import cv2 as cv

capture = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc(*'XVID')
path = 'video.mp4'
video_writer = cv.VideoWriter(path, fourcc, 30.0, (640, 480))

while True:
    ret, frame = capture.read()

    if ret:
        cv.imshow('webcam', frame)
        video_writer.write(frame)

    if cv.waitKey(1) == 13:
        break

capture.release()
video_writer.release()

cv.destroyAllWindows()
