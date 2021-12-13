#%%
#Importing packages 
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import math
from scipy.spatial.distance import euclidean
from scipy.optimize import minimize



#%%
# create exception for intersections function
class IntersectionError(Exception): 
    """Exception for get_intersections function"""
    pass

#%%
#function to calculate points of intersection of two circles
#source of function
#https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
def get_intersections(x0, y0, r0, x1, y1, r1):
    """
    circle 1: center (x0, y0), radius r0
    circle 2: center (x1, y1), radius r1
    """
    d = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting circles
    if d > r0 + r1 :
        raise IntersectionError
    # One circle within other
    if d < abs(r0-r1):
        raise IntersectionError
    # coincident circles
    if d == 0 and r0 == r1:
        raise IntersectionError
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)

#%%
#Function to evaluate accuracy of gamma calculation
def obj_func(gamma, p, r, o): 
    """
    gamma: value of ɣ
    p, r, o: (x,y) coordinates of pas, rec, opp
    """
    t = 0.25
    c = 4 
    d = euclidean(p,r)

    R_p = gamma*d*t
    R_r = gamma*d*(1-t)
    R_a = c*d/gamma

    inters = get_intersections(p[0],p[1],(R_a-R_p), r[0],r[1],(R_a-R_r))
    C_a1x, C_a1y, C_a2x, C_a2y = inters
    
    dist_Ca1_o = euclidean((C_a1x, C_a1y), o)
    dist_Ca2_o = euclidean((C_a2x, C_a2y), o)
    return abs(max(dist_Ca1_o, dist_Ca2_o) - R_a)

#%%
#using scipy.optimize to calculate gamma    
def calc(p, r, o, x0 = 0.5): 
    return minimize(obj_func, args=(p,r,o), x0 = x0).x[0]

