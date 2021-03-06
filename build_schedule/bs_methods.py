__author__ = "Colin McAllister"

from ast import List
from tokenize import String
from tracemalloc import start
from turtle import update
from webbrowser import get
from shift_classes import shift
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

    delete_all_shifts_for_user(token, start_date, get_user_id_from_email(token,user_email))

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
        if schedule_name not in ['emea tier 3', 'techops']:
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
            
def build_pinks(token, user_email, start_date: str, number_of_weeks : int, schedule_name):
    location_id = get_location_id(schedule_name)
    start_date = get_start_date(start_date)
    position = get_position(schedule_name)
    i=1
    current_date = start_date
    try:
        number_of_weeks = int(number_of_weeks)
    except:
        return('wrong CSV format for number of weeks')
    while i <= number_of_weeks:
        current_schedule = shift_classes.get_pink(location_id)
        for j in current_schedule:
            create_shift(token, user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, '0', position)
            current_date = current_date + timedelta(days=j[3])
        i+=1

def build_reds(token, user_email, start_date: str, number_of_weeks : int, schedule_name):
    location_id = get_location_id(schedule_name)
    start_date = get_start_date(start_date)
    position = get_position(schedule_name)
    delete_all_shifts_for_user(token, start_date, get_user_id_from_email(token, user_email))
    i=1
    current_date = start_date
    notes = 'check https://arcticwolf.atlassian.net/l/c/2wNs1gzp for responsibilities'
    try:
        number_of_weeks = int(number_of_weeks)
    except:
        return('wrong CSV format for number of weeks')
    while i <= number_of_weeks:
        current_schedule = [["red", 13, 8, 1, notes],["red", 13, 8, 1, notes],["red", 13, 8, 1, notes],["red", 13, 8, 1, notes],["red", 13, 8, 3, notes]]
        for j in current_schedule:
            create_shift(token, user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, '0', position)
            current_date = current_date + timedelta(days=j[3])
        i+=1

def build_oranges(token, user_email, start_date: str, number_of_weeks : int, schedule_name):
    location_id = get_location_id(schedule_name)
    start_date = get_start_date(start_date)
    position = get_position(schedule_name)
    delete_all_shifts_for_user(token, start_date, get_user_id_from_email(token, user_email))
    i=1
    current_date = start_date
    notes = 'check https://arcticwolf.atlassian.net/l/c/2wNs1gzp for responsibilities'
    try:
        number_of_weeks = int(number_of_weeks)
    except:
        return('wrong CSV format for number of weeks')
    while i <= number_of_weeks:
        current_schedule = [["orange", 15, 8, 1, notes],["orange", 15, 8, 1, notes],["orange", 15, 8, 1, notes],["orange", 15, 8, 1, notes],["orange", 15, 8, 3, notes]]
        for j in current_schedule:
            create_shift(token, user_email, current_date.replace(hour=j[1], tzinfo=tzutc()), j[2], j[0], j[4], location_id, '0', position)
            current_date = current_date + timedelta(days=j[3])
        i+=1


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
            request = requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)
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
        1: 4781862,2: 4781869,3: 4781872,4: 4781873,5: 4781874,6: 4781875,7: 4781876,8: 4781877,9: 4781878,10: 4781879
     }
    try:
         return teams[n]
    except: 
        return team_number

def get_team_number(site_id):
    try:
        n = int(site_id)
    except:
        print("Team number not INT")
    teams = {
        4781862:1 ,4781869:2,4781872:3,4781873:4,4781874:5,4781875:6,4781876:7,4781877:8,4781878:9,4781879:10
     }
    try:
         return teams[n]
    except: 
        return site_id

# assigns a position to each shift based on the schedule
def get_position(schedule_name):
    all_positions = {'tse1': 10762858, 'tse2': 10762859, 'tse3': 10762860, 'techops': 10762850}
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
        dt_start = datetime.strptime(str(input_date), '%d %b %Y')
        dt_start = dt_start.replace(hour=13, tzinfo=tzutc())
    except ValueError as e:
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

# takes in user email and returns WiW User ID
def get_user_id_from_name(token, user_first_name, user_last_name):
    user_email = user_first_name + '.' + user_last_name + '@arcticwolf.com'
    url_headers = get_url_and_headers('users?search='+ user_email, token)
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

#takes in user_id and returns user object
def get_user_from_id(token, user_id):
    url_headers = get_url_and_headers('users/'+str(user_id), token)
    i = 1
    while i < 10:
        try:
            j = requests.request("GET", url_headers[0], headers=url_headers[1]).json()['user']
            break
        except:
            i +=1 
    return shift_classes.user(j['first_name'], j['last_name'], j['email'], j['id'],j['positions'],j['role'],j['locations'],j['is_hidden'],j['is_active'])

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

def get_time_off_requests(token):
    url_headers = get_url_and_headers('requests?start=' + str(datetime(2022, 3, 1)) + "&end=" + str(datetime.now()+ timedelta(days=180)), token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_requests = response.json()['requests']
    return all_requests

def get_time_off_requests_for_user(token, user_id):
    url_headers = get_url_and_headers('requests?start=' + str(datetime(2022, 3, 1)) + "&end=" + str(datetime.now()+timedelta(days=100)) + '&user_id=' + str(user_id), token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    try: #permissions error
        all_requests = response.json()['requests']
    except Exception as e:
        all_requests = {}
    return store_time_off(all_requests)

def create_time_off_request(token, user, start_date, end_date):
    url_headers = get_url_and_headers('requests', token)
    payload = json.dumps({
        "user_id": user.wiw_employee_id, 
        "account_id" : get_user_id_from_email(token, 'sawi43kd@arcticwolf.net'),
        "start_time": start_date,
        "end_time" : end_date,
        # "created_at" : datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        # "status" : 2
    }) 
    success = False
    i = 1
    while success == False & i < 10:
        try:   
            request = requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)
            success = True
        except:
            success == False
            i += 1
    return request

def approve_time_off_request(token, request):
    url_headers = get_url_and_headers('requests/' + str(request.to_id), token)
    payload = {
        "status" : 2
    }
    i = 1
    while i < 10:
        try: 
            request = requests.request("PUT", url_headers[0], headers=url_headers[1], data=payload)
        except:
            i += 1
        return

def get_all_positions(token):
    url_headers = get_url_and_headers('positions', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_requests = response.json()['positions']
    all_positions = ''
    for i in all_requests:
        all_positions = all_positions + '\n' + str(i['name']) + ': ' + str(i['id'])

    return all_positions

def get_all_sites(token):
    url_headers = get_url_and_headers('sites', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_sites = response.json()['sites']
    all_positions = ''
    for i in all_sites:
        all_positions = all_positions + '\n' + str(i['name']) + ': ' + str(i['id'])

    return all_positions
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
                request = requests.request("POST", url_headers[0], headers=url_headers[1], data=payload)
                success = True
            except:
                success == False
                i += 1

    all_shifts_json = get_all_future_shifts_json(token)
    all_shifts = store_shifts_by_user_id(all_shifts_json)
    delete_all_shifts_for_user(token, start_date, get_user_id_from_email(token,new_user_email), all_shifts)
    for shift in all_shifts[user_id_to_copy]:
        if shift.start_time >= start_date:
            create_duplicate_shift(token, new_user_email, shift.start_time, shift.length, shift.color, shift.notes, shift.location_id, shift.site_id, shift.position_id)


#also deletes duplicate shifts
def get_all_future_shifts_json(token):    
# url_headers = get_url_and_headers('shifts')
    url_headers = get_url_and_headers('shifts?start=' + str(datetime.now()) + "&end=" + str(datetime.now()+ timedelta(days=360)) + "&unpublished=true", token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_shifts = response.json()['shifts']
    return all_shifts

def get_open_shifts(token):
    url_headers = get_url_and_headers('shifts?start=' + str(datetime.now()) + "&end=" + str(datetime.now()+ timedelta(days=180)) + '&include_onlyopen=true' + "&unpublished=true", token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_shifts = response.json()['shifts']
    return all_shifts

def delete_open_shifts(token, all_open_shifts=0):
    if all_open_shifts == 0: #option to pass in dictionary of shift\=]-
        all_shifts_json = get_open_shifts(token)
        all_open_shifts = store_shifts_in_array(token, all_shifts_json)
    try: 
        for shift in all_open_shifts:
            delete_shift(shift.shift_id, token)
    except:
        print('user has no shifts')

def get_all_shifts_json(token):    
# url_headers = get_url_and_headers('shifts')
    url_headers = get_url_and_headers('shifts?start=' + str(datetime(2022, 3, 1)) + "&end=" + str(datetime.now()+ timedelta(days=360)) + "&unpublished=true", token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_shifts = response.json()['shifts']
    return all_shifts

def get_all_wiw_users(token):
    all_users = {}
    url_headers = get_url_and_headers('users', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    all_users_json = response.json()['users']
    for u in all_users_json:
        all_users[u['id']] = (shift_classes.user(u['first_name'], u['last_name'], u['email'], u['id'], u['positions'], u['role'], u['locations'], u['is_hidden'], u['is_active']))
    return all_users

def delete_all_shifts_for_user(token, start_date, user_id, all_shifts=0):
    if all_shifts == 0: #option to pass in dictionary of shift\=]-
        all_shifts_json = get_all_shifts_json(token)
        all_shifts = store_shifts_by_user_id(all_shifts_json)
    try: 
        for shift in all_shifts[user_id]:
            if shift.start_time >= start_date:
                delete_shift(shift.shift_id, token)
    except:
        print('user has no shifts')


def delete_shift(shift_id, token):
    url_headers = get_url_and_headers('shifts/' + str(shift_id), token)
    response = requests.request("DELETE", url_headers[0], headers=url_headers[1])

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

def store_shifts_for_single_user(all_shifts_in):
        # key: user_id | value: array of shifts
    employee_shifts = []
    for i in all_shifts_in:
        start_time = datetime.strptime(i['start_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        end_time = datetime.strptime(i['end_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        new_shift = shift_classes.shift(int(i['id']), int(i['account_id']), int(i['user_id']), int(i['location_id']), int(i['position_id']),
                                int(i['site_id']), start_time, end_time, bool(i['published']), bool(i['acknowledged']), i['notes'], i['color'], bool(i['is_open']))
        employee_shifts.append(new_shift)
    return employee_shifts

def store_time_off(all_requests):
    requests = {}
    for i in all_requests:
        start_time = datetime.strptime(i['start_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        end_time = datetime.strptime(i['end_time'], '%a, %d %b %Y %H:%M:%S %z').astimezone(pytz.timezone('UTC'))
        new_request = shift_classes.time_off_request(i['id'], i['account_id'],i['user_id'], i['status'],i['type'],i['type_id'], i['hours'], start_time, end_time, 0,i['user_status'],i['type_label'])
        if int(i['user_id']) in requests:
            current_users_requests =requests.get(int(i['user_id']))
            current_users_requests.append(new_request)
            requests[int(i['user_id'])] = current_users_requests
        else: 
            requests[int(i['user_id'])] = [new_request]
    return requests


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

def store_shifts_in_array(token, all_shifts_in):
    array_o_shifts = []
    for i in all_shifts_in:
        new_shift = create_shift_from_json(i)
        array_o_shifts.append(new_shift)
    return array_o_shifts

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
def updated_shift_parameters(token):
    all_shifts_json = get_all_shifts_json(token)
    all_shifts = store_shifts_by_hash(token, all_shifts_json).values()
    for shift in all_shifts:
        updated_shift = shift_classes.shift(shift.shift_id, shift.account_id, shift.user_id, shift.location_id, shift.position_id, shift.site_id, shift.start_time, shift.end_time, shift.published, shift.acknowledged, shift.notes, shift.color, shift.is_open)
        # CHANGE THE NEXT LINE
        if (shift.color == '00b0f0') and (shift.location_id == 5134192):
             
            if shift.end_time.hour == 2:
                updated_shift.start_time = shift.start_time.replace(hour=16)
                updated_shift.end_time = shift.end_time.replace(hour=0)
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
    i = 1
    while i < 10:
        try: 
            request = requests.request("PUT", url_headers[0], headers=url_headers[1], data=payload)
        except:
            i += 1
        return



