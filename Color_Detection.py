import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

cv.namedWindow("threshold")

def nothing(x):
    print(x)

    return x

cv.createTrackbar("LH", "threshold", 0, 255, nothing)
cv.createTrackbar("LS", "threshold", 0, 255, nothing)
cv.createTrackbar("LV", "threshold", 0, 255, nothing)
cv.createTrackbar("UH", "threshold", 255, 255, nothing)
cv.createTrackbar("US", "threshold", 255, 255, nothing)
cv.createTrackbar("UV", "threshold", 225, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lh = cv.getTrackbarPos("LH", "threshold")
    ls = cv.getTrackbarPos("LS", "threshold")
    lv = cv.getTrackbarPos("LV", "threshold")
    uh = cv.getTrackbarPos("UH", "threshold")
    us = cv.getTrackbarPos("US", "threshold")
    uv = cv.getTrackbarPos("UV", "threshold")

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])

    mask = cv.inRange(hsv, lower, upper)

    res = cv.bitwise_and(frame, frame, mask= mask)

    cv.imshow("DetectedFrame", res)
    cv.imshow("OrgFrame", frame)
    if cv.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv.destroyAllWindows()