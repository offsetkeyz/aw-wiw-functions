__author__ = "Colin McAllister"

from csv import excel
import datetime
import time
import bs_methods
import excel_methods
import pytz

def build_schedule(token, file_name='tse2'):
    # replace the contents of the parenthesis with the file location
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/' + str(file_name) + '.csv'):
        if file_name == "pink":
            bs_methods.build_pinks(token, x[0], x[1], x[2], x[3])
        else:
            bs_methods.build_schedule(token, file_name, x[0], x[1], x[2], x[3], x[4])

def bulk_delete_all_shifts(token, file_name):
    all_shifts_json = bs_methods.get_all_future_shifts_json(token)
    all_shifts = bs_methods.store_shifts_by_user_id(all_shifts_json)
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/' + str(file_name) + '.csv'):
        bs_methods.delete_all_shifts_for_user(token, datetime.datetime.strptime(x[1], '%d %b %Y').astimezone(pytz.timezone('UTC')), bs_methods.get_user_id_from_email(token, x[0]), all_shifts)

def main():
    token = bs_methods.authenticate_WiW_API()
    start_time = time.perf_counter()

    bs_methods.delete_all_shifts_for_user(token, datetime.datetime(2022,3,1).astimezone(pytz.timezone('UTC')),bs_methods.get_user_id_from_email(token, 'osman.erol@arcticwolf.com'))
    bs_methods.delete_all_shifts_for_user(token, datetime.datetime(2022,3,1).astimezone(pytz.timezone('UTC')),bs_methods.get_user_id_from_email(token, 'tamara.perovic@arcticwolf.com'))


    # bs_methods.update_shift_start_time(token)

    build_schedule(token, 'pink')

    # bs_methods.get_all_future_shifts(token)

    # excel_methods.list_all_wiw_users(token)

    # bulk_delete_all_shifts(token, 'tse2')

    # bs_methods.update_shift_notes(token, 5132410)

    # bs_methods.copy_users_schedule(bs_methods.get_user_id_from_email(token,'divya.rathod@arcticwolf.com'), 'pruthvish.patel@arcticwolf.com', datetime.datetime(2022,4,1).astimezone(pytz.timezone('UTC')), token)
    # bs_methods.copy_users_schedule(bs_methods.get_user_id_from_email(token,'mike.tredinnick@arcticwolf.com'), 'chris.whitehead@arcticwolf.com', datetime.datetime(2022,4,1).astimezone(pytz.timezone('UTC')), token)

    end_time = time.perf_counter()
    print('Time: ' + str(end_time - start_time))

if __name__ == "__main__":
    main()