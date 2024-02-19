# Sample file to do CRUD operations on CSV files

import argparse
import csv
from pprint import pprint as pp
from memory_db import memory_db
from memory_db import DB_Initialization_Error


def build_parser():

    # Just get the filename for now
    parser = argparse.ArgumentParser(description="A program to do CRUD Ops on CSV files", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="filename to load")
    return parser

def display_records(mem_db):
    record_count = mem_db.total_records_db()
    print("[STATUS]: : Display Records")
    print("Total Records: ", record_count)
    first_record = int(input("Enter starting range: [0 for all]:"))
    last_record = int(input("Enter last record: "))

    mem_db.display_db(first_record, last_record)
    if (first_record > record_count or last_record > record_count):
        print(f"[ERROR]: : Records should be between 1 - {record_count}")

    return True

def delete_records(mem_db):
    print("[STATUS]: : Delete Records")
    return True

def update_records(mem_db):
    print("[STATUS]: : Update Records")
    return True

def end_display(mem_db):
    print("[STATUS]: : Exit")
    return END

user_cmds_dict = {'0': end_display,
                  '1': display_records,
                  '2': delete_records,
                  '3': update_records}

def display_and_parse_console(mem_db):
    ret_val = True
    print('File Operations')
    print('[1] Display records')
    print('[2] Delete records')
    print('[3] Update records')
    print('[0] Exit')
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

    # 4. Diplay the console for further instructions
    while (display_and_parse_console(csv_table) != END):
        continue

    # Done, shutdown db
    del csv_table