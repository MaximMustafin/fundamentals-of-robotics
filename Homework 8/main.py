# import math
import numpy as np
import cv2 as cv


def measure_distance_and_size(img_, fx_, number_of_contour):
    image_copy = img_
    gray_ = cv.cvtColor(img_, cv.COLOR_BGR2GRAY)
    img_median_blur = cv.medianBlur(gray_, ksize=5)

    kernel = np.ones((5, 5))

    img_canny = cv.Canny(img_median_blur, 100, 200)
    img_dial_canny = cv.dilate(img_canny, kernel, iterations=3)
    img_thre_canny = cv.erode(img_dial_canny, kernel, iterations=3)

    contours, hierarchy = cv.findContours(image=img_thre_canny, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

    # for i in range(0, len(contours)):
    #     cv.drawContours(image=image_copy, contours=contours[i], contourIdx=-1, color=(0, 255, 0), thickness=2,
    #                     lineType=cv.LINE_AA)
    #
    #     print(i)
    #     cv.imshow('Image', image_copy)
    #     cv.waitKey(1000)

    roi_contours = contours[number_of_contour]
    cv.drawContours(image=image_copy, contours=roi_contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                    lineType=cv.LINE_AA)
    x, y, width_, length_ = cv.boundingRect(roi_contours)
    print('x = ', x)
    print('y = ', y)
    print('width = ', width_, 'px')
    print('length = ', length_, 'px', '\n')

    real_chess_square_mm = 25

    distance = round(((real_chess_square_mm * fx_) / width_) / 10, 3)
    real_width = round((width_ * distance) / fx_, 2)
    real_height = round((length_ * distance) / fx_, 2)

    cv.putText(img_, 'Distance = ' + str(distance) + ' cm;',
               (50, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv.putText(img_, 'Width = ' + str(real_width) + ' cm, Length = ' + str(real_height) + ' cm',
               (50, 80), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv.imshow('Thre Canny', img_thre_canny)
    cv.imshow('Image', img_)

    cv.waitKey(0)


scale_percent = 30
ddepth = cv.CV_16S
scale = 1
delta = 0
lst_of_images = []

# iterator for file savings
it = 1

# 1.
######################################################################################################################

# Defining the dimensions of checkerboard
CHECKERBOARD = (7, 10)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
obj_points = []
# Creating vector to store vectors of 2D points for each checkerboard image
img_points = []

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
images_path = 'Images/'
for i in range(1, 56):
    img = cv.imread(images_path + str(i) + '.jpg')

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # gray = cv.GaussianBlur(gray, (7, 7), 0)

    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH +
                                            cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

    """
        If desired number of corner are detected,
        we refine the pixel coordinates and display
        them on the images of checker board
    """
    if ret:
        obj_points.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        img_points.append(corners2)

        # Draw and display the corners
        img = cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        lst_of_images.append(img)

        # cv.imwrite('FoundChessboard/' + 'img_' + str(it) + '.jpg', img)

        cv.putText(img, str(it), (50, 100), cv.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)

        cv.imshow('img', img)
        key = cv.waitKey(700)

    it += 1

cv.destroyAllWindows()

h, w = lst_of_images[0].shape[:2]

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)

fx = mtx[0, 0]
fy = mtx[1, 1]

print('fx = ', fx)  # fx
print('fy = ', fy)  # fy

# 2.
######################################################################################################################

ref_image = cv.imread('Images/ref_1.jpg')
image_with_coin = cv.imread('Images/coin_2.jpg')
image_with_rect = cv.imread('Images/rect_5.jpg')

width = int(image_with_coin.shape[1] * scale_percent / 100)
height = int(image_with_coin.shape[0] * scale_percent / 100)
dim = (width, height)

ref_image = cv.resize(ref_image, dim, interpolation=cv.INTER_AREA)
image_with_coin = cv.resize(image_with_coin, dim, interpolation=cv.INTER_AREA)
image_with_rect = cv.resize(image_with_rect, dim, interpolation=cv.INTER_AREA)

measure_distance_and_size(img_=ref_image, fx_=fx, number_of_contour=19)
measure_distance_and_size(img_=image_with_coin, fx_=fx, number_of_contour=63)

image_copy_rect = image_with_rect
gray = cv.cvtColor(image_copy_rect, cv.COLOR_BGR2GRAY)

corners = cv.goodFeaturesToTrack(gray, 150, 0.01, 10, useHarrisDetector=True)
corners = np.int0(corners)

x_1, y_1 = corners[93].ravel()
x_2, y_2 = corners[94].ravel()
x_3, y_3 = corners[97].ravel()
x_4, y_4 = corners[108].ravel()

cv.circle(image_with_rect, (x_1, y_1), 3, (255, 0, 0), -1)  # Blue
cv.circle(image_with_rect, (x_2, y_2), 3, (0, 255, 0), -1)  # Green
cv.circle(image_with_rect, (x_3, y_3), 3, (0, 0, 255), -1)  # Red
cv.circle(image_with_rect, (x_4, y_4), 3, (255, 0, 255), -1)  # Purple

# length_rect = int(math.sqrt((x_2 - x_4) ** 2 + (y_2 - y_4) ** 2))
# width_rect = int(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2))

length_rect = int(cv.norm(corners[108].ravel() - corners[94].ravel()))
width_rect = int(cv.norm(corners[108].ravel() - corners[97].ravel()))

print('length = ', length_rect)
print('width = ', width_rect)

real_chess_square_mm = 25

distance_rect = round(((real_chess_square_mm * 3 * fx) / width_rect) / 10, 3)
real_width_rect = round((width_rect * distance_rect) / fx, 2)
real_length_rect = round((length_rect * distance_rect) / fx, 2)

cv.putText(image_with_rect, 'Distance = ' + str(distance_rect) + ' cm;',
           (50, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

cv.putText(image_with_rect, 'Width = ' + str(real_width_rect) + ' cm, Length = ' + str(real_length_rect) + ' cm',
           (50, 80), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

cv.imshow('Image', image_with_rect)

# k = 0
# for i in corners:
#     x, y = i.ravel()
#     cv.circle(image_with_rect, (x, y), 3, 255, -1)
#     cv.imshow('Image', image_with_rect)
#     print(k)
#     k += 1
#     cv.waitKey(500)

cv.waitKey(0)
