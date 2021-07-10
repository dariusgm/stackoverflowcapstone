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
pipenv run python3 template.py
curl https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js -o js/tf.min.js
curl https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js.map -o js/tf.min.js.map
pipenv run python3 -m http.server 8080 --bind localhost

