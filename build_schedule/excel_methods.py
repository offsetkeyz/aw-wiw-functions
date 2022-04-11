from ctypes import alignment
from datetime import *
from distutils.command import build
import json
from lib2to3.pgen2 import token
import sched
from tkinter import CENTER, HORIZONTAL, VERTICAL
from dateutil.tz import *
import requests
import bs_methods
import shift_classes
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill, Border, Side, Alignment
from openpyxl.comments import Comment

workbook_location = '/Users/colin.mcallister/Library/CloudStorage/OneDrive-ArcticWolfNetworksInc/Documents/triage_schedule_from_wiw.xlsx'
workbook = load_workbook(workbook_location)
date_columns = {}
all_names = {}

def list_all_wiw_users(token):
    all_users = []
    url_headers = bs_methods.get_url_and_headers('users', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    for i in response.json()['users']:
        all_users.append(shift_classes.user(i['first_name'], i['last_name'], i['email'], i['employee_code'], i['positions'], i['role'], i['locations'], i['is_hidden'], i['is_active']))
    return all_users

#takes in location (schedule) ID and returns which worksheet
def check_location_id(location_id) -> str:
    schedules = {
        #5129876 : "Default"
        5132409 : "TSE1",
        5132410 : "TSE2",
        5134192 : "TSE3",
        5132412 : "TechOps",
        # 5189759 : "Colin Test",
        5227330 : "EMEATier1",
        # 5129876 : "Pink",
        5233779 : "EMEATier3"
    }
    try:
        return schedules[int(location_id)]
    except:
        return 0

def build_date_row():
    for sheet in workbook.sheetnames:
        current_ws = workbook[sheet]
        start_date = datetime(2022,3,1)
        for col in current_ws.iter_cols(min_row=1, max_row=1, min_col=3, max_col=360):
            for cell in col:
                cell.value = datetime.strftime(start_date, '%d %b %Y')
                date_columns[datetime.strftime(start_date, '%d %b %Y')] = cell.column #stores columns of dates in global dict. Columns same for all sheets
                cell.fill = PatternFill("solid", fgColor="FFEFC2")
                if datetime.strftime(datetime.strptime(cell.value, '%d %b %Y'), '%a').startswith('S'): #weekend
                    cell.fill = PatternFill("solid", fgColor="AFD5FF")
            start_date = start_date + timedelta(days=1)
        workbook.save(str(workbook_location))

def update_users(token):
    s2_employees = get_s2_employees()
    wiw_users = list_all_wiw_users(token)
    for user in wiw_users:
        try:
            user_details = s2_employees[str(user.email).strip().lower()]
        except:
            continue
        update_wiw_user(token,user_details)

def get_s2_employees():
    weekly_headcount = load_workbook('/Users/colin.mcallister/Downloads/Weekly Headcount Report - S2.xlsx', data_only=True)
    S2_Roster = weekly_headcount['Current Employee List']
    all_s2_employees = {}
    for row in range(2, S2_Roster.max_row):
        current_email = str(S2_Roster.cell(row=row, column=19).value).strip().lower()
        position = S2_Roster.cell(row=row, column=5).value
        active_status = S2_Roster.cell(row=row, column=22).value
        region = S2_Roster.cell(row=row, column=10).value
        employee_id = S2_Roster.cell(row=row, column=1).value
        all_s2_employees[current_email] = {'id' : employee_id, 'position' : position, 'status' :active_status, 'region' : region, 'email' : current_email}
    return all_s2_employees

def update_wiw_user(token,user_details): #10656558 is "unknown"
    all_positions = {'Triage Sec Eng 1': 10470912, 'Triage Sec Analyst': 10470912, 'Triage Sec Eng 2': 10471919, 'Triage Sec Eng 3': 10474041, 'Network Ops Supp Analyst': 10477571, 'Manager, iSOC': 10477572, 'TSE4': 10486791, 'ISOC Intern': 10652403, 'EMEA Intern': 10652404, 'Triage Sec Eng 4': 10486791, 'Triage Sec Engineer 1' : 10470912, 'USA': 10654095, 'CAN': 10654096, 'DEU' : 10665016, 'GBR' : 10665016, 'Dir Business Apps Sr': 10477570, 'Co-op/ Intern':10652403, 'Tech Lead Security Svs':10474045, 'Shift Lead Security Oper':10660927, 'Team Lead Security Ops':10474045,'Concierge Sec Eng 2':10668570, 'Mgr Security Ops Sr.':10668568, 'Team Lead Tech Ops':10477572,'Mgr Security Operations':10477572, 'Mgr Concierge Services':10477572,'Mgr, Security Operations':10477572, 'Triage Business Analyst':10668571,'Concierge Sec Eng 3':10665015,'Business Sys Mgr':10477572,'Dir Security Oper Sr':10477570,'Dir Security Svs':10477570}
    
    url_headers = bs_methods.get_url_and_headers('users/' + str(bs_methods.get_user_id_from_email(token, user_details['email'])),token)
    user_positions = []
    if user_details['position'] not in all_positions:
        user_positions.append(10656558)
        print(user_details['position'])
    else: 
        user_positions.append(all_positions[user_details['position']])

    payload = json.dumps({
        "employee_code": user_details['id'],
        "positions": [
            user_positions[0],
            all_positions[user_details['region']]
        ],
    }) 
    success=False
    i = 1
    while success == False and i < 10:
        try:
            response = requests.request("PUT", url_headers[0], headers=url_headers[1], data=payload)
            success = True  
        except:
            i+=1


def get_date_rows():
    current_ws = workbook['TSE1']
    for cell in current_ws[1]:
        date_columns[str(cell.value)] = cell.column #stores columns of dates in global dict. Columns same for all sheets

# returns dict with Worksheet as key and an array of names as value
def get_all_names():
    for sheet in workbook.worksheets:
        sheet_names = {} # names : column number
        for cell in sheet['A']:
            sheet_names[cell.value] = cell.row
        all_names[sheet.title] = sheet_names

#takes in shift and returns First and Last name STRING
def get_name_from_shift(token, shift_in) -> str:
    current_user = bs_methods.get_user_from_id(token, shift_in.user_id)
    return str(current_user.first_name) + ' ' + str(current_user.last_name) 

def check_sheet_for_name(name_in, schedule_name):
    if name_in not in all_names[schedule_name]:
        #add to worksheet
        ws = workbook[schedule_name]
        current_row = ws.max_row+1
        if current_row == 2:
            current_row = 3
        ws.cell(row=current_row, column=1).value = name_in
        #add to dict
        all_names[schedule_name][name_in] = current_row

def populate_user_in_excel_sheet(user_shifts, schedule_name, user):
        team_number = False
        for shift in user_shifts:
           ws = workbook[schedule_name]
           try:
                current_cell = ws.cell(row=all_names[schedule_name][user.full_name], column=date_columns[datetime.strftime(shift.start_time, '%d %b %Y')])
           except KeyError:
               continue
           current_cell.value = shift.length
           if shift.location_id not in [5227330,5233779] and 0 <= int(datetime.strftime(shift.start_time, '%-H')) <= 6:
               current_cell.value = str(int(current_cell.value)) + 'N'
           elif shift.location_id not in [5227330,5233779]:
                current_cell.value = str(int(current_cell.value)) + 'D'
            #checks if the shift is within 20 days of current day
           if team_number == False and (int(datetime.strftime(datetime.now(), '%-j'))-10) < int(datetime.strftime(shift.start_time, '%-j')) < (int(datetime.strftime(datetime.now(), '%-j'))+10):
                team_cell = ws.cell(row=all_names[schedule_name][user.full_name], column=2)
                team_cell.value = bs_methods.get_team_number(shift.site_id)
                team_number = True
           current_cell.fill = PatternFill("solid", fgColor=shift.color)
           current_cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),top=Side(style='thick'),bottom=Side(style='thick'))
           current_cell.comment = Comment(shift.notes, "iSOC Scheduling")

def input_time_off_requests():
    all_requests_json = bs_methods.get_time_off_requests(token)
    #TODO

def create_today_hyperlinks():
    for i in workbook.sheetnames:
        ws = workbook[i]
        column_letter=str(ws.cell(row=1, column=date_columns[datetime.strftime(datetime.now(), '%d %b %Y')]).column_letter)
        display_text = '#' + i + '!' + column_letter + str(ws.min_row) + ':' + column_letter + str(ws.max_row)
        ws['A2'].hyperlink = display_text
        ws['A2'].value = ">> TODAY <<"
        ws['A2'].style = "Hyperlink"
        ws['A2'].font = Font(bold=True, size=20)
        ws['A2'].alignment = Alignment(horizontal='center', vertical='center')
        ws['A2'].border = Border(left=Side(style='double'), right=Side(style='double'),top=Side(style='double'),bottom=Side(style='double'))

def clear_sheets():
    for i in workbook.sheetnames:
        ws = workbook[i]
        ws.delete_rows(2, ws.max_row)

def main():
    clear_sheets()
    build_date_row()
    get_date_rows()
    get_all_names()
    token = bs_methods.authenticate_WiW_API()
    all_shifts_json = bs_methods.get_all_shifts_json(token)
    all_shifts = bs_methods.store_shifts_by_user_id(all_shifts_json) #returns dict with user_id as key
    for user_id in all_shifts:
        user = bs_methods.get_user_from_id(token, user_id)
        user_shifts = all_shifts[user_id]
        schedule_name = check_location_id(user_shifts[0].location_id)
        if schedule_name == 0:
            continue #shift not on a tracked schedule
        check_sheet_for_name(user.full_name, schedule_name)
        populate_user_in_excel_sheet(user_shifts, schedule_name, user)
    # update_users(token)


    create_today_hyperlinks()



    workbook.save(str(workbook_location))


if __name__ == "__main__":
    main()

