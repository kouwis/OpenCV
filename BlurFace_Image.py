import cv2 as cv

img = cv.imread("ImagePath")
imgCopy = img.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(gray, 1.1, 2, cv.CASCADE_SCALE_IMAGE, (30,30))

for pixel in faces:
    x, y, w, h = [i for i in pixel]
    cv.rectangle(img, (x,y), (x+w, y+h), None, None)
    sub_face = img[y:y+h, x:x+w]
    sub_face = cv.GaussianBlur(sub_face, (27,27), 30)
    imgCopy[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face

cv.imshow("BlurFace", imgCopy)
cv.waitKey(0)
cv.destroyAllWindows()