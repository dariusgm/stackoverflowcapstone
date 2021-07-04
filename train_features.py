import json
import os
import sys

import numpy as np
import pandas as pd
from shared.train import train_on_df
from sklearn.model_selection import train_test_split


def main():
    print("Training Features")
    for f in os.listdir(os.path.join("data", "features")):
        df = pd.read_json(os.path.join("data", "features", f), dtype=float, lines=True).fillna(0)
        _model, history = train_on_df(df)

        # only use rows with label data
        if history.history['mean_squared_error'][0] != np.inf:
            with open(os.path.join("data", "metrics", f), 'wt') as metric_writer:
                metric_writer.write(json.dumps(history.history))


if __name__ == '__main__':
    main()
