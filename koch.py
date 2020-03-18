from math import sin, cos, pi, sqrt, asin
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
    print("Hello")

def change_curve(w):
    w.create_arc(45, 80, 85, 100, start=180, extent=180)

class MyApp:
    def __init__(self, parent):
        curve = [[0, 0], [1, 0], [1,1], [0,1], [0,0]]
        
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

    
        button_container = Frame(master)
        button_container.pack()

        w = DrawingCanvas(curve, seed, parent, width=2500, height=1300)
        w.pack()
        
        change_curve_button = Button(button_container, text="Change", command=w.next)
        change_curve_button.pack()

        reset_curve_button = Button(button_container, text="Reset", command=w.reset)
        reset_curve_button.pack()



class DrawingCanvas(Canvas):
    def __init__(self, curve, seed, master=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        
        self.original_curve = curve
        self.curve = curve
        self.seed = seed
        self.draw()
        
    def next(self):
        self.curve = update_curve(self.curve, self.seed)
        self.draw()

    def draw(self):
        w_width = 2500
        w_height = 1300
        scaling_factor = 0.3*w_width
        offsetX = 0.1*w_width
        offsetY = 0.2*w_height
        self.delete("all")
    
        for i in range(1, len(self.curve)):
            self.create_line(scaling_factor*self.curve[i-1][0]+offsetX,
                          w_height - scaling_factor*self.curve[i-1][1]-offsetY,
                          scaling_factor*self.curve[i][0]+offsetX,
                          w_height - scaling_factor*self.curve[i][1] -offsetY)

    def reset(self):
        self.curve = self.original_curve
        self.draw()

        
#seed = [[0, 0], [0.5, sqrt(3)/6], [1, 0]]

seed = [[0,0], [1/3, 0], [0.5, cos(pi/6)*(1/3)], [2/3,0], [1,0]]
#seed = [[0,0], [1/2, 1/4], [1/2, -1/4], [1,0]]

#Square wave
#seed = [[0,0], [0, 0.5], [0.5, 0.5], [0.5,0], [0.5, -0.5], [1,-0.5], [1,0]]

#modified square wave
seed1 = [[0,0], [1/4,0], [1/4,1/4], [1/2,1/4], [1/2, 0], [1/2, -1/4], [3/4, -1/4], [3/4, 0], [1,0]]

seeds = [seed, seed1]

#curve = [[0, 0], [1, 0], [1,1], [0,1], [0,0]]
#curve= [[0,0], [1,0]]
#draw_curve_turtle(seed)


master = Tk()
master.title("Koch curve")
app = MyApp(master)

master.mainloop()
