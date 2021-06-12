import os
import pandas as pd
from config import config
import json
import csv


def convert_to_json_by_column(input_path:str, output_path:str, column:str)-> None:
    '''
    Convert the content to several json files, splitted by the column name provided.
    
    '''

def convert_to_json(input_path: str, output_path:str, leave_columns) -> None:
    '''
    Convert the content of a csv file to a json, creating a new column for each value found.
    '''
    process_cols = {}
    with open(output_path, 'wt') as output_file:
        with open(input_path, 'rt') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            for line_index, elements in enumerate(file) :
                if line_index == 0:
                    process_cols = extract_header(elements, leave_columns)
                    continue
                else:
                    result_line = process_data(elements, process_cols)

                output_file.write(json.dumps(result_line) + '\n')
                        

def process_data(elements:list, process_cols:dict) -> dict:
    result_line = {}
    for column_index, e in enumerate(elements):
        column_meta_data = process_cols[column_index] 
        action = column_meta_data['action'] 
        name = column_meta_data['name']
        if action == 'explode':
            key = f"{name}_{e}"
            result_line[key] = 1
        elif action == 'leave':
            key = f"{name}"
            result_line[key] = 1
            
    return result_line

def extract_header(elements:list, leave_cols:list):
    process_cols = {}
    for column_index, e in enumerate(elements):
        if e in leave_cols:
            process_cols[column_index] = {'action': 'leave', 'name': e}
        else:
            process_cols[column_index] = {'action': 'explode', 'name': e}
            
    return process_cols


def main():
    os.makedirs('cache', exist_ok=True)
    for element in config:
        if 'leave_columns' in element:
            year = element['year']
            data_path = element['data_path']
            json_path = element['json_path']
            leave_columns = element['leave_columns']
            print(data_path)
            convert_to_json(input_path=data_path, output_path=json_path, leave_columns=leave_columns)



if __name__ == '__main__':
    main()