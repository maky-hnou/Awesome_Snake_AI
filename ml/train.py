import numpy as np

import tensorflow as tf


class TrainSnake:
    def __init__(self, train_x, train_y):
        self.train_x = train_x
        self.train_y = train_y

    def create_training_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(units=9, input_dim=7))
        model.add(tf.keras.layers.Dense(units=15, activation='relu'))
        model.add(tf.keras.layers.Dense(units=3,  activation='softmax'))

        model.compile(loss='mean_squared_error',
                      optimizer='adam',
                      metrics=['accuracy'])
        print(model.summary())
        model.fit((np.array(self.train_x).reshape(-1, 7)),
                  (np.array(self.train_y).reshape(-1, 3)),
                  batch_size=512,
                  epochs=500)

        model.save_weights('models/model.h5')
        model_json = model.to_json()
        with open('models/model.json', 'w') as json_file:
            json_file.write(model_json)
