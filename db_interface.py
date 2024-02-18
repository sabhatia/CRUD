# Sample file to do CRUD operations on CSV files

import argparse
import csv
from pprint import pprint as pp
from memory_db import memory_db

def build_parser():

    # Just get the filename for now
    parser = argparse.ArgumentParser(description="A program to do CRUD Ops on CSV files", 
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="filename to load")
    return parser

def open_csv_file(file_path_name):
    """
    Function to open a file

    Input
        Arg: the name of the file to use

    Output
        Status: If the operation succeeded or failed
        file_pointer: pointer to the opened file
    
    """
    file_pointer = -1
    print(f"STATUS: Loading file {file_path_name}")
    mode = 'rw'
    try:
        file_pointer = open(file_path_name) 
        return True, file_pointer
    except FileNotFoundError:
        return False, file_pointer

def load_csv_file(csv_file_pointer):
    data = []
    lines = csv_file_pointer.readlines()
    header_row = lines[0].strip().split(',')
    for line in lines[1:]:
        row = line.strip().split(',')
        data.append(row)

    pp(header_row)
    pp(data[1:6])
    return True, memory_db(header_row, data)

def end_display(mem_db):
    print("%%STATUS%%: Exit")
    return END

def display_records(mem_db):
    record_count = mem_db.total_records_db()
    print("%%STATUS%%: Display Records")
    print("Total Records: ", record_count)
    first_record = int(input("Enter starting range: [0 for all]:"))
    last_record = int(input("Enter last record: "))

    mem_db.display_db(first_record, last_record)
    if (first_record > record_count or last_record > record_count):
        print(f"%%ERROR%%: Records should be between 1 - {record_count}")

    return True

def delete_records(mem_db):
    print("%%STATUS%%: Delete Records")
    return True

def update_records(mem_db):
    print("%%STATUS%%: Update Records")
    return True

def display_and_parse_console(mem_db):
    ret_val = True
    user_cmds_dict = {'0': end_display,
                      '1': display_records,
                      '2': delete_records,
                      '3': update_records}
    print('File Operations')
    print('[1] Display records')
    print('[2] Delete records')
    print('[3] Update records')
    print('[0] Exit')
    user_cmd = input("Your Selection: ")

    if user_cmd in user_cmds_dict.keys():
        ret_val = user_cmds_dict[user_cmd](mem_db)
    else:
        print(f"%%ERROR%%: Invalid entry {user_cmd}. Accepted range 0-3")
    return ret_val

if __name__ == '__main__':

    END = -1
    # Parse the file to read and display a console

    # 1. Build the parser
    cli_parser = build_parser()

    # 2. Parse the file
    args = cli_parser.parse_args()
    csv_file = args.filename
    
    # 3. Ensure file is useable
    file_load_status, file_pointer = open_csv_file(csv_file)
    if file_load_status == False:
        print("%%ERROR%%: Unable to find/load file:", csv_file)
        exit()

    # 4. Read to memory
    file_page_status, csv_table = load_csv_file(file_pointer)
    if file_page_status == False:
        print("%%ERROR%%: Couldn't load file into memory")
        exit()

    # 4. Diplay the console for further instructions
    while (display_and_parse_console(csv_table) != END):
        continue

    # Done, close the file
    file_pointer.close()