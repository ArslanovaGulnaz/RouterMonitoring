# Подключаем библиотеки
import re
from typing import NoReturn

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import json

from mailparser import main
#from tloop import sample_job_every_120s

def get_last_email() -> str:
    with open('db', 'r', encoding='utf-8') as f:
        out = f.read()
        return out


def set_last_email(last_email: str) -> NoReturn:
    with open('db', 'w', encoding='utf-8') as f:
        f.write(last_email)

def set_to_sheet():
    router_data = main()

    last_email = get_last_email()
    new_data = []

    last_data = []

    '''---Нахождение последнего письма по условию. Output: str---'''
    cAP_Scene = next(x for x in reversed(router_data) if 'cAP_Scene' in x)
    wAP_Sklad = next(x for x in reversed(router_data) if 'wAP_Sklad' in x)
    wAP_Stolovaya = next(x for x in reversed(router_data) if 'wAP_Stolovaya' in x)
    cAP_ITShtab = next(x for x in reversed(router_data) if 'cAP_ITShtab' in x)
    Shtab_02 = next(x for x in reversed(router_data) if '02_Shtab' in x)
    Scene_05 = next(x for x in reversed(router_data) if '05_Scene' in x)
    Shater_04 = next(x for x in reversed(router_data) if '04_Shater' in x)
    wAP_Info = next(x for x in reversed(router_data) if 'wAP_Info' in x)
    Sphere_07 = next(x for x in reversed(router_data) if '07_Sphere' in x)
    wAP_3Shater = next(x for x in reversed(router_data) if 'wAP_3Shater' in x)
    Koryltay_01 = next(x for x in reversed(router_data) if '01_Koryltay' in x)
    SeletLive_03 = next(x for x in reversed(router_data) if '03_SeletLive' in x)
    
    '''-Добавление письма в массив---'''
    last_data.append(cAP_Scene)
    last_data.append(wAP_Sklad)
    last_data.append(wAP_Stolovaya)
    last_data.append(cAP_ITShtab)
    last_data.append(Shtab_02)
    last_data.append(Scene_05)
    last_data.append(Shater_04)
    last_data.append(wAP_Info)
    last_data.append(Sphere_07)
    last_data.append(wAP_3Shater)
    last_data.append(Koryltay_01)
    last_data.append(SeletLive_03)
    #last_data.append(sample_job_every_120s())
    #last_data.append(wan2)

    #print(last_data)

    '''
    Для обработки всех писем на почте
    for router in reversed(router_data):
        if router.strip() in last_email:
            break
        else:
            try:
                dt = re.search(r'.+?(?=Forum)', router).group(0)
                router_id = router.split()[-2].split('_')[-1]
    
                if 'WANN1' in router or 'WAN1' in router:
                    router_id = 'WAN1' # TODO: сменить 1 на WANN1
                else:
                    router_id = 'WAN2' # TODO: сменить 2 на WANN2
    
                if 'PROBLEM' in router.split()[-1]:
                    status = 'PROBLEM' # TODO: сменить False на PROBLEM
                else:
                    status = 'OK' # TODO: сменить TRUE на OK
    
                new_data.append([[dt], [router_id], [status]])
                if len(new_data) == 1:
                    set_last_email(router)
    
            except Exception as e:
                print(f'Error: {e} -> {router}')'''

    CREDENTIALS_FILE = 'pointsmonitoring-284014-49221dfdec9e.json'  # Имя файла с закрытым ключом, вы должны подставить свое

    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    spreadsheet_id = '1yGyCBwfpRpZ8V-1_VrhPGDvhRdr3ps3cvmGX9bHY0RE' # id таблицы, вставить свое

    range_ = 'A1:E1'  # TODO: Update placeholder value.
    value_input_option = 'RAW'


    '''values = [['3'], ['2'], ['3'], ['4'], ['5']] # не меняются значения в таблице
    value_range_body = {'values': values,
                        'majorDimension': 'COLUMNS'}
    
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    '''

    #values = [['3'], ['2'], ['3'], ['4'], ['5']]
    ''' ДЛЯ ВСЕХ ПИСЕМ 
    values = (new_data)
    for iteration, item in enumerate((new_data)):
        #print(f'A{iteration+1}:C{iteration+1}', item) #range в request с таким же диапазоном
    
        value_range_body = {'values': item,
                            'majorDimension': 'COLUMNS'}
    
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=f'A{iteration+1}:C{iteration+1}', valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()'''

    values = (last_data)
    for iteration, item in enumerate((last_data)):
        print(f'A{iteration+1}:A{iteration+1}', item) #range в request с таким же диапазоном

        value_range_body = {'values': [[item]],
                            'majorDimension': 'COLUMNS'}

        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=f'A{iteration+1}:A{iteration+1}', valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()
        #print(new_data)
    return response
    #wan1 = next(x for x in reversed(router_data) if 'WANN1' in x or 'WAN1' in x)
    #print(wan1)

