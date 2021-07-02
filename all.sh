#!/usr/bin/env bash
export PYTHONPATH='.'
pipenv run python3 setup.py
pipenv run python3 fetch_data.py
pipenv run python3 preprocessing.py
pipenv run python3 train.py
pipenv run python3 select_features.py
pipenv run python3 train_all.py
