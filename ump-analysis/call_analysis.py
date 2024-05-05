import pandas as pd
from sklearn import linear_model
import requests
import json
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import pybaseball as pyball
from df_headers import df_headers

pyball.cache.enable()

def correct_call(start_dt, end_dt) -> pd.DataFrame:
    """
    Pulls and cleans data to use in _correct_call
    """
    df_sc = pd.DataFrame(data=pyball.statcast(start_dt = start_dt, end_dt = end_dt), columns=df_headers('statcast'))
    # Remove rows that don't have the required data
    df_sc = df_sc[df_sc['description'].isin(['ball','called_strike'])]
    df_sc = df_sc[df_sc['plate_x'].notnull()]
    df_sc = df_sc[df_sc['plate_z'].notnull()]
    df_sc = df_sc[df_sc['sz_top'].notnull()]
    df_sc = df_sc[df_sc['sz_bot'].notnull()]
    # Add correct call column and populate for all rows
    df_sc['correct_call'] = df_sc.apply(_correct_call, axis = 1)
    return df_sc


def _correct_call(df_sc: pd.DataFrame) -> int:
    """
    Compares each relative strike zone to pitch location. If the umpire's call
    is at odds with this comparison, correct_call returns 0.
    """
    call_type: str = df_sc['type']
    plate_x: float = df_sc['plate_x']
    plate_z: float = df_sc['plate_z']
    sz_top: float = df_sc['sz_top']
    sz_bot: float = df_sc['sz_bot']
    sz_hor: float = (17/12) / 2 
    ball_rad: float = (2.94/12) / 2
    correct_call: int = 1

    if (abs(plate_x) > sz_hor) and (call_type == 'S'): # Outside of strikezone horizontally, called strike
        correct_call = 0
    elif (abs(plate_x) < sz_hor) and (plate_z < (sz_top + ball_rad)) and (plate_z > (sz_bot - ball_rad)) and (call_type == 'B'): # In strikezone, called ball
        correct_call = 0
    elif (plate_z > (sz_top + ball_rad)) and (call_type == 'S'): # High, called strike
        correct_call = 0
    elif (plate_z < (sz_bot - ball_rad)) and (call_type == 'S'): # Low, called strike
        correct_call = 0
    return correct_call


def red_analysis(df_sc: pd.DataFrame) -> pd.DataFrame:
    """
    Pulls and cleans data to use in _red_analysis
    """
    # Establish re288 dataframe with proper index and columns
    df_re288 = pd.DataFrame(data = pd.read_csv('./ump-analysis/re288.csv', header = None))
    df_re288.index = df_headers('re288-index') 
    df_re288.columns = df_headers('re288-columns')
    # Create new column called 'run_expectancy_delta' with _red_analyis logic
    df_sc['missed_call_red'] = df_sc.apply(_red_analysis, axis = 1, args = [df_re288])
    return df_sc


def _red_analysis(df_sc: pd.DataFrame, df_re288: pd.DataFrame) -> float:
    """
    Finds outs, if batters are on bases, and the count, then matches
    the situation to the RED matrix if there is a missed call.
    """
    if df_sc['correct_call'] == 0:
        first_base: str = '_'
        second_base: str = '_'
        third_base: str = '_'

        if pd.notnull(df_sc['on_1b']):
            first_base = '1'
        if pd.notnull(df_sc['on_2b']):
            second_base = '2'
        if pd.notnull(df_sc['on_3b']):
            third_base = '3'
        
        out_bases: str = f'{df_sc['outs_when_up']} {first_base}{second_base}{third_base}'
        count: str = f'[{df_sc['balls']}-{df_sc['strikes']}]'
        red = df_re288.loc[out_bases, count]
        return red

def missed_call_plotting(df_sc: pd.DataFrame, plot_type: str = 'kde'):
    """
    Either kde or scatter plotting for data.
    Valid inputs for plot_type are 'kde' and 'scatter'
    """
    # Parameters for relative strike zone
    sz_top_avg: float = df_sc.loc[:, 'sz_top'].mean()
    sz_bot_avg: float = df_sc.loc[:, 'sz_bot'].mean()
    sz_hor: float = (17/12) / 2 

    # Create a new dataframe with only the needed data
    df_mc = df_sc[['type', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'correct_call']]
    df_mc = df_mc[df_mc['correct_call'].isin([0])]

    # Calculate relative distance from strike zone for plotting
    df_mc['plate_z_rel'] = df_mc.apply(z_from_sz, axis = 1, args = [sz_top_avg, sz_bot_avg])

    fig, ax = plt.subplots(figsize=(4, 5))
    
    if plot_type == 'kde':
        sns.kdeplot(df_mc, x = 'plate_x', y = 'plate_z_rel', cmap = 'flare',
                    cut = 1, fill = True,levels = 15, thresh = .2)
    else:
        sns.scatterplot(df_mc, x = 'plate_x', y = 'plate_z_rel')

    #Draw strike zone on plot
    ax.add_patch(Rectangle((-sz_hor, sz_bot_avg ),(sz_hor * 2),((sz_top_avg - sz_bot_avg)),
                           edgecolor = 'black', facecolor = 'none'))
    ax.axis('off')
    plt.rcParams['savefig.transparent'] = True
    plt.savefig(f'{plot_type}plot.png', dpi=1000)
    plt.show()
    return

def z_from_sz(df_mc: pd.DataFrame, sz_top_avg: float, sz_bot_avg: float, ball_rad: float = 0.1208333) -> float:
    """
    Logic for determining the position for the y-axis of the plot.
    Returns a value relative to the average strike-zone.
    """
    z_pos = None
    if df_mc['plate_z'] > (df_mc['sz_top'] + ball_rad) : # If ball is above sz
        relative_pos = df_mc['plate_z'] - df_mc['sz_top']
        z_pos = relative_pos + sz_top_avg
    elif df_mc['plate_z'] < (df_mc['sz_bot'] - ball_rad): # If ball is below s
        relative_pos = df_mc['sz_bot'] - df_mc['plate_z']
        z_pos = sz_bot_avg - relative_pos
    elif ((df_mc['sz_top'] + ball_rad) - df_mc['plate_z']) > (df_mc['plate_z'] - (df_mc['sz_bot'] - ball_rad)): # If ball is in uppper half of sz
        relative_pos = df_mc['sz_top'] - df_mc['plate_z']
        z_pos = sz_top_avg - relative_pos
    else: # If ball is in sz, but not he upper half
        relative_pos = df_mc['plate_z'] - df_mc['sz_bot']
        z_pos = relative_pos + sz_bot_avg
    return z_pos

def umpire_match(df_sc: pd.DataFrame) -> pd.DataFrame:
    """
    Match umpire to each game using the statcast game_pk variable and MLB API.
    """
    s = requests.Session()
    game_pk = dict.fromkeys(df_sc.game_pk.unique()) # Find all unique game_pk's in the DataFrame

    for id in game_pk:
        boxscore = requests.get(f'https://statsapi.mlb.com/api/v1/game/{id}/boxscore').json()["info"] # Pull API info via game_pk
        umpire = re.search("HP: .*?1B", json.dumps(boxscore)).group() # Search for umpires label in info section of API
        umpire = umpire[4:len(umpire) - 4] # Remove first 4 characters (HP: ) and last 4 characters (. 1B)
        game_pk[id] = umpire
    
    df_sc['umpire'] = df_sc.apply(lambda x: game_pk[x.game_pk], axis = 1) # Match each rows game_pk to the game_pk dict, then return associated umpire.
    # df_sc['umpire'] = df_sc.apply(_umpirematch, axis = 1, args = [game_pk])
    return df_sc

def logit_model(df_sc: pd.DataFrame, dv: str = 'correct_call', iv: list = ['balls', 'strikes', 'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'effective_speed',
                                                                           'at_bat_number', 'spin_axis', 'delta_run_exp']):
    """
    Run logistic regression dependent variable on selected variables
    """
    model = linear_model.LogisticRegression()
    model.fit(df_sc[iv], df_sc[dv])