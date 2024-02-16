# Sample file to do CRUD operations on CSV files

import argparse
import csv
from pprint import pprint as pp

def build_parser():

    # Just get the filename for now
    parser = argparse.ArgumentParser(description="A program to do CRUD Ops on CSV files", formatter_class=argparse.RawDescriptionHelpFormatter)
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
    for line in lines:
        row = line.strip().split(',')
        data.append(row)

    pp(header_row)
    pp(data[1:6])
    return True, data

def display_records():
    print("Display Records")

def delete_records():
    print("Delete Records")

def update_records():
    print("Update Records")

def display_and_parse_console():
    user_cmds = ['exit', 'display', 'remove', 'update']
    print('File Operations')
    print('[1] Display Contents (All)')
    print('[2] Remove a record')
    print('[3] Update a row')
    print('[0] Exit')
    user_cmd = input("Your Selection: ")

    if user_cmd == '0':
        return END
    elif user_cmd == '1':
        display_records()
    elif user_cmd == '2':
        delete_records()
    elif user_cmd == '3':
        update_records()
    else:
        print(f"%%ERROR%%: Invalid entry {user_cmd}. Accepted range 0-3")
    return True

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
    while (display_and_parse_console() != END):
        continue

    # Done, close the file
    file_pointer.close()