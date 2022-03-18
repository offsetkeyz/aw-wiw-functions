
from datetime import datetime


class shift:
    shift_id = 0
    account_id = 0
    user_id = 0
    location_id = 0
    position_id = 0
    site_id = 0
    start_time = datetime(1,1,1)
    end_time = datetime(1,1,1)
    is_shared = False
    linked_users = []
    actionable = False
    block_id = 0

    def __init__(self, shift_id, account_id, user_id, location_id, position_id, site_id, start_time, end_time, is_shared, linked_users, actionable, block_id) -> None:
        self.shift_id = shift_id
        self.account_id=account_id
        self.user_id=user_id
        self.location_id=location_id
        self.position_id=position_id
        self.site_id=site_id
        self.start_time=start_time
        self.end_time=end_time
        self.is_shared=is_shared
        self.linked_users=linked_users
        self.actionable=actionable
        self.block_id=block_id

class user:
        first_name = ''
        last_name = ''
        email = ''
        employee_id = 0
        positions = []

        def __init__(self, first_name, last_name, email, employee_id, position) -> None:
            self.first_name=first_name
            self.last_name=last_name
            self.email=email
            self.position = position



            if employee_id == '':
                    self.employee_id = 0
            else:
                self.employee_id=employee_id

        def __repr__(self) -> str:
                all_positions = {10470912 : 'Triage Sec Eng 1', 10471903:'Triage Sec Analyst', 10471919:'Triage Sec Eng 2', 10474041:'Triage Sec Eng 3', 10477571:'Network Ops Supp Analyst', 10477572:'Manager, iSOC', 10486791:'TSE4', 10652403:'ISOC Intern', 10652404:'EMEA Intern', 10486791:'Triage Sec Eng 4', 10470912:'Triage Sec Engineer 1', 10656558:'unknown', 10654095:'USA', 10654096:'CAN'}

                output = str(self.first_name) + ' ' + str(self.last_name) + ': ' + str(self.employee_id)
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

def get_frontline_schedule(rotation_char):

        blue_notes_1 = "Oldest to Newest. --- Flex Start between 8 - 12 Local Time. The shift is scheduled for 12EST, but clock in anytime before that."
        blue_notes_2 = "Newest to Oldest. --- Flex Start between 8 - 12 Local Time. The shift is scheduled for 12EST, but clock in anytime before that."
        dark_blue_notes = ""
        yellow_notes = "Responsible for Entry Triage"
        purple_notes = "Responsible for Entry Triage"
        night_notes = ""
        red_notes = ""
        green_notes = "Backup coverage for Triage Team. Log Source Disappeared. Day Old Board."

        frontline_a = {
                1: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                2: [["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                3: [["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 3, yellow_notes]],
                4: [["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 4, purple_notes]],
                5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 8, night_notes]],
                6: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 3, night_notes]],
                # Starts on a Thursday and goes into the weekend. Has the Monday off.
                7: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1], ["red", 13, 12, 1, red_notes], ["red", 13, 12, 2, red_notes]],
                8: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                9: [["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 3, dark_blue_notes]],
                10: [["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 3, green_notes]]
        }

        frontline_b = {
                1: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 3, blue_notes_1]],
                2: [["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                3: [["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 1, yellow_notes],["orange", 17, 8, 3, yellow_notes]],
                4: [["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 1, purple_notes],["purple", 13, 8, 4, purple_notes]],
                5: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 8, night_notes]],
                6: [["gray", 1, 12, 1, night_notes],["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 1, night_notes], ["gray", 1, 12, 3, night_notes]],
                # Starts on a Thursday and goes into the weekend. Has the Tuesday off.
                7: [["light blue", 17, 8, 1, blue_notes_1],["light blue", 17, 8, 1, blue_notes_1], ["red", 13, 12, 1, red_notes], ["red", 13, 12, 1, red_notes]],
                8: [["light blue", 17, 8, 2, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 1, blue_notes_2],["light blue", 17, 8, 3, blue_notes_2]],
                9: [["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 1, dark_blue_notes],["dark blue", 17, 8, 3, dark_blue_notes]],
                10: [["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 1, green_notes],["green", 17, 8, 3, green_notes]]
        }

        current_schedule = frontline_a



        if rotation_char == 'b':
                current_schedule = frontline_b



        return current_schedule

def get_techops_schedule(rotation_char):

        schedule = []
        current_schedule = techops_a

        if rotation_char == 'b':
                current_schedule = techops_b

        techops_a = {
            1: [["teal", 17, 8, 1, "notes"],["teal", 17, 8, 1, "notes"], 
                    ["teal", 17, 8, 1, "notes"], ["teal", 17, 8, 1, "notes"], 
                    ["teal", 17, 8, 3, "notes"]],
            2: [["purple", 14, 8, 1, "notes"],["purple", 14, 8, 1, "notes"], 
                    ["purple", 14, 8, 1, "notes"], ["purple", 14, 8, 1, "notes"], 
                    ["purple", 14, 8, 3, "notes"]],
            3: [["green", 16, 8, 1, "notes"],["green", 16, 8, 1, "notes"], 
                    ["green", 16, 8, 1, "notes"], ["green", 16, 8, 1, "notes"], 
                    ["green", 16, 8, 3, "notes"]],
            4: [["red", 13, 8, 1, "notes"],["red", 13, 8, 1, "notes"], 
                    ["red", 13, 8, 1, "notes"], ["red", 13, 8, 1, "notes"], 
                    ["red", 13, 8, 4, "notes"]],
            5: [["gray", 1, 12, 1, "notes"],["gray", 1, 12, 1, "notes"], 
                    ["gray", 1, 12, 8, "notes"]],
            6: [["gray", 1, 12, 1, "notes"],["gray", 1, 12, 1, "notes"], 
                    ["gray", 1, 12, 1, "notes"], ["gray", 1, 12, 4, "notes"]],
            7: [["orange", 15, 8, 1, "notes"],["blue", 13, 12, 1, "notes"], 
                    ["blue", 13, 12, 2, "notes"]],
            8: [["orange", 15, 8, 1, "notes"],["orange", 15, 8, 1, "notes"], 
                    ["orange", 15, 8, 1, "notes"], ["orange", 15, 8, 3, "notes"]],
            9: [["orange", 15, 8, 1, "notes"],["orange", 15, 8, 1, "notes"], 
                    ["orange", 15, 8, 1, "notes"], ["orange", 15, 8, 1, "notes"],["orange", 15, 8, 3, "notes"]]
        }

        techops_b = {
            1: [["teal", 17, 8, 1, "notes"],["teal", 17, 8, 1, "notes"], 
                    ["teal", 17, 8, 1, "notes"], ["teal", 17, 8, 1, "notes"], 
                    ["teal", 17, 8, 3, "notes"]],
            2: [["purple", 14, 8, 1, "notes"],["purple", 14, 8, 1, "notes"], 
                    ["purple", 14, 8, 1, "notes"], ["purple", 14, 8, 1, "notes"], 
                    ["purple", 14, 8, 3, "notes"]],
            3: [["green", 16, 8, 1, "notes"],["green", 16, 8, 1, "notes"], 
                    ["green", 16, 8, 1, "notes"], ["green", 16, 8, 1, "notes"], 
                    ["green", 16, 8, 3, "notes"]],
            4: [["red", 13, 8, 1, "notes"],["red", 13, 8, 1, "notes"], 
                    ["red", 13, 8, 1, "notes"], ["red", 13, 8, 1, "notes"], 
                    ["red", 13, 8, 4, "notes"]],
            5: [["gray", 1, 12, 1, "notes"],["gray", 1, 12, 1, "notes"], 
                    ["gray", 1, 12, 8, "notes"]],
            6: [["gray", 1, 12, 1, "notes"],["gray", 1, 12, 1, "notes"], 
                    ["gray", 1, 12, 1, "notes"], ["gray", 1, 12, 4, "notes"]],
            7: [["orange", 15, 8, 1, "notes"],["blue", 13, 12, 1, "notes"], 
                    ["blue", 13, 12, 1, "notes"]],
            8: [["orange", 15, 8, 2, "notes"],["orange", 15, 8, 1, "notes"], 
                    ["orange", 15, 8, 1, "notes"], ["orange", 15, 8, 3, "notes"]],
            9: [["orange", 15, 8, 1, "notes"],["orange", 15, 8, 1, "notes"], 
                    ["orange", 15, 8, 1, "notes"], ["orange", 15, 8, 1, "notes"],["orange", 15, 8, 3, "notes"]]
        }

        return current_schedule


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
            9: [["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 1, light_blue_notes], 
                    ["light blue", 15, 8, 1, light_blue_notes], ["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 3, light_blue_notes]],
            10: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes], 
                    ["green", 14, 8, 1, green_notes], ["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]]
        }

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
            9: [["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 1, light_blue_notes], 
                    ["light blue", 15, 8, 1, light_blue_notes], ["light blue", 15, 8, 1, light_blue_notes],["light blue", 15, 8, 3, light_blue_notes]],
            10: [["green", 14, 8, 1, green_notes],["green", 14, 8, 1, green_notes], 
                    ["green", 14, 8, 1, green_notes], ["green", 14, 8, 1, green_notes],["green", 14, 8, 3, green_notes]]
        }
        if rotation_char == 'a':
                return tse3_schedule_a
        elif rotation_char == 'b':
                return tse3_schedule_b
        else:
                return tse3_schedule_c

        
def get_emea_schedule(rotation_char):
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

def get_pink(rotation_char):
        pink_notes = ''
        pink_emea = {
                1: [["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 3, pink_notes]],
                2: [["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 3, pink_notes]],
                3: [["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 1, pink_notes],["pink", 9, 8, 3, pink_notes]]
        }

        return pink_emea




def get_current_schedule(schedule_name, rotation_char):
    if schedule_name == "5132412":
        return get_techops_schedule(rotation_char)
    elif schedule_name == "5134192":
        return get_tse3_schedule(rotation_char)
    elif schedule_name == "5189759":
        return get_tse3_schedule(rotation_char)
    elif schedule_name == "5227330":
        return get_emea_schedule(rotation_char)
    elif schedule_name == "5129876":
        return get_pink(rotation_char)
    elif schedule_name == "5132409":
        return get_frontline_schedule(rotation_char)
    else:
        print('error with get_current_schedule in shift_classes.py')

def get_color_code(color):
    shift_color="ff98ff"    
    if color == "red":
        shift_color = "eb3223"
    elif color == "blue":
        shift_color = "4E73BE"
    elif color == "purple":
        shift_color = "8d3ab9"
    elif color == "orange":
        shift_color = "f6c242"
    elif color == "teal":
        shift_color = "93efdb"
    elif color == "green":
        shift_color = "42a611"
    elif color == "gray":
        shift_color = "a6a6a6"
    elif color == "yellow":
        shift_color = "ffff00"
    elif color == "light blue":
        shift_color = "00b0f0"
    elif color == "dark blue":
        shift_color = "0070c0"
    elif color == "pink":
        shift_color = "ff00dd"
    elif color == "orange":
        shift_color = "ffaa00"

    return shift_color


def get_location_id(schedule_name):
    schedule_name = schedule_name.lower().strip()
    schedules = {
        "default" : "5129876",
        "tse1" : "5132409",
        "tse2" : "5132410",
        "tse3" : "5134192",
        "techops" : "5132412",
        "colin test" : "5189759",
        "emea tier 1" : "5227330"
    }