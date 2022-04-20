
from datetime import datetime

class time_off_request:
        # to_id = 0
        # account_id = 0
        # user_id = 0
        status = 0
        type = 0
        type_id = 0
        hours = 0
        start_time = 0
        end_time = 0
        cancelled_by = 0
        user_status = 0
        type_label = ''

        def __init__(self, to_id=0, account_id=0, user_id=0, status=0, type=0, type_id=0, hours=0, start_time=0, end_time=0, cancelled_by=0, user_status=0, type_label='') -> None:
            self.to_id=to_id
            self.accoun_id=account_id
            self.user_id=user_id
            self.status=status
            self.type=type
            self.type_id=type_id
            self.hours=hours
            self.start_time=start_time
            self.end_time=end_time
            self.cancelled_by=cancelled_by
            self.user_status+user_status
            self.type_label=type_label


class shift:
    shift_id = 0
    account_id = 0
    user_id = 0
    location_id = 0
    position_id = 0
    site_id = 0
    start_time = datetime(1,1,1)
    end_time = datetime(1,1,1)
    length = 0
    published = False
    acknowledged = False
    notes = ''
    color = ''
    is_open = False

    def __init__(self, shift_id, account_id, user_id, location_id, position_id, site_id, start_time, end_time, published, acknowledged, notes, color, is_open) -> None:
        self.shift_id = shift_id
        self.account_id=account_id
        self.user_id=user_id
        self.location_id=location_id
        self.position_id=position_id
        self.site_id=site_id
        self.start_time=start_time
        self.end_time=end_time
        self.published=published
        self.acknowledged=acknowledged
        self.notes=notes
        self.color=color
        self.acknowledged=acknowledged
        self.is_open=is_open

        length_in_seconds = end_time - start_time
        self.length = length_in_seconds.seconds / 3600

class user:
        first_name = ''
        last_name = ''
        full_name = ''
        email = ''
        wiw_employee_id = 0
        positions = []
        role = 3 #only add to schedule if role = 3
        locations = [] #schedules
        is_hidden = False #only add to schedule if False
        is_active = True
        

        def __init__(self, first_name, last_name, email, wiw_employee_id, positions, role, locations, is_hidden, is_active) -> None:
            self.first_name=first_name
            self.last_name=last_name
            self.email=email
            self.positions=positions
            self.role = role
            self.locations = locations
            self.is_hidden = is_hidden
            self.is_active = is_active
            self.full_name = str(first_name) + ' ' + str(last_name)



            if wiw_employee_id == '':
                    self.wiw_employee_id = 0
            else:
                self.wiw_employee_id=int(wiw_employee_id)

        def __repr__(self) -> str:
                all_positions = {'Triage Sec Eng 1': 10470912, 'Triage Sec Analyst': 10470912, 'Triage Sec Eng 2': 10471919, 'Triage Sec Eng 3': 10474041, 'Network Ops Supp Analyst': 10477571, 'Manager, iSOC': 10477572, 'TSE4': 10486791, 'ISOC Intern': 10652403, 'EMEA Intern': 10652404, 'Triage Sec Eng 4': 10486791, 'Triage Sec Engineer 1' : 10470912, 'USA': 10654095, 'CAN': 10654096, 'DEU' : 10665016, 'GBR' : 10665016, 'Dir Business Apps Sr': 10477570, 'Co-op/ Intern':10652403, 'Tech Lead Security Svs':10474045, 'Shift Lead Security Oper':10660927, 'Team Lead Security Ops':10474045,'Concierge Sec Eng 2':10668570, 'Mgr Security Ops Sr.':10668568, 'Team Lead Tech Ops':10477572,'Mgr Security Operations':10477572, 'Mgr Concierge Services':10477572,'Mgr, Security Operations':10477572, 'Triage Business Analyst':10668571,'Concierge Sec Eng 3':10665015,'Business Sys Mgr':10477572,'Dir Security Oper Sr':10477570,'Dir Security Svs':10477570}

                output = str(self.first_name) + ' ' + str(self.last_name) + ': ' + str(self.wiw_employee_id)
                for i in self.position:
                        try:
                                output = str(output + " " + all_positions.get(i))
                        except:
                                break
                return output

class employee_for_pay:
    name = ""
    night_hours = 0
    weekend_hours = 0
    meals = 0
    overtime = 0
    row = 0
    week1_hours = 0
    week2_hours = 0
    shifts_worked = {}
    stat_hours = 0
    employee_id = 0


    def __init__(self, name, night_hours, weekend_hours, meals, overtime, row, shifts_worked, stat_hours_in, employee_id):
        self.name = name
        self.night_hours = night_hours
        self.weekend_hours = weekend_hours
        self.meals = meals
        self.overtime = overtime
        self.row = row
        self.shifts_worked = shifts_worked
        self.stat_hours = stat_hours_in
        self.employee_id = employee_id


#################################### Schedules ########################################
# Format: color, start time, length, days until next shift, notes



def get_frontline_schedule(rotation_char):

        blue_notes_1 = "Oldest to Newest. --- Flex Start between 8 - 12 Local Time. The shift is scheduled for 12EST, but clock in anytime before that."
        blue_notes_2 = "Newest to Oldest. --- Flex Start between 8 - 12 Local Time. The shift is scheduled for 12EST, but clock in anytime before that."
        dark_blue_notes_1 = "Oldest to Newest. Late Start."
        dark_blue_notes_2 = "Newest to Oldest. Late Start."
        yellow_notes = "Responsible for Entry Triage"
        purple_notes = "Responsible for Entry Triage"
        night_notes = ""
        red_notes = ""
        green_notes = "Backup coverage for Triage Team. Log Source Disappeared. Day Old Board."

        frontline_a = { # Format: color, start time, length, days until next shift, notes
                1: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                2: [["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                3: [["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 3, yellow_notes]],
                4: [["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 4, purple_notes]],
                5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 8, night_notes]],
                6: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 3, night_notes]],
                # Starts on a Thursday and goes into the weekend. Has the Monday off.
                7: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1], ["red", 13, 12, 1, red_notes]],
                8: [["red", 13, 12, 2, red_notes],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                9: [["dark blue", 17, 8, 1, dark_blue_notes_1],["dark blue", 17, 8, 1, dark_blue_notes_1],["dark blue", 17, 8, 1, dark_blue_notes_1],["dark blue", 17, 8, 1, dark_blue_notes_1],["dark blue", 17, 8, 3, dark_blue_notes_1]],
                10: [["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 3, green_notes]]
        }

        frontline_b = { # Format: color, start time, length, days until next shift, notes
                1: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                2: [["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                3: [["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 3, yellow_notes]],
                4: [["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 4, purple_notes]],
                5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 8, night_notes]],
                6: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 3, night_notes]],
                # Starts on a Thursday and goes into the weekend. Has the Tuesday off.
                7: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1], ["red", 13, 12, 1, red_notes]],
                8: [["red", 13, 12, 1, red_notes],["light blue", 17, 8, 2, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                9: [["dark blue", 17, 8, 1, dark_blue_notes_2],["dark blue", 17, 8, 1, dark_blue_notes_2],["dark blue", 17, 8, 1, dark_blue_notes_2],["dark blue", 17, 8, 1, dark_blue_notes_2],["dark blue", 17, 8, 3, dark_blue_notes_2]],
                10: [["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 3, green_notes]]
        }

        if rotation_char == 'b':
                return frontline_b
        return frontline_a

def get_tse2_schedule(rotation_char):
        all_notes = get_tse2_notes()
        orange_notes = all_notes['orange_notes']
        red_notes = all_notes['red_notes']
        green_notes= all_notes['green_notes']
        teal_notes= all_notes['teal_notes']
        night_and_weekend_notes= all_notes['night_and_weekend_notes']
        purple_notes= all_notes['purple_notes']

        tse2_a = { # has monday off rotation
                1: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]],
                2: [['orange', 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 4, orange_notes]],
                3: [["gray", 1, 12, 1, night_and_weekend_notes],["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 8, night_and_weekend_notes]],
                4: [["gray", 1, 12, 1, night_and_weekend_notes],["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 4, night_and_weekend_notes]],
                5: [["purple", 15, 8, 1, purple_notes],["blue", 13, 12, 1, night_and_weekend_notes]],
                6: [["blue", 13, 12, 2, night_and_weekend_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 3, purple_notes]],
                7: [["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 3, red_notes]],
                8: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]],
                9: [["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 3, teal_notes]],
                10: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 3, purple_notes]]
        }

        tse2_b = {# tuesday off rotation
                1: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]],
                2: [['orange', 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 1, orange_notes],["orange", 17, 8, 4, orange_notes]],
                3: [["gray", 1, 12, 1, night_and_weekend_notes],["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 8, night_and_weekend_notes]],
                4: [["gray", 1, 12, 1, night_and_weekend_notes],["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 1, night_and_weekend_notes], ["gray", 1, 12, 4, night_and_weekend_notes]],
                5: [["purple", 15, 8, 1, purple_notes],["blue", 13, 12, 1, night_and_weekend_notes]],
                6: [["blue", 13, 12, 1, night_and_weekend_notes],["purple", 15, 8, 2, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 3, purple_notes]],
                7: [["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 1, red_notes],["red", 15, 8, 3, red_notes]],
                8: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]],
                9: [["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 1, teal_notes],["teal", 13, 8, 3, teal_notes]],
                10: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 3, purple_notes]]
        }

        if rotation_char == 'b':
                return tse2_b
        return tse2_a

def get_tse2_notes():
        notes = {        
                'teal_notes' : """8am - 12pm EST - Incident Triage as scheduled in PagerDuty.
                12-4pm - Lunch/Breaks/Assist where needed.
                Open/Pending Tier 2 ticket work Zendesk.        
                """,
                'red_notes': '''
                10 am-12 pm EST - Assist where needed/Breaks/Ticket work
                12 pm-4pm EST - Incident Triage as scheduled in PagerDuty
                4 pm-6 pm EST - Assist where needed/Breaks/Ticket work
                ''',
                'orange_notes': '''
                12pm - 4pm EST - Lunch/Break/Assist where needed/ Ticket work
                4 pm - 8 pm EST - Incident Triage as scheduled in PagerDuty
                ''',
                'purple_notes': '''
                2 hours working on SCCS requests
                Entry/ Ticket work Tier 2 open&Pending          
                ''',
                'night_and_weekend_notes': '''
                * Incident triage as scheduled with team
                * Ticket work
                * Hourly checks on AC/EMEA boards
                ''',
                'green_notes': '''
                Main priority - Ticket work Tier 2 open&Pending
                Main Priority #2 - Supporting Tier 3 Security investigation
                Shadow sessions/Training new hires
                Assist where needed (e.g. SCCS, Entry)
                '''
                }
        return notes

        
        
        

def get_EMEA_tier3(rotation_char):
        yellow_notes = "AC Board Coverage 11a-5pm Frankfurt Time"
        orange_notes = "AC Board Coverage 8a-11a Frankfurt Time"
        teal_notes = "AC Board Coverage 5p-8p Frankfurt Time"
        purple_notes = "No Board Coverage"

        emea_t3_a = { 
                1: [["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 3, purple_notes]],
                2: [["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 3, purple_notes]],
                3: [["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 3, purple_notes]],
                4: [["orange", 7, 8, 1, orange_notes],["orange", 7, 8, 1, orange_notes],["orange", 7, 8, 1, orange_notes],["orange", 7, 8, 1, orange_notes],["orange", 7, 8, 3, orange_notes]]
        }

        emea_t3_b = { 
                1: [["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 3, yellow_notes]],
                2: [["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 3, yellow_notes]],
                3: [["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 3, yellow_notes]],
                4: [["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 1, yellow_notes],["yellow", 8, 8, 3, yellow_notes]]
        }

        emea_t3_c = {
                1: [["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 3, purple_notes]],
                2: [["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 1, purple_notes],["purple", 8, 8, 3, purple_notes]],
                3: [["teal", 11, 8, 1, teal_notes],["teal", 11, 8, 1, teal_notes],["teal", 11, 8, 1, teal_notes],["teal", 11, 8, 1, teal_notes],["teal", 11, 8, 3, teal_notes]]
        }

        if rotation_char == 'b':
                return emea_t3_b
        elif rotation_char == 'c':
                return emea_t3_c
        return emea_t3_a

def get_tse3_schedule(rotation_char):
        teal_a_notes = "CFE Alpha Board 16:00 - 20:00 EST and Miss Investigations"
        teal_b_notes = "CFE Bravo Board 16:00 - 20:00 EST and DTR"
        teal_c_notes = "CFE Charlie Board 16:00 - 20:00 EST and Flex Shift (Surge support for Miss Investigations, DTR, Security Investigations)"
        yellow_a_notes = "CFE Alpha Board 12:00 - 16:00 EST  and PenTest Board"
        yellow_b_notes = "CFE Bravo Board 12:00 - 16:00 EST and SCCS"
        yellow_c_notes = "CFE Charlie Board 12:00 - 16:00 EST and Flex Shift (Surge support for PenTest Board, SCCS, Security Investigations)"
        orange_a_notes = "CFE Alpha Board 8-12 EST. Project Shift (Beta testing tools, automation, Surge support for SCCS, etc)"
        orange_b_notes = "CFE Bravo Board 8-12 EST. Project Shift (Beta testing tools, automation, Surge support for SCCS, etc)"
        orange_c_notes = "CFE Charlie Board 8-12 EST. Project Shift (Beta testing tools, automation, Surge support for SCCS, etc)"
        green_notes = "On-Call After Hours. Security Investigations and Projects"
        purple_notes = 'Security Investigations'
        light_blue_notes = 'Security Investigations / Projects'
        red_notes = "Split Combined Board amongst team members. Flex Shift (Security Investigations, SCCS, PenTest Board)"
        night_notes = "Split Combined Board amongst team members. Flex Shift (Security Investigations, SCCS, PenTest Board)"
        
# Format: color, start time, length, days until next shift, notes
        tse3_schedule_a = {
            1: [["teal", 17, 8, 1, teal_a_notes],["teal", 17, 8, 1, teal_a_notes], 
                    ["teal", 17, 8, 1, teal_a_notes], ["teal", 17, 8, 1, teal_a_notes], 
                    ["teal", 17, 8, 3, teal_a_notes]],
            2: [["yellow", 15, 8, 1, yellow_a_notes],["yellow", 15, 8, 1, yellow_a_notes], 
                    ["yellow", 15, 8, 1, yellow_a_notes], ["yellow", 15, 8, 1, yellow_a_notes], 
                    ["yellow", 15, 8, 3, yellow_a_notes]],
            3: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 1, purple_notes], ["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            4: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 8, night_notes]],
            5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 4, night_notes]],
            6: [["purple", 15, 8, 1, purple_notes],["red", 13, 12, 1, red_notes], 
                    ["red", 13, 12, 2, red_notes]],
            7: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            8: [["orange", 13, 8, 1, orange_a_notes],["orange", 13, 8, 1, orange_a_notes], 
                    ["orange", 13, 8, 1, orange_a_notes], ["orange", 13, 8, 1, orange_a_notes],["orange", 13, 8, 3, orange_a_notes]],
            9: [["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 1, light_blue_notes], 
                    ["light blue", 15, 8, 1, light_blue_notes], ["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 3, light_blue_notes]],
            10: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes], 
                    ["green", 14, 8, 1, green_notes], ["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]]
        }
# Format: color, start time, length, days until next shift, notes
        tse3_schedule_b = {
            1: [["teal", 17, 8, 1, teal_b_notes],["teal", 17, 8, 1, teal_b_notes], 
                    ["teal", 17, 8, 1, teal_b_notes], ["teal", 17, 8, 1, teal_b_notes], 
                    ["teal", 17, 8, 3, teal_b_notes]],
            2: [["yellow", 15, 8, 1, yellow_b_notes],["yellow", 15, 8, 1, yellow_b_notes], 
                    ["yellow", 15, 8, 1, yellow_b_notes], ["yellow", 15, 8, 1, yellow_b_notes], 
                    ["yellow", 15, 8, 3, yellow_b_notes]],
            3: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 1, purple_notes], ["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            4: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 8, night_notes]],
            5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 4, night_notes]],
            6: [["purple", 15, 8, 1, purple_notes],["red", 13, 12, 1, red_notes], 
                    ["red", 13, 12, 1, red_notes]],
            7: [["purple", 15, 8, 2, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            8: [["orange", 13, 8, 1, orange_b_notes],["orange", 13, 8, 1, orange_b_notes], 
                    ["orange", 13, 8, 1, orange_b_notes], ["orange", 13, 8, 1, orange_b_notes],["orange", 13, 8, 3, orange_b_notes]],
            9: [["light blue", 17, 8, 1, light_blue_notes],["light blue", 17, 8, 1, light_blue_notes], 
                    ["light blue", 17, 8, 1, light_blue_notes], ["light blue", 17, 8, 1, light_blue_notes],["light blue", 17, 8, 3, light_blue_notes]],
            10: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes], 
                    ["green", 14, 8, 1, green_notes], ["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]]
        }
# Format: color, start time, length, days until next shift, notes
        tse3_schedule_c = {
            1: [["teal", 17, 8, 1, teal_c_notes],["teal", 17, 8, 1, teal_c_notes], 
                    ["teal", 17, 8, 1, teal_c_notes], ["teal", 17, 8, 1, teal_c_notes], 
                    ["teal", 17, 8, 3, teal_c_notes]],
            2: [["yellow", 15, 8, 1, yellow_c_notes],["yellow", 15, 8, 1, yellow_c_notes], 
                    ["yellow", 15, 8, 1, yellow_c_notes], ["yellow", 15, 8, 1, yellow_c_notes], 
                    ["yellow", 15, 8, 3, yellow_c_notes]],
            3: [["purple", 15, 8, 1, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 1, purple_notes], ["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            4: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 8, night_notes]],
            5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], 
                    ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 4, night_notes]],
            6: [["purple", 15, 8, 1, purple_notes],["red", 13, 12, 1, red_notes], 
                    ["red", 13, 12, 1, red_notes]],
            7: [["purple", 15, 8, 2, purple_notes],["purple", 15, 8, 1, purple_notes], 
                    ["purple", 15, 8, 4, purple_notes]],
            8: [["orange", 13, 8, 1, orange_c_notes],["orange", 13, 8, 1, orange_c_notes], 
                    ["orange", 13, 8, 1, orange_c_notes], ["orange", 13, 8, 1, orange_c_notes],["orange", 13, 8, 3, orange_c_notes]],
            9: [["light blue", 17, 8, 1, light_blue_notes],["light blue", 17, 8, 1, light_blue_notes], 
                    ["light blue", 17, 8, 1, light_blue_notes], ["light blue", 17, 8, 1, light_blue_notes],["light blue", 17, 8, 3, light_blue_notes]],
            10: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes], 
                    ["green", 14, 8, 1, green_notes], ["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]]
        }
        if rotation_char == 'a':
                return tse3_schedule_a
        elif rotation_char == 'b':
                return tse3_schedule_b
        return tse3_schedule_c

        
def get_emea_t1_schedule(rotation_char):
        purple_notes = ''
        green_notes =''
        yellow_notes = ''
        teal_notes = ''
        blue_notes = ''
        emea_a = { # purple, green, yellow, teal, purple, weekend, purple
                1: [["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 3, purple_notes]],
                2: [["green", 7, 8, 1, green_notes],["green", 7, 8, 1, green_notes],["green", 7, 8, 1, green_notes],["green", 7, 8, 1, green_notes],["green", 7, 8, 3, green_notes]],
                3: [["yellow", 15, 8, 1, yellow_notes],["yellow", 15, 8, 1, yellow_notes],["yellow", 15, 8, 1, yellow_notes],["yellow", 15, 8, 1, yellow_notes],["yellow", 15, 8, 2, yellow_notes]],
                4: [["teal", 23, 8, 1, teal_notes],["teal", 23, 8, 1, teal_notes],["teal", 23, 8, 1, teal_notes],["teal", 23, 8, 1, teal_notes],["teal", 23, 8, 5, teal_notes]],
                5: [["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 2, purple_notes],["blue", 7, 12, 1, blue_notes],["blue", 7, 12, 1, blue_notes]],
                6: [["purple", 9, 8, 3, purple_notes],["purple", 9, 8, 1, purple_notes],["purple", 9, 8, 3, purple_notes]]
        }

        return emea_a

def get_techops_schedule(rotation_char): #TODO finish this. In production.
        teal_notes = ''
        green_notes = ''
        red_notes = ''
        gray_notes = ''
        orange_notes = ''

        techops_a = {
            1: [["teal", 17, 8, 1, teal_notes],["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 1, teal_notes], ["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 3, teal_notes]],
            2: [["teal", 17, 8, 1, teal_notes],["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 1, teal_notes], ["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 3, teal_notes]],
            3: [["green", 16, 8, 1, green_notes],["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 1, green_notes], ["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 3, green_notes]],
            4: [["green", 16, 8, 1, green_notes],["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 1, green_notes], ["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 3, green_notes]],
            5: [["red", 13, 8, 1, red_notes],["red", 13, 8, 1, red_notes], 
                    ["red", 13, 8, 1, red_notes], ["red", 13, 8, 1, red_notes], 
                    ["red", 13, 8, 4, red_notes]],
            6: [["gray", 1, 12, 1, gray_notes],["gray", 1, 12, 1, gray_notes], 
                    ["gray", 1, 12, 8, gray_notes]],
            7: [["gray", 1, 12, 1, gray_notes],["gray", 1, 12, 1, gray_notes], 
                    ["gray", 1, 12, 1, gray_notes], ["gray", 1, 12, 4, gray_notes]],
            8: [["orange", 15, 8, 1, orange_notes],["blue", 13, 12, 1, orange_notes], 
                    ],
            9: [["blue", 13, 12, 2, orange_notes], ["orange", 15, 8, 1, orange_notes],["orange", 15, 8, 1, orange_notes], 
                    ["orange", 15, 8, 1, orange_notes], ["orange", 15, 8, 3, orange_notes]],
            10: [["orange", 15, 8, 1, orange_notes],["orange", 15, 8, 1, orange_notes], 
                    ["orange", 15, 8, 1, orange_notes], ["orange", 15, 8, 1, orange_notes],["orange", 15, 8, 3, orange_notes]]
        }

        techops_b = {
            1: [["teal", 17, 8, 1, teal_notes],["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 1, teal_notes], ["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 3, teal_notes]],
            2: [["teal", 17, 8, 1, teal_notes],["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 1, teal_notes], ["teal", 17, 8, 1, teal_notes], 
                    ["teal", 17, 8, 3, teal_notes]],
            3: [["green", 16, 8, 1, green_notes],["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 1, green_notes], ["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 3, green_notes]],
            4: [["green", 16, 8, 1, green_notes],["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 1, green_notes], ["green", 16, 8, 1, green_notes], 
                    ["green", 16, 8, 3, green_notes]],
            5: [["red", 13, 8, 1, red_notes],["red", 13, 8, 1, red_notes], 
                    ["red", 13, 8, 1, red_notes], ["red", 13, 8, 1, red_notes], 
                    ["red", 13, 8, 4, red_notes]],
            6: [["gray", 1, 12, 1, gray_notes],["gray", 1, 12, 1, gray_notes], 
                    ["gray", 1, 12, 8, gray_notes]],
            7: [["gray", 1, 12, 1, gray_notes],["gray", 1, 12, 1, gray_notes], 
                    ["gray", 1, 12, 1, gray_notes], ["gray", 1, 12, 4, gray_notes]],
            8: [["orange", 15, 8, 1, orange_notes],["blue", 13, 12, 1, orange_notes], 
                    ],
            9: [["blue", 13, 12, 1, orange_notes], ["orange", 15, 8, 2, orange_notes],["orange", 15, 8, 1, orange_notes], 
                    ["orange", 15, 8, 1, orange_notes], ["orange", 15, 8, 3, orange_notes]],
            10: [["orange", 15, 8, 1, orange_notes],["orange", 15, 8, 1, orange_notes], 
                    ["orange", 15, 8, 1, orange_notes], ["orange", 15, 8, 1, orange_notes],["orange", 15, 8, 3, orange_notes]]
        }
        current_schedule = techops_a
        if rotation_char == 'b':
                current_schedule = techops_b
        return current_schedule

def get_pink(schedule_name): #TODO Finish this.
        pink_notes = ''

        pink_NA = [["pink", 14, 8, 1, pink_notes],["pink", 14, 8, 1, pink_notes],["pink", 14, 8, 1, pink_notes],["pink", 14, 8, 1, pink_notes],["pink", 14, 8, 3, pink_notes]]
        

        pink_emea = [["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 3, pink_notes]]
        

        if schedule_name in ["5227330",'5233779']:
                return pink_emea
        else:
                return pink_NA




def get_current_schedule(schedule_name, rotation_char):
    if schedule_name == "5132412":
        return get_techops_schedule(rotation_char)
    elif schedule_name == "5134192":
        return get_tse3_schedule(rotation_char)
    elif schedule_name == "5227330":
        return get_emea_t1_schedule(rotation_char)
    elif schedule_name == "5132410":
        return get_tse2_schedule(rotation_char)
    elif schedule_name == "5129876":
        return get_pink(rotation_char)
    elif schedule_name == "5132409":
        return get_frontline_schedule(rotation_char)
    elif schedule_name == '5233779':
        return get_EMEA_tier3(rotation_char)
    else:
        print('error with get_current_schedule in shift_classes.py')

def get_color_code(color):
    shift_color = color
    if color == "red":
        shift_color = "FF0000"
    elif color == "blue" or color == "dark blue":
        shift_color = "0070c0"
    elif color == "purple":
        shift_color = "8d3ab9"
    elif color == "orange":
        shift_color = "FFC000"
    elif color == "teal":
        shift_color = "72F2DA"
    elif color == "green":
        shift_color = "42a611"
    elif color == "gray":
        shift_color = "a6a6a6"
    elif color == "yellow":
        shift_color = "ffff00"
    elif color == "light blue":
        shift_color = "00b0f0"
    elif color == "pink":
        shift_color = "ff00dd"

    return shift_color

