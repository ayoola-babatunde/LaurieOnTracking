#%%

from matplotlib.pyplot import axis
import pandas as  pd
import Metrica_IO as mio
import Metrica_Viz as mviz
import gamma 
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from tqdm import tqdm, trange
#%%

# set up initial path to data
DATADIR = "C:/Users/Ayoola_PC/Documents/cap2/sample-data/data"
game_id = 2 # let's look at sample match 2

# read in the event data
events = mio.read_event_data(DATADIR,game_id)
#events = pd.read_json("C:/Users/Ayoola_PC/Documents/cap/sample-data/data/Sample_Game_3/Sample_Game_3_events.json")

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

#get all passes

passes = events[events['Type']=='PASS']
home_passes = home_events[home_events.Type=='PASS']
away_passes = away_events[away_events.Type=='PASS']


#%%

# READING IN TRACKING DATA
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters 
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

# %%
# truncated normal
def truncnorm(N): 
    """Get N samples of a truncated normal distribution"""
    lower = 0
    upper = 3
    mu = 0.2
    sigma = 0.7
    N = N

    samples = stats.truncnorm.rvs((lower-mu)/sigma, 
    (upper-mu)/sigma, loc=mu,scale=sigma,size=N)
    
    return samples

pot_x0 = truncnorm(1000000)

# %%
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
# %%

def get_os(start_frame, home_passing): 
    """Return coordinates of all opponents on the field
    
    home_passing (bool) Is home team passing? T/F """
    if home_passing: #if home team is passing, opponents are the away team
        team = 'Away'
        df = tracking_away
    else: 
        team = 'Home'
        df = tracking_home

    coords = df.loc[start_frame]

    all_os = []

    for x in range(2, len(coords)-2, 2): #all opponents
        all_os.append((coords[x], coords[x+1]))
    
    return all_os

away_nums = [25, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28]

# %%
all_pass_gammas = []
for x in trange(home_passes.shape[0]): 
    #print(f'Pass {x+1}')
    row = home_passes.iloc[x]
    pass_gamma = [np.inf] #values of gamma for this pass
    p, r = get_p_r(
        start_frame = row['Start Frame'], home_passing = True)
    #print(row)

    os_ = get_os(
        start_frame= row['Start Frame'], 
        home_passing=True)
    #print(os_)

    for ind, o in enumerate(os_): 
        #print(away_nums[ind])
        #print(p, o)

        #check if p, r, o coordinates and not nans
        if np.isnan(np.array(p + r + o)).sum() > 0: 
            #print('firstcheck') 
            continue

        #check if passing to self
        elif p == o or r == o: 
            #print('secondcheck')
            continue

        else: 
            #trying out a uniform distribution for starting location
            tries = 0
            while tries < 15: #15 tries with different start x0
                try: 
                    tries+=1
                    x0 = np.random.choice(pot_x0)
                    gamma_result = gamma.calc(p, r, o, x0)

                    #this code only runs if optimize is  successful
                    #print(gamma_result, x0, tries)
                    pass_gamma.append(gamma_result)
                    break
                except gamma.IntersectionError: #optimize function fails
                    pass
                except Exception as e: 
                    print('other e?')
                    break

    all_pass_gammas.append(min(pass_gamma))


# %%
home_passes['gamma'] = all_pass_gammas

#%%
# sort by gamma, riskiest passes to make
# smallest gammas
small_gam = home_passes.sort_values('gamma').iloc[:5][['Start Frame', 'gamma']]

#largest gammas
large_gam = home_passes.sort_values('gamma').iloc[-5:][['Start Frame', 'gamma']]

# %%
