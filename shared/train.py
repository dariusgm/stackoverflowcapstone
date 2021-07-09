from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

def train_on_df(df, full:bool=False):

    if full:
        epochs = 5
    else:
        epochs = 1

    # only use rows with label data
    df = df[df['ConvertedComp'] > 0]
    target = df['ConvertedComp']
    df = df.drop(columns=['CompTotal', "Respondent", "ConvertedComp"])
    X_train, X_test, y_train, y_test = train_test_split(df, target,
                                                        test_size=0.2)


    model = build_and_compile_model()

    history = model.fit(X_train.values, y_train.values,
                        verbose=1,
                        epochs=epochs, batch_size=1,
                        validation_data=(X_test, y_test))
    return model, history

def build_and_compile_model():
    model = keras.Sequential([
        layers.Dense(1)
    ])

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  # optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  metrics=[tf.keras.metrics.MeanSquaredError(), tf.keras.metrics.MeanAbsoluteError()])
    return model
