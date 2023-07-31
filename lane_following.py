import cv2
import numpy as np
import matplotlib.pyplot as plt
import lane_detection

def get_lane_center(lanes: list[(lane_detection.Line,lane_detection.Line)]):
    '''Finds lane closest to robot
    Args:
        lanes (list[(Line,Line)]): list of lanes
    
    Returns:
    the lane closest to the center frame of the robot'''

    steepest_slope = 0
    closest_lane = lanes[0]

    for lane in lanes:
        current_slope = max(abs(lane[0].get_slope()),abs(lane[1].get_slope()))
        # compare steeper slopes
        if current_slope > steepest_slope:
            closest_lane = lane
            steepest_slope = current_slope
    return [closest_lane]
    #return (closest_intercept,closest_slope)

def get_center_line(lane: list[(lane_detection.Line,lane_detection.Line)], screen_height: int=180) -> lane_detection.Line:
    '''Finds the center line based on the center lane
    Args:
        lane (list[(Line,Line)]): list of lanes
        screen_height (int,optional): height of screen'''
    center_slope = 1/((1/lane[0].get_slope() + 1/lane[1].get_slope())/2)
    center_intercept = (lane[0].get_x_intercept()[0] + lane[1].get_x_intercept()[0])/2
    x1 = ((-1*screen_height) + center_slope * center_intercept)/center_slope
    return lane_detection.Line(x1,0,center_intercept,screen_height)

def recommend_direction(x_intercept: int,slope: float, line: lane_detection.Line, width:int = 650):
    '''Determines the heading for the robot compared to the center line
    Args:
        x_intercept (int): x=intercept of center line
        slope (int): slope of center line
        line (Line): center line
        width (int, optional): width of screen'''
    msg = ""
    mid_right = width/2 + 50
    mid_left = width/2 - 50
    strafe_direction = ""
    direction = ""

    # if the line is almost horizontal
    if abs(slope) < 0.2:
        print("turn left or right 45 degrees")

    # if line is on right side of screen and relatively vertical
    if  x_intercept > mid_right and x_intercept < width:
        strafe_direction = "crab right"
    # if line is on left side of screen and relatively vertical
    elif x_intercept < mid_left and x_intercept > 0:
        strafe_direction = "crab left"
    # if line is relatively horizontal
    else:
        strafe_direction = "strafe forward"
    print(strafe_direction)

    # instructions for which direction to turn
    if slope < 0:
        msg = "rotate right "
        direction =  "counter-clockwise"
    elif slope > 0:
        msg = "turn left "
        direction = "clockwise"

    # get angle at which to turn
    opposite = max(line.get_points()[1],line.get_points()[3]) - min(line.get_points()[1], line.get_points()[3])
    hypotenuse = line.length()
    turn_in_radians = np.arccos(opposite/hypotenuse)
    turn_in_degrees = turn_in_radians*180/np.pi
    msg += "by " + str(turn_in_degrees) + " degrees " + direction
    print(msg)

    return strafe_direction

