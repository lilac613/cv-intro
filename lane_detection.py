import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
#from dt_apriltags import Detector


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
    def get_x_intercept(self,screen_height=180):
        '''returns x-ntercept of line'''
        if self.y1==self.y2:
            return None
        return ((((screen_height - self.y1)/self.get_slope())+ self.x1),0)
    def get_points(self):
        return (self.x1, self.y1, self.x2, self.y2)
    def length(self):
        return ((self.x1-self.x2)**2 + (self.y1-self.y2)**2)**0.5
    def dealt(self,bool):
        self.d = bool
    def dealtWith(self):
        return self.d

def detect_lines(my_img, edges, threshold1, threshold2, apertureSize,minLineLength,maxLineGap):
    '''Takes an image and detects lines on it.
    Args:
        img (result of cv2.imread()): the image to process.
        edges (result of cv2.Canny()): edges on the image.
        threshold1 (int): the first threshold for the Canny edge detector.
        threshold2 (int): the second thlane_detection.pyreshold for the Canny edge detector.
        apertureSize (int): the aperture size for the Sobel operator.
        minLineLength (int): the minimum length of a line.
        maxLineGap (int): the maximum gap between two points to be considered the same line.
    
    Returns:
    the list of lines (list)
    '''
    lines = cv2.HoughLinesP(
                 edges,
                 rho=1,
                 theta=np.pi/180,
                 threshold=70,
                 minLineLength=100,
                 maxLineGap=30,
         )
    ret_lines = []
    for line in lines:

        x1, y1, x2, y2 = line[0]
        ret_lines.append(Line(x1,y1,x2,y2))

    return ret_lines

def draw_lines(img, lines: list[Line], color: tuple[int,int,int]=(0,255,0)):
    '''Takes an image and draws the lines on that image
    Args:
        img (result of cv2.imread()): the image to process
        lines (list[Line]): list of lines to be drawn on image
        color (tuple[int,int,int], optional): the color of the line
        
    Returns:
    the image with lines drawn
    '''
    temp_img =img
    i = 0
    for line in lines:
        (x1, y1, x2, y2) = line.get_points()
        cv2.line(temp_img, (int(x1),int(y1)), (int(x2),int(y2)), color, 2)
    return temp_img

def get_slope_intercepts(lines: list[Line]) -> tuple[list[float], list[int]]:
    '''Determines the slopes and x-intercepts of lines
    Args:
        lines (list[Line]): list of lines to determine slope and x-intercept
        
    Returns:
    a tuple of a list of slopes and a list of intercepts ([slopes],[intercepts])'''
    slopes = []
    intercepts = []
    for line in lines:
        slopes.append(line.get_slope())
        intercepts.append(line.get_x_intercept())
    return (slopes,intercepts)

def merge_collinear_lines(lines: list[Line], intercept_margin=20, slope_margin=1) -> list[Line]:
    '''Attempt to merge collinear lines
    Args:
        lines (list[Line]): list of lines that may or may not be collinear
        intercept_margin (int, optional): margin of error for proximity of x-intercepts
        slope_margin (int, optional): margin of error for difference in magnitudes of slopes
        
    Returns:
    list of non-collinear lines'''
    cleanedLines = []
    for i in range(len(lines)):
        if lines[i].dealtWith():
            continue
        lines[i].dealt(True)
        current_slope = lines[i].get_slope()
        current_intercept = lines[i].get_x_intercept()[0]
        if current_slope>0:
            minx1 = min(lines[i].get_points()[0],lines[i].get_points()[2])
            miny1 = min(lines[i].get_points()[1],lines[i].get_points()[3])
            maxx2 = max(lines[i].get_points()[0],lines[i].get_points()[2])
            maxy2 = max(lines[i].get_points()[1],lines[i].get_points()[3])
            for j in range(i+1,len(lines)):
                if not lines[j].dealtWith() and abs(current_intercept-lines[j].get_x_intercept()[0])<intercept_margin and lines[j].get_slope()>0 and abs(lines[j].get_slope() - current_slope)<slope_margin:
                    minx1 = min(lines[j].get_points()[0],lines[j].get_points()[2],minx1)
                    miny1 = min(lines[j].get_points()[1],lines[j].get_points()[3],miny1)
                    maxx2 = max(lines[j].get_points()[2],lines[j].get_points()[0],maxx2)
                    maxy2 = max(lines[j].get_points()[3],lines[j].get_points()[1],maxy2)
                    lines[j].dealt(True)
            cleanedLines.append(Line(minx1,miny1,maxx2,maxy2))
        else:
            minx1 = min(lines[i].get_points()[0],lines[i].get_points()[2])
            maxy1 = max(lines[i].get_points()[1],lines[i].get_points()[3])
            maxx2 = max(lines[i].get_points()[0],lines[i].get_points()[2])
            miny2 = min(lines[i].get_points()[1],lines[i].get_points()[3])
            for j in range(i+1,len(lines)):
                if not lines[j].dealtWith() and abs(current_intercept-lines[j].get_x_intercept()[0])<intercept_margin and lines[j].get_slope()<0 and abs(lines[j].get_slope() - current_slope)<slope_margin:
                    minx1 = min(lines[j].get_points()[0],lines[j].get_points()[2],minx1)
                    maxy1 = max(lines[j].get_points()[1],lines[j].get_points()[3],maxy1)
                    maxx2 = max(lines[j].get_points()[2],lines[j].get_points()[0],maxx2)
                    miny2 = min(lines[j].get_points()[3],lines[j].get_points()[1],miny2)
                    lines[j].dealt(True)
            cleanedLines.append(Line(minx1,maxy1,maxx2,miny2))
    return cleanedLines


def detect_lanes(lines: list[Line], intercept_margin=40, slope_margin = 1):
    '''Detect pairs of lines that comprise a lane
    Args:
        lines (list[Line]): list of lines that may form a lane'''
    lanes = []
    cleanedLines = merge_collinear_lines(lines)
    cleanedLines.sort(key=lambda x: x.get_x_intercept()[0])
    pairBefore = False
    startPoint = 1
    endPoint = len(cleanedLines)

    # NEED TO HAVE CASES FOR WHEN THE LENGTH OF CLEANED LINES IS LESS THAN 1

    # if the lines can consecutively make a lane starting from the first lane
    if (cleanedLines[1].get_x_intercept()[0] - cleanedLines[0].get_x_intercept()[0]) < (cleanedLines[2].get_x_intercept()[0]  - cleanedLines[1].get_x_intercept()[0]):
        startPoint = 0
        pairBefore = True
    # if the last line is not part of a lane or the first part is not part of a lane
    if (pairBefore and len(cleanedLines)%2 != 0) or (not pairBefore and len(cleanedLines)%2==0):
        endPoint = len(cleanedLines)-1
    for i in range(startPoint,endPoint,2):
        lanes.append((cleanedLines[i],cleanedLines[i+1]))
    return lanes

def draw_lanes(img,lanes,diffLaneColors=False):
    '''Draws lanes on an 
    Args: 
        img (result of cv2.imread()): the image to process
        lanes (list[(Line,Line)]): list of lanes to draw
        diffLaneColors (boolean, optional): whether the lanes should have different colors or not'''
    temp_img = img
    for lane in lanes:
        (x1, y1, x2, y2) = lane[0].get_points()
        (x3, y3, x4, y4) = lane[1].get_points()
        if diffLaneColors:
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        else:
            color = (0,255,0)
        cv2.line(temp_img, (int(x1),int(y1)), (int(x2),int(y2)), color, 2)
        cv2.line(temp_img, (int(x3),int(y3)), (int(x4),int(y4)), color, 2)
    return temp_img