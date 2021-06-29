import numpy as np

# Make numpy printouts easier to read.
import pandas as pd

np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

def build_and_compile_model(size):
    model = keras.Sequential([
        layers.InputLayer(input_shape=(None, size)),
        # layers.Dense(512, activation='relu'),
        # layers.Dense(256, activation='relu'),
        # layers.Dense(128, activation='relu'),
        # layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(loss='mean_absolute_error',
                  optimizer=tf.keras.optimizers.Adam(0.001))
    return model

def main():
    print("Training")
    dataset = pd.read_csv("2020_filled.csv", dtype=float, sep=",")

    # only use rows with label data
    dataset = dataset[~ dataset['CompTotal'].isna()]
    print(len(dataset))
    label = dataset['CompTotal']
    dataset.drop("CompTotal", inplace=True, axis=1)
    dataset.drop("CompTotal_NA", inplace=True, axis=1)
    features = dataset.fillna(0.0)
    model = build_and_compile_model(len(dataset.columns))
    model.build()

    history = model.fit(
        x=features.to_numpy(), y=label,
        verbose=1, epochs=100)
    print(model.summary())
    print(history)

if __name__ == '__main__':
    main()