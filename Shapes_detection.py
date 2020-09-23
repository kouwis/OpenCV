import cv2

img = cv2.imread("Image path")
img2 = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
dilated = cv2.dilate(threshold, None, 0)
contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


img2 = cv2.resize(img, (520, 480))
cv2.imshow("img", img2)



for contour in contours:
    if cv2.contourArea(contour) < 300:   #Select the best value for area from [120, 300, 2000, 5300] to get the best accuracy
        continue
    else:
        approx = cv2.approxPolyDP(contour, 0.009* cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], 0, (210, 200, 150), 3)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

        elif len(approx) == 4:
            x1 ,y1, w, h = cv2.boundingRect(approx)
            aspectRatioSq = float(w)/h

            if aspectRatioSq >= 0.95 and aspectRatioSq <= 1.05:
              cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

            else:
              cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

        elif len(approx) == 5:
            cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        elif len(approx) == 6:
            cv2.putText(img, "Hexagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        elif len(approx) == 7:
            cv2.putText(img, "Heptagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        elif len(approx) == 8:
            cv2.putText(img, "Octagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        elif len(approx) == 10:
            cv2.putText(img, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        elif len(approx) == 13:
            cv2.putText(img, "Heart", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        else:
            cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

img = cv2.resize(img, (520, 480))
cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
