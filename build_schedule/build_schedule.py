__author__ = "Colin McAllister"

import timeit
import bs_methods

def main(schedule_name='tse1'):
    start_time = timeit.default_timer()
    token = bs_methods.authenticate_WiW_API()

    bs_methods.get_all_shifts_future_shifts(token)
    # replace the contents of the parenthesis with the file location
    for x in bs_methods.get_employee_list('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/' + str(schedule_name) + '.csv'):
        bs_methods.build_schedule(token, schedule_name, x[0], x[1], x[2], x[3], x[4])

    stop_time = timeit.default_timer()
    print('Time: ', stop_time - start_time)  

if __name__ == "__main__":
    main()