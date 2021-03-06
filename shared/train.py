import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)
epochs = 1

def clean(df):
    target = df['ConvertedComp']
    df = df.drop(columns=['CompTotal', "Respondent", "ConvertedComp"])
    return df, target


def train_splitted(train: pd.DataFrame, test: pd.DataFrame):
    X_train, y_train = clean(train)
    X_test, y_test = clean(test)
    model = build_and_compile_model()

    history = model.fit(X_train.values, y_train.values,
                        verbose=0,
                        epochs=3, batch_size=1,
                        validation_data=(X_test, y_test))
    return model, history, list(X_train.columns)


def train_on_df(df):

    df, target = clean(df)
    X_train, X_test, y_train, y_test = train_test_split(df, target,
                                                        test_size=0.2)

    model = build_and_compile_model()

    history = model.fit(X_train.values, y_train.values,
                        verbose=0,
                        epochs=1, batch_size=1,
                        validation_data=(X_test, y_test))
    return model, history, list(df.columns)


def build_and_compile_model():
    model = keras.Sequential([
        layers.Dense(1)
    ])

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  metrics=[tf.keras.metrics.MeanSquaredError(),
                           tf.keras.metrics.MeanAbsoluteError()])
    return model
