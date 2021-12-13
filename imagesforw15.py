#%%
import pandas  as  pd
import numpy as np
import Metrica_IO as mio
import Metrica_Viz as mviz
import matplotlib.patches as patches
import gamma #python file in directory, not prebuilt module
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

# set up initial path to data
DATADIR = "C:/Users/Ayoola_PC/Documents/cap2/sample-data/data"
game_id = 2 # let's look at sample match 2

# read in the event data
events = mio.read_event_data(DATADIR,game_id)

# Bit of housekeeping: unit conversion from metric data units to meters
events = mio.to_metric_coordinates(events)

# only looking at completed passes (for now)
# in the future, the most likely reciever for 
# incomplete passes can be calculated
events = events.dropna(axis=0, subset=['From', 'To'])

# get number of passer and reciever
# i.e. convert 'Player9' to 9
events['From_n'] = events.apply(lambda row: row.From[6:], axis=1)
events['To_n'] = events.apply(lambda row: row.To[6:], axis=1)


#%%

# Get events by team
home_events = events[events['Team']=='Home']
away_events = events[events['Team']=='Away']

# Get all shots
shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

# Get all home goals
home_goals = home_shots[home_shots.Subtype=='ON TARGET-GOAL']


#%%
#### TRACKING DATA ####

# READING IN TRACKING DATA
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters 
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

# %%
# Plot players in the lead up to third goal (frame 120895-121055)
for x in range(120895, 121065): 
    fig, ax = mviz.plot_frame(tracking_home.loc[x], tracking_away.loc[x])
    fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/{x}")

# %%
#Field with rectangle
fig, ax = mviz.plot_frame(tracking_home.loc[120975], tracking_away.loc[120975])
rect = patches.Rectangle((8, -10), 22, 20, fill = None)
ax.add_patch(rect)
ax.set_aspect('equal')
fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/field1")


# %%
#moment of pass
fig, ax = mviz.plot_frame(tracking_home.loc[120975], tracking_away.loc[120975])
rect = patches.Rectangle((8, -10), 22, 20, fill = None)
ax.add_patch(rect)
ax.set_xlim(7.5,30.5)
ax.set_ylim(-10.5,10.5)
ax.set_aspect('equal') #aspect ratio 
fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/field2")


#extra opponents removed
fig, ax = mviz.plot_frame(tracking_home.loc[120975], 
tracking_away.drop(['Away_20_x', 'Away_20_y', 'Away_21_x', 'Away_21_y'], axis=1).loc[120975])
rect = patches.Rectangle((8, -10), 22, 20, fill = None)
ax.add_patch(rect)
ax.set_xlim(7.5,30.5)
ax.set_ylim(-10.5,10.5)
ax.set_aspect('equal') #aspect ratio 
fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/field3")


# %%

#Function to draw circles
def draw_circles(gam, p, r, o): 
    t = 0.25 #scaling factor
    d = euclidean(p,r) #dist btw p,r
    c = 4 #other scaling factor

    R_p = gam*d*t
    R_r = gam*d*(1-t)
    R_a = c*d/gam

    C_a1x, C_a1y, C_a2x, C_a2y = gamma.get_intersections(p[0],p[1],(R_a-R_p), r[0],r[1],(R_a-R_r))
    
    dist_Ca1_o = euclidean((C_a1x, C_a1y), o)
    dist_Ca2_o = euclidean((C_a2x, C_a2y), o)

    C_p = plt.Circle((p[0], p[1]), R_p, fill = False)
    C_r = plt.Circle((r[0], r[1]), R_r, fill = False)
    C_a1 = plt.Circle((C_a1x, C_a1y), R_a, fill = False, color = 'red')
    C_a2 = plt.Circle((C_a2x, C_a2y), R_a, fill = False, color = 'orange')

    return C_p, C_r, C_a1, C_a2

#coordinates of passer, reciever, and two opponents 
p_ = (13.63, 2.06)
r_ = (25.55, -3.03)
o1 = (23.42, -5.34) #gamma = 0.315 no 19
o2 = (14.76, 3.02) #gamma = 0.355 no 20
o3 = (25.28, 6.72) #gamma = 1.00 no 21

# %%
#explaining gamma
#opponent 19 only
#hide opponent 20 and 21
#varying gamma slightly o1
for index, gam in enumerate(np.linspace(0.001, 0.315, 5)): 
    fig, ax = mviz.plot_frame(tracking_home.loc[120975], 
    tracking_away.drop(['Away_20_x', 'Away_20_y', 'Away_21_x', 'Away_21_y'], axis=1).loc[120975])
    rect = patches.Rectangle((8, -10), 22, 20, fill = None)
    ax.add_patch(rect)
    ax.set_xlim(7.5,30.5)
    ax.set_ylim(-10.5,10.5)
    ax.set_aspect('equal') #aspect ratio of football pitch

    circles_g1 = draw_circles(gam, p_, r_, o1)
    ax.add_patch(circles_g1[0])
    ax.add_patch(circles_g1[1])
    ax.add_patch(circles_g1[2])
    ax.add_patch(circles_g1[3])
    ax.text(9,9,f'ɣ = {gam:.2f}')
    fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/fieldgam{index}")




# %%
#gamma for opp 20
# drop opp 19 and 21
fig, ax = mviz.plot_frame(tracking_home.loc[120975], 
tracking_away.drop(['Away_19_x', 'Away_19_y', 'Away_21_x', 'Away_21_y'], axis=1).loc[120975])
rect = patches.Rectangle((8, -10), 22, 20, fill = None)
ax.add_patch(rect)
ax.set_xlim(7.5,30.5)
ax.set_ylim(-10.5,10.5)
ax.set_aspect('equal') #aspect ratio of football pitch

circles_g1 = draw_circles(0.355, p_, r_, o2)
ax.add_patch(circles_g1[0])
ax.add_patch(circles_g1[1])
ax.add_patch(circles_g1[2])
ax.add_patch(circles_g1[3])
ax.text(9,9,'ɣ = 0.36')
fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/fieldopp20")


# %%
#gamma for opp 21
# drop opp 19 and 20
fig, ax = mviz.plot_frame(tracking_home.loc[120975], 
tracking_away.drop(['Away_19_x', 'Away_19_y', 'Away_20_x', 'Away_20_y'], axis=1).loc[120975])
rect = patches.Rectangle((8, -10), 22, 20, fill = None)
ax.add_patch(rect)
ax.set_xlim(7.5,30.5)
ax.set_ylim(-10.5,10.5)
ax.set_aspect('equal') #aspect ratio of football pitch

circles_g1 = draw_circles(1.002, p_, r_, o3)
ax.add_patch(circles_g1[0])
ax.add_patch(circles_g1[1])
ax.add_patch(circles_g1[2])
ax.add_patch(circles_g1[3])
ax.text(9,9,'ɣ = 1.00')
fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/fieldopp21")


# %%

# get coord of passer and reciever in frame
def get_p_r(start_frame, home_passing): 
    """Return coordinates of passer and reciever 
    at particular frame in tracking data

    home_passing (bool) Is home team passing? T/F"""
    if home_passing: 
        team = 'Home'
        track_df = tracking_home
    else: 
        team = 'Away'
        track_df = tracking_away

    event_row = events[events['Start Frame'] == start_frame]
    passer_no, rec_no = event_row['From_n'].item(), event_row['To_n'].item()

    

    coords = track_df.loc[start_frame]
    p = (coords[f'{team}_{passer_no}_x'], 
    coords[f'{team}_{passer_no}_y'])
    r = (coords[f'{team}_{rec_no}_x'], 
    coords[f'{team}_{rec_no}_y'])

    return p, r


#%%
small = [11810, 86854, 12180, 134048,  59835, 104244, 16388,  73902]
extreme_gamma_small = [0.001, 0.014, 0.019, 0.022, 0.026, 0.029, 0.030, 0.032]
for index, frame in enumerate(small): 
    fig, ax = mviz.plot_frame(tracking_home.loc[frame], tracking_away.loc[frame])
    ax.set_aspect('equal') #aspect ratio of football pitch
    p, r = get_p_r(frame, True)
    ax.arrow(p[0], p[1], r[0]-p[0], r[1]-p[1], 
            length_includes_head = True, head_width = 2)
    ax.text(-50,30,f'ɣ = {extreme_gamma_small[index]}')
    fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/egammasmall{index}")


# %%
large = [ 96470,  89751,  89791,  94129,  54472, 116727, 119168,  40585,
        58281,  65246]
extreme_gamma_large = [1.48324976, 1.56954178, 1.58953521, 1.62898618, 1.70546405,
       1.73366545, 1.73792076, 1.76374491, 1.79084266, 1.79601076]
for index, frame in enumerate(large): 
    fig, ax = mviz.plot_frame(tracking_home.loc[frame], tracking_away.loc[frame])
    ax.set_aspect('equal') #aspect ratio of football pitch
    p, r = get_p_r(frame, True)
    ax.arrow(p[0], p[1], r[0]-p[0], r[1]-p[1], 
            length_includes_head = True, head_width = 2)
    ax.text(-50,30,f'ɣ = {extreme_gamma_large[index]:.3f}')
    fig.savefig(f"C:/Users/Ayoola_PC/Documents/cap2/LaurieOnTracking/trackclips/egammalarge{index}")

# %%
