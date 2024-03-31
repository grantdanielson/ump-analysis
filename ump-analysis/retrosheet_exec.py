from io import BytesIO
from zipfile import ZipFile
import os
import pybaseball as pyball

event_list = "BGAME -y 2023 -f 0-84 2023ANA.EVA 2023ARI.EVN 2023ATL.EVN 2023BAL.EVA 2023BOS.EVA 2023CHA.EVA 2023CHN.EVN 2023CIN.EVN 2023CLE.EVA 2023COL.EVN 2023DET.EVA 2023HOU.EVA 2023KCA.EVA 2023LAN.EVN 2023MIA.EVN 2023MIL.EVN 2023MIN.EVA 2023NYA.EVA 2023NYN.EVN 2023OAK.EVA 2023PHI.EVN 2023PIT.EVN 2023SDN.EVN 2023SEA.EVA 2023SFN.EVN 2023SLN.EVN 2023TBA.EVA 2023TEX.EVA 2023TOR.EVA 2023WAS.EVN > 2023events.csv"


def exec_event_files(season):
    #pyball.retrosheet.events(season='2023', type='regular',export_dir= './retrosheet')
    file_list = os.listdir('./retrosheet')
    files: str = ', '.join(file_list)
    print(file_list)
    print(files)
    os.system(f'cd ./retrosheet && {event_list}')

exec_event_files('2023')