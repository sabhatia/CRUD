# Sample file to do CRUD operations on CSV files

import argparse
import csv
from inquirer import confirm
from pprint import pprint as pp
from memory_db import memory_db
from memory_db import DB_Initialization_Error


def build_parser():

    # Just get the filename for now
    parser = argparse.ArgumentParser(description="A program to do CRUD Ops on CSV files", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="filename to load")
    return parser

def display_all_records(mem_db):
    first_record = 1
    last_record = mem_db.total_records_db() + 1
    
    print(f"[STATUS]: Display All Records")
    mem_db.display_recs(first_record, last_record)

def display_records(mem_db):
    record_count = mem_db.total_records_db()
    print("[STATUS]: : Display Records")
    print("Total Records: ", record_count)

    # Get and validate initial value
    first_record = int(input(f"Enter starting range: [1 - {record_count}]: "))
    if first_record < 1 or first_record > record_count:
        print(f"[ERROR]: You entered {first_record} for intial value. Expected [1 - {record_count}].")
        return False
    
    # Get and validate final value
    last_record = int(input(f"Enter last record: [{first_record + 1} - {record_count + 1}]: "))
    if last_record < first_record + 1 or last_record > record_count + 1:
        print(f"[ERROR]: You entered {last_record} for end value. Expected [{first_record + 1} - {record_count + 1}].")
        return False
    
    mem_db.display_recs(first_record, last_record)
    return True

def delete_records(mem_db):
    print("[STATUS]: : Delete Records")
    record_count = mem_db.total_records_db()

    # Get and validate value
    del_record = int(input(f"Enter record to delete [1 - {record_count}]: "))
    if del_record < 1 or del_record > record_count:
        print(f"[ERROR]: You entered {del_record}. Expected [1 - {record_count}].")
        return False

    # Lets print some context
    first_row = max(1, del_record - 2)
    last_row = min(mem_db.total_records_db(), del_record + 2)
    mem_db.display_recs(first_row, last_row)

    if mem_db.delete_recs(del_record) == True:
        print(f"[STATUS]: Record {del_record} deleted")
    else:
        print(f"[ERROR]: Could not delete record {del_record}")
    mem_db.display_recs(first_row, last_row)
    return True

def update_records(mem_db):
    print("[STATUS]: : Update Records")

    record_count = mem_db.total_records_db()

    # Get and validate value
    upd_record = int(input(f"Enter record to update [1 - {record_count}]: "))
    if upd_record < 1 or upd_record > record_count:
        print(f"[ERROR]: You entered {upd_record}. Expected [1 - {record_count}].")
        return False

    # Lets print some context
    first_row = max(1, upd_record - 2)
    last_row = min(mem_db.total_records_db(), upd_record + 2)
    mem_db.display_recs(first_row, last_row)

    # Get user input for updates
    user_edu = input(f"Education Level [Bachelors|Masters|PHD]: ").strip()
    user_year = int(input(f"Joining Year [2010 - 2020]: "))
    user_city = input(f"City [Bangalore|Pune|New Delhi]: ").strip()
    user_pay = input(f"Payment Tier [1-3]: ").strip()
    user_age = int(input(f"Age [20 - 99]: "))
    user_gender = input(f"Gender [Male|Female]: ").strip()
    user_benched = input(f"Benched [Yes|No]: ").strip()
    user_experience = int(input(f"Experience [1-9]: "))
    user_leave = int(input(f"On Leave [1|0]: "))
                  
    # Get confirmation
    user_record = [user_edu, 
                   user_year,
                   user_city,
                   user_pay,
                   user_age,
                   user_gender,
                   user_benched,
                   user_experience,
                   user_leave]
    print(f"Changing record FROM: \n")
    mem_db.display_recs(upd_record, upd_record+1)
    print(f"TO: \n{user_record}\n")
    answer = confirm("Proceed? (Y/N): ")
    if answer:
        mem_db.delete_recs(upd_record)
        mem_db.add_recs(user_record)

    return True

def end_display(mem_db):
    print("[STATUS]: : Exit")
    return END

user_cmds_dict = {'0': display_all_records,
                  '1': display_records,
                  '2': delete_records,
                  '3': update_records,
                  '4': end_display}

def display_and_parse_console(mem_db):
    ret_val = True
    print('File Operations')
    print('[0] Display all records')
    print('[1] Display records')
    print('[2] Delete records')
    print('[3] Update records')
    print('[4] Exit')
    user_cmd = input("Your Selection: ")
    if user_cmd in user_cmds_dict.keys():
        ret_val = user_cmds_dict[user_cmd](mem_db)
    else:
        print(f"[ERROR]: Invalid entry {user_cmd}. Accepted range 0-3")
    return ret_val

if __name__ == '__main__':

    END = -1
    # Parse the file to read and display a console

    # 1. Build the parser
    cli_parser = build_parser()

    # 2. Parse the file
    args = cli_parser.parse_args()
    csv_file = args.filename
    
    # 3. Initialize the DB
    try:
        csv_table = memory_db(csv_file)
    except DB_Initialization_Error as dbE:
        print("[ERROR]: ", dbE.message)
        exit()
    print(f"[STATUS]: Initialized DB with {csv_table.total_records_db()} records.")

    # 4. Diplay the console for further instructions
    while (display_and_parse_console(csv_table) != END):
        continue

    # Done, shutdown db
    del csv_table