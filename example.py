from email.policy import default
import cv2
 
img = cv2.imread('./data/t.png')
cv2.imshow('img', img)
drag = False
default_x, default_y, w, h = -1, -1, -1, -1
green = (0, 255, 0) 

def mouse(event, x, y, flag, param):
    global drag, default_x, default_y, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drag = True
        default_x = x
        default_y = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drag:
            draw = img.copy()
            cv2.rectangle(draw, (default_x, default_y), (x, y), green, 2)
            cv2.imshow("img", draw)

    elif event == cv2.EVENT_LBUTTONUP:
        if drag:
            drag = False
            w = x - default_x
            h = y - default_y
            if w > 0 and h > 0:
                draw = img.copy()
                cv2.rectangle(draw, (default_x, default_y), (x, y), green, 2)
                cv2.imshow("img", draw)
                
            else:
                cv2.imshow('img', img)

# 원본 이미지인 img를 띄워주는 코드는 없음
cv2.setMouseCallback('img', mouse)
cv2.waitKey()
cv2.destroyAllWindows()