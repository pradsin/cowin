import requests
import sys
import time
from playsound import playsound

read_from_url = False

districts = [650, 651, 145, 148, 144]

while True:
    slot_found = False

    for district in districts:
        URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}'
        payload = {}
        headers = {
            'Accept': "*/*",
            'User-Agent': 'gzip, deflate, br',
            'PostmanRuntime/7.26.10': 'PostmanRuntime/7.26.10',
            'Connection': 'keep-alive'
        }

        url = URL.format(district_id=district, date='09-05-2021')
        response = requests.request('GET', url, data=payload, headers=headers)

        if response.status_code == 200:
            vaccines = response.json()
        else:
            continue

        for center in vaccines['centers']:
            for session in center['sessions']:
                min_age_limit = int(session['min_age_limit'])
                if min_age_limit < 45:
                    available_capacity = int(session['available_capacity'])
                    if available_capacity > 2:
                        print('\n\n\n', center, '\n\n\n')
                        slot_found = True
    if slot_found:
        for i in range(20):
            playsound('C:\\Windows\\Media\\notify.wav')
            time.sleep(2)

    if not slot_found:
        print("no available slots found.")

    print("Sleeping for 30 seconds before trying again")

    slot_found = False

    for i in range(30):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
    print('.')
