#!/usr/bin/env python

#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1B_2355.csv'
path_to_video_mp4_file_with_name = './Video.mp4'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
#####################################################################################################
def Shape(contours,color):
    M = cv2.moments(contours)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    approx = cv2.approxPolyDP(contours,0.01*cv2.arcLength(contours,True),True)
    if len(approx)==3:
	writecsv(color,"Triangle",(cx,cy))
    elif len(approx)==4:
	pts = np.array([approx[0], approx[1], approx[2],approx[3]]) 
	x = pts[[0,1,2,3], [0,0,0,0],[0,0,0,0]]
	y = pts[[0,1,2,3], [0,0,0,0],[1,1,1,1]]
	m1=(y[2]-y[0])/(x[2]-x[0])
	m2=(y[3]-y[1])/(x[3]-x[1])
	m=m1*m2
	if m==-1:
	   writecsv(color,"Rhombus",(cx,cy))
	else:
	   writecsv(color,"Trapizium",(cx,cy))
    elif len(approx)==5:
	writecsv(color,"Pentagon",(cx,cy))
    elif len(approx) == 6:
	writecsv(color,"Hexagon",(cx,cy))
    elif len(approx) > 9:
	writecsv(color,"Circle",(cx,cy))
    return
#Finding only required contour by removing unwanted/noise contours
def contour(contours):
    req_contours = []
    for cnt in contours:
	area=cv2.contourArea(cnt)
	if area >= 5000:
	   req_contours.append(cnt)		
    return req_contours
#Threshold the input images
def Color():
    lower_red = np.array([0,135,170],np.uint8)
    upper_red  = np.array([45,255,255],np.uint8)
    red=cv2.inRange(hsv,lower_red , upper_red )
    _,contours,h = cv2.findContours(red,3,2)
    req_contour_r=contour(contours)
  		
    lower_blue = np.array([83,120,120],np.uint8)
    upper_blue = np.array([170,255,255],np.uint8)
    blue=cv2.inRange(hsv, lower_blue, upper_blue)
    _,contours,h = cv2.findContours(blue,3,2)
    req_contour_b=contour(contours)	
	
    lower_green = np.array([50,110,100],np.uint8)
    upper_green = np.array([80,255,255],np.uint8)
    green=cv2.inRange(hsv, lower_green, upper_green)
    _,contours,h = cv2.findContours(green,3,2)
    req_contour_g=contour(contours)

    rb=cv2.add(red,blue)
    rbg=cv2.add(rb,green)
    _,contours,h = cv2.findContours(rbg,3,2)
    contours_all=contour(contours)

    return req_contour_r,req_contour_b,req_contour_g,rbg,contours_all


def main(video_file_with_path):
    global hsv
    req_contours = []
    all_old = 0
    r_old = 0
    b_old = 0
    g_old = 0
    a = 0
    color_r = "Red"
    color_b = "Blue"
    color_g = "Green"

    cap = cv2.VideoCapture(video_file_with_path)
    cap.set(cv2.CAP_PROP_FPS, 16.57)
    out = cv2.VideoWriter('Videooutput.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 16.57, (1280,720))
    image_red = cv2.imread("Overlay_Images/yellow_flower.png",-1)
    image_blue = cv2.imread("Overlay_Images/pink_flower.png",-1)
    image_green = cv2.imread("Overlay_Images/red_flower.png",-1)

    while(cap.isOpened()):
     ret, img = cap.read()
     hsv1=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
     kernal= np.ones((5,5) , np.float32)/25
     hsv = cv2.GaussianBlur(hsv1, (5,5), 0)
     contour_r,contour_b,contour_g,Current_img,req_all_contour = Color()
     #Checking for any Color(Contour) is appearing using bitwise operators( Not/And)
     r_new = len(contour_r)
     b_new = len(contour_b)
     g_new = len(contour_g)
     all_new = len(req_all_contour)
     if all_new > all_old :
       all_old = all_new
       if all_new == 1:
	   current_contour = req_all_contour[0]
	   previous_frame = Current_img
	   x,y,w,h = cv2.boundingRect(current_contour)
	   if r_new > r_old :
	    overlay_image = cv2.resize(image_red,(w,h))
	    req_shape = Shape(current_contour,color_r)
	    a = 1
	    r_old = r_new

           elif b_new > b_old :
	    overlay_image = cv2.resize(image_blue,(w,h))
	    req_shape = Shape(current_contour,color_b)
	    a = 2
	    b_old = b_new

	   elif g_new > g_old :
	    overlay_image = cv2.resize(image_green,(w,h))
            req_shape = Shape(current_contour,color_g)
	    a = 3
	    g_old = g_new
       else:
	   mask_inv = cv2.bitwise_not(previous_frame)
	   req_contour_frame = cv2.bitwise_and(Current_img,  Current_img,  mask=mask_inv)
	   _,contours,h = cv2.findContours(req_contour_frame,3,2)
	   current_contour = max(contours, key = cv2.contourArea)
           previous_frame = Current_img
	   x,y,w,h = cv2.boundingRect(current_contour)
           if r_new > r_old :
	    overlay_image = cv2.resize(image_red,(w,h))
	    req_shape = Shape(current_contour,color_r)
	    a = 1
	    r_old = r_new

           elif b_new > b_old :
	    overlay_image = cv2.resize(image_blue,(w,h))
	    req_shape = Shape(current_contour,color_b)
	    a = 2
	    b_old = b_new

	   elif g_new > g_old :
	    overlay_image = cv2.resize(image_green,(w,h))
            req_shape = Shape(current_contour,color_g)
	    a = 3
	    g_old = g_new
     #blend_transparent(Overlaying)
     if a == 1 : 
	img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:], overlay_image)
	
     elif a == 2: 
	img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:], overlay_image)

     elif a == 3:   
	img[y:y+h,x:x+w,:] = blend_transparent(img[y:y+h,x:x+w,:], overlay_image)
	
     cv2.imshow('img',img)
     out.write(img)
     cv2.waitKey(40)

    cap.release()
    cv2.destroyAllWindows()
    
#####################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main(path_to_video_mp4_file_with_name)
