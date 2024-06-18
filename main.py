import numpy as np
import cv2
import time

capImg = cv2.VideoCapture('2.mp4')

while (capImg.isOpened()):
    rat, frame = capImg.read()

    if frame is None:
        break
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # [750:1000, 0:950]
    # [550:800, 1000:2550] +1000 к изночальному х
    # [350:600, 0:1150]
    '''
        #Это маска для [350:600, 0:1150]
     
     low_Blue = np.array([90, 90, 90],
                    dtype="uint8")
    high_Blue = np.array([135, 255, 255],
                         dtype="uint8")

    low_Yel = np.array([25, 95, 100],
                   dtype="uint8")
    high_Yel = np.array([35, 100, 100],
    high_Red_O = np.array([5, 165, 155],
                          dtype="uint8")
    low_Red_V = np.array([165, 255, 40],
                 dtype="uint8")'''
    crop_frame = frame[750:1000, 0:950]
    crop_frame_hsv = frame_hsv[750:1000, 0:950]

    # настройка границ цвет. диап.
    low_Blue = np.array([100, 100, 100],
                    dtype="uint8")
    high_Blue = np.array([135, 255, 255],
                         dtype="uint8")

    low_Yel = np.array([25, 95, 100],
                   dtype="uint8")
    high_Yel = np.array([35, 100, 100],
                          dtype="uint8")
    low_Red_O= np.array([0, 85, 110],
               dtype="uint8")
    high_Red_O = np.array([5, 165, 155],
                          dtype="uint8")
    low_Red_V = np.array([165, 255, 40],
                 dtype="uint8")
    high_Red_V = np.array([180, 205, 120],
                          dtype="uint8")

    # наложение маски
    blue_mask = cv2.inRange(crop_frame_hsv, low_Blue,
                            high_Blue)

    yel_mask = cv2.inRange(crop_frame_hsv, low_Yel,
                           high_Yel)
    red1_mask = cv2.inRange(crop_frame_hsv,
                       low_Red_O, high_Red_O)
    red2_mask = cv2.inRange(crop_frame_hsv,
    low_Red_V, high_Red_V)

    full_mask = red1_mask + red2_mask + blue_mask +yel_mask

    contours, hierarchy = cv2.findContours(full_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for icontour in contours:
        rect = cv2.minAreaRect(icontour)
        area = int(rect[1][0] * rect[1][1])

        if area > 100:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            if box[2][1]!=0: print(box[2][1]) # вывод координаты
            cv2.drawContours(crop_frame, [box], 0,
            (0, 255, 255), 2)


    cv2.imshow("Crop_frame", crop_frame)

    time.sleep(0.1)
    key_press = cv2.waitKey(30)
    if key_press == ord('q'):
        break
capImg.release()
cv2.destroyAllWindows()


