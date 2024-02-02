import numpy as np
import keras
from keras import layers

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
# model.summary()

batch_size = 128
epochs = 15
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# # https://issint.ru/2023/01/25/nejjroset-na-python-dlja-chajjnikov-prostojj-primer-za-5-minut/?ysclid=lrxj6pih5x335876630
# # https://dzen.ru/a/X2c_BEwHzgYE4j-u
# # https://python.ivan-shamaev.ru/how-to-build-your-own-neural-network-from-scratch-in-python/?ysclid=lrxiy3u2rd545368970
# # https://pythonist.ru/keras-cnn-tutorial/?ysclid=lrxitx7p2c243047278

# # https://github.com/HelloKunal/NeuralNetworks_by_TariqRashid/blob/master/python_jupyter_code.py


# import json
# import numpy as np
# import keras
# from keras import layers

# from NumpyArrayEncoder import NumpyArrayEncoder


# # Model / data parameters
# num_classes = 4
# input_shape = (1,5)

# # # Load the data and split it between train and test sets
# # (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# # # Scale images to the [0, 1] range
# # x_train = x_train.astype("float32") / 255
# # x_test = x_test.astype("float32") / 255
# # # Make sure images have shape (28, 28, 1)
# # x_train = np.expand_dims(x_train, -1)
# # x_test = np.expand_dims(x_test, -1)
# # print("x_train shape:", x_train.shape)
# # print(x_train.shape[0], "train samples")
# # print(x_test.shape[0], "test samples")


# # # convert class vectors to binary class matrices
# # y_train = keras.utils.to_categorical(y_train, num_classes)
# # y_test = keras.utils.to_categorical(y_test, num_classes)

# # Build the model
# # https://keras.io/examples/vision/mnist_convnet/
# # model = keras.Sequential(
# #     [
# #         keras.Input(shape=input_shape),
# #         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
# #         layers.MaxPooling2D(pool_size=(2, 2)),
# #         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
# #         layers.MaxPooling2D(pool_size=(2, 2)),
# #         layers.Flatten(),
# #         layers.Dropout(0.5),
# #         layers.Dense(num_classes, activation="softmax"),
# #     ]
# # )

# model = keras.Sequential(
#     [
#         keras.Input(shape=input_shape),
#         layers.Dense(10, activation="relu"),
#         layers.Dense(num_classes, activation="softmax"),
#     ],
# )

# # model.summary()

# # # Train the model
# # batch_size = 128
# # epochs = 15
# # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# # model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, verbose=0)

# # # Evaluate the trained model
# # score = model.evaluate(x_test, y_test, verbose=0)
# # print("Test loss:", score[0])
# # print("Test accuracy:", score[1])


# config = model.get_config()
# strConfig = json.dumps(config)
# # print(strConfig)

# # new_model = keras.Sequential.from_config(config)
# # model.to_json() and keras.models.model_from_json()

# # keras.layers.Layer.get_weights(): Returns a list of NumPy arrays of weight values.
# # keras.layers.Layer.set_weights(weights): Sets the model weights to the values provided (as NumPy arrays).
# # layer_2.set_weights(layer_1.get_weights())


# # https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork/blob/master/part2_neural_network.ipynb
# # https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork/blob/master/part3_neural_network_mnist_data_with_rotations.ipynb

# # model.get_weights()
# weights = model.get_weights()
# strWeights = json.dumps(weights, cls=NumpyArrayEncoder)
# # print(strWeights)

# newModel = keras.Sequential.from_config(config)
# newModel.set_weights(weights)

# newStrConfig =  json.dumps(newModel.get_config())
# newStrWeights = json.dumps(newModel.get_weights(), cls=NumpyArrayEncoder)

# print (strConfig==newStrConfig, strWeights == newStrWeights)

# model.compile(
#     optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),
#     loss=keras.losses.SparseCategoricalCrossentropy(),
#     metrics=[keras.metrics.SparseCategoricalAccuracy()],
# )
# newModel.compile(
#     optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),
#     loss=keras.losses.SparseCategoricalCrossentropy(),
#     metrics=[keras.metrics.SparseCategoricalAccuracy()],
# )


# x=np.random.randint(-1,  high=2, size=input_shape) - 0.0001
# print (x)
# y1=model.predict(x, batch_size=None, verbose=0, steps=None, callbacks=None)
# print(y1.shape)
# print(y1)

# y2=newModel.predict(x, batch_size=None, verbose=0, steps=None, callbacks=None)
# print(y2.shape)
# print(y2)


# # agent.model.predict(np.array([0,0,0,0]).reshape(1,4),verbose=None)

# # print("Generate predictions for 3 samples")
# # predictions = model.predict(x_test[:3])
# # print("predictions shape:", predictions.shape)
