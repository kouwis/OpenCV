import cv2 as cv
import numpy as np
import time


def empty(x):
    pass

# Create Trackbars

cv.namedWindow("TrackBar")
cv.resizeWindow("TrackBars", 640, 240)
cv.createTrackbar("Hue Min", "TrackBar", 0, 179, empty)
cv.createTrackbar("Sat Min", "TrackBar", 0, 255, empty)
cv.createTrackbar("Val Min", "TrackBar", 0, 255, empty)
cv.createTrackbar("Hue Max", "TrackBar", 179, 179, empty)
cv.createTrackbar("Sat Max", "TrackBar", 255, 255, empty)
cv.createTrackbar("Val Max", "TrackBar", 255, 255, empty)

cap = cv.VideoCapture(0)
out = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

time.sleep(1)

for i in range(60):
    _, background = cap.read()

while True:

    _, img = cap.read()

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    h_min = cv.getTrackbarPos("Hue Min", "TrackBar")
    h_max = cv.getTrackbarPos("Hue Max", "TrackBar")
    s_min = cv.getTrackbarPos("Sat Min", "TrackBar")
    s_max = cv.getTrackbarPos("Sat Max", "TrackBar")
    v_min = cv.getTrackbarPos("Val Min", "TrackBar")
    v_max = cv.getTrackbarPos("Val Max", "TrackBar")

    # Get the clack's color
    lower1 = np.array([h_min, s_min, v_min])
    upper1 = np.array([h_max, s_max, v_max])

    # Get the complementary color
    lower2 = np.array([h_min+180, s_min, v_min])
    upper2 = np.array([h_max + 180, s_max, v_max])

    mask1 = cv.inRange(hsv, lower1, upper1)
    mask2 = cv.inRange(hsv, lower2, upper2)

    mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask1 = cv.morphologyEx(mask1, cv.MORPH_DILATE, np.ones((3,3), np.uint8))

    mask2 = cv.bitwise_not(mask1)

    # To get the background out from video
    res1 = cv.bitwise_and(img, img, mask=mask2)

    # To get the cloak out from video
    res2 = cv.bitwise_and(background, background, mask=mask1)

    # Add the background to the cloak
    output = cv.addWeighted(res2, 0.8, res1, 1, 0)

    out.write(output)

    cv.imshow("Invisible cloak", output)

    if cv.waitKey(1) & 0xff == ord("q"):
        break

cv.destroyAllWindows()
cap.release()
out.release()