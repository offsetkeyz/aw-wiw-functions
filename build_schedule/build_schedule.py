__author__ = "Colin McAllister"

import time
import bs_methods

def build_schedule(token, schedule_name='tse1'):
    # replace the contents of the parenthesis with the file location
    for x in bs_methods.get_employee_starts_from_csv('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/' + str(schedule_name) + '.csv'):
        bs_methods.build_schedule(token, schedule_name, x[0], x[1], x[2], x[3], x[4])

def main():
    token = bs_methods.authenticate_WiW_API()
    start_time = time.perf_counter()
    bs_methods.delete_conflicting_shifts_for_user(bs_methods.get_user_id_from_email(token,'stephanie.legue@arcticwolf.com'),token)
    end_time = time.perf_counter()
    print('Time for user_id: ' + str(end_time - start_time))
    # build_schedule(token)

if __name__ == "__main__":
    main()