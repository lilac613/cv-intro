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
        self.d = False
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
    def length(self):
        return ((self.x1-self.x2)**2 + (self.y1-self.y2)**2)**0.5
    def dealt(self,bool):
        self.d = bool
    def dealtWith(self):
        return self.d

def detect_lines(my_img, threshold1, threshold2, apertureSize,minLineLength,maxLineGap):
    '''Takes an image as input and returns a list of detected lines'''
    gray = cv2.cvtColor(my_img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    #edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) # detect edges
    edges = cv2.Canny(gray,0, 45, apertureSize=3)
    lines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi/180,
                threshold=100,
                minLineLength=100,
                maxLineGap=30,
        )
    ret_lines = []
    for line in lines:

        x1, y1, x2, y2 = line[0]
        ret_lines.append(Line(x1,y1,x2,y2))

    return ret_lines

def draw_lines(img, lines, color=(0,255,0)):
    '''Takes an image and a list of lines as inputs and returns an image with the lines drawn on it'''
    temp_img =img
    for line in lines:
        (x1, y1, x2, y2) = line.get_points()
        cv2.line(temp_img, (x1,y1), (x2,y2), color, 2)
    return temp_img

def get_slope_intercepts(lines):
    '''Takes in list of lines as input and returns a list of slopes and a list of intercepts'''
    slopes = []
    intercepts = []
    for line in lines:
        slopes.append(line.get_slope())
        intercepts.append(line.get_x_intercept())
    return (slopes,intercepts)

def filterLines(lines):
    '''removes collinear lines'''
    print("SDF")
    cleanedLines = []
    for i in range(len(lines)):
        if lines[i].dealtWith():
            continue
        current_slope = lines[i].get_slope()
        minx1 = min(lines[i].get_points()[0],lines[i].get_points()[2])
        miny1 = min(lines[i].get_points()[1],lines[i].get_points()[3])
        maxx2 = max(lines[i].get_points()[0],lines[i].get_points()[2])
        maxy2 = max(lines[i].get_points()[1],lines[i].get_points()[3])
        for j in range(i+1,len(lines)):
            if abs(lines[j].get_slope() - current_slope)<1 and not lines[j].dealtWith():
                minx1 = min(lines[j].get_points()[0],lines[j].get_points()[2],minx1)
                miny1 = min(lines[j].get_points()[1],lines[j].get_points()[3],miny1)
                maxx2 = max(lines[j].get_points()[2],lines[j].get_points()[0],maxx2)
                maxy2 = max(lines[j].get_points()[3],lines[j].get_points()[1],maxy2)
                lines[j].dealt(True)
        cleanedLines.append(Line(minx1,miny1,maxx2,maxy2))

    # for line in lines:
    #     #loop thru cleanedLines, see if line with close enough slope is already within cleanedlines 
    #     canAdd = True
    #     for cleanedLine in cleanedLines:
    #         #if exists, set canAdd to false
    #         if abs(cleanedLine.get_x_intercept()[0] - line.get_x_intercept()[0]) < 0.5:# or cleanedLine.length() < line.length():
    #             canAdd = False

    #     if canAdd:
    #         cleanedLines.append(line)
    print(cleanedLines)
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
    cleanedLines.sort(key=lambda x: x.get_x_intercept()[0])
    print(len(cleanedLines))
    pairBefore = False
    startPoint = 1
    endPoint = len(cleanedLines)
    if (cleanedLines[1].get_x_intercept()[0] - cleanedLines[0].get_x_intercept()[0]) < (cleanedLines[2].get_x_intercept()[0]  - cleanedLines[1].get_x_intercept()[0]):
        startPoint = 0
        pairBefore = True
    if (pairBefore and len(cleanedLines)%2 != 0) or (not pairBefore and len(cleanedLines)%2==0):
        endPoint = len(cleanedLines)-1
    for i in range(startPoint,endPoint,2):
        lanes.append((cleanedLines[i],cleanedLines[i+1]))
    return lanes

def draw_lanes(img,lanes):
    '''Takes an image and list of lanes as inputs and returns an image with lanes drawn on it'''
    temp_img = img
    for lane in lanes:
        for line in lane:
            (x1, y1, x2, y2) = line.get_points()
            cv2.line(temp_img, (x1,y1), (x2,y2), (0,255,0), 2)
    return temp_img



    
    
    


    


