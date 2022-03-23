import numpy as np
import cv2 as cv


def nothing(x):
    pass


def salt_pepper_noise(input_image, probability):
    '''
    Corrupt an input image with salt-and-pepper noise
    '''
    output_noise_img = input_image.copy()
    if len(input_image.shape) == 2:
        black = 0
        white = 255
    else:
        colorspace = input_image.shape[2]
        if colorspace == 3:
            black = np.array([0, 0, 0])
            white = np.array([255, 255, 255])
        else:
            black = np.array([0, 0, 0, 255])
            white = np.array([255, 255, 255, 255])
    probs = np.random.random(output_noise_img.shape[:2])
    output_noise_img[probs < (probability / 2)] = black
    output_noise_img[probs > 1 - (probability / 2)] = white
    return output_noise_img


source_image = cv.imread('image.png')
# source_image = cv.imread('image_face.jpg')

scale_percent = 80

width = int(source_image.shape[1] * scale_percent / 100)
height = int(source_image.shape[0] * scale_percent / 100)
dim = (width, height)

image = cv.resize(source_image, dim, interpolation=cv.INTER_AREA)

# bilateral_filter = cv.bilateralFilter(src=image, d=9, sigmaColor=75, sigmaSpace=75)
# cv.imshow('source_image', image)
# cv.imshow('bilateral', bilateral_filter)
# cv.waitKey(0)

prob = 0

cv.namedWindow('source_image')
cv.createTrackbar('Prob', 'source_image', 0, 100, nothing)

while True:
    cv.imshow('source_image', image)

    k = cv.waitKey(0)

    prob = cv.getTrackbarPos('Prob', 'source_image')

    if k == ord('e'):
        noise_image = salt_pepper_noise(image, float(prob) / 100)
        averaging_blur = cv.blur(noise_image, ksize=(15, 15))
        median_blur = cv.medianBlur(noise_image, ksize=15)
        gaussian_blur = cv.GaussianBlur(noise_image, ksize=(15, 15), sigmaX=0, sigmaY=0)
        bilateral_filter = cv.bilateralFilter(src=noise_image, d=9, sigmaColor=75, sigmaSpace=75)

        noise_name = 'noise_image_' + str(prob)

        cv.imshow(noise_name, noise_image)
        cv.imshow('averaging_blur', averaging_blur)
        cv.imshow('median_blur', median_blur)
        cv.imshow('gaussian_blur', gaussian_blur)
        cv.imshow('bilateral_filter', bilateral_filter)

    if k == ord('c'):
        cv.destroyWindow(noise_name)
        cv.destroyWindow('averaging_blur')
        cv.destroyWindow('median_blur')
        cv.destroyWindow('gaussian_blur')
        cv.destroyWindow('bilateral_filter')

    if k == ord('q'):
        cv.destroyAllWindows()
        break
