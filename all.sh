#!/usr/bin/env bash
export PYTHONPATH='.'
export PIPENV_VERBOSITY=-1
echo "Setup"
pipenv run python3 setup.py
echo "Fetching Data"
pipenv run python3 fetch_data.py
echo "Preprocessing"
pipenv run python3 preprocessing.py
echo "MinMax"
pipenv run python3 minmax.py
echo "Reject"
pipenv run python3 reject.py
echo "Scale"
pipenv run python3 scale.py
echo "Training Features"
pipenv run python3 train_features.py
echo "Select Features"
pipenv run python3 select_features.py
echo "Training on best features"
pipenv run python3 train_all.py
echo "Generating Template"
pipenv run python3 template.py
curl https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js -o js/tf.min.js
curl https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js.map -o js/tf.min.js.map

pipenv run python3 blog.py
# this is just do get the data into the blog, as the blog is (currently) a private repository
pipenv run python3 blog_copy.py
echo "Done, surving app on localhost:8080"
pipenv run python3 -m http.server 8080 --bind localhost


