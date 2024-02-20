'''
This file defines a class that performs CRUD operations.
These operations are done on an in memory DB.
It also supports load and flush operations to a file on disk. 
'''
from pprint import pprint as pp
import csv
import shutil

class memory_db:
    def __init__(self, csv_filename: str):

        self.csv_filename = csv_filename     
        self.csv_file_pointer = -1
        try:   
            self.csv_file_pointer= open(self.csv_filename, mode='r') 
        except FileNotFoundError as fe:
            raise DB_Initialization_Error(csv_filename, 
                                          "Could not open file: " + csv_filename)
        
        self.header, self.data = memory_db.load_csv_file(self.csv_file_pointer)

    def __del__(self):
        self.csv_file_pointer.close()

        # Create a backup - just in case
        file_extention = ".bak"
        shutil.copy2(self.csv_filename, self.csv_filename + file_extention)

        # Dump contents to file
        with open(self.csv_filename, 'w', newline="") as new_csv_fp:
            writer = csv.writer(new_csv_fp)
            writer.writerow(self.header)
            writer.writerows(self.data)

    @staticmethod
    def open_csv_file(file_path_name: str):
        """
        Function to open a file

        Input
            Arg: the name of the file to use

        Output
            Status: If the operation succeeded or failed
            file_pointer: pointer to the opened file
        
        """
        file_pointer = -1
        print(f"[STATUS]: : Loading file {file_path_name}")
        mode = 'rw'
        return open()

    @staticmethod    
    def load_csv_file(csv_file_pointer):
        data = []
        lines = csv_file_pointer.readlines()
        header_row = lines[0].strip().split(',')
        for line in lines[1:]:
            row = line.strip().split(',')
            data.append(row)
        return header_row, data

    def display_recs(self, first_row = 1, last_row = 5):
        total_recs = self.total_records_db()

        # First verify the indices
        # Lists use 0-based indexing
        # DB uses 1-based indexing
        # Rules
        # 0 based index: [0:len-1] - [1:len]
        # 1 based index: [1: len] - [2:len+1]

        assert(first_row > 0 and first_row <= total_recs)
        assert(last_row > first_row and last_row <= total_recs + 1)
        print(self.header)
        
        # TODO: Add index checking
        start_row = first_row - 1
        stop_row = last_row - 1
        for row in range(start_row, stop_row):
            print(f"Record {row+1}: {self.data[row]}")
    
    def delete_recs(self, del_row):
        if (del_row < 1 or del_row > self.total_records_db()):
            print(f"[ERROR]: Invalid index {del_row}. Acceptable range {1 - self.total_records_db()}")
            return False
        
        del self.data[del_row - 1]
        return True

    def total_records_db(self):
        return len(self.data)
    
class DB_Initialization_Error(Exception):
    def __init__(self, file_name: str, message: str):
        super().__init__()
        self.file_name = file_name
        self.message = message