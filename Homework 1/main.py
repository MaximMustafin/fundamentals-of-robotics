import cv2 as cv
import numpy as np

img_path = "image.jpg"
image = cv.imread(img_path)
image_warp = cv.imread("cards.jpg")


# Divide an image in patches and saves them to the disk as a patch with series names
def task1():
    image_height = image.shape[0]
    image_width = image.shape[1]

    m = int(image_height / 3)
    n = int(image_width / 3)

    k = 100

    for y in range(0, image_height, m):
        for x in range(0, image_width, n):
            if (image_height - y) < m or (image_width - x) < n:
                break

            x1 = x + n
            y1 = y + m

            if x1 >= image_width and y1 >= image_height:
                x1 = image_width - 1
                tiles = image[y:y + m, x:x + n]
                cv.imwrite('saved_patches/' + str(k + 3) + '.jpg', tiles)
                cv.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 1)
            elif y1 <= image_height:
                y1 = image_height - 1
                tiles = image[y:y + m, x:x + n]
                cv.imwrite('saved_patches/' + str(k + 3) + '.jpg', tiles)
                cv.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 1)

            k += 1


def draw_circle(event, x, y, flags, param):
    global mouse_x, mouse_y, print_status, p
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(image_warp, (x, y), 3, (255, 255, 0), -1)
        mouse_x, mouse_y = x, y
        p += 1
        print_status = True


# Warp an image with a mouse clicking and rotate it with a perspective transformation
def task2():
    global p
    p = 0
    f = 0
    cv.imshow("img_warp", image_warp)
    cv.setMouseCallback('img_warp', draw_circle)

    x1 = 0, 0
    x2 = 0, 0
    x3 = 0, 0
    x4 = 0, 0

    global print_status
    print_status = False

    while True:
        cv.imshow('img_warp', image_warp)
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
    image_output = cv.warpPerspective(image_warp, matrix, (width, height))

    cv.imshow('image_output', image_output)
    cv.waitKey(0)


# Record a video from a webcam with OpenCV and save it to the disk with mp4 compression
def task3():
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


if __name__ == '__main__':
    # task1()
    task2()
    # task3()
