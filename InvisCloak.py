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
lower_bound = np.array([0, 0, 0])
upper_bound = np.array([0, 0, 0])
lower_bounds = {
    "white": np.array([0, 0, 180]),
    "green": np.array([55, 80, 60]),
    "blue": np.array([80, 120, 10]),
    "black": np.array([0, 0, 0]),
    "red" : np.array([0, 15, 90]),
    "red2": np.array([170, 15, 90])
}
upper_bounds = {
    "white": np.array([170, 105, 255]),
    "green": np.array([90, 255, 255]),
    "blue": np.array([130, 255, 255]),
    "black" : np.array([255, 0, 10]),
    "red": np.array([30, 255, 255]),
    "red2": np.array([180,255,255])
    }
while True:
    try:
        print("\nColour List;")
        print("blue\nwhite\ngreen\nblank\nblack")
        hue = input("Please type the colour of your cloak: ")
        
        if hue == ('white'):
            lower_bound = lower_bounds["white"]
            upper_bound = upper_bounds["white"]
            break
        elif hue == ('green'):
            lower_bound = lower_bounds["green"]
            upper_bound = upper_bounds["green"]
            break
        elif hue == ('blue'):
            lower_bound = lower_bounds["blue"]
            upper_bound = upper_bounds["blue"]
            break
        elif hue == ('black'):
            lower_bound = lower_bounds["black"]
            upper_bound = upper_bounds["black"]
            break
        elif hue == 'red':
            lower_bound = lower_bounds["red"]
            upper_bound = upper_bounds["red"]
            break
        else:
            print("Invalid Input, please enter a value listed")
    except ValueError:
        print("Enter only values from the list")

time.sleep(6)
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
    if hue == 'red':
        lower_bound = lower_bounds['red']
        upper_bound = upper_bounds['red']
    mask1 = cv2.inRange(hsv, lower_bound,upper_bound)
    if hue == 'red':
        lower_bound = lower_bounds['red2']
        upper_bound = upper_bounds['red2']
    mask2 = cv2.inRange(hsv, lower_bound,upper_bound)
#Combining the masks so that It can be viewd as in one frame
    mask1 = mask1 + mask2
#After combining the mask we are storing the value in deafult mask.
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations = 5)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations = 1)

    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(background,background,mask=mask1)
    res2 = cv2.bitwise_and(img,img,mask=mask2)
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow('Invisible Cloak',final_output)
    k = cv2.waitKey(10)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()