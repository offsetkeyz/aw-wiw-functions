__author__ = "Colin McAllister"

from csv import excel
import datetime
import time
import bs_methods
import excel_methods
import pytz

def build_schedule(token, file_name='tse1'):
    # replace the contents of the parenthesis with the file location
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/csvs/' + str(file_name) + '.csv'):
        if file_name == "pink":
            bs_methods.build_pinks(token, x[0], x[1], x[2], x[3])
        else:
            bs_methods.build_schedule(token, file_name, x[0], x[1], x[2], x[3], x[4])

def bulk_delete_all_shifts(token, file_name):
    all_shifts_json = bs_methods.get_all_future_shifts_json(token)
    all_shifts = bs_methods.store_shifts_by_user_id(all_shifts_json)
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/csvs/' + str(file_name) + '.csv'):
        bs_methods.delete_all_shifts_for_user(token, datetime.datetime.strptime(x[1], '%d %b %Y').astimezone(pytz.timezone('UTC')), bs_methods.get_user_id_from_email(token, x[0]), all_shifts)
        

def main():
    token = bs_methods.authenticate_WiW_API()
    start_time = time.perf_counter()

    bs_methods.copy_users_schedule(bs_methods.get_user_id_from_email(token,'shay.bingham@arcticwolf.com'), 'gagan.sahota@arcticwolf.com', datetime.datetime(2022,8,1).astimezone(pytz.timezone('UTC')), token)

    # bs_methods.build_pinks(token, 'andrew.sides@arcticwolf.com', '1 Aug 2022', 20, 'tse1')


    # bs_methods.updated_shift_parameters(token)

    # build_schedule(token, 'tse3')

    # bs_methods.get_all_future_shifts(token)

    # excel_methods.list_all_wiw_users(token)

    # bulk_delete_all_shifts(token, 'tse1')

    # bs_methods.build_schedule(token,'tse3','keith.perlman@arcticwolf.com','17 Jun 2022','10a','2','6')

    # bs_methods.build_oranges(token, 'sam.durston@arcticwolf.com', '18 Jul 2022', 25, 'techops')
    # bs_methods.build_reds(token, 'premal.patel@arcticwolf.com', '18 Jul 2022', 25, 'techops')

    # bs_methods.delete_all_shifts_for_user(token, datetime.datetime(2022,7,19).astimezone(pytz.timezone('UTC')),bs_methods.get_user_id_from_email(token, 'colin.mcallister@arcticwolf.com'))

    # print(bs_methods.get_all_sites(token))

    bs_methods.delete_open_shifts(token)

    end_time = time.perf_counter()
    print('Time: ' + str(end_time - start_time))

if __name__ == "__main__":
    main()