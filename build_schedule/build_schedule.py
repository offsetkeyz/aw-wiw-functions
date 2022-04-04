__author__ = "Colin McAllister"

from csv import excel
import datetime
import time
import bs_methods
import excel_methods
import pytz

def build_schedule(token, schedule_name='tse1'):
    # replace the contents of the parenthesis with the file location
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/' + str(schedule_name) + '.csv'):
        bs_methods.build_schedule(token, schedule_name, x[0], x[1], x[2], x[3], x[4])

def main():
    token = bs_methods.authenticate_WiW_API()
    start_time = time.perf_counter()
    # bs_methods.get_all_future_shifts(token)

    # excel_methods.list_all_wiw_users(token)

    bs_methods.copy_users_schedule(bs_methods.get_user_id_from_email(token,'colin.mcallister@arcticwolf.com'), 'stephanie.legue@arcticwolf.com', datetime.datetime.now().astimezone(pytz.timezone('UTC')), token)
    end_time = time.perf_counter()
    print('Time for user_id: ' + str(end_time - start_time))

if __name__ == "__main__":
    main()