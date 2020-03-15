from math import sin, cos, pi, sqrt, atan
from turtle import * 
from tkinter import *
import time

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
    if point2[0]-point1[0] == 0.0:
            return  0
    elif point1[0] <= point2[0]:
        return -atan((point2[1]-point1[1])/(point2[0]-point1[0]))
    else:
        return -atan((point2[1]-point1[1])/(point2[0]-point1[0])) + pi
            
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

def draw_curve(curve):
    master = Tk()
    master.title("Koch curve")
    w_height = 1000
    w_width = 2000
    w = Canvas(master, width=w_width, height=w_height)
    w.pack()
    scaling_factor = 0.8*w_width
    offsetX = 0.1*w_width
    offsetY = 0.1*w_height
    
    for i in range(1, len(curve)):
        w.create_line(scaling_factor*curve[i-1][0]+offsetX,
                      w_height - scaling_factor*curve[i-1][1]-offsetY,
                      scaling_factor*curve[i][0]+offsetX,
                      w_height - scaling_factor*curve[i][1] -offsetY)
    mainloop()
         

#seed = [[0, 0], [0.5, sqrt(3)/6], [1, 0]]

seed = [[0,0], [1/3, 0], [0.5, cos(pi/6)*(1/3)], [2/3,0], [1,0]]
#seed = [[0,0], [1/2, 1/4], [1/2, -1/4], [1,0]]

curve = [[0, 0], [1, 0]]
      
for x in range(0, 6):
    curve = update_curve(curve, seed)

draw_curve(curve)

'''
color('red', 'yellow')
begin_fill()
speed(0)
scaling_factor = 1000
for point in curve:
    scaled_pos = [point[0]*scaling_factor-scaling_factor/2,
                  point[1]*scaling_factor]
    goto(scaled_pos)

goto(0,0)

end_fill()
done()
'''
