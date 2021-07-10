import json
import os
import sys

import numpy as np
import pandas as pd
from shared.train import train_on_df
from sklearn.model_selection import train_test_split
import tensorflowjs as tfjs


def main():
    print("Training on best columns")

    df = pd.read_json(os.path.join("data", "all_2020.json"), dtype=float,
                      lines=True).fillna(0)
    model, history, columns = train_on_df(df, full=True)

    tfjs.converters.save_keras_model(model, os.path.join("data", "model", "tfjs_2020.model"))
    print(history.history)
    with open(os.path.join("data", "meta", "metrics.json"),
              'wt') as feature_list:
        feature_list.write(json.dumps(history.history))

    with open(os.path.join("data", "meta", "feature_list.json"),
              'wt') as feature_list:
        feature_list.write(json.dumps(columns))

if __name__ == '__main__':
    main()
