#!/usr/bin/env bash
export PYTHONPATH='.'
export PIPENV_VERBOSITY=-1
pipenv run python3 setup.py
pipenv run python3 fetch_data.py
pipenv run python3 preprocessing.py
pipenv run python3 scale.py
pipenv run python3 train_features.py
pipenv run python3 select_features.py
pipenv run python3 train_all.py
