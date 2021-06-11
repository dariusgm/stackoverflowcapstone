import os
import pandas as pd
from config import config

# Stolen from myself: https://github.com/dariusgm/stackoverflow2020/blob/main/Blog.ipynb

def to_list(elements) -> list:
    '''
    Return a list of elements that where separated by ";"

    :param elements: the (potencial) elements to convert to a list, can be (str) or (np.nan)
    :returns: (list[str]) list of elements with 0 or more elements
    
    Example:
    >>> import numpy as np; to_list(np.nan)
    []
    
    >>> to_list("c++;c#")
    ["c++", "c#"]
    '''

    if type(elements) != str: # assuming nan
        return []
    else:
        return elements.split(";")
    


def df_to_features(df: pd.DataFrame, column: str) -> list:
    '''
    Explode a column of a pd.DataFrame containing several features
    
    :param df: (pd.DataFrame) DataFrame that have the column to explode
    :param column: (str) The name of the column with the values to explode
    
    :returns: (list[dict]) A list of dicts that have a true value for a particular line
    
    Example:
    >>> df_to_features(pd.DataFrame([{'a': 'b;c'}]), 'a')
    [{'a_b': 1, 'a_c': 1}]
    '''
    
    records = []
    for index, row in df.iterrows():
        line = {}
        elements = to_list(row[column])
        if len(elements)>0:
            for e in elements:
                # comparing to original code, I add here the original column name,
                # preventing collisions with Yes / No Answers
                line[f"{column}_{e}"] = 1
                    
        records.append(line)
        
    return records


def df_extract_features(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Extract features of a particular column and returns the filled pd.DataFrame back
    
    :param df: (pd.DataFrame) The DataFrame with the data to be extracted
    :param column: (str) The column with the data to extract
    :returns: pd.DataFrame with feature columns, filled missing values with 0 
    
    Example:
    >>> df_extract_features(pd.DataFrame([{'a': 'b;c'}, {'a': 'c'}]), 'a')
    pd.DataFrame([{'b': 1.0, 'c': 1}, {'b': 0.0, 'c': 1}])
    '''
    return pd.DataFrame(df_to_features(df, column)).fillna(0.)


def calculate_and_save(df: pd.DataFrame, column:str,  year:int) -> pd.DataFrame:
    '''
    Calculate features and cache result. Further calls will return the precalculated results
    
    :param df: (pd.DataFrame) The DataFrame with the data to be processed
    :param column: (str) The column with the data to process
    :param year: (int) the year of the data, used as cache key
    :returns: go.Figure, ready to use plotly figure
    '''
    
    cache_key = f"{year}_{column}.csv"
    cache_path = os.path.join('cache', cache_key)
    if os.path.exists(cache_path):
        return pd.read_csv(cache_path).set_index('id')
    df = df_extract_features(df, column)
    df.to_csv(cache_path, index_label='id')
    return df

def main():
    os.makedirs('cache', exist_ok=True)
    for element in config:
        if 'columns' in element:
            year = element['year']
            data_path = element['data_path']
            df = pd.read_csv(data_path, dtype=str)
            for col in element['columns']:
                print(f'calculating {col}')
                calculate_and_save(df, col, year)
                



if __name__ == '__main__':
    main()