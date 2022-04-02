# Homework 1, Task 1 - Divide an image in patches and saves them to the disk as a patch with series names

import cv2 as cv

image = cv.imread('image.jpg')  # reading image from directory

image_height = image.shape[0]  # put image's height to variable
image_width = image.shape[1]  # put image's width to variable

m = int(image_height / 3)  # how many patches is needed to divide an image
n = int(image_width / 3)

k = 100

# dividing an image to patches, and saving them to images
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
