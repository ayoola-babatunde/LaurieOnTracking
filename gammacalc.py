#%%
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import math
from scipy.spatial.distance import euclidean
from scipy.optimize import minimize
#%%
#data
p_ = (1, 1)
r_ = (4, 1)
o_ = (3, 0)
all_points = [p_,r_,o_]
labels = ['P', 'R', 'O']

#%%
#https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
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


def obj_func(gamma, p, r, o): 
    t = 0.25
    c = 4 
    d = euclidean(p,r)

    R_p = gamma*d*t
    R_r = gamma*d*(1-t)
    R_a = c*d/gamma
    #print(gamma)
    inters = get_intersections(p[0],p[1],(R_a-R_p), r[0],r[1],(R_a-R_r))
    C_a1x, C_a1y, C_a2x, C_a2y = inters
    #print(inters)
    dist_Ca1_o = euclidean((C_a1x, C_a1y), o)
    dist_Ca2_o = euclidean((C_a2x, C_a2y), o)
    return abs(max(dist_Ca1_o, dist_Ca2_o) - R_a)
    
minimize(obj_func, args=(p_,r_,o_), x0 = 0.5)

#%%

#testing gamma
t = 0.25 #weird scaling factor
d = euclidean(p,r) #euclidean distance
c = 4 #weird scaling factor

R_a_store = []
plot = True

for gamma in np.arange(0.0001, 0.7, 0.05): 
    print(gamma)

    R_p = gamma*d*t
    R_r = gamma*d*(1-t)
    R_a = c*d/gamma
    R_a_store.append(R_a)

    C_a1x, C_a1y, C_a2x, C_a2y = get_intersections(p[0],p[1],(R_a-R_p), r[0],r[1],(R_a-R_r))
    #print(inters)
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
        #A_1 = ptch.Arc((C_a1x, C_a1y), R_a*2, R_a*2, 0, 90, 115)
        ax.add_patch(C_p)
        ax.add_patch(C_r)
        ax.add_patch(C_a1)
        ax.add_patch(C_a2)
        ax.plot([o[0], C_a1x], [o[1], C_a1y], color = 'red')
        ax.plot([o[0], C_a2x], [o[1], C_a2y], color = 'orange')

        plt.ylim(-2,5)
        plt.xlim(-2,6)
        plt.show()

#%%
#Arc?
fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.scatter(x,y)
A_1 = ptch.Arc((1,1), 5, 5, 0, 0, 180)
ax.add_patch(A_1)
plt.show()
# %%
R1 = 10; L1_x, L1_y = 0, 0
R2 = 15; L2_x, L2_y = 60, 0
Ra = 5000

stor_x, stor_y = [], []

for x in range(5000): 
    try: 
        pts = get_intersections(L1_x, L1_y, Ra-R1, L2_x, L2_y, Ra-R2)
        
        stor_x.append(pts[0])
        stor_y.append(pts[1])
        stor_x.append(pts[2])
        stor_y.append(pts[3])
        Ra-=10
    except Exception as e: 
        continue
# %%

plt.scatter(stor_x, stor_y, marker='.')
plt.xlim(left=0)
plt.vlines(30, -2000,2000)
# %%
