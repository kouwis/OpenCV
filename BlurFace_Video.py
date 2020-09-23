import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()
    framec = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

    faces = cascade.detectMultiScale(gray, 1.1, 2, cv.CASCADE_SCALE_IMAGE, (30, 30))
    for pixel in faces:
        x, y, w, h = [i for i in pixel]
        cv.rectangle(frame, (x, y), (x+w, y+h), None, None)
        sub_face = frame[y:y+h, x:x+w]
        sub_face = cv.GaussianBlur(sub_face, (29, 29), 30)
        framec[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
    framec = cv.resize(framec, (480,360))
    cv.imshow("BlurVideo", framec)
    if cv.waitKey(30) & 0xff == ord("q"):
        break
cap.release()
cv.destroyAllWindows()