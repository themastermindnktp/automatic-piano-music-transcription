import os
import sys
from math import floor

import matplotlib.pyplot as plt
import numpy as np

from tensorflow import keras

from amt.converter import CONVERTER_FOLDER
from amt.converter.transform import transform

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def predict_cnn(file_name):
    transform(file_name)
    nn = keras.models.load_model('amt/models/cnn.h5')

    X = np.loadtxt(f"{CONVERTER_FOLDER}/transform.txt")

    n = floor(X.shape[0] / 5)
    X_dim = X.shape[1]
    X_train = X[0:5 * n].reshape(n, 5, X_dim, 1)

    y = nn.predict(X_train)

    np.savetxt(f"{CONVERTER_FOLDER}/result.txt", y, fmt="%4f")
