# Homework 2, Task 1 - Use the city map image to annotate it by clicking on the starting point of the route,
# intermediate points to be connected with lines in order to indicate the route along the streets to reach the end point

import cv2 as cv
import math

route = []
isDrawing = True
map_ratio = 1.478
route_length = 0.0


def calculate_distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def mouse_click_event(event, x, y, flags, param):
    global route, route_length

    if event == cv.EVENT_LBUTTONDOWN and isDrawing:
        cv.circle(map_, (x, y), 3, (0, 0, 255), -1)
        route.append((x, y))

        if route:
            cv.line(map_, route[len(route) - 1], route[len(route) - 2], (255, 221, 28), 2)
            route_length += calculate_distance(route[len(route) - 1], route[len(route) - 2])


map_ = cv.imread('map_100m.png')

cv.imshow('map', map_)
cv.setMouseCallback('map', mouse_click_event)

while True:
    cv.imshow('map', map_)

    key = cv.waitKey(1)
    if key == ord('e'):
        break
    if key == ord('q') and isDrawing:
        isDrawing = False
        text = "Route's length = " + str(int(route_length * map_ratio)) + " meters"
        cv.putText(map_, text, (100, 600), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=2, color=(255, 0, 0))


cv.destroyAllWindows()
