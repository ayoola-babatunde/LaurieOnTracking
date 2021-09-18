#%%
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import math
#%%
#data
x = [1, 4, 3]
y = [1, 1, 2]
labels = ['P', 'R', 'O']

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


#%%

#plt.ylim(0, 4); plt.xlim(0,4)
#circ1 = plt.Circle((1,1),1, fill = False)
#ax.add_patch(circ1)



for i, val in enumerate(labels):
    ax.annotate(val, (x[i], y[i]))


t = 0.25 #weird scaling factor
d = 3 #euclidean distance
c = 4 #weird scaling factor

for gamma in np.arange(0.0001, 0.5, 0.025): 
    print(gamma)

    R_p = gamma*d*t
    R_r = gamma*d*(1-t)
    R_a = c*d/gamma

    inters = get_intersections(1,1,(R_a-R_p), 4,1,(R_a-R_r))
    print(inters)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    plt.scatter(x,y)
    C_p = plt.Circle((x[0], y[0]), R_p, fill = False)
    C_r = plt.Circle((x[1], y[1]), R_r, fill = False)
    C_a1 = plt.Circle((inters[0], inters[1]), R_a, fill = False, color = 'red')
    C_a2 = plt.Circle((inters[2], inters[3]), R_a, fill = False, color = 'red')
    #A_1 = ptch.Arc((inters[0], inters[1]), R_a*2, R_a*2, 0, 90, 115)
    ax.add_patch(C_p)
    ax.add_patch(C_r)
    ax.add_patch(C_a1)
    ax.add_patch(C_a2)

    plt.ylim(-2,5)
    plt.xlim(-2,10)
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
# %%
