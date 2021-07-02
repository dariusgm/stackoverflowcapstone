import json
import os
import sys

import numpy as np
import pandas as pd
from shared.train import train_on_df
from sklearn.model_selection import train_test_split


def main():
    print("Training on best columns")

    df = pd.read_json(f"all.json", dtype=float, lines=True).fillna(0)
    model, history = train_on_df(df, full=True)

    model.save("2020.model")
    print(history.history)


if __name__ == '__main__':
    main()
