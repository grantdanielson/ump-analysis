import pandas as pd
import numpy as np
import pybaseball as pyball
from df_headers import df_headers
#from retrosheet_exec import exec_event_files

def correct_call(df_sc: pd.DataFrame) -> int:
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
    baseball_rad: float = 0.120833
    correct_call: int = 1

    if (abs(plate_x) > sz_hor) and (call_type == 'S'):
        correct_call = 0
    elif (abs(plate_x) < sz_hor) and (plate_x < (sz_top + baseball_rad)) and (plate_x > (sz_bot - baseball_rad)) and (call_type == 'B'):
        correct_call = 0
    elif (plate_z < (sz_top + baseball_rad)) and (plate_z > (sz_bot - baseball_rad)) and (abs(plate_x) < sz_hor) and (call_type == 'B'):
        correct_call = 0
    elif (plate_z > (sz_top + baseball_rad)) and (call_type == 'S'):
        correct_call = 0
    elif (plate_z < (sz_bot - baseball_rad)) and (call_type == 'S'):
        correct_call = 0
    return correct_call


def import_umpires(season):
    """
    Downloads and unzips retrosheet event data and .exe, then matches
    umpires to pitches.
    """
    df_rs = pd.DataFrame(data = pd.read_csv(f'./retrosheet/{season}events.csv', names = df_headers('retrosheet-games')))
    print(df_rs)
    df_rs = df_rs[['game_id','home_plate_umpire']]
    print(df_rs)
    return


def remove_empty():
    """
    Removes columns that have no data at all.
    """
    df_sc.dropna(how = 'all', axis = 1, inplace = True)

df_sc = pd.DataFrame(data=pyball.statcast(start_dt = "2023-03-30", end_dt = "2023-04-01"), columns=df_headers('statcast'))

df_sc = df_sc[df_sc['description'].isin(['ball','called_strike'])]
df_sc = df_sc[df_sc['plate_x'].notnull()]
df_sc = df_sc[df_sc['plate_z'].notnull()]
df_sc = df_sc[df_sc['sz_top'].notnull()]
df_sc = df_sc[df_sc['sz_bot'].notnull()]
df_sc['correct_call'] = df_sc.apply(correct_call, axis = 1)

#remove_empty()

#df_rs = pd.DataFrame(data=pyball.retrosheet.season_game_logs('2023'))

import_umpires('2023')

#df_sc.to_csv("statcast_data_calls_all.csv", index=False, encoding='utf8')