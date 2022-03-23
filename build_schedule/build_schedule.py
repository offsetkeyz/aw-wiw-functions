__author__ = "Colin McAllister"

import bs_methods

# default file locations. request access from Colin McAllister
tse3_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/tse3.csv'
tse2_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/tse2.csv'
tse1_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/tse1.csv'
emea_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/emea.csv'
emea_t3_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/emea_t3.csv'
techops_employee_list = '/Users/colin.mcallister/OneDrive - Arctic Wolf Networks Inc/Documents/techops.csv'

# replace the contents of the parenthesis with the file location
for x in bs_methods.get_employee_list('sample.csv'):
    bs_methods.build_schedule(x[0], x[1], x[2], x[3], x[4], x[5])