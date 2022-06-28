# aw-wiw-functions
This ReadMe provides depracated instructions on how to download and run the code. This project has evolved and has not been maintained for basic usage by external parties.

____
# DEPRECATED
### How to use build_schedule.py
1. Open the file in VS code
2. At the bottom of the file, inside the parenthesis of `get_employee_list()`, replace the contents with the location of the file. A sample file has been provided to you in the repo directory.
3. Once the file is formatted and saved, you can run the code.
4. Enter the password for the service account and the API key (both found in LastPass).
5. Keep an eye out for errors.

This process takes about 1 minute per user.

#### Format the CSV
There are notes in the sample CSV about how to format it, but let me go into a bit more depth.
Each line should look like this:
  `email@arcticwolf.com, 30 Feb 2021, tse1, 1b, 0, 0`
  
  Parameters:
  1. **Email address.**
  2. **Start date of the first shift in UTC.** This can get a little bit complicated for rotating nights and weekend shifts. You will have to reference the `shift_classes.py` file for the schedules. The schedules are stored in dictionary format with the keys being the week numbers and the values being an array of shifts.
     - A users first shift must fall on the first shift in the dictionary. 
       - ![image](https://user-images.githubusercontent.com/25734824/159770687-a924747d-2efd-4034-a338-4f6e70a08d61.png)
     - In the above case, the scheduler will built out 5 light blue shifts in a row, starting on the daate entered here (UTC)
       - if the date entered is a Tuesday, they will be scheduled Tuesday, through Saturday, and **their whole schedule will be off by one day.**
     - If the user is starting on a night shift, you will have to enter the start date of the first night shift.
       - REMEMBER that night shifts start the following day in UTC.
       - So, if a night shift starts at 8p EST on 11 Mar 2022, then you need to enter 12 Mar 2022 as the start date.
  3. **Schedule Name.** Accepted names are the following:
     - default
     - tse1
     - tse2
     - tse3
     - techops
     - emea tier 1
     - emea tier 3
  4. **Starting Week and Rotation Character** 
     - Choose which week number the user's schedule will start on (based on the tables in `shift_classes.py`
     - The rotation char is used differently by each team. 
       - for tier1, it is used to rotate if the user has monday (a) or tuesday (b) off in their rotation
       - for tier2 and tier3, it is used to rotate through boards and other tasks, as well as if they have monday (a) or tuesday (b) off in their rotation.
  5. **Rotation Int**
     - This is used to determine if the team will rotate between a/b schedules or a/b/c schedules
       - This feature is only used for tier2 and above. **For tier 1, please put 2** 
  8. **Team Number** If used, this will add a job site filter to each shift so that users can quickly filter on team numbers.
     - If this is not needed, please put 0.
