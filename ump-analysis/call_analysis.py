import pandas as pd
import numpy as np
from datetime import datetime
import pybaseball as pyball
from retrosheet_exec import exec_event_files

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


def import_umpires():
    """
    Downloads and unzips retrosheet event data and .exe, then matches
    umpires to pitches.
    """
    df_rs = pd.DataFrame(data=game_logs('2023'))
    df_rs = df_rs[['date','ump_home_id','ump_home_name']]
    return


def remove_empty():
    """
    Removes columns that have no data at all.
    """
    df_sc.dropna(how = 'all', axis = 1, inplace = True)


headers: list = ['pitch_type', 'game_date', 'release_speed', 'release_pos_x',
       'release_pos_z', 'player_name', 'batter', 'pitcher', 'events',
       'description', 'spin_dir', 'spin_rate_deprecated',
       'break_angle_deprecated', 'break_length_deprecated', 'zone', 'des',
       'game_type', 'stand', 'p_throws', 'home_team', 'away_team', 'type',
       'hit_location', 'bb_type', 'balls', 'strikes', 'game_year', 'pfx_x',
       'pfx_z', 'plate_x', 'plate_z', 'on_3b', 'on_2b', 'on_1b',
       'outs_when_up', 'inning', 'inning_topbot', 'hc_x', 'hc_y',
       'tfs_deprecated', 'tfs_zulu_deprecated', 'fielder_2', 'umpire', 'sv_id',
       'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'sz_top', 'sz_bot',
       'hit_distance_sc', 'launch_speed', 'launch_angle', 'effective_speed',
       'release_spin_rate', 'release_extension', 'game_pk', 'pitcher.1',
       'fielder_2.1', 'fielder_3', 'fielder_4', 'fielder_5', 'fielder_6',
       'fielder_7', 'fielder_8', 'fielder_9', 'release_pos_y',
       'estimated_ba_using_speedangle', 'estimated_woba_using_speedangle',
       'woba_value', 'woba_denom', 'babip_value', 'iso_value',
       'launch_speed_angle', 'at_bat_number', 'pitch_number', 'pitch_name',
       'home_score', 'away_score', 'bat_score', 'fld_score', 'post_away_score',
       'post_home_score', 'post_bat_score', 'post_fld_score',
       'if_fielding_alignment', 'of_fielding_alignment', 'spin_axis',
       'delta_home_win_exp', 'delta_run_exp']
df_sc = pd.DataFrame
df_sc = pd.DataFrame(data=pyball.statcast(start_dt = "2023-03-30", end_dt = "2023-04-01"), columns=headers)

df_sc = df_sc[df_sc['description'].isin(['ball','called_strike'])]
df_sc = df_sc[df_sc['plate_x'].notnull()]
df_sc = df_sc[df_sc['plate_z'].notnull()]
df_sc = df_sc[df_sc['sz_top'].notnull()]
df_sc = df_sc[df_sc['sz_bot'].notnull()]
df_sc['correct_call'] = df_sc.apply(correct_call, axis = 1)

#remove_empty()

df_rs = pd.DataFrame(data=pyball.retrosheet.season_game_logs('2023'))

import_umpires()

#df_sc.to_csv("statcast_data_calls_all.csv", index=False, encoding='utf8')