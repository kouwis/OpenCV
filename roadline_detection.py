import cv2 as cv
import numpy as np

def ROI(img, vertices):
    mask = np.zeros_like(img)
    color = 255
    cv.fillPoly(mask, vertices, True, color)
    maskedImg = cv.bitwise_and(img, mask)
    return maskedImg

def drawLine(img, lines):
    img = np.copy(img)
    blank = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x, y, w, h in line:
            cv.line(blank, (x ,y), (w, h), (0, 0, 255), 10)
    img = cv.addWeighted(img, 0.8, blank, 1, 0)
    return img

def process(img):
    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]
    vertices = [
        (0, height),
        (900, 500),
        (width, height)
    ]
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 90, 120)
    dilated = cv.dilate(canny, None, 0)
    cropped = ROI(dilated, np.array([vertices], np.int32))
    lines = cv.HoughLinesP(
        cropped,
        rho=2,
        theta=np.pi/180,
        threshold=50,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=100
    )
    draw = drawLine(img, lines)
    return draw

cap = cv.VideoCapture("d.mp4")

while True:
    _, frame = cap.read()
    frame = process(frame)
    frame = cv.resize(frame, (720, 480))
    cv.imshow("LineDetection", frame)
    if cv.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv.destroyAllWindows()