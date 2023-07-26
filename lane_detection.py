import cv2
import numpy as np
import matplotlib.pyplot as plt
from dt_apriltags import Detector

class Line:
    def __init__(self,x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def get_slope(self):
        '''returns slope of line'''
        if self.x1==self.x2:
            return None
        return (self.y2-self.y1)/(self.x2-self.x1)
    def get_x_intercept(self):
        '''returns x-ntercept of line'''
        if self.y1==self.y2:
            return None
        return ((self.get_slope()*self.x1 - self.y1)/self.get_slope(),0)
    def get_points(self):
        return (self.x1, self.y1, self.x2, self.y2)

def detect_lines(img, threshold1, threshold2, apertureSize,minLineLength,maxLineGap):
    '''Takes an image as input and returns a list of detected lines'''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                100,
                minLineLength,
                maxLineGap,
        ) # detect lines
    ret_lines = []
    for line in lines:

        x1, y1, x2, y2 = line[0]
        ret_lines.append(Line(x1,y1,x2,y2))

    return ret_lines

def draw_lines(img, lines, color=(0,255,0)):
    '''Takes an image and a list of lines as inputs and returns an image with the lines drawn on it'''
    for line in lines:
        (x1, y1, x2, y2) = line.get_points()
        cv2.line(img, (x1,y1), (x2,y2), color, 2)
    return img

def get_slope_intercepts(lines):
    '''Takes in list of lines as input and returns a list of slopes and a list of intercepts'''
    slopes = []
    intercepts = []
    for line in lines:
        slopes.append(line.get_slope())
        intercepts.append(line.get_x_intercept())
    return (slopes,intercepts)

def get_array_x_int(elem):
    return elem[1]

def filterLines(lines):
    lineData = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        #print(line[0])
        slope = (y2 - y1)/(x2 - x1)
        xInt = (slope * x1 - y1) / slope
        lineData.append([slope, xInt, x1, y1, x2, y2])
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #print(lineData)

    cleanedLines = []
    for line in lineData:
        #loop thru cleanedLines, see if line with close enough slope is already within cleanedlines 
        canAdd = True
        for cleanedLine in cleanedLines:
            #if exists, set canAdd to false
            if abs(cleanedLine[1] - line[1]) < 3:
                canAdd = False

        if canAdd:
            cleanedLines.append(line)
        return cleanedLines

def detect_lanes(lines):
    '''Takes a list of lines as an input and returns a list of lanes
    # xinterceptsUnsorted = [point[0] for point in lines]
    # xintercepts = xinterceptsUnsorted.sort()

    # solely get intercept points
    (_, intercept_points) = get_slope_intercepts(lines)
    # disregard y-coordinate of x-intercept
    x_intercepts = [point[0] for point in intercept_points]
    # key: value -> x-intercept, line
    unsorted_intercept_and_line = dict(zip(x_intercepts,lines))

    # sort dictionary by key
    intercept_and_line = dict(sorted(unsorted_intercept_and_line.items()))

    for index,key in enumerate(intercept_and_line.keys()):'''
    
    lanes = []
    cleanedLines = filterLines(lines)
    cleanedLines.sort(key=get_array_x_int)

    pairBefore = False
    startPoint = 1
    endPoint = len(cleanedLines)
    if (cleanedLines[1][1] - cleanedLines[0][1]) < (cleanedLines[2][1] - cleanedLines[1][1]):
        startPoint = 0
        pairBefore = True
    if (pairBefore and len(cleanedLines)%2 != 0) or (not pairBefore and len(cleanedLines)%2==0):
        endPoint = len(cleanedLines)-1
    for i in range(startPoint,endPoint,2):
        lanes.append((cleanedLines[i],cleanedLines[i+1]))
    return lanes

def draw_lanes(img,lanes):
    '''Takes an image and list of lanes as inputs and returns an image with lanes drawn on it'''
    return draw_lines(img, lanes, (0,255,0))






    
    
    


    


