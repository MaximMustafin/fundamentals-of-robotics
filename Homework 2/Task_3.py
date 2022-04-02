# Homework 2, Task 3 - Annotate a video fragment with text and save the annotated video to a file

import cv2 as cv

video = cv.VideoCapture('video.mp4')

fourcc = cv.VideoWriter_fourcc(*'XVID')
path = 'video_with_annotations_path.avi'
video_writer = cv.VideoWriter(path, fourcc, 25.0, (1280, 720))
annotate_flag = False
org = (100, 600)
while video.isOpened():
    ret, frame = video.read()
    if ret:
        if annotate_flag:
            cv.putText(frame, text, org, fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 255, 255))

        cv.imshow('video', frame)
        video_writer.write(frame)
        key = cv.waitKey(27)

        if key == ord('b'):
            annotate_flag = True
            print("Enter text")
            text = str(input())

        if key == ord('s') and annotate_flag:
            annotate_flag = False

        if key == ord('e'):
            break

    else:
        break

video.release()
video_writer.release()
cv.destroyAllWindows()
