import os
import pandas as pd
# import pybaseball as pyball
# Use pybaseball instead of local retrosheet when it's updated to use the new chadwickbureau/retrosheet formatting
import retrosheet

retrosheet_dir = './ump-analysis/retrosheet'

def pull_event_files(season, type, export_dir = retrosheet_dir):
    """
    Pull and download event files to the specfified directory.
    """
    # Use pyball instead of local retrosheet when it's updated to use the new chadwickbureau/retrosheet formatting
    # pyball.retrosheet.events(season='2023', type='regular',export_dir= export_dir)
    # pyball.retrosheet.teamfile.(season, export_dir)
    retrosheet.events(season, type, export_dir)
    retrosheet.teamfile(season, export_dir)
    os.rename(f'{export_dir}/TEAM{season}', f'{export_dir}/team{season}')

def pull_umpires_file(season) -> pd.DataFrame:
   df_rs_ump = retrosheet.umpires(season)
   return df_rs_ump


def exec_event_files(season, exec_type, export_dir = retrosheet_dir):
    """
    Execute event files with BEVENT or BGAME.
    """
    file_list = os.listdir(export_dir)
    file_list = [f for f in file_list if f.startswith(f'{season}') and f.endswith(('.EVA','.EVN','.EVE'))]
    files: str = ' '.join(file_list)
    print(files)

    match exec_type:
        case 'events':
            exported_file = f'{season}events.csv'
            exec_command = f'BEVENT -y {season} -f 0-96 {files} > {exported_file}'
        case 'game':
            exported_file = f'{season}game.csv'
            exec_command = f'BGAME -y {season} -f 0-84 {files} > {exported_file}'
    
    os.system(f'cd {export_dir} && {exec_command}')
    print(f'{season} data successfully parsed as {exported_file}')