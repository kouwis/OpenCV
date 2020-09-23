import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorKNN()

while True:

    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (360,280))

    canny = cv.Canny(gray, 60, 200)
    canny = cv.resize(canny, (360, 280))

    gray_bilateral = cv.bilateralFilter(gray, 20, 50, 50)
    fgbg_ = fgbg.apply(gray_bilateral)

    canny_b = cv.Canny(gray_bilateral, 60, 200)
    canny_b = cv.resize(canny_b, (360,280))

    h_stick = np.hstack((gray, canny, canny_b, fgbg_))
    cv.imshow("Bilateral", h_stick)
    if cv.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv.destroyAllWindows()