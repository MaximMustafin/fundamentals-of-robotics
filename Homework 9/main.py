import cv2 as cv
import numpy as np

cap = cv.VideoCapture('http://192.168.0.100:4747/mjpegfeed')

imgTarget = cv.imread('Rose.jpg')
scale_percent = 20
width = int(imgTarget.shape[1] * scale_percent / 100)
height = int(imgTarget.shape[0] * scale_percent / 100)
dim = (width, height)
imgTarget = cv.resize(imgTarget, dim, interpolation=cv.INTER_AREA)

myVideo = cv.VideoCapture('video4.mp4')

detection = False
frameCounter = 0

success, imgVideo = myVideo.read()
height_target, width_target, channel_target = imgTarget.shape
imgVideo = cv.resize(imgVideo, (width_target, height_target))

orb = cv.ORB_create(nfeatures=1000)
# sift = cv.SIFT_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget, None)
# kp1, des1 = sift.detectAndCompute(imgTarget, None)
# imgTarget = cv.drawKeypoints(imgTarget, kp1, None)

while True:
    success, imgWebcam = cap.read()
    imgAug = imgWebcam.copy()
    # (h, w) = imgWebcam.shape[:2]
    # (cX, cY) = (w // 2, h // 2)
    #
    # M = cv.getRotationMatrix2D((cX, cY), -90, 1.0)
    # imgWebcam = cv.warpAffine(imgWebcam, M, (w, h))

    kp2, des2 = orb.detectAndCompute(imgWebcam, None)
    # kp2, des2 = sift.detectAndCompute(imgWebcam, None)
    # imgWebcam = cv.drawKeypoints(imgWebcam, kp2, None)

    if detection == False:
        myVideo.set(cv.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0

    else:
        if frameCounter == myVideo.get(cv.CAP_PROP_FRAME_COUNT):
            myVideo.set(cv.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, imgVideo = myVideo.read()
        imgVideo = cv.resize(imgVideo, (width_target, height_target))

    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # flann = cv.FlannBasedMatcher()
    # matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print(len(good))
    imgFeatures = cv.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)

    if len(good) > 20:
        detection = True
        srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)  # looping and finding each of the
        # good matches
        dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, mask = cv.findHomography(srcPts, dstPts, cv.RANSAC, 5)
        print(matrix)

        pts = np.float32([[0, 0], [0, height_target], [width_target, height_target],
                          [width_target, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, matrix)
        img2 = cv.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)

        imgWarp = cv.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))

        maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
        cv.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
        maskInv = cv.bitwise_not(maskNew)
        imgAug = cv.bitwise_and(imgAug, imgAug, mask=maskInv)
        imgAug = cv.bitwise_or(imgWarp, imgAug)

    cv.imshow('maskNew', imgAug)
    cv.imshow('imgWarp', imgWarp)
    # cv.imshow('img2', img2)
    # cv.imshow('imgFeatures', imgFeatures)
    # cv.imshow('myVideo', imgVideo)
    cv.imshow('Webcam', imgWebcam)
    cv.waitKey(1)
    frameCounter += 1
