import numpy as np

import tensorflow as tf


class TrainSnake:
    def __init__(self, train_x, train_y):
        self.train_x = train_x
        self.train_y = train_y

    def create_training_model(self):
        # model = tf.keras.Sequential()
        # model.add(tf.keras.layers.Dense(units=9, input_dim=7))
        #
        # model.add(tf.keras.layers.Dense(units=15, activation='relu'))
        # model.add(tf.keras.layers.Dense(units=1, activation='softmax'))
        #
        # model.compile(loss='mean_squared_error', optimizer='adam',
        #               metrics=['accuracy'])
        # print(model.summary)
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(units=25, activation='relu',
                                        input_shape=(7, 1)))
        model.add(tf.keras.layers.Dense(units=1, activation='linear'))
        opt = tf.keras.optimizers.Adam(learning_rate=0.01, beta_1=0.9,
                                       beta_2=0.999, epsilon=1e-07,
                                       amsgrad=False, name='Adam')
        model.compile(optimizer=opt, loss='mse')
        print(model.summary())
        model.fit((np.array(self.train_x).reshape(-1, 7, 1)),
                  (np.array(self.train_y).reshape(-1, 3, 1)),
                  batch_size=256, epochs=300)

        model.save_weights('model.h5')
        model_json = model.to_json()
        with open('model.json', 'w') as json_file:
            json_file.write(model_json)
