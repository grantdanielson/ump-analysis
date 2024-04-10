import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pybaseball as pyball
import retrosheet_exec
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
    sz_hor: float = 0.83
    baseball_rad: float = 0.1208333
    correct_call: int = 1

    if (abs(plate_x) > sz_hor) and (call_type == 'S'): # Outside of strikezone horizontally, called strike
        correct_call = 0
    elif (abs(plate_x) < sz_hor) and (plate_z < (sz_top + baseball_rad)) and (plate_z > (sz_bot - baseball_rad)) and (call_type == 'B'): # In strikezone, called ball
        correct_call = 0
    elif (plate_z > (sz_top + baseball_rad)) and (call_type == 'S'): # High, called strike
        correct_call = 0
    elif (plate_z < (sz_bot - baseball_rad)) and (call_type == 'S'): # Low, called strike
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


def import_umpires(season, type = 'regular', exec_type = 'game', export_dir = './ump-analysis/retrosheet'):
    """
    Import umpire data from retrosheets and match it to statcast.

    Will probably delete since I don't think I need it (rip like 6 hours)
    """
    if not os.path.isfile(f'{export_dir}/{season}events.csv'):
        retrosheet_exec.pull_event_files(season, type, export_dir)
        retrosheet_exec.exec_event_files(season, exec_type, export_dir)
    
    df_rs = pd.DataFrame(data = pd.read_csv(f'./ump-analysis/retrosheet/{season}events.csv', names = df_headers('retrosheet-games')))
    #print(df_rs)
    #df_rs = df_rs[['game_id','home_plate_umpire']]
    #print(df_rs)
    return df_rs


def missed_call_plotting(df_sc: pd.DataFrame):
    """
    Adds partial working plotting with strike zone layer.
    """
    sz_top_avg: float = df_sc.loc[:, 'sz_top'].mean()
    sz_bot_avg: float = df_sc.loc[:, 'sz_bot'].mean()
    sz_hor: float = 0.83
    df_mc = df_sc[['type', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'correct_call']]
    df_mc = df_mc[df_mc['correct_call'].isin([0])]

    df_mc['plate_x_S'] = df_mc.apply(x_from_sz, axis = 1, args = ['S'])
    df_mc['plate_z_S'] = df_mc.apply(z_from_sz, axis = 1, args = ['S', sz_top_avg, sz_bot_avg])
    df_mc['plate_x_B'] = df_mc.apply(x_from_sz, axis = 1, args = ['B'])
    df_mc['plate_z_B'] = df_mc.apply(z_from_sz, axis = 1, args = ['B', sz_top_avg, sz_bot_avg])

    plate_x_S_array: np.array = df_mc['plate_x_S']
    plate_x_S_array = plate_x_S_array[~np.isnan(plate_x_S_array)]
    plate_z_S_array: np.array = df_mc['plate_z_S']
    plate_z_S_array = plate_z_S_array[~np.isnan(plate_z_S_array)]
    plate_x_B_array: np.array = df_mc['plate_x_B']
    plate_x_B_array = plate_x_B_array[~np.isnan(plate_x_B_array)]
    plate_z_B_array: np.array = df_mc['plate_z_B']
    plate_z_B_array = plate_z_B_array[~np.isnan(plate_z_B_array)]

    fig, ax = plt.subplots()
    ax.scatter(plate_x_S_array, plate_z_S_array)
    ax.scatter(plate_x_B_array, plate_z_B_array)
    ax.add_patch(Rectangle((-sz_hor, sz_bot_avg),
                           (sz_hor * 2), (sz_top_avg - sz_bot_avg),
                           edgecolor = 'black',
                           facecolor = 'none'))
    plt.show()
    return

def x_from_sz(df_mc: pd.DataFrame, call_type: str) -> float:
    """
    Logic for whether or not ot return a value.
    """
    x_pos: float = None
    match call_type:
        case 'S': # Determined when calling this function
            if df_mc['type'] == 'S': # Checking to see this rows 'type' matches the call_type argument
                x_pos = df_mc['plate_x']
        case 'B': # Same as above, but with B instead of S
            if df_mc['type'] == 'B': 
                x_pos = df_mc['plate_x']
    return x_pos

def z_from_sz(df_mc: pd.DataFrame, call_type: str, sz_top_avg: float, sz_bot_avg: float) -> float:
    """
    Logic for determining the position for the y-axis of the scatter plot.
    
    Works but needs to optomized/cleaned
    """
    z_pos = None
    match call_type:
        case 'S': # Determined when calling this function
            if df_mc['type'] == 'S': # Checking to see this rows 'type' matches the call_type argument
                if df_mc['plate_z'] > df_mc['sz_top']: # If ball is above sz
                    relative_pos = df_mc['plate_z'] - df_mc['sz_top']
                    z_pos = relative_pos + sz_top_avg
                elif df_mc['plate_z'] < df_mc['sz_bot']: # If ball is below sz
                    relative_pos = df_mc['sz_bot'] - df_mc['plate_z']
                    z_pos = sz_bot_avg - relative_pos # If ball is in uppper half of sz
                elif (df_mc['sz_top'] - df_mc['plate_z']) > (df_mc['plate_z'] - df_mc['sz_bot']):
                    relative_pos = df_mc['sz_top'] - df_mc['plate_z']
                    z_pos = sz_top_avg - relative_pos
                else: # If ball is in sz, but not he upper half
                    relative_pos = df_mc['plate_z'] - df_mc['sz_bot']
                    z_pos = relative_pos + sz_bot_avg
        case 'B': # Same as above, but with B instead of S
            if df_mc['type'] == 'B':
                if df_mc['plate_z'] > df_mc['sz_top']:
                    relative_pos = df_mc['plate_z'] - df_mc['sz_top']
                    z_pos = relative_pos + sz_top_avg
                elif df_mc['plate_z'] < df_mc['sz_bot']:
                    relative_pos = df_mc['sz_bot'] - df_mc['plate_z']
                    z_pos = sz_bot_avg - relative_pos
                elif (df_mc['sz_top'] - df_mc['plate_z']) > (df_mc['plate_z'] - df_mc['sz_bot']):
                    relative_pos = df_mc['sz_top'] - df_mc['plate_z']
                    z_pos = sz_top_avg - relative_pos
                else:
                    relative_pos = df_mc['plate_z'] - df_mc['sz_bot']
                    z_pos = relative_pos + sz_bot_avg
    return z_pos

#df_rs = pd.DataFrame(data=pyball.retrosheet.season_game_logs('2023'))

df_sc = correct_call(start_dt = "2023-03-30", end_dt = "2023-04-01")

#missed_call_plotting(df_sc)

#df_sc = red_analysis(df_sc)

#print(df_sc)

#df_sc.to_csv("statcast_data_calls_all_red.csv", index=False, encoding='utf8')