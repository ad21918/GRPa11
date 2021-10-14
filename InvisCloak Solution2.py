# DataFlair Invisible Cloak project using OpenCV.

import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

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

# Store a single frame as background 
_, background = cap.read()
time.sleep(5)
_, background = cap.read()

#define all the kernels size  
open_kernel = np.ones((8, 8),np.uint8)
close_kernel = np.ones((9, 9),np.uint8)
dilation_kernel = np.ones((10, 10), np.uint8)

# Function for remove noise from mask 
def filter_mask(mask):

    close_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)

    open_mask = cv2.morphologyEx(close_mask, cv2.MORPH_OPEN, open_kernel)

    dilation = cv2.dilate(open_mask, dilation_kernel, iterations = 5)

    return dilation


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
        
while cap.isOpened():
    ret, frame = cap.read()  # Capture every frame
    # convert to hsv colorspace 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Filter mask
    mask = filter_mask(mask)

    # Apply the mask to take only those region from the saved background 
    # where our cloak is present in the current frame
    cloak = cv2.bitwise_and(background, background, mask=mask)

    # create inverse mask 
    inverse_mask = cv2.bitwise_not(mask)

    # Apply the inverse mask to take those region of the current frame where cloak is not present 
    current_background = cv2.bitwise_and(frame, frame, mask=inverse_mask)

    # Combine cloak region and current_background region to get final frame 
    combined = cv2.add(cloak, current_background)

    cv2.imshow("Final output", combined)
    
    k = cv2.waitKey(10)
    if k==27:
        break
    
cap.release()
cv2.destroyAllWindows()