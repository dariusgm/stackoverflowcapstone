# Hi!

Welcome to my second capstone project. I generated predictions for job salary based on survey data from stack overflow 2020. You can find the analysis in notebook.ipynb.


If you would like to rebuild the results by yourself, I provided a `Pipfile` with the libs you need.

The code was running on an older mac or on ubuntu - windows may not work.



# Fetching Repository

```bash
git clone https://github.com/dariusgm/stackoverflowcapstone 
```

# Installation
## Native


Install `pyenv` on your platform, see: https://github.com/pyenv/pyenv


```bash
pyenv install 3.9.2
pyenv local 3.9.2
python3 -m pip install --upgrade pip
pip install pipenv
pyenv rehash
echo "installing, this may take some time..."
pipenv install --dev --python 3.9.2 --skip-lock
```

## Using Docker

```bash
sudo docker build -t stackoverflowcapstone .


```
--mount type=bind,source="$(pwd)",target=/app .


# Pipeline
In case you want to run the entire pipeline by yourself, just execute `all.sh` in the project root and be a bit patient - it should be done in about 30 minutes. At the end, it will start a local webserver that serve the trained model in a web app.

# Serving
## Native

In case you want to just serve the model locally, use the build-in python webserver:
`pipenv run python3 -m http.server 8080 --bind localhost`
[http://localhost:8080](http://localhost:8080)


## Using Docker

   

## Repository Structure

Most of the directories will be created while processing, so the (current) view may look different from the provided structure here
```bash
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
├── analysis.ipynb              - report and analysis code for plots and some insides
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
