import datetime
import csv
import os
from types import new_class

##### VARIABLES #####

follow_up_schedule = []  # A list to store schedule records

test_patients = [
    ['John', 'Campbell', '01-12-2020', '12', '2'],
    ['Merry', 'Barnett', '01-12-2020', '3', '1'],
    ['Jordan', 'Frost', '01-12-2020', '6', '2'],
    ['Linda', 'Wright', '01-12-2020', '24', '2'],
    ['Angela', 'Rogers', '01-12-2020', '0', '1'],
    ['Sarah', 'Mcnaught', '01-12-2020', '0', '1'],
]
headers_list = [
    'File_No', 'First_Name', 'Last_Name', 'Last_Visit_Date',
    'Follow_Up_Freq', 'Next_Follow_Up_Date', 'Priority'
]

today = datetime.date.today()

##### Import Saved Data #####

def clear_screen():
    '''Clears the command line interface '''

    def check_system_and_clear(): return os.system(
        'cls' if os.name in ('nt', 'dos') else 'clear')
    check_system_and_clear()

def import_from_cv():
    '''Imports saved data to follow_up_schedule'''

    file = os.getcwd() + '/Schedule.csv'
    with open(file, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            if row:
                follow_up_schedule.append(row)


##### DATA IMPORT & CLEAR SCREEN #####

import_from_cv()

clear_screen()

##### FUNCTIONS #####


def print_follow_up_schedule(follow_up_schedule=follow_up_schedule):
    '''Prints the follow_up_schedule list in a table format'''

    print('')  # New line

    # Print the follow up schedule headers
    padding = ' ' * 8
    for header in headers_list:
        print(f'\033[38;5;15;48;5;20m{header}{padding}\033[0m', end='')

    print('')  # New line

    # Print dashed line (---) seprating the headers from the rows
    print('-' * (sum([len(header)
          for header in headers_list]) + 8 * len(headers_list)))

    # Print the follow up schedule rows
    for j in range(len(follow_up_schedule)):
        for i in range(len(headers_list)):
            i_padding = ' ' * \
                ((len(headers_list[i]) + 8) -
                 len(str(follow_up_schedule[j][i])))
            print(
                f'\033[38;5;15;48;5;12m{follow_up_schedule[j][i]}{i_padding}\033[0m', end='')

        print('')  # New line


def add_patient(first_name, last_name, last_visit_date, follow_up_freq, priority, file_no=''):
    '''Adds patient to the follow_up_schedule list
    File_no is optional; it is used for editing
    All new patients get autogenerated file_no
    '''

    if not file_no:
        file_no = max(int(patient[0]) for patient in follow_up_schedule) + 1

    if ' m' not in follow_up_freq:
        follow_up_freq = follow_up_freq + ' m'

   
    # 30.4375 is the average month length in days
    next_follow_up_date = today + \
        datetime.timedelta(
            days=int(follow_up_freq.replace(' m', '')) * 30.4375)

    # Avoid placing next_follow_up_date during weekends
    i = 1
    while next_follow_up_date.weekday() in [5, 6]:
        next_follow_up_date += datetime.timedelta(days=i)
        i += 1

    next_follow_up_date = next_follow_up_date.strftime("%d-%m-%Y")

    patient_info = [first_name, last_name, last_visit_date,
                    follow_up_freq, next_follow_up_date, priority]
    patient_info = [str(file_no)] + patient_info
    follow_up_schedule.append(patient_info)

    return patient_info


def add_patient_interface():
    '''Interface for adding patients to the follow_up_schedule
    '''

    duplicate = False #to store the value of the check_duplicate function
    input_list.clear()
    clear_screen()

    what_next = ''
    while what_next != '-1':

        duplicate = False  # to store the value of the check_duplicate function
        input_list = []

        # Each header will be used as a key for the user input during adding patient information
        for header in headers_list:
            if header not in ['Next_Follow_Up_Date']:
                if headers_list.index(header) != 0:
                    header = header.replace('_', ' ')
                    if header in ["Follow Up Freq", "Priority"]:
                        input_item = input(f'{header}: ')
                        while not input_item.isdigit() and input_item != '-1':
                            input_item = input(
                                f'\033[91mPlease enter the a whole number for the {header}: \033[0m')

                    elif header in ['First Name', 'Last Name']:
                        input_item = input(f'{header}: ')
                        while not input_item.isalpha() and input_item != '-1':
                            input_item = input(
                                f'\033[91mplease enter a valid {header} or type -1 to go to main menu: \033[0m')

                    elif header == 'Last Visit Date':
                        input_item = input(
                            f'{header} in <dd-mm-yyyy> format or hit enter for today: ') or datetime.datetime.strftime(today, '%d-%m-%Y')
                        print('\033[96mLast Visit Date is ' +
                              input_item + '\033[0m')
                        
                        # Make sure the format of the entered date is correct
                        while not all(x.isdigit() for x in input_item.split('-'))  or\
                             input_item.count('-') != 2 or\
                                 len(input_item) != 10:
                            input_item = input(f'{header} please enter a valid date format or hit enter for today: ') or datetime.datetime.strftime(
                                today, '%d-%m-%Y')
                            print('\033[96mLast Visit Date is ' +
                                  input_item + '\033[0m')

                    if input_item == "-1":
                        clear_screen()
                        main_screen()
                    else:
                        input_list.append(input_item.lower().title())

                # Check if there is duplicate name with the same first and last name
                if header == 'Last Name':
                    duplicate = check_duplicate(input_list)[0]
                    file_no = check_duplicate(input_list)[1]

                    if duplicate:
                        print('')
                        print(
                            f'\033[91mThis patient is already on the follow up schedule with a file no: {file_no}\033[0m')
                        print('')
                        input_list.clear()
                        break

        if not duplicate:
            print('')
            add_confirmation = input(
                '\033[96mTo add the above information to your patients list (Y/N)?: \033[0m')
            print('')

            if add_confirmation.lower() == 'y':
                add_patient(input_list[0], input_list[1],
                            input_list[2], input_list[3], input_list[4])
                export_to_cv()
                print('\033[92mThe record was saved successfully\033[0m')
                print('')
                what_next = input(
                    '\033[96mHit enter to add another or type -1 to go to main menu: \033[0m')

    clear_screen()
    main_screen()


def check_duplicate(patient_info):
    ''''''
    duplicate = False
    file_no = None

    for patient in follow_up_schedule:
        if patient[1] == patient_info[0] and patient[2] == patient_info[1]:
            duplicate = True
            file_no = patient[0]
            break

    return [duplicate, file_no]


def add_test_patients():
    for patient in test_patients:
        duplicate = check_duplicate([patient[0], patient[1]])[0]

        if not duplicate:
            add_patient(patient[0], patient[1],
                        patient[2], patient[3], patient[4])
            print(
                f'\033[92m{patient[0]} {patient[1]} was  added successfully \033[0m')
        else:
            print(
                f'\033[91m{patient[0]} {patient[1]} is already on the schedule\033[0m')


def refresh():
    print('')
    export_to_cv()
    go_to_main_screen = input('\033[96mHit enter to gao to main screen\033[0m')

    if go_to_main_screen == "-1":
        clear_screen()
        main_screen()


def main_screen():

    main_menu = input("\033[96mPlease select from the options below:\033[0m\n\n\
\033[93m1:\033[0m View the follow up schedule\n\
\033[93m2:\033[0m Add patients to the follow up schedule \n\
\033[93m3:\033[0m Add a group of test patients to the follow up schedule \n\
\033[93m4:\033[0m Edit/delete patients from the follow up schedule\n\
\033[93m5:\033[0m Sort the follow up schedule\n\
\033[93m-1:\033[0m Anywhere in the program to return \n\
\033[93m0:\033[0m Quit the program: \n")

    if main_menu == '1':
        clear_screen()
        print_follow_up_schedule()
        print('')
        main_screen()

    elif main_menu == '2':
        print('')
        add_patient_interface()
        export_to_cv()
        clear_screen()
        main_screen()

    elif main_menu == '3':
        clear_screen()
        add_test_patients()
        export_to_cv() 
        print('')
        go_to_main_screen = input(
            '\033[96mHit enter to view schedule or type -1 to go to main menu\033[0m: ')

        if go_to_main_screen == '':
            clear_screen()
            print_follow_up_schedule()
            print('')
            go_to_main_screen = input(
                '\033[96mHit enter return to main screen\033[0m: ')
            if go_to_main_screen.isascii():
                clear_screen()
                main_screen()
        else:
            clear_screen()
            main_screen()

    elif main_menu == '4':
        clear_screen()
        print_follow_up_schedule()
        print('')
        edit_delete_interface()
        refresh()

    elif main_menu == '5':
        clear_screen()
        print_follow_up_schedule()
        print('')
        sort_interface()

    elif main_menu in ['0', '-1']:
        clear_screen()
        print('Good Bye!')
        quit()

    else:
        print('\033[91mPlease enter one of the mentioned options only\033[0m')
        first_time_main_menu = False
        main_screen()

def search_name(search_string):
    '''search follow_up_schedule for matching search_string\n
       search can be done by first name and/or last name
    '''

    search_results_list = []

    if len(search_string.split(' ')) > 1:
        first_name, last_name = search_string.split(' ')
        first_name = first_name.strip().lower()
        last_name = last_name.strip().lower()

        for patient in follow_up_schedule:

            if patient[1].lower().find(first_name) != -1 and patient[2].lower().find(last_name) != -1:
                search_results_list.append(patient[0])

            else:
                continue

    else:
        search_string = search_string.strip().lower()

        # loop through the follow_up_schedule and append file_no of patient records whom first_name or last_name matches the search_string
        for patient in follow_up_schedule:

            if patient[1].lower().find(search_string) != -1 or patient[2].lower().find(search_string) != -1:
                search_results_list.append(patient[0])

            else:
                continue

    return search_results_list


def edit_delete_interface():

    input_list = []

    search_string = input(
        "\033[96mSearch by part of/complete first and/or last name, or type -1 to go to main menu: \033[0m")

    if search_string == '-1':
        clear_screen()
        main_screen()

    elif search_name(search_string):
        search_result = search_name(search_string)
        filtered_follow_up_schedule = [
            patient for patient in follow_up_schedule if patient[0] in search_result]
        clear_screen()
        print_follow_up_schedule(filtered_follow_up_schedule)
        print('')

        mode_selection = input(f'\033[96mPlease select from the options below: \033[0m\n\n\
\033[93mdel:\033[0m to enter delete mode\n\
\033[93medit:\033[0m to enter edit mode:\n')
        print('')

        while mode_selection != '-1':

            if mode_selection == "del":
                delete_selection = input(
                    '\033[96mYou can delete one ore more records by selecting file numbers separated by comma: \033[0m')
                delete_patient(search_result, delete_selection,
                               follow_up_schedule, filtered_follow_up_schedule)

            elif mode_selection == "edit":

                edit_selection = input(
                    '\033[96mPlease enter the number of the file you want to edit: \033[0m')
                if edit_selection == "-1":
                    break
                while (not edit_selection.strip().isdigit()
                       or edit_selection not in search_result):
                    print('')
                    edit_selection = input(
                        '\033[91mPlease select from the file numbers above\033[0m: ')

                    if edit_selection == "-1":
                        break

                print('')
                edit_patient(edit_selection.strip())

            else:
                mode_selection = input(
                    '\033[31mPlease select a valid selection mode: \033[0m')

        clear_screen()
        main_screen()

    else:
        print('')
        what_next = input(
            '\033[91mNo match was found hit enter to try again or type -1 to go to main menu: \033[0m')
        print('')
        if what_next == '-1':
            clear_screen()
            main_screen()

        else:
            edit_delete_interface()


def delete_patient(search_result, delete_selection, follow_up_schedule, filtered_follow_up_schedule):

    while delete_selection != '-1' and delete_selection != '':

        deleted_flag = False
        deleted_list = []
        delete_list = delete_selection.split(',')
        delete_list = [item.strip() for item in delete_list]

        if delete_list and follow_up_schedule and filtered_follow_up_schedule:
            for patient in filtered_follow_up_schedule:
                if patient[0] in delete_list and set(delete_list).issubset(set(search_result)):
                    deleted_list.append(patient)
                    deleted_flag = True

            for n in range(len(deleted_list)):
                follow_up_schedule.remove(deleted_list[n])
                filtered_follow_up_schedule.remove(deleted_list[n])

            if deleted_flag:
                clear_screen()
                print_follow_up_schedule(filtered_follow_up_schedule)
                print('\033[32mRecord/s were deleted successfully\033[0m')
                print('')
                export_to_cv()
                if filtered_follow_up_schedule != []:
                    delete_selection = input(
                        '\033[96mYou can delete one ore more records by selecting file numbers separated by comma: \033[0m')
                else:
                    break

        if not set(delete_list).issubset(set(search_result)):
            delete_selection = input(
                f'\033[91mPlease select from the file numbers above or type -1 to go to main menu: \033[,5,60m')
            if delete_selection == '-1':
                clear_screen()
                main_screen()

    edit_delete_interface()


def edit_patient(file_no):

    duplicate = False
    input_list = []

    if file_no != '-1':

        patient_file = [
            patient for patient in follow_up_schedule if patient[0] == file_no][0]
        headers_dic = {'First Name': 1, 'Last Name': 2,
                       'Last Visit Date': 3, 'Follow Up Freq': 4, 'Priority': 6}

        for header in headers_list:

            if header != 'Next_Follow_Up_Date':

                if headers_list.index(header) != 0:

                    header = header.replace('_', ' ')
                    if header in ["Follow Up Freq", "Priority"]:

                        input_item = input(
                            f'\033[96m{header}: \033[0m{patient_file[headers_dic[header]]}, \033[96menter a new value below or hit enter to skip: \033[0m')
                        while not input_item.isdigit():
                            if input_item == '':
                                input_item = patient_file[headers_dic[header]]
                                break
                            else:
                                input_item = input(
                                    f'\033[91mPlease enter the a whole number for the {header} or hit enter to skip: \033[0m')

                        input_list.append(input_item.title())
                    elif header in ['First Name', 'Last Name']:
                        input_item = input(
                            f'\033[96m{header}: \033[0m{patient_file[headers_dic[header]]}, \033[96menter a new value below or hit enter to skip: \033[0m')

                        while not input_item.isalpha() and input_item != '-1':
                            if input_item == '':
                                input_item = patient_file[headers_dic[header]]

                                break
                            else:
                                input_item = input(
                                    f'\033[96mPlease enter a valid {header} or type -1 to go to main menu: \033[0m')

                        input_list.append(input_item.title())

                    elif header == 'Last Visit Date':
                        input_item = input(
                            f'\033[96m{header}: \033[0m{patient_file[headers_dic[header]]}, \033[96mPlease enter a new value below in <dd-mm-yyyy> format or hit enter to skip: \033[0m')

                        while not all(x.isdigit() for x in input_item.split('-')) or input_item.count('-') != 2:
                            if input_item == '':
                                input_item = patient_file[headers_dic[header]]

                                break
                            else:
                                input_item = input(
                                    f'\033[91mPlease enter a valid {header} or type -1 to go to main menu: \033[0m')

                        input_list.append(input_item)

                    if input_item == "-1":
                        clear_screen()
                        main_screen()

                if header == 'Last Name':

                    duplicate = check_duplicate(input_list)[0]
                    file_no = check_duplicate(input_list)[1]

                if duplicate and file_no != patient_file[0]:
                    print(
                        f'\033[91mThis patient is already on the follow up schedule with a file no: {file_no}\033[0m')
                    print('')
                    input_list.clear()
                    break

    if not duplicate:
        print('')
        add_confirmation = input(
            '\033[96mDo you want to save the new edits (Y/N)?: \033[0m')
        print('')

        if add_confirmation.lower() == 'y':
            follow_up_schedule.remove(patient_file)
            a = add_patient(input_list[0], input_list[1], input_list[2],
                            input_list[3], input_list[4], patient_file[0])
            export_to_cv()
            print_follow_up_schedule(
                [follow_up_schedule[int(follow_up_schedule.index(a))]])
            print('')
            what_next = input(
                '\033[96mHit enter to start a new search or type -1 to go to main menu: \033[0m')
            print('')
            if what_next != "-1":

                edit_delete_interface()

            else:

                clear_screen()
                main_screen()

        else:
            edit_delete_interface()


def sort_follow_up_schedule(index=5, reverse=False):

    if index in [4, 6]:
        follow_up_schedule.sort(key=lambda x: datetime.datetime.strptime(
            x[index-1], "%d-%m-%Y"), reverse=reverse)
    elif index == 5:
        follow_up_schedule.sort(key=lambda x: int(
            x[4].replace(' m', '')), reverse=reverse)
    elif index == 1:
        follow_up_schedule.sort(key=lambda x: int(x[0]), reverse=reverse)
    else:
        follow_up_schedule.sort(key=lambda x: x[index-1], reverse=reverse)

    print_follow_up_schedule()
    print('')
    sort_interface()


def sort_interface():

    sort_method = input('\033[96mPlease select from the options below:\033[0m\n\n\
\033[93m1:\033[0m sort by file number\n\
\033[93m2:\033[0m  sort by first name\n\
\033[93m3:\033[0m  sort by last name\n\
\033[93m4:\033[0m  sort by follow up frequency\n\
\033[93m5:\033[0m  sort by follow up date\n\
\033[93m6:\033[0m  sort by priority\n\
*type des after selection for descending order (e.g, 1 des)\n\
-1: retrun to main menu\n')

    try:
        sort_method_clean = sort_method.replace('des', '').strip()
        if sort_method == '-1':
            clear_screen()
            main_screen()

        elif int(sort_method_clean) not in list(range(1, 8)):
            clear_screen()
            print(f'\033[91m\'{sort_method}\' is not a valid option\033[0m')
            print('')
            sort_interface()

    except:
        clear_screen()
        print(f'\033[91m\'{sort_method}\' is not a valid option\033[0m')
        print('')
        sort_interface()

    clear_screen()
    if 'des' in sort_method:
        sort_follow_up_schedule(int(sort_method_clean), True)
    else:
        sort_follow_up_schedule(int(sort_method_clean))


def export_to_cv():

    file = os.getcwd() + '/Schedule.csv'

    with open(file, 'w') as f:
        writer = csv.writer(f)

        for row in follow_up_schedule:
            writer.writerow(row)


##### USER INTERFACE #####
main_screen()
