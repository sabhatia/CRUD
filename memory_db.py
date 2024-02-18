'''
This file defines a class that performs CRUD operations.
These operations are done on an in memory DB.
It also supports load and flush operations to a file on disk. 
'''
from pprint import pprint

class memory_db:
    def __init__(self, header, data):
        self.header = header
        self.data = data

    def display_db(self, first_row = 0, last_row = 5):
        print(self.header)
        
        # TODO: Add index checking
        start_row = first_row
        stop_row = last_row
        for row in range(start_row, stop_row):
            print(f"Record {row+1}: {self.data[row]}")
    
    def total_records_db(self):
        return len(self.data)