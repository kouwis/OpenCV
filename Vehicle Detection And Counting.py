import cv2 as cv
import numpy as np

cap = cv.VideoCapture("traffic.mp4")
_, frame1 = cap.read()
_, frame2 = cap.read()
min_width = 40
min_height = 40
matches = []
line_length = 550
offset = 10
cars = 0

def get_centroid(x,y,w,h):

    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return cx,cy

def Image_Processing(frame1, frame2):
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, th = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilate = cv.dilate(th, np.ones((3,3)))
    closing = cv.morphologyEx(dilate, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2)))
    contours, h = cv.findContours(dilate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours

while True:

    for cnt in Image_Processing(frame1, frame2):

        (x, y, w, h) = cv.boundingRect(cnt)

        contour_valid = (w > min_width) and (h > min_height)

        if not contour_valid:
            continue
        cv.rectangle(frame1, (x - 5, y - 5), (x + w + 5, y + h + 5), (255, 255, 0), 2)
        cv.line(frame1, (0, line_length), (1300, line_length), (0, 255, 255), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv.circle(frame1, centroid, 5, (255, 0, 0), -1)
        for x, y in matches:
            if y < (line_length + offset) and y > (line_length - offset):
                cv.line(frame1, (0, line_length), (1300, line_length), (0, 0, 255), 7)
                cars += 1
                matches.remove((x, y))
                print(cars)

    cv.putText(frame1, "Number of cars: " + str(cars),(10,30), cv.FONT_HERSHEY_COMPLEX, 1.1, (0,0,0), 2)
    cv.imshow("frame", frame1)
    cv.waitKey(1)
    frame1 = frame2
    _, frame2 = cap.read()

cv.destroyAllWindows()
cap.release()