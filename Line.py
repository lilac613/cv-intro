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