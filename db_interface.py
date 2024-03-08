# Sample file to do CRUD operations on CSV files

import argparse
from copy import deepcopy
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
    upd_row = int(input(f"Enter record to update [1 - {record_count}]: "))
    if upd_row < 1 or upd_row > record_count:
        print(f"[ERROR]: You entered {upd_row}. Expected [1 - {record_count}].")
        return False

    # Lets print some context
    first_row = max(1, upd_row - 2)
    last_row = min(mem_db.total_records_db(), upd_row + 2)
    mem_db.display_recs(first_row, last_row)
    upd_record = mem_db.get_rec(upd_row - 1)

    # Get user input for updates
    new_record = deepcopy(upd_record)
    in_record = list()

    in_record.append(input(f"Education Level [Bachelors|Masters|PHD] (blank for {new_record[0]}): ").strip()) # [0]
    in_record.append(input(f"Joining Year [2010 - 2020] (blank for {new_record[1]}): ").strip())
    in_record.append(input(f"City [Bangalore|Pune|New Delhi] (blank for {new_record[2]}): ").strip())
    in_record.append(input(f"Payment Tier [1-3] (blank for {new_record[3]}): ").strip())
    in_record.append(input(f"Age [20 - 99] (blank for {new_record[4]}): ").strip())
    in_record.append(input(f"Gender [Male|Female] (blank for {new_record[5]}): ").strip())
    in_record.append(input(f"Benched [Yes|No] (blank for {new_record[6]}): ").strip())
    in_record.append(input(f"Experience [1-9] (blank for {new_record[7]}): ").strip())
    in_record.append(input(f"On Leave [1|0] (blank for {new_record[8]}): ").strip())

    new_record = [x if x else y for x,y in zip(in_record, upd_record)]

    # Get confirmation
    print(f"Changing record From: \n")
    mem_db.display_recs(upd_row, upd_row+1)
    print(f"TO: \n{new_record}\n")
    answer = confirm("Proceed? (Y/N): ")
    if answer:
        print("Updating Record...")
        mem_db.delete_recs(upd_row)
        mem_db.add_recs(new_record)

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