# Take an image that has a closed object (rectangle, ball, smartphone), detect its contours using the findContours commands,
# and by selecting the contour of the object, enlarge this object using trackbar.

import cv2 as cv


def scale_roi(*args):
    scale_factor_ = 1 + args[0] / 100.0
    scaled_roi = cv.resize(roi, None, fx=scale_factor_, fy=scale_factor_, interpolation=cv.INTER_LINEAR)
    cv.imshow(ROI_name, scaled_roi)


image = cv.imread('smartphone.jpg')

# resize source image
scale_percent = 70
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv.resize(image, dim, interpolation=cv.INTER_AREA)
image_copy = image.copy()

# convert source image to gray
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

image_name = 'Image'
ROI_name = 'ROI'

# form thresh
ret, thresh = cv.threshold(gray_image, 150, 255, cv.THRESH_BINARY)

# find contours
contours, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

x, y, width, height = cv.boundingRect(contours[1])
roi = image_copy[y:y + height, x:x + width]

# create trackbar
scale_factor = 1

for i in range(0, 4):
    cv.drawContours(image=image_copy, contours=contours[i], contourIdx=-1, color=(0, 255, 0), thickness=2,
                    lineType=cv.LINE_AA)

cv.imshow(image_name, image_copy)
cv.createTrackbar("Scale", image_name, scale_factor, 100, scale_roi)

cv.waitKey(0)

for i in range(2, 4):
    x, y, width, height = cv.boundingRect(contours[i])
    roi = image_copy[y:y + height, x:x + width]

    cv.imshow(image_name, image_copy)

    cv.waitKey(0)

cv.destroyAllWindows()
