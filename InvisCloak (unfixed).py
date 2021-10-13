# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:42:04 2021

@author: brand
"""

import numpy as np
import cv2 #opencv for image processing
#creating a videocapture object
import time
cap = cv2.VideoCapture(0) #this is my webcam
lower_bound = np.array([])
upper_bound = np.array([])
lower_bounds = {
    "blue" : np.array([78, 146, 10]),
    "white" : np.array([0, 0, 168]),
    "green" : np.array([50, 80, 50]),
    "blank" : np.array([0, 60, 0])
}
upper_bounds = {
    "blue": np.array([140, 255, 255]),
    "white": np.array([172, 111, 255]),
    "green": np.array([90, 255, 255]),
    "blank": np.array([255, 255, 255])
    }
colour = input("Please type the colour of your cloak: ")
time.sleep(5)
background = 0
#getting the background image
for i in range(50):
    ret, background = cap.read()
while cap.isOpened():
    ret, img = cap.read() #simply reading from the web cam
    if not ret:
        break
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #all this Comes in the while loop
    key = colour
    if key == ord('q'):
        break
    elif key == ord('b'):
        lower_bound = lower_bounds["blue"]
        upper_bound = upper_bounds["blue"]
    elif key == ord('w'):
        lower_bound = lower_bounds["white"]
        upper_bound = upper_bounds["white"]
    elif key == ord('g'):
        lower_bound = lower_bounds["green"]
        upper_bound = upper_bounds["green"]
    print(lower_bound)
    print(upper_bound)
    upper_bound = upper_bound
    lower_bound = lower_bound
    mask1 = cv2.inRange(hsv, lower_bound,upper_bound)
    upper_bound = upper_bound
    lower_bound = lower_bound
    mask2 = cv2.inRange(hsv,lower_bound,upper_bound)
#Combining the masks so that It can be viewd as in one frame
    mask1 = mask1 + mask2
#After combining the mask we are storing the value in deafult mask.
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations = 2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations = 1)

    mask2 =cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(background,background,mask=mask1)
    res2 = cv2.bitwise_and(img,img,mask=mask2)
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow('Invisible Cloak',final_output)
    k = cv2.waitKey(10)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()