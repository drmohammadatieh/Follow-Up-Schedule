import datetime
import csv
import os

print(os.getcwd())


##### GLOBAL VARIABLES #####

follow_up_schedule = []  # A list to store schedule records
# For testing and trying the application features

test_patients = [
    ['John', 'Campbell', '01-12-2021', '12', '2'],
    ['Merry', 'Barnett', '01-12-2021', '3', '1'],
    ['Jordan', 'Frost', '01-12-2021', '3', '2'],
    ['Linda', 'Wright', '01-12-2019', '24', '2'],
    ['Angela', 'Rogers', '01-12-2018', '0', '1'],
    ['Sarah', 'Mcnaught', '01-12-2018', '0', '1'],
]
# Headers for the follow up schedule table 
headers_list = [
    'File_No', 'First_Name', 'Last_Name', 'Last_Visit_Date',
    'Follow_Up_Freq', 'Next_Follow_Up_Date', 'Priority'
]
today = datetime.date.today()


##### DATA IMPORT & CLEAR SCREEN FUNCTIONS #####

def clear_screen():
    '''Clears the command line interface.'''

    return os.system(
        'cls' if os.name in ('nt', 'dos') else 'clear')

def import_from_cv():
    '''Imports saved data to follow_up_schedule.'''

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
    '''Prints the follow_up_schedule list in a table format.'''

    print('') # A new line

    # Print the follow up schedule headers
    padding = ' ' * 5
    for header in headers_list:
        print(f'\033[38;5;15;48;5;20m{header}{padding}\033[0m', end='')

    print('') # A new line

    # Print dashed line (---) seprating the headers from the rows
    print('-' * (sum([len(header)
          for header in headers_list]) + 5 * len(headers_list)))

    # Print the follow up schedule rows
    for j in range(len(follow_up_schedule)):
        for i in range(len(headers_list)):
            i_padding = ' ' * \
                ((len(headers_list[i]) + 5) -
                 len(str(follow_up_schedule[j][i])))
            print(
                f'\033[38;5;15;48;5;12m{follow_up_schedule[j][i]}{i_padding}\033[0m', end='')

        print('') # A new line


def add_patient(first_name, last_name,
 last_visit_date, follow_up_freq, priority, file_no=''):
    '''Adds patient to the follow_up_schedule list.\n
File_no is optional; it is used for editing.\n
All new patients get autogenerated file_no.
    '''

    # Auto generate a file number based on the maximum available file number
    # in the follow_up_schedule 
    if not file_no:
        if not follow_up_schedule:
            file_no = 1
        else:
            file_no = max(int(patient[0]) for patient in follow_up_schedule) + 1

    # 'm' stands for month/s
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
    patient_info = [
        first_name, last_name, last_visit_date,
        follow_up_freq, next_follow_up_date, priority
    ]

    if follow_up_freq == '0 m':
        patient_info[4] = 'As Needed' #next_follow_up_date will be set "As Needed"
  
    patient_info = [str(file_no)] + patient_info
    follow_up_schedule.append(patient_info)

    return patient_info


def add_patient_interface():
    '''Interface for adding patients to the follow_up_schedule.'''

    input_item = ''
    while input_item != '-1':

        clear_screen()
        duplicate = False  # to store the value of the check_duplicate function
        input_list = []
        
        # Each header will be used as a key for the user input during adding patient information
        for header in headers_list:
            if header not in ['Next_Follow_Up_Date' ,'File_No']:
                header = header.replace('_', ' ')
                if header in ["Follow Up Freq", "Priority"]:
                    if header == 'Follow Up Freq':
                        input_item = input(f'{header} (in months): ').strip()
                    else:
                        input_item = input(f'{header} (1 = highest priority, 2 less ...etc): ').strip()
                    while not input_item.isdigit() and input_item != '-1':
                        input_item = input(
                            f'\033[91mPlease enter a whole number for the {header}: \033[0m').strip()

                elif header in ['First Name', 'Last Name']:
                    input_item = input(f'{header}: ').strip()
                    while not input_item.replace(' ','').isalpha() and input_item != '-1':
                        input_item = input(
                            f'\033[91mplease enter a valid {header} or enter -1 to go to main menu: \033[0m').strip()

                elif header == 'Last Visit Date':
                    # Make sure the format of the entered date is correct
                    while input_item != '-1':
                        try:
                            input_item = input(
                        f'{header} in <dd-mm-yyyy> format or hit enter for today: ') or\
                                datetime.datetime.strftime(today, '%d-%m-%Y')
                            input_item = datetime.datetime.strptime(input_item,'%d-%m-%Y').date()
                            input_item = datetime.datetime.strftime(input_item,'%d-%m-%Y')
                            print('\033[96mLast Visit Date is ' +
                            input_item + '\033[0m')
                            break
                        except: 
                            continue
                    
                input_item.strip()

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
                        print('') # A new line
                        what_next = input(f'\033[91mThis patient is already on the follow up schedule with a file no: {file_no}\033[0m')
                        
                        if what_next == '':
                            input_list.clear()
                            break

        if not duplicate:
            print('') # A new line
            add_confirmation = input(
                '\033[96mSave the information above (Y/N)?: \033[0m')
            print('') # A new line

            if add_confirmation.lower() == 'y':
                add_patient(input_list[0], input_list[1],
                            input_list[2], input_list[3], input_list[4])
                export_to_cv()
                print('\033[92mThe record was saved successfully\033[0m')
                print('') # A new line
                input_item = input(
                    '\033[96mHit enter to add another patient or enter -1 to go to main menu: \033[0m')

    clear_screen()
    main_screen()


def check_duplicate(patient_info):
    '''Checks for duplicate entries
while adding and editing patients.   
'''
    duplicate = False
    file_no = None

    # If the first and last name are already on the follow up schedule, duplicate = True:
    for patient in follow_up_schedule:
        if patient[1] == patient_info[0] and patient[2] == patient_info[1]:
            duplicate = True
            file_no = patient[0]
            break

    return [duplicate, file_no]


def add_test_patients():
    '''Adds a group of test patients
for testing and trying application feature.
'''
    for patient in test_patients:
        duplicate = check_duplicate([patient[0], patient[1]])[0]

        if not duplicate:
            add_patient(patient[0], patient[1],
                        patient[2], patient[3], patient[4])
            print(
                f'\033[92m{patient[0]} {patient[1]} was added successfully \033[0m')
        else:
            print(
                f'\033[91m{patient[0]} {patient[1]} is already on the follow up schedule\033[0m')


def search_name(search_string):
    '''Search follow_up_schedule for matching search_string.\n
search can be done by first name and/or last name partial or complete.
    '''

    search_results_list = []

    # If more than one search string:
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

        # loop through the follow_up_schedule and append file_no of patient records
        # whom first_name or last_name matches the search_string
        for patient in follow_up_schedule:
            if patient[1].lower().find(search_string) != -1 or patient[2].lower().find(search_string) != -1:
                search_results_list.append(patient[0])
            else:
                continue

    return search_results_list


def edit_delete_interface():
    '''Interface for editing and deleting patients.'''

    clear_screen()
    print_follow_up_schedule()
    print('') # A new line

    # Starts by searching a record
    search_string = input(
        "\033[96mSearch by first and/or last name partial/complete or enter -1 to go to main menu: \033[0m")

    if search_string == '-1':
        clear_screen()
        main_screen()

    # If a match/es is/are found, print the filtered_follow_up_schedule:
    elif search_name(search_string):
        search_result = search_name(search_string)
        filtered_follow_up_schedule = [
            patient for patient in follow_up_schedule if patient[0] in search_result]
        clear_screen()
        print_follow_up_schedule(filtered_follow_up_schedule)
        print('') # A new line

        mode_selection = input(f'\033[96mPlease enter one of the options below: \033[0m\n\n\
\033[93mdel :\033[0m to enter delete mode\n\
\033[93medit:\033[0m to enter edit mode\n\
\033[93m    :\033[0m hit enter to search again\n\n\
> ')

        while mode_selection != '-1':

            # If delete mode is selected:
            if mode_selection == "del":
                delete_selection = input(
                    '\033[96mYou can delete one or more records by selecting file numbers separated by a comma: \033[0m')
                delete_patient(search_result, delete_selection,
                               follow_up_schedule, filtered_follow_up_schedule)

            #If edit mode is selected:
            elif mode_selection == "edit":
                print('') # A new line
                edit_selection = input(
                    '\033[96mPlease enter the number of the file you want to edit: \033[0m')
                if edit_selection == "-1":
                    break
                while (not edit_selection.strip().isdigit()
                       or edit_selection not in search_result):
                    print('') # A new line
                    edit_selection = input(
                        '\033[91mPlease enter one of the file numbers above or enter -1 to go to main screen\033[0m: ')
                    if edit_selection == "-1":
                        clear_screen()
                        main_screen()

                print('') # A new line
                edit_patient(edit_selection.strip())

            elif mode_selection == '':
                clear_screen()
                print_follow_up_schedule()
                print('') # A new line
                edit_delete_interface()

            else:
                mode_selection = input(
                    '\033[31mPlease enter a valid selection mode: \033[0m')

        clear_screen()
        main_screen()

    # If there is no match found:
    else:
        print('') # A new line
        what_next = input(
            '\033[91mNo match was found hit enter to try again or enter -1 to go to main menu: \033[0m')
        print('') # A new line
        if what_next == '-1':
            clear_screen()
            main_screen()

        else:
            edit_delete_interface()


def edit_patient(file_no):
    '''Edits patient records.'''

    duplicate = False
    input_list = []

    if file_no != '-1':

        patient_file = [
            patient for patient in follow_up_schedule if patient[0] == file_no][0] # Finds the selected patient record
        headers_dic = {'First Name': 1, 'Last Name': 2,
                       'Last Visit Date': 3, 'Follow Up Freq': 4, 'Priority': 6}

        # Each field wil be shown to the user with an option to enter a new valuse or skip:
        for header in headers_list:
            input_item =''
            if header not in ['Next_Follow_Up_Date','File_No']:
                header = header.replace('_', ' ')
                if header in ["Follow Up Freq", "Priority"]:
                    input_item = input(
                        f'{header}: {patient_file[headers_dic[header]]}\n\033[96mPlease enter a new value below or hit enter to skip: \033[0m')
                    while not input_item.isdigit() and input_item != '-1':
                        if input_item == '':  #if editing this field is skipped the original value will be retained
                            input_item = patient_file[headers_dic[header]]
                            break
                        else:
                            input_item = input(
                                f'\033[91mPlease enter a whole number for the {header} or hit enter to skip: \033[0m')

                    input_list.append(input_item)
                elif header in ['First Name', 'Last Name']:
                    input_item = input(
                        f'{header}: {patient_file[headers_dic[header]]}\n\033[96mPlease enter a new value below or hit enter to skip: \033[0m')

                    while not input_item.isalpha() and input_item != '-1':
                        if input_item == '':  #if editing this field is skipped the original value will be retained
                            input_item = patient_file[headers_dic[header]]
                            break
                        else:
                            input_item = input(
                                f'\033[96mPlease enter a valid {header} or enter -1 to go to main menu: \033[0m')

                    input_list.append(input_item.title())

                elif header == 'Last Visit Date':
                    # Make sure the format of the entered date is correct
                    while input_item != '-1':
                        try:
                            input_item = input(
                        f'{header}:{patient_file[headers_dic[header]]}\n\033[96mPlease enter a new date in <dd-mm-yyyy> format or hit enter to skip: \033[0m') or\
                                patient_file[headers_dic[header]]  #if editing this field is skipped the original value will be retained
                            input_item = datetime.datetime.strptime(input_item,'%d-%m-%Y').date()
                            input_item = datetime.datetime.strftime(input_item,'%d-%m-%Y')
                            break
                        except: 
                            continue

                    input_list.append(input_item)

                if input_item == "-1":
                    clear_screen()
                    main_screen()

            # Make sure the edited patient file doesn't result in a duplicate
            if header == 'Last Name':
                duplicate = check_duplicate(input_list)[0]
                file_no_of_duplicate = check_duplicate(input_list)[1]
           
            # If there is a duplicate with different file_no:
            if duplicate and file_no_of_duplicate != patient_file[0]:
                print('') # A new line
                what_next = input(f'\033[91mThis patient is already on the follow up schedule with a file no {file_no_of_duplicate}\n\
hit enter to start over:\033[0m')
                
                if what_next == '':
                   print('') # A new line
                   edit_patient(file_no)
              
    # If editing the same file number then this is not a duplicate:            
    if file_no_of_duplicate == None:
        print('') # A new line
        add_confirmation = input(
            '\033[96mDo you want to save the new edits (Y/N)?: \033[0m')
        print('') # A new line

        if add_confirmation.lower() == 'y':
            follow_up_schedule.remove(patient_file)
            patient = add_patient(input_list[0], input_list[1], input_list[2],
                            input_list[3], input_list[4], patient_file[0])
            export_to_cv()
            print_follow_up_schedule(
                [follow_up_schedule[int(follow_up_schedule.index(patient))]])
            print('') # A new line
            what_next = input(
                '\033[96mHit enter to start a new search or enter -1 to go to main menu: \033[0m')
            print('') # A new line

            if what_next != "-1":
                clear_screen()
                edit_delete_interface()

            else:
                clear_screen()
                main_screen()
        
        else:
            clear_screen()
            edit_delete_interface()

    else:
        clear_screen()
        main_screen()



    edit_delete_interface()


def delete_patient(search_result, delete_selection, follow_up_schedule, filtered_follow_up_schedule):
    '''Deletes patient records.'''

    # If there are files selected to be deleted and no -1 (retrun to main screen) option is selected:
    while delete_selection != '-1':
    
        deleted_flag = False
        deleted_list = []
        to_delete_list = delete_selection.split(',')
        to_delete_list = [item.strip() for item in to_delete_list if item.strip() !=''] # Creates list of file_no/s to delete

        if to_delete_list: 
            for patient in filtered_follow_up_schedule:
                # Check if the file_no to be deleted in the records and in the search result:
                if patient[0] in to_delete_list and set(to_delete_list).issubset(set(search_result)): 
                    deleted_list.append(patient)
                    deleted_flag = True

            # Remove the deleted record from the the following lists:
            for n in range(len(deleted_list)):
                follow_up_schedule.remove(deleted_list[n])
                filtered_follow_up_schedule.remove(deleted_list[n])
                search_result.remove(deleted_list[n][0])
            
            # Print the edited follow_up_schedule and export to the csv file:
            if deleted_flag:
                clear_screen()
                print_follow_up_schedule(filtered_follow_up_schedule)
                print('\033[32mRecord/s were deleted successfully\033[0m')
                print('') # A new line
                export_to_cv()

                # Check if the user is willing to delete more records:
                if filtered_follow_up_schedule != []:
                    delete_selection = input(
               '\033[96mYou can delete one or more records by selecting file numbers separated by a comma\n\
or hit enter to start a new search: \033[0m')

                    if delete_selection != []:
                        continue
                else:
                    what_next = input('\033[96m No more records, hit enter to go to main screen: \033[0m')
                    break

        # If the record that is recquested to be deleted is not in the search_result:                    
        if not set(to_delete_list).issubset(set(search_result)):
            delete_selection = input(
                f'\033[91mPlease enter one of the file numbers above or -1 to go to main menu: \033[0m')
            if delete_selection == '-1':
                clear_screen()
                main_screen()

    clear_screen()
    main_screen()

def sort_follow_up_schedule(index=5, order='a', priority = 'a'):
    '''Sorts the follow_up_schedule by column.'''

    #headers_list indices: 'File_No':0, 'First_Name':1, 'Last_Name':2, 'Last_Visit_Date':3,
    #'Follow_Up_Freq':4, 'Next_Follow_Up_Date':5, 'Priority:6
  
    if index == 1:
        follow_up_schedule.sort(key=lambda x: int(x[0]), reverse = True if order == 'd' else False)
    elif index in [4, 6]:
        if index == 6:
            if order == 'a':
                if priority == 'a': # next_follow_up_date-->ascending, priority-->ascending
                    follow_up_schedule.sort(key=lambda x: (datetime.datetime.strptime(
                        x[5], "%d-%m-%Y")if x[5] !='As Needed' else datetime.datetime.strptime('1-1-4000',
                        '%d-%m-%Y'), int(x[6])) )
                else: # next_follow_up_date-->ascending, priority-->descending
                    follow_up_schedule.sort(key=lambda x: (datetime.datetime.strptime(
                        x[5], "%d-%m-%Y") if x[5] !='As Needed' else datetime.datetime.strptime('1-1-4000',
                        '%d-%m-%Y'), -int(x[6])) )
    
            else:
                if priority == 'a': # next_follow_up_date-->descending, priority-->ascending
                    follow_up_schedule.sort(key=lambda x: (datetime.datetime.strptime(
                        x[5], "%d-%m-%Y") if x[5] !='As Needed' else datetime.datetime.strptime('1-1-4000',

                        '%d-%m-%Y'), -int(x[6])),reverse=True)
                else:  # next_follow_up_date-->descending, priority-->descending
                    follow_up_schedule.sort(key=lambda x: (datetime.datetime.strptime(
                        x[5], "%d-%m-%Y")if x[5] !='As Needed' else  datetime.datetime.strptime('1-1-4000',
                        '%d-%m-%Y'), int(x[6])),reverse=True)

    elif index == 5:
        follow_up_schedule.sort(key=lambda x: int(
            x[4].replace(' m', '')), reverse = True if order == 'd' else False)

    else:
        follow_up_schedule.sort(key=lambda x: x[index-1], reverse = True if order == 'd' else False)

    print_follow_up_schedule()
    print('') # A new line
    sort_interface()


def sort_interface():
    '''Interface to sort the follow_up_schedule.'''

    sort_method = input('\033[96mPlease enter one of the options below:\033[0m\n\n\
\033[93m1-7:\033[0m sort by column\n\
\033[93md:\033[0m after number selection for descending order (e.g, 1 d)\n\
\033[93ma/d a/d:\033[0m after choice 6 to sort the date and priority in ascending/descending order (e.g, 6 a d)\n\
\033[93m-1:\033[0m retrun to main menu\n\n\
> ')

    if sort_method != '-1':
        try:
            # Prepare the sorting method from the user input
            sort_method_clean = sort_method.replace('d', '').replace('a','').strip()
            sort_method_list = sort_method.strip().split(' ')

            if sort_method == '-1':
                clear_screen()
                main_screen()

            elif int(sort_method_clean) not in list(range(1, 8)):
                clear_screen()
                print(f'\033[91m\'{sort_method}\' is not a valid option\033[0m')
                print('') # A new line
                sort_interface()

        except:
            clear_screen()
            print(f'\033[91m\'{sort_method}\' is not a valid option\033[0m')
            print('') # A new line
            sort_interface()

        clear_screen()

        # Sort in descending or ascending order
        if 3 > len(sort_method_list) > 1:
            sort_follow_up_schedule(int(sort_method_clean),sort_method_list[1])
        elif len(sort_method_list) == 3 :
            sort_follow_up_schedule(int(sort_method_clean),sort_method_list[1],sort_method_list[2])
        else:
             sort_follow_up_schedule(int(sort_method_clean))

    else:
        clear_screen()
        main_screen()

def check_out_and_follow(file_no):
    '''Checks the patient out after attending the appointment\n
and retrun to the follow_up_schedule with the next_follow_up_date
'''

    if file_no != '-1':

        patient_file = [
            patient for patient in follow_up_schedule if patient[0] == file_no][0] # Finds the selected patient record
        
        # Remove the old patient record from the follow schedule and return the new one with the new date:
        follow_up_schedule.remove(patient_file)
        patient = add_patient(patient_file[1], patient_file[2], datetime.datetime.strftime(today, '%d-%m-%Y'),patient_file[4],patient_file[6]
                        ,patient_file[0])
        export_to_cv()
        print_follow_up_schedule(
            [follow_up_schedule[int(follow_up_schedule.index(patient))]])
        print('') # A new line
        
        what_next = input(
            '\033[96mHit enter to start a new search or enter -1 to go to main menu: \033[0m')
        print('') # A new line

        if what_next != "-1":
            clear_screen()
            print_follow_up_schedule()
            print('') # A new line
            check_out_and_follow_interface()

        else:
            clear_screen()
            main_screen()

    else:
        clear_screen()
        check_out_and_follow_interface()



def check_out_and_follow_interface():
    '''Interface for checking out patients and scheduling next
follow up due date 
    '''

    # Start by searching a record
    search_string = input(
        "\033[96mSearch by first and/or last name partial/complete or\
 enter -1 to go to main menu: \033[0m")

    if search_string == '-1':
        clear_screen()
        main_screen()

    # If a match/es is/are found:
    elif search_name(search_string):
        search_result = search_name(search_string)
        filtered_follow_up_schedule = [
            patient for patient in follow_up_schedule if patient[0] in search_result]
        clear_screen()
        print_follow_up_schedule(filtered_follow_up_schedule)
        print('') # A new line

        selection = input(
                    '\033[96mEnter the file number of the  patient you want to\
 checkout and return to the follow up schedule: \033[0m')
           
        while (not selection.strip().isdigit()
                or selection not in search_result):
            print('') # A new line
            selection = input(
                '\033[91mPlease enter one of the file numbers above or\
enter -1 to go to main screen\033[0m: ')

            if selection == "-1":
                clear_screen()
                main_screen()

        print('') # A new line
        clear_screen()
        check_out_and_follow(selection)
       
        if selection == '':
            clear_screen()
            print_follow_up_schedule()
            print('') # A new line
            check_out_and_follow_interface()

    # If there is no match found:
    else:
        print('') # A new line
        what_next = input(
            '\033[91mNo match was found hit enter to try again or\
 enter -1 to go to main menu: \033[0m')
        print('') # A new line
        if what_next == '-1':
            clear_screen()
            main_screen()
        else:
            clear_screen()
            print_follow_up_schedule() 
            print('') # A new line
            check_out_and_follow_interface()

def export_to_cv():
    '''Exports the follow_up_schedule to a csv file'''

    file = os.getcwd() + '/Schedule.csv'

    with open(file, 'w') as f:
        writer = csv.writer(f)
        for row in follow_up_schedule:
            writer.writerow(row)

##### USER INTERFACE #####

def main_screen():
    '''Main user interface'''

    main_menu = input("\033[96mPlease enter one of the options below:\033[0m\n\n\
\033[93m 1:\033[0m View the follow up schedule\n\
\033[93m 2:\033[0m Add patients \n\
\033[93m 3:\033[0m Add test patients\n\
\033[93m 4:\033[0m Search/Edit/delete patients\n\
\033[93m 5:\033[0m Sort the follow up schedule\n\
\033[93m 6:\033[0m Check out patient and return to the follow up schedule\n\
\033[93m-1:\033[0m Anywhere to return to the main menu \n\
\033[93m 0:\033[0m Quit\n\n\
> ")

    if main_menu == '1':
        clear_screen()
        print_follow_up_schedule()
        print('') # A new line
        main_screen()
       
    elif main_menu == '2':
        clear_screen()
        add_patient_interface()
        export_to_cv()
        clear_screen()
        main_screen()

    elif main_menu == '3':
        clear_screen()
        add_test_patients()
        export_to_cv() 
        print('') # A new line
        go_to_main_screen = input(
            '\033[96mHit enter to view schedule or enter -1 to go to main menu\033[0m: ')

        if go_to_main_screen == '':
            clear_screen()
            print_follow_up_schedule()
            print('') # A new line
            go_to_main_screen = input(
                '\033[96mHit enter to return to main screen\033[0m: ')
            if go_to_main_screen.isascii():
                clear_screen()
                main_screen()
        else:
            clear_screen()
            main_screen()

    elif main_menu == '4':
        edit_delete_interface()
        export_to_cv()
        clear_screen()
        main_screen()

    elif main_menu == '5':
        clear_screen()
        print_follow_up_schedule()
        print('') # A new line
        sort_interface()

    elif main_menu in ['0', '-1']:
        clear_screen()
        print('\033[92mGood Bye!\033[0m')
        quit()

    elif main_menu == '6':
        clear_screen()
        print_follow_up_schedule()
        print('') # A new line
        check_out_and_follow_interface()

    else:
        
        go_to_main_screen = input('\033[96mPlease enter one of the mentioned options only. Hit enter to try again, otherwise the application will quit\033[0m ')

        if go_to_main_screen == "":
        
            clear_screen()
            main_menu = ''
            main_screen()

        else:
            quit()
                
       
main_screen()

    
