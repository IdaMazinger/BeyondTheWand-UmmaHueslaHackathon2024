import os

import tensorflow as tf
import numpy as np


def train_wand_gesture():
    counter = 0
    x_list = []
    y_list = []
    for filename in os.listdir('training_data'):
        data = np.genfromtxt('training_data/' + filename, delimiter=',')
        x_value = data[1:, 0:4]
        y_value = [1 if counter < 101 else 0]  # one is gesture, 0 is random
        # X = np.append(X, x_value, axis=0)
        x_list.append(x_value)
        y_list.append(y_value)
        counter += 1

    x_list_padded = tf.keras.preprocessing.sequence.pad_sequences(x_list, padding='post', maxlen=20)
    X = np.array(x_list_padded, dtype=np.float32).reshape(-1, 20*4)
    y = np.array(y_list, dtype=np.float32)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(12, input_shape=(20*4,), activation='relu'))
    model.add(tf.keras.layers.Dense(8, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=500, batch_size=100)

    _, accuracy = model.evaluate(X, y)
    print('Accuracy: ', accuracy)
    model.save('wand_gesture1.keras')


if __name__ == '__main__':
    train_wand_gesture()