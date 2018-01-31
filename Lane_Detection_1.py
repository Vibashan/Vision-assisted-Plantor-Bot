#!/usr/bin/env python

import numpy as np
import cv2
import time

cap = cv2.VideoCapture('track_2.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    resize_img=cv2.resize(frame,(600,600))

    gray = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
    kernal= np.ones((5,5) , np.float32)/25
    median=cv2.medianBlur(gray, 25)


    ret,thresh = cv2.threshold(median,220,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    canny_edges = cv2.Canny(thresh,50,150)

    _,contours, h = cv2.findContours(canny_edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    sort=sorted(contours, key=cv2.contourArea, reverse=True)
    L1=sort[0]
    M1 = cv2.moments(L1)
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])

    cv2.circle(resize_img,(cx1,cy1),2,(255,0,0),4)

    cv2.imshow('frame',resize_img)
    #cv2.imshow('frame_1',resize_img)
    time.sleep(0.01)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()