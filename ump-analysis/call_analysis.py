import pandas as pd
import numpy as np
import os
import pybaseball as pyball
import retrosheet_exec
from df_headers import df_headers

def correct_call(start_dt, end_dt) -> pd.DataFrame:
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


def import_umpires(season, type = 'regular', exec_type = 'game', export_dir = './ump-analysis/retrosheet'):
    """
    Import umpire data from retrosheets and match it to statcast.
    """
    if not os.path.isfile(f'{export_dir}/{season}events.csv'):
        retrosheet_exec.pull_event_files(season, type, export_dir)
        retrosheet_exec.exec_event_files(season, exec_type, export_dir)
    
    df_rs = pd.DataFrame(data = pd.read_csv(f'./ump-analysis/retrosheet/{season}events.csv', names = df_headers('retrosheet-games')))
    #print(df_rs)
    #df_rs = df_rs[['game_id','home_plate_umpire']]
    #print(df_rs)
    return df_rs


def remove_empty():
    """
    Removes columns that have no data at all.
    """
    #df_sc.dropna(how = 'all', axis = 1, inplace = True)

#remove_empty()

#df_rs = pd.DataFrame(data=pyball.retrosheet.season_game_logs('2023'))

#df_sc = correct_call(start_dt = "2023-03-30", end_dt = "2023-04-01")
#df_rs = import_umpires('2023')
df_pm = pd.DataFrame(data = pd.read_csv('player-map.csv'))
df_pm.columns = [['IDPLAYER', 'PLAYERNAME', 'BIRTHDATE', 'FIRSTNAME', 'LASTNAME', 'TEAM', 'LG', 'POS', 'IDFANGRAPHS', 'FANGRAPHSNAME', 'MLBID', 'MLBNAME', 'CBSID', 'CBSNAME', 'RETROID', 'BREFID', 'NFBCID', 'NFBCNAME', 'ESPNID', 'ESPNNAME', 'KFFLNAME', 'DAVENPORTID', 'BPID', 'YAHOOID', 'YAHOONAME', 'MSTRBLLNAME', 'BATS', 'THROWS', 'FANTPROSNAME', 'LASTCOMMAFIRST', 'ROTOWIREID', 'FANDUELNAME', 'FANDUELID', 'DRAFTKINGSNAME', 'OTTONEUID', 'HQID', 'RAZZBALLNAME', 'FANTRAXID', 'FANTRAXNAME', 'ROTOWIRENAME', 'ALLPOS', 'NFBCLASTFIRST', 'ACTIVE', 'UNDERDOG']]
print(df_pm)
df_pm_use = df_pm[['FIRSTNAME','LASTNAME','POS','MLBID','RETROID']]
df_pm_use.to_csv('./players-maped.csv')

#df_sc.to_csv("statcast_data_calls_all.csv", index=False, encoding='utf8')