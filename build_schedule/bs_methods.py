__author__ = "Colin McAllister"

from tracemalloc import start
from turtle import update
import shift_classes
import requests
import json
import csv
from datetime import *
from dateutil.tz import *
import pytz

def authenticate_WiW_API():
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
        return token
    except:
        print(str(response) + " | Password or API Key Incorrect.")
        return authenticate_WiW_API()

def get_url_and_headers(type, token):
    url = "https://api.wheniwork.com/2/" + str(type)
    headers = {
    'Host': 'api.wheniwork.com',
    'Authorization': 'Bearer ' + token, 
    }
    return [url, headers]    

# Builds out a full rotation given the below parameters.
def build_schedule(token, schedule_name,user_email, start_date, starting_week, rotations, team_number):
    user_email = check_email_format(user_email)
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
                create_shift(token, user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, team_number, position)
                current_date = current_date + timedelta(days=j[3])
        for y in range(1, starting_week):
            current_week_schedule = current_schedule.get(y)
            for j in current_week_schedule:
                create_shift(token, user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, team_number, position)
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
            

def create_shift(token, user_email, start_time, length, color, notes, schedule_id, team_number, position):
    user_id = get_user_id_from_email(token, user_email)
    
    start_hour = int(start_time.strftime('%H'))
    start_time = start_time.replace(hour=(start_hour + is_DST(start_time, schedule_id)))
    end_time = start_time + timedelta(hours=length) 

    shift_color = shift_classes.get_color_code(color)
    url_headers = get_url_and_headers('shifts', token)
    payload = json.dumps({
        "user_id": user_id, 
        "location_id": schedule_id,
        "start_time": start_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "end_time" : end_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "color": shift_color,
        "notes" : notes,
        "site_id" : get_team_id(team_number),
        "position_id": position
    }) 
    success = False
    i = 1
    while success == False & i < 10:
        try:   
            requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)
            success = True
        except:
            success == False
            i += 1


# parses through a csv for employees schedule and feeds the info into build_schedule()
# 
# files are listed at the top.
def get_employee_starts_from_csv(input_file):
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

def get_team_id(team_number):
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
        return team_number

# assigns a position to each shift based on the schedule
def get_position(schedule_name):
    all_positions = {'tse1': 10470912, 'tse1': 10470912, 'tse2': 10471919, 'tse3': 10474041, 'techops': 10477571}
    try:
        return all_positions[schedule_name]
    except:
        print("error with get_position()")
        return 0

#Checks email for correct format. Not super necessary unless taking user input
def check_email_format(user_name):
    if not user_name.endswith('@arcticwolf.com'):
        print("Incorrect Format with username: " + user_name)
        user_name=check_email_format()
    return user_name

# converts datetime to correct format for WiW API
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
def get_user_id_from_email(token, user_email):
    url_headers = get_url_and_headers('users?search='+user_email, token)
    success = False
    i = 1
    while success == False & i < 10:
        try:
            response = requests.request("GET", url_headers[0], headers=url_headers[1])
            success = True
        except:
            success = False
            i +=1 
    try:
        user_id = response.json()['users'][0]['id']
    except:
        print("User: " + user_email + " not in When I Work")
        user_id = 0
    return user_id

def get_user_from_id(token, user_id):
    url_headers = get_url_and_headers('users/'+user_id, token)
    i = 1
    while i < 10:
        try:
            return requests.request("GET", url_headers[0], headers=url_headers[1])
        except:
            i +=1 
    return

#takes DateTime and returns 0 if no and -1 if yes.
def is_DST(dt, schedule_id):
    dst_start = datetime(2022, 3, 13, 7, 0, tzinfo=tzutc())
    dst_end = datetime(2022, 11, 6, 7, 0, tzinfo=tzutc())

    if schedule_id == "5227330": # EMEA has different DST
        dst_start = datetime(2022, 3, 27, 3, 0, tzinfo=tzutc())
        dst_end = datetime(2022, 10, 30, 3, 0, tzinfo=tzutc())

    if (dst_start < dt < dst_end):
        return -1
    return 0

#######################################################################################################################################################
###################################################              SHIFTS            ####################################################################
#######################################################################################################################################################

def copy_users_schedule(user_id_to_copy, new_user_email, start_date, token):
    def create_duplicate_shift(token, user_email, start_time, length, color, notes, schedule_id, team_number, position):
        user_id = get_user_id_from_email(token, user_email)    
        start_hour = int(start_time.strftime('%H'))
        start_time = start_time.replace(hour=(start_hour))
        end_time = start_time + timedelta(hours=length) 
        shift_color = shift_classes.get_color_code(color)
        url_headers = get_url_and_headers('shifts', token)
        payload = json.dumps({
            "user_id": user_id, 
            "location_id": schedule_id,
            "start_time": start_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
            "end_time" : end_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
            "color": shift_color,
            "notes" : notes,
            "site_id" : get_team_id(team_number),
            "position_id": position
        }) 
        success = False
        i = 1
        while success == False & i < 10:
            try:   
                requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)
                success = True
            except:
                success == False
                i += 1

    all_shifts_json = get_all_future_shifts_json(token)
    all_shifts = store_shifts_by_user_id(all_shifts_json)
    for shift in all_shifts[user_id_to_copy]:
        if shift.start_time >= start_date:
            create_duplicate_shift(token, new_user_email, shift.start_time, shift.length, shift.color, shift.notes, shift.location_id, shift.site_id, shift.position_id)

    
            

#also deletes duplicate shifts
def get_all_future_shifts_json(token):    
# url_headers = get_url_and_headers('shifts')
    url_headers = get_url_and_headers('shifts?start=' + str(datetime.now()) + "&end=" + str(datetime.now()+ timedelta(days=180)) + "&unpublished=true", token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_shifts = response.json()['shifts']
    #TODO Delete for loop below.
    # for shift in all_shifts:
    return all_shifts

def delete_shift(shift_id, token):
    url_headers = get_url_and_headers('shifts/' + str(shift_id), token)
    response = requests.request("DELETE", url_headers[0], headers=url_headers[1])

def get_time_off_requests(token):
    print('in progress')

def store_shifts_by_user_id(all_shifts_in):
        # key: user_id | value: array of shifts
    employee_shifts = {}
    for i in all_shifts_in:
        start_time = datetime.strptime(i['start_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        end_time = datetime.strptime(i['end_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        new_shift = shift_classes.shift(int(i['id']), int(i['account_id']), int(i['user_id']), int(i['location_id']), int(i['position_id']),
                                int(i['site_id']), start_time, end_time, bool(i['published']), bool(i['acknowledged']), i['notes'], i['color'], bool(i['is_open']))
        if int(i['user_id']) in employee_shifts:
            current_users_shifts = employee_shifts.get(int(i['user_id']))
            current_users_shifts.append(new_shift)
            employee_shifts[int(i['user_id'])] = current_users_shifts
        else: 
            employee_shifts[int(i['user_id'])] = [new_shift]
    return employee_shifts

# deletes all duplicate shifts
def store_shifts_by_hash(token, all_shifts_in):
    hashed_shifts = {}
    for i in all_shifts_in:
        new_shift = create_shift_from_json(i)
        shift_hash = get_shift_hash(new_shift)
        if shift_hash in hashed_shifts: #deletes any duplicate shifts
            delete_shift(new_shift.shift_id,token)
        else:
            hashed_shifts[shift_hash] = new_shift
    return hashed_shifts

#creates a unique hash for each shift by multiplying the start time by user ID
# allows for quick lookup of duplicate shifts
def get_shift_hash(shift_in):
    start_time = int(shift_in.start_time.strftime('%Y%m%d%H%M'))
    user_id = int(shift_in.user_id)
    return start_time * user_id

# takes a json shift object and creates
def create_shift_from_json(i):
        start_time = datetime.strptime(i['start_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        end_time = datetime.strptime(i['end_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        return shift_classes.shift(int(i['id']), int(i['account_id']), int(i['user_id']), int(i['location_id']), int(i['position_id']),
                                int(i['site_id']), start_time, end_time, bool(i['published']), bool(i['acknowledged']), i['notes'], i['color'], bool(i['is_open']))

# TODO In Progress Don't use
def update_shift_notes(token, schedule_id_in):
    all_shifts_json = get_all_future_shifts_json(token)
    all_shifts = store_shifts_by_hash(token, all_shifts_json).values()
    for shift in all_shifts:
        if shift.location_id == 5132410: #TSE2
            all_notes = shift_classes.get_tse2_notes()
            updated_shift = shift_classes.shift(shift.shift_id, shift.account_id, shift.user_id, shift.location_id, shift.position_id, shift.site_id, shift.start_time, shift.end_time, shift.published, shift.acknowledged, shift.notes, shift.color, shift.is_open)
            if shift.color.lower() == 'eb3223': #red
                updated_shift.notes = all_notes['red_notes']
            elif shift.color == '72F2DA' or shift.color.lower() == '93efdb': #teal
                updated_shift.notes = all_notes['teal_notes']
            update_shift(token, updated_shift)
            
 # Takes in the updated shift information and updates the shift ID in WiW           
def update_shift(token, updated_shift_in):
    url_headers = get_url_and_headers('shifts/' + str(updated_shift_in.shift_id),token)
    payload = json.dumps({
        "id": updated_shift_in.shift_id, 
        "location_id": updated_shift_in.location_id,
        "position_id":updated_shift_in.position_id,
        "site_id":updated_shift_in.site_id,
        "start_time": updated_shift_in.start_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "end_time": updated_shift_in.end_time.strftime("%a, %d %b %Y %H:%M:%S %z"),
        "notes":updated_shift_in.notes,
        "color":updated_shift_in.color
    }) 
    request = requests.request("PUT", url_headers[0], headers=url_headers[1], data=payload)
    # print(request)


    # if schedule_name == "5132412":
    #     return get_techops_schedule(rotation_char)
    # elif schedule_name == "5134192":
    #     return get_tse3_schedule(rotation_char)
    # elif schedule_name == "5189759": #Colin Test
    #     return get_tse3_schedule(rotation_char)
    # elif schedule_name == "5227330":
    #     return get_emea_t1_schedule(rotation_char)
    # elif schedule_name == "5132410":
    #     return get_tse2_schedule(rotation_char)
    # elif schedule_name == "5129876":
    #     return get_pink(rotation_char)
    # elif schedule_name == "5132409":
    #     return get_frontline_schedule(rotation_char)
    # elif schedule_name == '5233779':
    #     return get_EMEA_tier3(rotation_char)

    # if color == "red":
    #     shift_color = "eb3223"
    # elif color == "blue":
    #     shift_color = "4E73BE"
    # elif color == "purple":
    #     shift_color = "8d3ab9"
    # elif color == "orange":
    #     shift_color = "f6c242"
    # elif color == "teal":
    #     shift_color = "93efdb"
    # elif color == "green":
    #     shift_color = "42a611"
    # elif color == "gray":
    #     shift_color = "a6a6a6"
    # elif color == "yellow":
    #     shift_color = "ffff00"
    # elif color == "light blue":
    #     shift_color = "00b0f0"
    # elif color == "dark blue":
    #     shift_color = "0070c0"
    # elif color == "pink":
    #     shift_color = "ff00dd"



