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

read_from_file = False

all_districts = {622: 'Agra', 623: 'Aligarh', 625: 'Ambedkar Nagar', 626: 'Amethi', 627: 'Amroha', 628: 'Auraiya',
                 646: 'Ayodhya', 629: 'Azamgarh', 630: 'Badaun', 631: 'Baghpat', 632: 'Bahraich', 633: 'Balarampur',
                 634: 'Ballia', 635: 'Banda', 636: 'Barabanki', 637: 'Bareilly', 638: 'Basti', 687: 'Bhadohi',
                 639: 'Bijnour', 640: 'Bulandshahr', 641: 'Chandauli', 642: 'Chitrakoot', 643: 'Deoria', 644: 'Etah',
                 645: 'Etawah', 647: 'Farrukhabad', 648: 'Fatehpur', 649: 'Firozabad', 650: 'Gautam Buddha Nagar',
                 651: 'Ghaziabad', 652: 'Ghazipur', 653: 'Gonda', 654: 'Gorakhpur', 655: 'Hamirpur', 656: 'Hapur',
                 657: 'Hardoi', 658: 'Hathras', 659: 'Jalaun', 660: 'Jaunpur', 661: 'Jhansi', 662: 'Kannauj',
                 663: 'Kanpur Dehat', 664: 'Kanpur Nagar', 665: 'Kasganj', 666: 'Kaushambi', 667: 'Kushinagar',
                 668: 'Lakhimpur Kheri', 669: 'Lalitpur', 670: 'Lucknow', 671: 'Maharajganj', 672: 'Mahoba',
                 673: 'Mainpuri', 674: 'Mathura', 675: 'Mau', 676: 'Meerut', 677: 'Mirzapur', 678: 'Moradabad',
                 679: 'Muzaffarnagar', 680: 'Pilibhit', 682: 'Pratapgarh', 624: 'Prayagraj', 681: 'Raebareli',
                 683: 'Rampur', 684: 'Saharanpur', 685: 'Sambhal', 686: 'Sant Kabir Nagar', 688: 'Shahjahanpur',
                 689: 'Shamli', 690: 'Shravasti', 691: 'Siddharthnagar', 692: 'Sitapur', 693: 'Sonbhadra',
                 694: 'Sultanpur', 695: 'Unnao', 696: 'Varanasi', 141: 'Central Delhi', 145: 'East Delhi',
                 140: 'New Delhi', 146: 'North Delhi', 147: 'North East Delhi', 143: 'North West Delhi',
                 148: 'Shahdara', 149: 'South Delhi', 144: 'South East Delhi', 150: 'South West Delhi',
                 142: 'West Delhi'}

districts_to_search = [650, 651, 145, 148, 144, 188, 696, 670]
while True:
    available = []
    for district in districts_to_search:

        if read_from_file:
            with open('C:\\Users\\prads\\Desktop\\Vaccine.json') as f:
                vaccines = json.load(f)
        else:
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

            print('state:{}\ndistrict:{}\naddress:{}\npin:{}\navailable:{}'.format(center['state_name'],
                                                                                   center['district_name'],
                                                                                   center['address'],
                                                                                   center['pincode'],
                                                                                   available_capacity))
        for i in range(40):
            playsound('C:\\Windows\\Media\\notify.wav')
            time.sleep(2)
    else:
        print("no available slots found.")

    print("Sleeping for 30 seconds before trying again")

    slot_found = False

    for i in range(30):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
    print('.')
