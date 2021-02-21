import cv2 as cv
import numpy as np


cv.namedWindow("image")
img = cv.imread("cards.jpg")

# This for cam
# cap = cv.VideoCapture(0)

height = img.shape[0]
width = img.shape[1]
border = [[0,0], [width, 0], [width, height], [0, height]]
points = []

def mouse_clicks(event, x, y, flags, param):

    if event == cv.EVENT_LBUTTONDOWN:
        points.append([x,y])

        if len(points) == 4:
            m = cv.getPerspectiveTransform(np.float32(points), np.float32(border))
            out = cv.warpPerspective(img, m, (width, height))
            cv.imshow("warp", out)

cv.setMouseCallback("image", mouse_clicks)

while True:

    # _, img = cap.read()

    cv.imshow("image", img)
    if cv.waitKey(1) & 0xff == ord("q"):
        break

cv.destroyAllWindows()