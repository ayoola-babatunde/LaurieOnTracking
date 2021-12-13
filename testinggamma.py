#%%
#Importing packages 
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import math
from scipy.spatial.distance import euclidean
from scipy.optimize import minimize

#%%
#test dataget to make diagrams 
#p,r,0 = passer, reciever, opponent
p,r,o = (2.8747200000000035, -6.010519999999998), (0.5851199999999968, -10.46928), (35.43791999999999, -2.485399999999998)
#p = (1, 1)
#r = (4, 1)
#o = (3, 0)
all_points = [p,r,o]
labels = ['p', 'r', 'o']

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
        raise Exception('non intersecting')
    # One circle within other
    if d < abs(r0-r1):
        raise Exception('one inside another')
    # coincident circles
    if d == 0 and r0 == r1:
        raise Exception('coincident')
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

    #get the center of the circles that form the arcs
    inters = get_intersections(p[0],p[1],(R_a-R_p), 
                                r[0],r[1],(R_a-R_r))
    C_a1x, C_a1y, C_a2x, C_a2y = inters
    
    dist_Ca1_o = euclidean((C_a1x, C_a1y), o)
    dist_Ca2_o = euclidean((C_a2x, C_a2y), o)
    return abs(max(dist_Ca1_o, dist_Ca2_o) - R_a)

#%%
#using scipy.optimize to calculate gamma    
def calc(p, r, o): 
    return minimize(obj_func, args=(p,r,o), x0 = 0.5).x[0]

#%%
#Drawing diagrams
#testing gamma
t = 0.25 #scaling factor
d = euclidean(p,r) #dist btw p,r
c = 4 #other scaling factor

R_a_store = []
plot = True

#Loop to make plots for different values of gamma
for ind, gamma in enumerate(np.linspace(0.0001, 3, 5)): 
    print(gamma)

    R_p = gamma*d*t
    R_r = gamma*d*(1-t)
    R_a = c*d/gamma
    R_a_store.append(R_a)

    C_a1x, C_a1y, C_a2x, C_a2y = get_intersections(p[0],p[1],(R_a-R_p), r[0],r[1],(R_a-R_r))
    
    dist_Ca1_o = euclidean((C_a1x, C_a1y), o)
    dist_Ca2_o = euclidean((C_a2x, C_a2y), o)

    print(abs(max(dist_Ca1_o, dist_Ca2_o) - R_a)) 

    if plot: 
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        x = [x[0] for x in all_points]
        y = [y[1] for y in all_points]

        ax.scatter(x,y)
        C_p = plt.Circle((x[0], y[0]), R_p, fill = False)
        C_r = plt.Circle((x[1], y[1]), R_r, fill = False)
        C_a1 = plt.Circle((C_a1x, C_a1y), R_a, fill = False, color = 'red')
        C_a2 = plt.Circle((C_a2x, C_a2y), R_a, fill = False, color = 'orange')
        print(dist_Ca1_o, dist_Ca2_o, R_a)

        ax.add_patch(C_p)
        ax.add_patch(C_r)
        ax.add_patch(C_a1)
        ax.add_patch(C_a2)
        ax.text(-1,4,f'ɣ = {gamma:.2f}')
        plt.ylim(-35,35)
        plt.xlim(-20,20)
        
        #plt.savefig(f'C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/gifims/img{ind}.png')
        plt.show()


# %%
