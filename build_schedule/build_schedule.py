__author__ = "Colin McAllister"

import timeit
import bs_methods

start_time = timeit.default_timer()
# replace the contents of the parenthesis with the file location
for x in bs_methods.get_employee_list('/Users/colin.mcallister/Documents/WiW API/aw-wiw-functions/build_schedule/tse1.csv'):
    bs_methods.build_schedule(x[0], x[1], x[2], x[3], x[4], x[5])

stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)  