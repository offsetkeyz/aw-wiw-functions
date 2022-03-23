__author__ = "Colin McAllister"

import shift_classes
import requests
import json
import csv
from datetime import *
from dateutil.tz import *

password = input("Enter Password: ")
api_key = input("Enter API Key: ")

url = "https://api.wheniwork.com/2/login"
payload = json.dumps({
"username": "sawi43kd@arcticwolf.net", 
"password": password 
})
headers = {
'W-Key': api_key,
'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
try:
    token = response.json()['token']
    print("Good to Go!")
except:
    print(str(response) + " | Password or API Key Incorrect.")

# Builds out a full rotation given the below parameters.
def build_schedule(user_email, start_date, schedule_name, starting_week, rotations, team_number):
    user_email = get_user_email(user_email)
    start_date = get_start_date(start_date)
    location_id = get_location_id(schedule_name)
    starting_week_rotation = starting_week
    rotation_char = starting_week_rotation[-1]
    position = get_position(schedule_name)

    if len(starting_week_rotation) == 3:
        starting_week = int(starting_week_rotation[:2])
    else:
        starting_week = int(starting_week_rotation[0])
    i=1
    current_date = start_date
    # build out 3 rotations
    while i <= 3:
        current_schedule = shift_classes.get_current_schedule(location_id, rotation_char)
        for x in range(starting_week, len(current_schedule) + 1): 
            current_week_schedule = current_schedule.get(x)
            for j in current_week_schedule:
                create_shift(user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, team_number, position)
                current_date = current_date + timedelta(days=j[3])
        for y in range(1, starting_week):
            current_week_schedule = current_schedule.get(y)
            for j in current_week_schedule:
                create_shift(user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, team_number, position)
                current_date = current_date + timedelta(days=j[3])
        if schedule_name != 'emea tier 3':
            try: #rotate through a/b or a/b/c
                if int(rotations) > 2:
                    if rotation_char == 'a':
                        rotation_char = 'b'
                    elif rotation_char == 'b':
                        rotation_char = 'c'
                    else:
                        rotation_char = 'a'
                else:
                    if rotation_char == 'a':
                        rotation_char = 'b'
                    else:
                        rotation_char = 'a'
            except:
                print('error switching rotation character line 65')
        i = i+1
            

def create_shift(user_email, start_time, length, color, notes, schedule_id, team_number, position):
    user_id = get_user_id_from_email(user_email)
    
    start_hour = int(start_time.strftime('%H'))
    start_time = start_time.replace(hour=(start_hour + is_DST(start_time, schedule_id)))
    end_time = start_time + timedelta(hours=length) 

    shift_color = shift_classes.get_color_code(color)
    url_headers = get_url_and_headers('shifts')
    payload = json.dumps({
        "user_id": user_id, 
        "location_id": schedule_id,
        "start_time": start_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "end_time" : end_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "color": shift_color,
        "notes" : notes,
        "site_id" : get_team(team_number),
        "position_id": position
    }) 
    response = requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)


# parses through a csv for employees schedule and feeds the info into build_schedule()
# 
# files are listed at the top.
def get_employee_list(input_file):
    employee_list = []
    with open(input_file, "r") as text_file:
        reader = csv.reader(text_file)
        for row in reader:
            try: 
                if str(row[0]).startswith('#'): #ignore comments in text file
                    continue
            except:
                continue
            current_row = []
            for item in row:
                current_row.append(item.strip())

            employee_list.append(current_row)
    return employee_list

def get_team(team_number):
    try:
        n = int(team_number)
    except:
        print("Team number not INT")
    teams = {
        1: 4781862,2: 4781869,3: 4781872,4: 4781873,5: 4781874,6: 4781875,7: 4781876,8: 4781877,9: 4781878,10: 4781873
     }
    try:
         return teams[n]
    except: 
        print("error with team number")
        return 0

def get_position(schedule_name):
    all_positions = {'tse1': 10470912, 'tse1': 10470912, 'tse2': 10471919, 'tse3': 10474041, 'techops': 10477571}
    try:
        return all_positions[schedule_name]
    except:
        print("error with get_position()")
        return 0

#Checks email for correct format. Not super necessary unless taking user input
def get_user_email(user_name):
    if not user_name.endswith('@arcticwolf.com'):
        print("Incorrect Format with username: " + user_name)
        user_name=get_user_email()
    return user_name

def get_start_date(input_date):
    try:
        dt_start = datetime.strptime(input_date, '%d %b %Y')
        dt_start = dt_start.replace(hour=13, tzinfo=tzutc())
    except ValueError:
        print ("Incorrect format with get_start_date: " + input_date)
    return dt_start

#takes in schedule name and manually returns the ID
def get_location_id(schedule_name):
    schedule_name = schedule_name.lower().strip()
    schedules = {
        "default" : "5129876",
        "tse1" : "5132409",
        "tse2" : "5132410",
        "tse3" : "5134192",
        "techops" : "5132412",
        "colin test" : "5189759",
        "emea tier 1" : "5227330",
        "pink" : "5129876",
        "emea tier 3": '5233779'
    }
    try: 
        return schedules.get(schedule_name)
    except:
        return schedules.get("default")

# takes in user email and returns WiW User ID
def get_user_id_from_email(user_email):
    url_headers = get_url_and_headers('users?search='+user_email)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    try:
        user_id = response.json()['users'][0]['id']
    except:
        print("User: " + user_email + " not in When I Work")
    return user_id

def get_url_and_headers(type):
    url = "https://api.wheniwork.com/2/" + type
    headers = {
    'Host': 'api.wheniwork.com',
    'Authorization': 'Bearer ' + token, 
    }
    return [url, headers]

#takes DateTime and returns 0 if no and -1 if yes.
def is_DST(dt, schedule_id):
    dst_start = datetime(2022, 3, 13, 7, 0, tzinfo=tzutc())
    dst_end = datetime(2022, 11, 6, 7, 0, tzinfo=tzutc())

    if schedule_id == "5227330": # EMEA has different DST
        dst_start = datetime(2022, 3, 27, 3, 0, tzinfo=tzutc())
        dst_end = datetime(2022, 10, 30, 3, 0, tzinfo=tzutc())

    if (dt > dst_start and dt < dst_end):
        return -1
    return 0