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
    model, history = train_on_df(df, full=True)

    model.save(os.path.join("data", "model", "2020.model"))
    tfjs.converters.save_keras_model(model, os.path.join("data", "model", "tfjs_2020.model"))
    print(history.history)




if __name__ == '__main__':
    main()
