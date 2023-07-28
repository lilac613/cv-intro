import cv2
import numpy as np
import matplotlib.pyplot as plt
import lane_detection

def get_lane_center(lanes):
    '''takes in list of lanes and returns intercept and slope of closest lane'''
    closest_slope = 0
    closest_intercept = 0
    closest_lane = lanes[0]
    for lane in lanes:

        center_slope = 1/((1/lane[0].get_slope() + 1/lane[1].get_slope())/2)
        center_intercept = (lane[0].get_x_intercept()[0] + lane[1].get_x_intercept()[0])/2
        if abs(center_slope) > abs(closest_slope):
            closest_lane = lane
            closest_slope = center_slope
            closest_intercept = center_intercept
    return [closest_lane]
    #return (closest_intercept,closest_slope)

def get_center_line(lane):
    center_slope = 1/((1/lane[0].get_slope() + 1/lane[1].get_slope())/2)
    center_intercept = (lane[0].get_x_intercept()[0] + lane[1].get_x_intercept()[0])/2

def draw_center_lane(img, center_intercept, center_slope, xPoint, yPoint):
    global imgPixelHeight
    imgPixelHeight = img.shape[0]
    cv2.line(img, (int(center_intercept), imgPixelHeight), (int(xPoint), int(yPoint)), (0,0,255), 6)
    return img

def recommend_direction(center,slope):
    '''Takes the center of the closest lane and its slope as inputs and returns a direction'''
    if slope < 0:
        return "left"
    elif slope > 0:
        return "right"
    return "forward"

