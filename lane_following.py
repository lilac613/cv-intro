import cv2
import numpy as np
import matplotlib.pyplot as plt
from dt_apriltags import Detector
import lane_detection.py

def get_lane_center(lanes):
    '''takes in list of lanes and returns intercept and slope of closest lane'''
    for lane in lanes:
        