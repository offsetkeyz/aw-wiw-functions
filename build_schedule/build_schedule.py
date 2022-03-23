__author__ = "Colin McAllister"

import bs_methods

# replace the contents of the parenthesis with the file location
for x in bs_methods.get_employee_list('sample.csv'):
    bs_methods.build_schedule(x[0], x[1], x[2], x[3], x[4], x[5])