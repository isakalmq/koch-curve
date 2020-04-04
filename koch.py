from math import sin, cos, tan, pi, sqrt, asin
from turtle import * 
from tkinter import *
import time

itera = 0

def transform_point(mat, point):
    return [mat[0][0]*point[0] + mat[0][1]*point[1],
            mat[1][0]*point[0] + mat[1][1]*point[1]]

def transform_seed(mat, seed):
    new_seed = []
    for point in seed:
        new_seed.append(transform_point(mat, point))

    return new_seed;

def move_each(starting_point, seed):
    new_seed = []
    for point in seed:
        new_seed.append([(starting_point[0] + point[0]),
                         (starting_point[1] + point[1])])
    return new_seed;

def calculate_rotation(point1, point2):
    b = point2[0] - point1[0] 
    h = point2[1] - point1[1]
    hyp = sqrt(b**2 + h**2)
    if(b > 0):
        return -asin(h/hyp)
    else:
        return -pi + asin(h/hyp)
    
def update_curve(curve, seed):
    new_curve = []
    scaling = sqrt(((curve[0][0]-curve[1][0])**2 +
                    (curve[0][1]-curve[1][1])**2))
    new_curve.append(curve[0])
    for i in range(1, len(curve)):
        rotation = calculate_rotation(curve[i-1], curve[i])
            
        matrix = [[scaling*cos(rotation),  scaling*sin(rotation)],
                  [-scaling*sin(rotation), scaling*cos(rotation)]]
        transformed_seed = transform_seed(matrix, seed)
        new_curve.extend(
            move_each(curve[i-1], transformed_seed[1:len(transformed_seed)]))

    return new_curve;

#-----------------------------------------------------------------------
# Calulates the largest and smallest x and y value in the curve,
# represented by a list (any length) of lists (of length 2, containing
# coordinates).
#
# Returns four coordinates in the order: largest x, smallest x,
# largest y, smallest y
# ----------------------------------------------------------------------
def calc_max_min_x_y(curve):
    max_x = curve[0][0]
    min_x = curve[0][0]
    max_y = curve[0][1]
    min_y = curve[0][1]
    
    for point in curve[1:len(curve)]:
        if point[0] > max_x:
            max_x = point[0]
        elif point[0] < min_x:
            min_x = point[0]

        if point[1] > max_y:
            max_y = point[1]
        elif point[1] < min_y:
            min_y = point[1]
    return max_x, min_x, max_y, min_y
        
        

def redraw(w, w_height, w_width, curve):
    scaling_factor = 0.3*w_width
    offsetX = 0.1*w_width
    offsetY = 0.2*w_height
    w.delete(ALL)
    
    for i in range(1, len(curve)):
        w.create_line(scaling_factor*curve[i-1][0]+offsetX,
                      w_height - scaling_factor*curve[i-1][1]-offsetY,
                      scaling_factor*curve[i][0]+offsetX,
                      w_height - scaling_factor*curve[i][1] -offsetY)

def change_curve(w):
    w.create_arc(45, 80, 85, 100, start=180, extent=180)

class MyApp:
    def __init__(self, parent):
        #Single line
        #curve = [[0,0], [1,0]]

        #Triangle
        #curve = [[0,0], [1,0], [0.5, 0.5*tan(pi/3)], [0,0]]
        
        #Square
        curve = [[0, 0], [1, 0], [1,1], [0,1], [0,0]]

        #Change direction of the lines
        curve.reverse()
        
        #Modified square wave
        #seed = [[0,0], [1/4,0], [1/4,1/4], [1/2,1/4], [1/2, 0], [1/2, -1/4], [3/4, -1/4], [3/4, 0], [1,0]]

        #?
        #seed = [[0, 0], [0.5, sqrt(3)/6], [1, 0]]

        #?
        #seed = [[0,0], [1/3, 0], [0.5, cos(pi/6)*(1/3)], [2/3,0], [1,0]]

        #?
        #seed = [[0,0], [1/2, 1/4], [1/2, -1/4], [1,0]]

        #Square wave
        #seed = [[0,0], [0, 0.5], [0.5, 0.5], [0.5,0], [0.5, -0.5], [1,-0.5], [1,0]]

        seed = [[0,0], [1/4, 0], [1/2, 0], [1/2, 1/4], [1/4, 1/4], [1/4, 1/2], [1/2, 1/2], [3/4, 1/2], [3/4, 1/4], [3/4, 0], [1,0]]
                                                     
        button_container = Frame(master)
        button_container.pack()

        w = DrawingCanvas(curve, seed, parent, width=300, height=500)
        w.bind("<Button-5>", w.zoom)
        w.bind("<Button-4>", w.zoom)
        w.bind("<Configure>", w.configured_window)
        w.pack(fill="both", expand=True)

        change_curve_button = Button(button_container, text="Change", command=w.next)
        change_curve_button.pack()

        reset_curve_button = Button(button_container, text="Reset", command=w.reset)
        reset_curve_button.pack()



class DrawingCanvas(Canvas):
    def __init__(self, curve, seed, master=None, **kwargs):
        Canvas.__init__(self, master, bg='white', **kwargs)
        
        self.original_curve = curve
        self.curve = curve
        self.seed = seed

        #Used for determining if the view is zoomed or moved 
        self.default_view = True

        #Values used for drawing
        self.scaling_factor = 0
        self.offset_x = 0
        self.offset_y = 0
        
    def next(self):
        self.curve = update_curve(self.curve, self.seed)
        if self.default_view:
            self.calculate_default_values()
        self.draw()

    def draw(self):
        w_width = self.winfo_width()
        w_height = self.winfo_height()
        offsetX = 0
        offsetY = 0
        self.delete("all")

        for i in range(1, len(self.curve)):
            self.create_line(\
                self.scaling_factor * self.curve[i-1][0] + self.offset_x,
                self.scaling_factor * self.curve[i-1][1] + self.offset_y,
                self.scaling_factor * self.curve[i][0] + self.offset_x,
                self.scaling_factor * self.curve[i][1] + self.offset_y)

    def reset(self):
        self.curve = self.original_curve
        self.draw()
        
    def calculate_default_values(self):
        w_width = self.winfo_width()
        w_height = self.winfo_height()
        largest_x, smallest_x, largest_y, smallest_y = calc_max_min_x_y(self.curve)
        
        x_ratio = w_width / (largest_x - smallest_x)
        y_ratio = w_height / (largest_y - smallest_y)
        
        self.scaling_factor =  min(x_ratio, y_ratio)*0.9
        
        if(x_ratio < y_ratio):
            self.offset_x = 0.05 * w_width - smallest_x * self.scaling_factor
            self.offset_y = w_height/2 - (largest_y + smallest_y)/2 * self.scaling_factor
        else:
            self.offset_x = w_width/2 - (largest_x + smallest_x)/2 * self.scaling_factor
            self.offset_y =0.05 * w_height - smallest_y * self.scaling_factor
            
    def zoom(self, event):
        if event.num == 5:
            self.scaling_factor *=0.9
        else:
            self.scaling_factor *=1.1
        self.draw()
    def configured_window(self, event):
        self.calculate_default_values()
        self.draw()
        

master = Tk()
master.title("Koch curve")
app = MyApp(master)

master.mainloop()
