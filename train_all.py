import json
import math
import os
import sys

import pandas as pd
from shared.train import train_splitted
import tensorflowjs as tfjs


def main():
    folds = 5
    df = pd.read_json(os.path.join("data", "all_2020.json"), dtype=float,
                      lines=True).fillna(0)

    # Only train on real salary values
    df = df[df['ConvertedComp'] > 0]
    df = df.reset_index()

    size = len(df)
    chunk_size = int(size / folds+1) # adding 1 here, as we always start with chunk from zero
    training_set = list(range(0, size, chunk_size))

    models = []
    histories = []
    all_columns = []

    print(f"Total Records: {size}")

    for index, lower_bound in enumerate(training_set):
        higher_bound = min(lower_bound + chunk_size, size)
        copy_df = df.copy(True)
        print(f"Training fold {index}")
        test_df = copy_df.isin(range(lower_bound, higher_bound))
        training_df = copy_df.drop(range(lower_bound, higher_bound), inplace=False)


        model, history, columns = train_splitted(training_df, test_df)
        print(history.history)
        models.append(model)
        histories.append(history)
        all_columns.append(columns)

    # get winner
    winner_index = 0
    winner_score = math.inf
    for index, history in enumerate(histories):
        for score in history.history['val_mean_squared_error']:
            if score < winner_score:
                winner_index = index
                winner_score = score


    print(f"winning model after kfold: {winner_index}, using for prediction")


    tfjs.converters.save_keras_model(models[winner_index], os.path.join("data", "model", "tfjs_2020.model"))

    with open(os.path.join("data", "meta", "metrics.json"),
              'wt') as feature_list:
        feature_list.write(json.dumps(histories[winner_index].history))

    with open(os.path.join("data", "meta", "feature_list.json"),
              'wt') as feature_list:
        feature_list.write(json.dumps(all_columns[winner_index]))

if __name__ == '__main__':
    main()
