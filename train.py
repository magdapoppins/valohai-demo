import os
import json
import numpy as np
import tensorflow as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--epoch', type=int, default=5)
parser.add_argument('--learning_rate', type=float, default=0.01)
args = parser.parse_args()


input_path = os.getenv('VH_INPUTS_DIR', './inputs')
f = os.path.join(input_path, 'mnist/mnist.npz')

with np.load(f, allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

def log(epoch, logs):
    print()
    print(json.dumps({
        'epoch': epoch,
        'loss': str(logs['loss']),
        'acc': str(logs['acc'])
    }))

cb = tf.keras.callbacks.LambdaCallback(on_epoch_end=log)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=args.learning_rate),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.fit(x_train, y_train, epochs=args.epoch, callbacks=[cb])

model.evaluate(x_test,  y_test, verbose=2)

path = os.getenv('VH_OUTPUTS_DIR', './outputs')

model.save(os.path.join(path, 'my_model.h5'))
