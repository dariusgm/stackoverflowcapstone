import json
import sys

import numpy as np
import os

import pandas as pd
from keras import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers import Normalization

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)


def build_and_compile_model():
    model = keras.Sequential([
        layers.Dense(1)
    ])

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  # optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  metrics=[tf.keras.metrics.MeanSquaredError(), tf.keras.metrics.MeanAbsoluteError()])
    return model


def off():
    print("Training")
    df = pd.read_csv("2020_filled.csv", dtype=float, sep=",")

    # only use rows with label data
    df = df[df['CompTotal'] > 0]
    print(len(df))
    target = df['CompTotal']
    df = df.drop(columns=['CompTotal', 'CompTotal_NA', 'Respondent'])


def test():
    df = pd.read_json("cache/2020_Age.json", lines=True)


def data():
    for f in os.listdir("features"):
        df = pd.read_json(f"features/{f}", dtype=float, lines=True).fillna(0)

        # only use rows with label data
        df = df[df['CompTotal'] > 0]
        target = df['CompTotal']
        # scale target to 0..1
        target = target / max(target)
        df = df.drop(columns=['CompTotal', "Respondent"])
    return

def main():
    print("Training")
    os.makedirs("metrics", exist_ok=True)
    for f in os.listdir("features"):
        df = pd.read_json(f"features/{f}", dtype=float, lines=True).fillna(0)

        # only use rows with label data
        df = df[df['CompTotal'] > 0]
        target = df['CompTotal']
        # target = target / max(target)
        df = df.drop(columns=['CompTotal', "Respondent"])
        X_train, X_test, y_train, y_test = train_test_split(df, target,
                                                            test_size=0.2)

        # print(X_train.shape, 'train examples')
        # print(X_test.shape, 'test examples')
        #
        # print(y_train.shape, 'train labels')
        # print(y_test.shape, 'test labels')

        # dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).prefetch(tf.data.AUTOTUNE).batch(1)
        model = build_and_compile_model()
        # model.build()
        # print(model.summary())


        history = model.fit(X_train.values, y_train.values,
                            verbose=1,
                            epochs=1, batch_size=1, validation_data=(X_test, y_test))

        if history.history['mean_squared_error'][0] != np.inf:
            print(f"Positive: {f}", file=sys.stderr)
            print(X_train.columns)
            print(history.history)
            with open(f"metrics/{f}", 'wt') as metric_writer:
                metric_writer.write(json.dumps(history.history))



if __name__ == '__main__':
    main()
