import cv2 as cv

image = cv.imread('image.png')
sample_image = cv.imread('sample_image.png')

scale_percent = 35

width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

global resized_image
resized_image = cv.resize(image, dim, interpolation=cv.INTER_AREA)

image_hsv = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV)
lab_image = cv.cvtColor(resized_image, cv.COLOR_BGR2LAB)
yCrCb_image = cv.cvtColor(resized_image, cv.COLOR_BGR2YCrCb)

imageH = image_hsv[:, :, 0]
imageS = image_hsv[:, :, 1]
imageV = image_hsv[:, :, 2]


def nothing(x):
    pass


def click_event(event, x, y, flags, params):
    global h, s, v, next
    if event == cv.EVENT_LBUTTONDOWN:
        print('x - ', x, ', y - ', y)

        b = resized_image[y, x, 0]
        g = resized_image[y, x, 1]
        r = resized_image[y, x, 2]

        h = image_hsv[y, x, 0]
        s = image_hsv[y, x, 1]
        v = image_hsv[y, x, 2]

        next = True

        print('b - ', b, ', g - ', g, ', r - ', r)
        print('h - ', h, ', s - ', s, ', v - ', v, '\n')


def task():
    cv.imshow('source_image', resized_image)
    cv.imshow('lab_image', lab_image)
    cv.imshow('YCrCb_image', yCrCb_image)
    cv.imshow('hsv_image', image_hsv)
    cv.setMouseCallback('hsv_image', click_event)

    cv.imshow('hue_image', imageH)
    cv.imshow('saturation_image', imageS)
    cv.imshow('value_image', imageV)

    cv.createTrackbar('Value', 'hsv_image', 0, 255, nothing)

    global next
    next = False

    while True:
        cv.imshow('hsv_image', image_hsv)
        image_hsv[:, :, 2] = cv.getTrackbarPos('Value', 'hsv_image')

        if next:
            hue = h
            saturation = s
            value = v

            print('hue - ', hue, ', saturation - ', saturation, ', value - ', value, '\n')
            hsv_pixel = cv.cvtColor(sample_image, cv.COLOR_BGR2HSV)
            hsv_pixel[:, :, 0] = hue
            hsv_pixel[:, :, 1] = saturation
            hsv_pixel[:, :, 2] = value
            rgb_pixel = cv.cvtColor(hsv_pixel, cv.COLOR_HSV2BGR)
            lab_pixel = cv.cvtColor(rgb_pixel, cv.COLOR_BGR2LAB)
            yCrCb_pixel = cv.cvtColor(rgb_pixel, cv.COLOR_BGR2YCrCb)

            cv.imshow('hsv_pixel', hsv_pixel)
            cv.imshow('rgb_pixel', rgb_pixel)
            cv.imshow('lab_pixel', lab_pixel)
            cv.imshow('yCrCb_pixel', yCrCb_pixel)

            next = False
        cv.waitKey(1)


if __name__ == '__main__':
    task()
