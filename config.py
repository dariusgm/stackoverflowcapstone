import os


config = [
    # {
    #     'year': '2011',
    #     'url': 'https://drive.google.com/uc?export=download&id=0Bx0LyhBTBZQgUGVYaGx3SzdUQ1U',
    #     'packed_path': os.path.join('data','2011.zip'),
    #     'unpack_path': os.path.join('data', 'unpack', '2011.zip'),
    #     'data_path': os.path.join('data', 'unpack', '2011.zip', '2011 Stack Overflow Survey Results.csv')

    # },
    {
        'year': '2012',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrX3JaZWVwWEpHNWM',
        'packed_path': os.path.join('data','2012.zip'),
        'unpack_path': os.path.join('data','unpack','2012.zip'),
        'data_path': os.path.join('data', 'unpack', '2012.zip', '2012 Stack Overflow Survey Results.csv')
    
    },    
    {
        'year': '2013',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrenpPNTc5UE1PYW8',
        'packed_path': os.path.join('data','2013.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2013.zip'),
        'data_path': os.path.join('data', 'unpack', '2013.zip', '2013 Stack Overflow Survey Responses.csv')
    
    },
    {
        'year': '2014',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrempjMktvWFNaQzA',
        'packed_path': os.path.join('data','2014.zip'),
        'unpack_path': os.path.join('data','unpack', '2014.zip'),
        'data_path': os.path.join('data', 'unpack', '2014.zip', '2014 Stack Overflow Survey Responses.csv')
    },
    {
        'year': '2015',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsra1psanV1MEdxZk0',
        'packed_path': os.path.join('data','2015.zip'),
        'unpack_path': os.path.join('data','unpack','2015.zip'),
        'data_path': os.path.join('data', 'unpack', '2015.zip', '2015 Stack Overflow Developer Survey Responses.csv')
    },    
    {
        'year': '2016',
        'url': 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrV0VldnVIT1hyb0E',
        'packed_path': os.path.join('data','2016.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2016.zip'),
        'data_path': os.path.join('data', 'unpack', '2016.zip', '2016 Stack Overflow Survey Results', '2016 Stack Overflow Survey Responses.csv')
    },
    {
        'year': '2017',
        'url': 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM',
        'packed_path': os.path.join('data','2017.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2017.zip'),
        'data_path': os.path.join('data', 'unpack', '2017.zip', 'survey_results_public.csv')
    },
    {
        'json_path': os.path.join('2018.json'),
        'year': '2018',
        'url': 'https://drive.google.com/uc?export=download&id=1_9On2-nsBQIw3JiY43sWbrF8EjrqrR4U',
        'packed_path': os.path.join('data','2018.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2018.zip'),
        'data_path': os.path.join('data', 'unpack', '2018.zip', 'survey_results_public.csv'),
    },
    {
        'year': '2019',
        'url': 'https://drive.google.com/uc?id=1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV&export=download',
        'packed_path': os.path.join('data','2019.zip'),
        'unpack_path': os.path.join('data','unpack', '2019.zip'),
        'data_path': os.path.join('data', 'unpack', '2019.zip', 'survey_results_public.csv'),
        'json_path': os.path.join('2019.json'),
        # 'leave_columns': [ 'Respondent','CompTotal','ConvertedComp']
    },
    {
        'year': '2020',
        'url': 'https://drive.google.com/uc?id=1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB&export=download',
        'packed_path': os.path.join('data', '2020.zip'),
        'unpack_path': os.path.join('data', 'unpack', '2020.zip'),
        'data_path': os.path.join('data', 'unpack', '2020.zip', 'survey_results_public.csv'),
        'json_path': os.path.join('data', '2020.json'),
        'numeric_columns': ['Age', 'Age1stCode', 'YearsCode', 'YearsCodePro', 'WorkWeekHrs'],
        'leave_columns': ['CompTotal', 'Respondent', 'ConvertedComp'],
        # indicating that only one value can be picked
        'exclusive_columns': [
            'CompFreq',
            'Country',
            'CurrencyDesc',
            'CurrencySymbol',
            'EdLevel',
            'Employment',
            'Ethnicity',
            'Hobbyist',
            'JobSat',
            'JobSeek',
            'MainBranch',
            'NEWDevOps',
            'NEWDevOpsImpt',
            'NEWEdImpt',
            'NEWLearn',
            'NEWOffTopic',
            'NEWOnboardGood',
            'NEWOtherComms',
            'NEWOvertime',
            'NEWPurpleLink',
            'NEWSOSites',
            'OpSys',
            'OrgSize',
            'PurchaseWhat',
            'Sexuality',
            'SOAccount',
            'SOComm',
            'SOPartFreq',
            'SOVisitFreq',
            'SurveyEase',
            'SurveyLength',
            'Trans',
            'UndergradMajor',
            'WelcomeChange'
        ]
        #'leave_columns': ['Respondent', 'CompTotal']
    }
]