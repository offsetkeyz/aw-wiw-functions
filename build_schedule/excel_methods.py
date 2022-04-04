from datetime import *
from distutils.command import build
from dateutil.tz import *
import requests
import bs_methods
import shift_classes
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill

workbook_location = '/Users/colin.mcallister/Library/CloudStorage/OneDrive-ArcticWolfNetworksInc/Documents/test_triage_schedule.xlsx'
workbook = load_workbook(workbook_location)
date_columns = {}

def list_all_wiw_users(token):
    all_users = []
    url_headers = bs_methods.get_url_and_headers('users', token)
    response = requests.request("GET", url_headers[0], headers=url_headers[1])
    for i in response.json()['users']:
        all_users.append(shift_classes.user(i['first_name'], i['last_name'], i['email'], i['employee_code'], i['positions']), int(i['role']), i['locations'], bool(i['is_hidden']), bool(i['is_active']))
    return all_users

def build_date_row():
    for sheet in workbook.sheetnames:
        current_ws = workbook[sheet]
        start_date = datetime.now()
        for col in current_ws.iter_cols(min_row=1, max_row=1, min_col=3, max_col=360):
            for cell in col:
                cell.value = datetime.strftime(start_date, '%d %b %Y')
                cell.fill = PatternFill("solid", fgColor="FFEFC2")
                if datetime.strftime(datetime.strptime(cell.value, '%d %b %Y'), '%a').startswith('S'): #weekend
                    cell.fill = PatternFill("solid", fgColor="AFD5FF")
            start_date = start_date + timedelta(days=1)
        workbook.save(workbook_location)

def get_all_date_columns():
    print()
    
build_date_row()