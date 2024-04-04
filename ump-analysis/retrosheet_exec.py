import os
import pybaseball as pyball
import retrosheet

retrosheet_dir = './ump-analysis/retrosheet'
event_list = "BGAME -y 2023 -f 0-84 2023ANA.EVA 2023ARI.EVN 2023ATL.EVN 2023BAL.EVA 2023BOS.EVA 2023CHA.EVA 2023CHN.EVN 2023CIN.EVN 2023CLE.EVA 2023COL.EVN 2023DET.EVA 2023HOU.EVA 2023KCA.EVA 2023LAN.EVN 2023MIA.EVN 2023MIL.EVN 2023MIN.EVA 2023NYA.EVA 2023NYN.EVN 2023OAK.EVA 2023PHI.EVN 2023PIT.EVN 2023SDN.EVN 2023SEA.EVA 2023SFN.EVN 2023SLN.EVN 2023TBA.EVA 2023TEX.EVA 2023TOR.EVA 2023WAS.EVN > 2023events.csv"

def pull_event_files(season, type, exec_type, export_dir = retrosheet_dir):
    #pyball.retrosheet.events(season='2023', type='regular',export_dir= export_dir)
    #retrosheet.events(season, type, export_dir)
    retrosheet.teamfile(season, export_dir)
    os.rename(f'{export_dir}/TEAM{season}', f'{export_dir}/team{season}')

def exec_event_files(season, type, exec_type, export_dir = retrosheet_dir):
    file_list = os.listdir(export_dir)
    file_list = [f for f in file_list if f.endswith(('.EVA','.EVN','.EVE'))]
    files: str = ' '.join(file_list)
    print(files)

    match exec_type:
        case 'events':
            exec_command = f'BEVENT -y {season} -f 0-96 {files} > {season}events.csv'
        case 'game':
            exec_command = f'BGAME -y {season} -f 0-84 {files} > {season}game.csv'
        case 'box':
            exec_command = ''
    os.system(f'cd {export_dir} && {exec_command}')

exec_event_files('2023', 'regular', 'events')