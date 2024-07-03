# -*- coding: utf-8 -*-
"""alphabet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1torEZxCQqNzdty7TAf2zwT-YcVQNfRpf
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import cv2
from random import randint
from google.colab.patches import cv2_imshow
from google.colab.files import upload
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_squared_error as mse
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from tensorflow import keras

! pip install -q kaggle
! mkdir ~/.kaggle
! cp ./kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download -d sachinpatel21/az-handwritten-alphabets-in-csv-format
! unzip az-handwritten-alphabets-in-csv-format.zip

add = './A_Z Handwritten Data.csv'
da = pd.read_csv(add)

y = da['0']
X = da.drop(['0'], axis=1)
alpha = {0: 'a',
         1: 'b',
         2: 'c',
         3: 'd',
         4: 'e',
         5: 'f',
         6: 'g',
         7: 'h',
         8: 'i',
         9: 'j',
         10: 'k',
         11: 'l',
         12: 'm',
         13: 'n',
         14: 'o',
         15: 'p',
         16: 'q',
         17: 'r',
         18: 's',
         19: 't',
         20: 'u',
         21: 'v',
         22: 'w',
         23: 'x',
         24: 'y',
         25: 'z'}

y = y.replace(alpha)
X.where(da < 105, 1, inplace=True)
X.where(da >= 105, 0, inplace=True)
X.to_csv('X.csv', index=False)
y.to_csv('y.csv', index=False)

X = pd.read_csv('./X.csv')
y = pd.read_csv('./y.csv',squeeze=True)

from google.colab import drive
drive.mount('/content/drive')

r = randint(0, X.shape[0])
img_sample_X = X.iloc[r].replace({1:255}).values.reshape(28, 28)
img_sample_y = y[r]
cv2_imshow(img_sample_X)
print(img_sample_y.upper())

lb = LabelBinarizer()
y = lb.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.95)

model_ann = keras.models.Sequential([
                                 keras.layers.Dense(units=28 * 28 * 2, activation='relu', input_shape=(28 * 28,)),

                                 keras.layers.Dense(units=28 * 28 * 1.5, activation='relu'),

                                 keras.layers.Dense(units=28 * 28, activation='relu'),

                                 keras.layers.Dense(units=28 * 28 / 2, activation='relu'),

                                 keras.layers.Dense(units=512, activation='relu'),
                                 
                                 keras.layers.Dense(units=128, activation='relu'),

                                 keras.layers.Dense(units=26, activation='softmax')
                                 ])
model_ann.compile(optimizer='Adagrad', loss='categorical_crossentropy', metrics=['accuracy'])
model_ann.summary()

history = model_ann.fit(X_train, y_train, batch_size=60, epochs=35, validation_data=(X_test, y_test))

plt.figure(figsize=(16, 10))
plt.grid(axis='both', ls=':', color='k')
plt.xlim((1, 35))
plt.xticks(range(1, 36, 2))
plt.yticks(np.linspace(0, 1.0659, 10).tolist())
plt.plot(range(1, 36), history.history['loss'],
         range(1, 36), history.history['accuracy'],
         range(1, 36), history.history['val_loss'],
         range(1, 36), history.history['val_accuracy'], marker='.')
plt.legend([*history.history], loc='center right')
plt.show()

pres = model_ann.predict(X_test)
un_dic = np.argmax(pres, axis=1)
y_pred = pd.Series(alpha)[un_dic].values

classes = range(26)
y_test = pd.Series(alpha)[y_test.dot(classes)].values

(y_pred==y_test).sum() / y_pred.size * 100

model_ann.save('./alpha_model/')
