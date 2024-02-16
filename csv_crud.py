# Sample file to do CRUD operations on CSV files

import sys
import argparse

def build_parser():

    # Just get the filename for now
    parser = argparse.ArgumentParser(description="A program to do CRUD Ops on CSV files", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help="filename to load")
    return parser


def load_file(file_path_name):
    """
    Function to open a file

    Input
        Arg: the name of the file to use

    Output
        Status: If the operation succeeded or failed
        file_pointer: pointer to the opened file
    
    """
    file_pointer = -1
    print(f"STATUS: Loading file {file_path}")
    mode = 'rw'
    try:
        with open(file_path_name) as file_pointer:
            return True, file_pointer
    except FileNotFoundError:
        return False, file_pointer

def display_and_parse_console():
    print("No options available yet")
    user_cmd = input("Press a key to continue (0 to quit): ")
    if user_cmd == "0":
        return END
    
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
    if load_file(csv_file) == False:
        print("%%ERROR%%: Unable to find/load file:", csv_file)
        exit()

    # 2. Diplay the console for further instructions
    while (display_and_parse_console() != END):
        continue

    file_pointer.close()