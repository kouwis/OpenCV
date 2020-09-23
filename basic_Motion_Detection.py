import cv2 as cv

cap = cv.VideoCapture("test.mp4")

_, frame1 = cap.read()
_, frame2 = cap.read()

while True:
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(threshold, None, iterations= 3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 1000:
            continue

        cv.rectangle(frame1, (x, y), (x+ w, y+ h), (0, 255, 255), 1)

    cv.imshow("DetectMotion", frame1)
    frame1 = frame2
    _, frame2 = cap.read()

    if cv.waitKey(20) & 0xff == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
