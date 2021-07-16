import csv
import json
import os

import numpy as np
from config import config


def convert_to_json_by_column(input_path: str, output_path: str, column: str,
                              process_cols: dict) -> None:
    """
    Convert the content to several json files, splitted by the column name provided.
    """

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


def convert_to_json(input_path: str, output_path: str, leave_columns,
                    numeric_columns) -> (dict, dict):
    """
    Convert the content of a csv file to a json, creating a new column for each value found.
    """
    process_cols = {}
    with open(output_path, 'wt') as output_file:
        with open(input_path, 'rt') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            for line_index, elements in enumerate(file):
                if line_index == 0:
                    process_cols = extract_header(elements, leave_columns,
                                                  numeric_columns)
                    continue
                else:
                    # process all column, for spark
                    result_line = process_data(elements, process_cols, None)
                    output_file.write(json.dumps(result_line) + '\n')

    return process_cols


def is_na(e):
    if type(e) == list:
        return all(lambda x: is_na(x), e)
    # convert string "NA" to NA column
    if type(e) == str and e == 'NA':
        return True
    # convert float na to NA column
    elif type(e) == float and np.isna(e):
        return True
    return False


def process_data(elements: list, process_cols: dict, column: str) -> dict:
    result_line = {}
    for column_index, e in enumerate(elements):
        column_meta_data = process_cols[column_index]
        action = column_meta_data['action']
        name = column_meta_data['name']

        # always pass Respondent id for later merging
        # convert label to 0 in case it not exists, will be removed before training
        if action == 'leave':
            if e == 'NA':
                result_line[name] = 0
            else:
                result_line[name] = e

        if column == None or name == column['name']:
            if (is_na(e)):
                key = f"{name}_NA"
                result_line[key] = 1
                continue

            elif action == 'explode':
                # explode values in case of multiple possible answers
                # still they can be nans
                if ';' in e:
                    for nested_element in e.split(';'):
                        if (is_na(e)):
                            key = f"{name}_NA"
                            result_line[key] = 1
                        else:
                            key = f"{name}_{nested_element}"
                            result_line[key] = 1
                else:
                    key = f"{name}_{e}"
                    result_line[key] = 1
            elif action == 'numeric':
                key = f"{name}"
                # handle "Younger than 5 years" answer for Age1Code
                try:
                    float(e)
                    result_line[key] = e
                except:
                    if (e == 'NA'):
                        print("a")
                    key = f"{name}_{e}"
                    result_line[key] = 1

    return result_line


def extract_header(elements: list, leave_cols: list,
                   numeric_cols: list) -> dict:
    process_cols = {}
    for column_index, e in enumerate(elements):
        if e in leave_cols:
            process_cols[column_index] = {'action': 'leave', 'name': e}
        elif e in numeric_cols:
            process_cols[column_index] = {'action': 'numeric', 'name': e}
        else:
            process_cols[column_index] = {'action': 'explode', 'name': e}

    return process_cols


def main():
    for element in config:
        if 'leave_columns' in element:
            year = element['year']
            data_path = element['data_path']
            json_path = element['json_path']
            leave_columns = element['leave_columns']
            numeric_columns = element['numeric_columns']
            print(f"IN: {data_path}")
            cols_dict = convert_to_json(
                input_path=data_path,
                output_path=json_path,
                leave_columns=leave_columns,
                numeric_columns=numeric_columns
            )

            # process by columns for visualisation purpose
            # and for model building
            for column_index, column in cols_dict.items():
                if column['name'] not in leave_columns:
                    output_path = os.path.join('data', 'preprocessing',
                                               f"{year}_{column['name']}.json")
                    if not os.path.exists(output_path):
                        print(f"OUT: {output_path}")
                        convert_to_json_by_column(data_path, output_path,
                                                  column, cols_dict)


if __name__ == '__main__':
    main()
