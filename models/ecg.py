import pandas as pd 
from tensorflow import keras
from tensorflow.keras import utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Conv2D, Flatten, Dense


df_train = pd.read_csv("data/mitbih_train.csv", header=None)
df_test = pd.read_csv("data/mitbih_test.csv", header=None)
df_test_x = pd.read_csv("data/test_data.csv")

X_train = df_train.values[:, :-1]
y_train = df_train.values[:, -1].astype(int)

X_test  = df_test.values[:, :-1]
y_test  = df_test.values[:, -1].astype(int)

# testx,testy = df_test.values[:,-1]
testx,testy = df_test_x.values[:,:-1],df_test_x.values[:,-1].astype(int)

x_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1, 1)
x_test = X_test.reshape(X_test.shape[0], X_test.shape[1],1, 1)
testx = testx.reshape(testx.shape[0],testx.shape[1],1,1)

y_train = utils.to_categorical(y_train)
y_test  = utils.to_categorical(y_test)
testy = utils.to_categorical(testy,num_classes=5)

input_shape = x_train.shape[1:]
num_classes= 5
smodel = Sequential()
smodel.add(InputLayer(input_shape=input_shape))
smodel.add(Conv2D(16, kernel_size=5, activation='relu', padding='same'))
smodel.add(Flatten())
smodel.add(Dense(16))
smodel.add(Dense(num_classes,activation='softmax'))
smodel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
batch_size = 100
num_epochs = 10
shistory = smodel.fit(x_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_data=(testx,testy))

# print(shistory.history["acc"])
# score = smodel.evaluate(x_test,y_test,verbose=2)
# print("Testing")
# smodel.save_model(smodel, 'ecg_cnn.hdf5')

def predict(x_test,y_test,verbose2):
    score = smodel.evaluate(x_test,y_test,verbose=2)
    return score


