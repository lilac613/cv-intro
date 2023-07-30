import cv2
import numpy as np
import matplotlib.pyplot as plt
import lane_detection

def get_lane_center(lanes: list[lane_detection.Line]):
    '''Finds lane closest to robot'''
    steepest_slope = 0
    closest_lane = lanes[0]
    for lane in lanes:
        current_slope = max(abs(lane[0].get_slope()),abs(lane[1].get_slope()))
        #center_intercept = (lane[0].get_x_intercept()[0] + lane[1].get_x_intercept()[0])/2
        if current_slope > steepest_slope:
            closest_lane = lane
            steepest_slope = current_slope
    return [closest_lane]
    #return (closest_intercept,closest_slope)

def get_center_line(lane, screen_height=180):
    '''Finds the center line based on the center lane'''
    center_slope = 1/((1/lane[0].get_slope() + 1/lane[1].get_slope())/2)
    center_intercept = (lane[0].get_x_intercept()[0] + lane[1].get_x_intercept()[0])/2
    x1 = ((-1*screen_height) + center_slope * center_intercept)/center_slope
    return lane_detection.Line(x1,0,center_intercept,screen_height)

def draw_center_lane(img, center_intercept, center_slope, xPoint, yPoint):
    global imgPixelHeight
    imgPixelHeight = img.shape[0]
    cv2.line(img, (int(center_intercept), imgPixelHeight), (int(xPoint), int(yPoint)), (0,0,255), 6)
    return img

def recommend_direction(x_intercept,slope, width = 650):
    '''Takes the center of the closest lane and its slope as inputs and returns a direction'''
    mid_right = width/2 + 100
    mid_left = width/2 - 100
    strafe_direction = ""
    if  x_intercept > mid_right and x_intercept < width:
        strafe_direction = "right"
    elif x_intercept < mid_left and x_intercept > 0:
        strafe_direction = "left"
    else:
        strafe_direction = "forward"
    
    if slope < 0:
        print("turn right")
    elif slope > 0:
        print("turn left")

    return strafe_direction

