from datetime import *
from distutils.command import build
from lib2to3.pgen2 import token
import sched
from dateutil.tz import *
import requests
import bs_methods
import shift_classes
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill, Border, Side

workbook_location = '/Users/colin.mcallister/Library/CloudStorage/OneDrive-ArcticWolfNetworksInc/Documents/test_triage_schedule.xlsx'
workbook = load_workbook(workbook_location)
date_columns = {}
all_names = {}

def list_all_wiw_users(token):
    all_users = []
    url_headers = bs_methods.get_url_and_headers('users', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    for i in response.json()['users']:
        all_users.append(shift_classes.user(i['first_name'], i['last_name'], i['email'], i['employee_code'], i['positions']), int(i['role']), i['locations'], bool(i['is_hidden']), bool(i['is_active']))
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
        5227330 : "EMEA Tier1",
        # 5129876 : "Pink",
        5233779 : "EMEA Tier3"
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

def main():
    # build_date_row()
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

    # for i in workbook.sheetnames:
    #     ws = workbook[i]
    #     ws['A2'].hyperlink = 'A' + str(date_columns[datetime.strftime(datetime.now(), '%d %b %Y')])
    #     ws['A2'].value = "TODAY"
    #     ws['A2'].style = "Hyperlink"

    workbook.save(str(workbook_location))


if __name__ == "__main__":
    main()

