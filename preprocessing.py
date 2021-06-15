import os
import pandas as pd
from config import config
import json
import csv

def convert_to_json_by_column(input_path:str, output_path:str, column:str, process_cols:dict)-> None:
    '''
    Convert the content to several json files, splitted by the column name provided.
    
    '''
    with open(output_path, 'wt') as output_file:
        with open(input_path, 'rt') as csvfile:
            file = csv.reader(csvfile, delimiter=',') 
            for line_index, elements in enumerate(file):
                if line_index == 0:
                    # we have the header already
                    continue
                else:
                    # process selected column, 
                    ## for visualisation in jupyter
                    ## for ML Model
                    result_line = process_data(elements, process_cols, column)

                output_file.write(json.dumps(result_line) + '\n')

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
                    # process all column, for spark
                    result_line = process_data(elements, process_cols, None)
                    output_file.write(json.dumps(result_line) + '\n')

    return process_cols
               

def process_data(elements:list, process_cols:dict, column: str) -> dict:
    result_line = {}
    for column_index, e in enumerate(elements):
        column_meta_data = process_cols[column_index] 
        action = column_meta_data['action'] 
        name = column_meta_data['name']
        if column == None or name == column['name']: 
            if action == 'explode':
                key = f"{name}_{e}"
                result_line[key] = 1
            elif action == 'leave':
                key = f"{name}"
                result_line[key] = 1
            
    return result_line

def extract_header(elements:list, leave_cols:list) -> dict:
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
            print(f"IN: {data_path}")
            cols_dict = convert_to_json(input_path=data_path, output_path=json_path, leave_columns=leave_columns)
            # process by columns for visualtisation purpose
            # and for model buliding
            for column_index, column in cols_dict.items():
                if column['name'] not in leave_columns:
                    output_path = os.path.join("cache", f"{year}_{column['name']}.json")
                    print(f"OUT: {output_path}")
                    convert_to_json_by_column(data_path, output_path, column, cols_dict)

if __name__ == '__main__':
    main()