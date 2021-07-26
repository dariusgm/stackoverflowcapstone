# stackoverflow capstone project

This project contains code for my solution for the "capstone" project at he nanodegree of udacity, data science.

# Fetching Repository

```
git clone https://github.com/dariusgm/stackoverflowcapstone 
```


# Installation Native

You can install a webserver in case you want to play around with the code and add external resources to it. When you want to use python:

Install pyenv on your platform, see: https://github.com/pyenv/pyenv

```
pyenv install 3.9.2
pyenv local 3.9.2
python3 -m pip install --upgrade pip
pip install pipenv
pyenv rehash
pipenv install --dev --python 3.9.2 --skip-lock
pipenv shell
```

# Stackoverflow Capstone Project



### Instructions:
1. Run the following commands in the project's root directory to set up everything.
	
```bash
all.sh
```

This will do the entire processing of the data, allowing you to serve the trained model using localhost:8000

2. Run the following command in the app's directory to run your web app.
    `pipenv run python3 -m http.server 8080 --bind localhost`

3. Go to http://localhost:8080/
4. Here you can do predictions using the created model and the input you provide for the features
5. If you are interested in the analysis, run `pipenv run jupyter-notebook` and open `analysis.ipynb`. 
   You can inspect the output directly using a normal html browser by opening `analysis.html`.

## Repository Structure

Most of the directories will be created while processing, so the (current) view may look different from the provided structure here
```
├── data
│   ├── features - Contains files where each feature (group may be a better name) is stored
│   ├── meta     - Meta Information on the data
│   │   ├──  feature_list.json     - List of all features that should be considered when building up the final model (and for predictions)
│   │   ├──  max.json     - max values of all features. Needed for outlier detection and scaling.
│   │   ├──  min.json     - min values of all features. Needed for outlier detection and scaling.
│   │   └──  reject.json  - Responses that should be rejected from the dataset, as they are outliers.
│   ├── metrics
│   │   └──  <year>_<group>.json  - Quality of the group for predicting the salary (only based on this group)
│   ├── model
│   │   └──  tfjs_2020.model  - final tensorflow js model used for predictions
│   │        ├── group1-shard1of1.bin - tensorflow binary data
│   │        └── model.json - meta information for tensorflow model 
│   ├── preprocessing
│   │   └──  <year>_<group>.json  - Preprocessed data for each group
│   ├── unpack
│   │   └──  <year>.zip  - unpacked survey data for a given year. The structure is different for each year. (directories)
│   ├── *.zip
│   │   └──  <year>.zip  - packed raw data for a particular year. (files)
│   ├── 2020.json - Unscaled combined data from all features, missing na values
│   └── all_2020.json - Scaled combined data from all features
├── js
│   ├── capstone.js - Javascript code for model initialisation and value selection from user input
│   ├── tf.min.js - minified tensorflow js
│   └── tf.min.js.map - SourceMap file for tensorflow js
├── shared
│   ├── __ini__.py - init file
│   └── train.py - Code for execute the training steps (on features and on the full feature set)
├── .gitignore
├── .python-version             - sets the python version for pyenv
├── all.sh                      - run the entire pipeline (in the correct order) for create a model and serve the app
├── analysis.html               - html version of analysis.ipynb
├── analysis.ipynb              - analysis code for plots and some insides
├── blog.py                     - convert the index.html to a format that can be included in the pelican based blog
├── blog_copy.py                - copy required data for the blog to the correct place for serving by the blog
├── capstone.html               - converted index.html file to make it compatible for pelican blog
├── config.py                   - configuration for raw data (sources, exclusiveness and more)
├── fetch_data.py               - download raw data from google drive
├── index.html                  - ready to use tiny app for making predictions (without pelican code modifications)
├── LICENCE                     - licence file
├── minmax.py                   - calculate min and max values for each feature. required for scaling.
├── Pipefile                    - dependency management file using `pipenv`
├── preprocessing.py            - create new columns out of selections from the answers. respect categorical or numerical features.
├── README.md                   - this file
├── reject.py                   - based on min/max values, select outliers that should be rejected from the dataset
├── scale.py                    - scale all features
├── select_features.py          - based on calculated metrics, select features that should be used in final model
├── setup.py                    - create required directory strcture
├── template.py                 - generate html template (for direct usage)
├── train_all.py                - train model based on the best selected features
├── train_features.py           - train model for each feature group and write metrics
```
