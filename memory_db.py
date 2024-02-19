'''
This file defines a class that performs CRUD operations.
These operations are done on an in memory DB.
It also supports load and flush operations to a file on disk. 
'''
from pprint import pprint as pp

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
        if self.csv_file_pointer == -1:
            return
        self.csv_file_pointer.close()

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

        pp(header_row)
        pp(data[1:6])
        
        return header_row, data

    def display_db(self, first_row = 0, last_row = 5):
        print(self.header)
        
        # TODO: Add index checking
        start_row = first_row
        stop_row = last_row
        for row in range(start_row, stop_row):
            print(f"Record {row+1}: {self.data[row]}")
    
    def total_records_db(self):
        return len(self.data)
    
class DB_Initialization_Error(Exception):
    def __init__(self, file_name: str, message: str):
        super().__init__()
        self.file_name = file_name
        self.message = message