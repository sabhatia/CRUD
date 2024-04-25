''' 
This script reads a CSV file and stores it both in json format and redis format
To-Do: Add options for JSON and REDIS
'''
import csv
import json
import redis

from pprint import pprint

def csv_to_json(file_in, file_out):
    data = []
    success = True
    csv_file, json_file = None, None
    try:
        # Open the CSV file
        csv_file = open(file_in, 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

        # Open the json file
        json_file = open(dst_file, 'w')
        json.dump(data, json_file)

    except Exception as e:
        print(f'Encountered error: {e}')
        success = False
    finally:
        if (csv_file != None):
            csv_file.close()
        if (json_file != None):
            json_file.close()
    
    # Everything looks good
    return success

def csv_to_redis(file_in):

    data = []
    success = True

    csv_file, redis_client = None, None
    try:
        # Open the CSV file
        csv_file = open(file_in, 'r')
        csv_reader = csv.reader(csv_file)

        # Open Redis connection
        redis_client = redis.Redis(host='localhost', port=6379)

        # Read in the data
        for row in csv_reader:
            redis_client.rpush('employee', str(row))
   
    except Exception as e:
        print(f'Encountered error: {e}')
        success = False
    
    finally:
        if (csv_file != None):
            csv_file.close()
        if (redis_client != None):
            redis_client.close()

    # Everything looks good
    return success

if __name__ == '__main__':

    # TO-DO: Use args for this
    src_file = './parser/employee.csv'
    dst_file = './parser/employee.json'

    # Convert to JSON
    csv_json_res = csv_to_json(src_file, dst_file)
    if (csv_json_res == False):
        print("ERROR: Conversion to json failed.")

    # Insert to REDIS
    csv_redis_res = csv_to_redis(src_file)
    if (csv_redis_res == False):
        print("ERROR: Conversion to Redis failed.")