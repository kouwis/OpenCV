import cv2 as cv
import numpy as np

# This function to get the Region of interests for every frame
def ROI(img, vertices):

    mask = np.zeros_like(img)
    cv.fillPoly(mask, vertices, True, 100)
    maskedImg = cv.bitwise_and(img, mask)

    return maskedImg

# This function to draw detected line and get steering advice
def Draw_line(img, lines):

    img = np.copy(img)
    blank = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x, y, w, h in line:
            cv.line(blank, (x, y), (w, h), (0, 0, 255), 10)

            # Here to get start and end points in lanes to make a steering advice
            top_right = int(lines[0][0][0])
            top_left = int(lines[0][0][1])
            bot = int(lines[0][0][3])
            mid = int((top_right + top_left) / 2)
            cv.line(blank, (mid, top_left), (mid, bot), (0, 255, 0), 2)
            right = np.abs(mid - top_right)
            left = np.abs(mid - top_left)
            if (right and left) < 160: # 160 is a Random variable
                continue
            elif right > left and right > 160:
                cv.line(blank, (mid, top_left), (top_left, top_left), (255,255,255), 4)
                cv.putText(blank, "Turn Left",  (mid - 30, top_left - 30), cv.FONT_HERSHEY_COMPLEX, 1.1, (0,255,0), 3)
            else:
                cv.line(blank, (mid, top_left), (top_right, top_left), (255, 255, 255), 4)
                cv.putText(blank, "Turn Right", (mid - 30, top_left - 30), cv.FONT_HERSHEY_COMPLEX, 1.1, (0, 255, 0), 3)

    # Here to add blank img to the original img
    img = cv.addWeighted(img, 0.8, blank, 1, 0)

    return img

# This function to preprocess every frame in video
def Img_process(frame):

    height = frame.shape[0]
    width = frame.shape[1]
    vertices = [
        (0 , height),
        (900, 500), # These are the best height and width variables after many attempts in this video
        (width, height)
    ]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7,7), 2)
    canny = cv.Canny(blur, 100, 200)
    dilate = cv.dilate(canny, np.ones((7,7)))
    cropped = ROI(dilate, np.array([vertices], np.int32))
    lines = cv.HoughLinesP(
        cropped,
        rho= 1,
        theta= np.pi/180,
        threshold= 15,
        lines=np.array([]),
        minLineLength=30,
        maxLineGap=40
    )
    draw = Draw_line(frame, lines)
    return draw

cap = cv.VideoCapture("Roadline.mp4")

while True:

    _, frame = cap.read()
    frame = Img_process(frame)
    frame = cv.resize(frame, (640,400))
    cv.imshow("Frame", frame)
    if cv.waitKey(50) & 0xff == ord("q"):
        break

cap.release()
cv.destroyAllWindows()