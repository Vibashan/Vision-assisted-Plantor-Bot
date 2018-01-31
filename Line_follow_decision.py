#!/usr/bin/env python

import numpy as np
import cv2
import time

largest_area=0

cap = cv2.VideoCapture('track_move_4.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    resize_img=cv2.resize(frame,(600,600))
    crop_img=resize_img[300:600,0:600] 

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    kernal= np.ones((5,5) , np.float32)/25
    median=cv2.medianBlur(gray, 25)

    ret,thresh = cv2.threshold(median,220,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)  
    _,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>largest_area):
            Large_cnt=cnt
                  
    M = cv2.moments(Large_cnt) 
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print(cx)
    print(cy)
    cv2.line(crop_img,(300,600),(cx,cy),(255,0,0),2)
    cv2.line(crop_img,(300,600),(300,150),(0,255,0),2)

    if(0<cx<270):
        print "RIGHT"
    elif(330<cx<600):
        print "LEFT"
    else:
        print "STRAIGHT"

    cv2.imshow('frame',crop_img)
    time.sleep(0.05)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
