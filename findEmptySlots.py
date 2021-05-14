import os

try:
    import requests
except ImportError:
    print("Trying to Install required module: requests\n")
    os.system('python -m pip install requests')
# -- above lines try to install requests module if not present
# -- if all went well, import required module again ( for global access)
import requests

try:
    from playsound import playsound
except ImportError:
    print("Trying to Install required module: requests\n")
    os.system('python -m pip install playsound')
# -- above lines try to install requests module if not present
# -- if all went well, import required module again ( for global access)
from playsound import playsound

import json
import sys
import time
from datetime import date, datetime, timedelta
import random

read_from_file = False

# Array of districts, put all nearby districts separated by comma
districts_to_search = [650, 651, 652, 145, 148, 144]
today = date.today().strftime("%d-%m-%Y")
second = (date.today() + timedelta(days=7)).strftime("%d-%m-%Y")
third = (date.today() + timedelta(days=14)).strftime("%d-%m-%Y")
dates_to_search = [today]
# dates_to_search.append(second)
# dates_to_search.append(third)
retry_after_seconds = [10, 20]
alert_for_times = 1


while True:
    available = []
    for district in districts_to_search:
        for date_to_search in dates_to_search:
            if read_from_file:
                with open('C:\\Users\\prads\\Desktop\\Vaccine.json') as f:
                    vaccines = json.load(f)
            else:
                URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={district_id}&date={date}'
                payload = {}
                headers = {
                    'authority': 'cdn-api.co-vin.in',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                    'accept': 'application/json, text/plain, */*',
                    'dnt': '1',
                    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI1NzI4N2UzYy01ZDBjLTRiYTMtODk5ZC02YjEzNTFmNDkyNGQiLCJ1c2VyX2lkIjoiNTcyODdlM2MtNWQwYy00YmEzLTg5OWQtNmIxMzUxZjQ5MjRkIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5ODczNDQxNzc4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjY5NTk1OTU5MjU2NTUwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTAuMC40NDMwLjkzIFNhZmFyaS81MzcuMzYiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0xMlQwNDoyMToxOC41NThaIiwiaWF0IjoxNjIwNzkzMjc4LCJleHAiOjE2MjA3OTQxNzh9.lQeJR586h9qQwTM9gy8CNMz7fva_cS79ZSRN3wMgYCc',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                    'origin': 'https://selfregistration.cowin.gov.in',
                    'sec-fetch-site': 'cross-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://selfregistration.cowin.gov.in/',
                    'accept-language': 'en-US,en;q=0.9,hi;q=0.8'
                }

                url = URL.format(district_id=district, date=date_to_search)
                response = requests.request('GET', url, data=payload, headers=headers)

                if response.status_code == 200:
                    vaccines = response.json()
                else:
                    print("E", end='')
                    continue

            for center in vaccines['centers']:
                for session in center['sessions']:
                    min_age_limit = int(session['min_age_limit'])
                    if min_age_limit < 45:
                        available_capacity = int(session['available_capacity'])
                        if available_capacity > 9:
                            available.append(center)
                            slot_found = True
                            break
    if len(available) > 0:
        # json_formatted_str = json.dumps(available, indent=2)
        # print(json_formatted_str)

        for center in available:
            print("-" * 40)
            available_capacity = 0

            for session in center['sessions']:
                available_capacity += int(session['available_capacity'])

            now = datetime.now().time()
            print('\ntime:{}\nstate:{}\ndistrict:{}\naddress:{}\npin:{}\navailable:{}'.format(now,
                                                                                              center['state_name'],
                                                                                              center['district_name'],
                                                                                              center['address'],
                                                                                              center['pincode'],
                                                                                              available_capacity))

        if len(available) > 0:
            for i in range(alert_for_times):
                playsound('C:\\Windows\\Media\\notify.wav')
                time.sleep(1)

    # else:
    #     print("no available slots found.")
    #
    # print("Sleeping for {} seconds before trying again".format(retry_after_seconds))

    slot_found = False

    for i in range(random.randint(retry_after_seconds[0], retry_after_seconds[1])):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
    print('-', end='')
