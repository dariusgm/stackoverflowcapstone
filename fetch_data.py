import requests
import os
from zipfile import ZipFile
import pandas as pd

urls = [
    {
        'year': '2011',
        'url': 'https://drive.google.com/uc?export=download&id=0Bx0LyhBTBZQgUGVYaGx3SzdUQ1U',
        'local_path': os.path.join('data','2011.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2011.zip'),
        'data_path': os.path.join('data', 'unpack', '2011.zip', '2011 Stack Overflow Survey Results.csv')

    },
    {
        'year': '2012',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrX3JaZWVwWEpHNWM',
        'local_path': os.path.join('data','2012.zip'),
        'unpack_path': os.path.join('data','unpack','2012.zip'),
        'data_path': os.path.join('data', 'unpack', '2012.zip', '2012 Stack Overflow Survey Results.csv')
    
    },    
    {
        'year': '2013',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrenpPNTc5UE1PYW8',
        'local_path': os.path.join('data','2013.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2013.zip'),
        'data_path': os.path.join('data', 'unpack', '2013.zip', '2013 Stack Overflow Survey Responses.csv')
    
    },
    {
        'year': '2014',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrempjMktvWFNaQzA',
        'local_path': os.path.join('data','2014.zip'),
        'unpack_path': os.path.join('data','unpack', '2014.zip'),
        'data_path': os.path.join('data', 'unpack', '2014.zip', '2014 Stack Overflow Survey Responses.csv')
    },
    {
        'year': '2015',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsra1psanV1MEdxZk0',
        'local_path': os.path.join('data','2015.zip'),
        'unpack_path': os.path.join('data','unpack','2015.zip'),
        'data_path': os.path.join('data', 'unpack', '2015.zip', '2015 Stack Overflow Developer Survey Responses.csv')
    },    
    {
        'year': '2016',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrV0VldnVIT1hyb0E',
        'local_path': os.path.join('data','2016.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2016.zip'),
        'data_path': os.path.join('data', 'unpack', '2016.zip', '2016 Stack Overflow Survey Results', '2016 Stack Overflow Survey Responses.csv')
    },
    {
        'year': '2017',
        'url': 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM',
        'local_path': os.path.join('data','2017.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2017.zip'),
        'data_path': os.path.join('data', 'unpack', '2017.zip', 'survey_results_public.csv')
    },
    {
        'year': '2018',
        'url': 'https://drive.google.com/uc?export=download&id=1_9On2-nsBQIw3JiY43sWbrF8EjrqrR4U',
        'local_path': os.path.join('data','2018.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2018.zip'),
        'data_path': os.path.join('data', 'unpack', '2018.zip', 'survey_results_public.csv')
    },

    {
        'year': '2019',
        'url': 'https://drive.google.com/uc?id=1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV&export=download',
        'local_path': os.path.join('data','2019.zip'),
        'unpack_path': os.path.join('data','unpack', '2019.zip'),
        'data_path': os.path.join('data', 'unpack', '2019.zip', 'survey_results_public.csv')
    },
    {
        'year': '2020',
        'url': 'https://drive.google.com/uc?id=1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB&export=download',
        'local_path': os.path.join('data','2020.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2020.zip'),
        'data_path': os.path.join('data', 'unpack', '2020.zip', 'survey_results_public.csv')
    }
]

def fetch():
    for element in urls:
        
        url = element['url']
        local_path = element['local_path']
        # Inspired by https://365datascience.com/tutorials/python-tutorials/python-requests-package/
        if not os.path.exists(local_path):
            print(f"fetching {url}")
            with requests.get(url, stream = True) as stream:
                with open(local_path, 'wb') as target_file:
                    for chunk in stream.iter_content(chunk_size = 1024 * 1024):
                        target_file.write(chunk)
        else:
            print(f"file {local_path} exists, skipping")

def unpack():
    for element in urls:
        local_path = element['local_path']
        unpack_path = element['unpack_path']
        if not os.path.exists(unpack_path):
            print(f"unpacking {local_path}")
            with ZipFile(local_path, 'r') as zipObj:
                zipObj.extractall(unpack_path)
        else:
            print(f"direcory {unpack_path} exists, skipping")

def analyse():
    for element in urls:
        data_path = element['data_path']
        df = pd.read_csv(data_path, dtype=str)
        columns = df.columns
        size = len(df)
        print("")
        print(f' path: {data_path}, size: {size}, columns: {len(columns)}')
        # for col in columns:
        #    print(f"  {col}")

def main():
    os.makedirs(os.path.join('data', 'unpack'), exist_ok = True)
    fetch()
    unpack()
    analyse()

if __name__ == '__main__':
    main()

