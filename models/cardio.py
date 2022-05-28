import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPRegressor


def cardio_predict(X_test, Y_test, mlp_selected):
  Y_pred_test = mlp_selected.predict(X_test)[-20:].round() #np
  print(Y_pred_test)
  print(Y_test[-20:])
  c = 0
  for i in range(20):
    if Y_pred_test[i] == Y_test[i]:
      c+=1
  return c*2


def useCardio():
  data = pd.read_csv ('data/cardio_train.csv', delimiter=';', encoding = "ISO-8859-1")
  data['bmi'] = (data['weight'] / (((data['height']/100)**2))).round(decimals=2)
  data['age_y'] = (data['age']/365).round(decimals=2)
  data['bmi_high'] = (data['bmi'] >= 30).astype(int)
  data = data.drop("age", 1)
  data = data.drop("id", 1)

  dataX = data.iloc[:,[0,1,2,3,4,5,6,7,8,9,11,12,13]]
  dataY = data.iloc[:,10]
  X_train, X_test, Y_train, Y_test = train_test_split(dataX, dataY,random_state=1, test_size=0.2)

  training_accuracy = []
  testing_accuracy = []
  Layer1 = range(10,90,20)
  Layer2 = range(10,90,20)
  LayersComb = len(Layer1)*len(Layer2)
  Step=0
  score=0

  for i in Layer1 :
    for j in Layer2 :
      mlp = MLPRegressor(hidden_layer_sizes=(i,j),activation="logistic" ,random_state=1, max_iter=2000).fit(X_train, Y_train)
      Y_pred_train = mlp.predict(X_train).round()
      training_accuracy.append(accuracy_score(Y_train, Y_pred_train))
      Y_pred_test = mlp.predict(X_test).round()
      acc_score = accuracy_score(Y_test,Y_pred_test)
      testing_accuracy.append(acc_score)
      Step = Step + 1
      if score < acc_score:
          score = acc_score
          best_Layer1 = i
          best_Layer2 = j
          best_Step = Step
      
  mlp_selected = MLPRegressor(hidden_layer_sizes=(70,70),activation="logistic" ,random_state=1, max_iter=2000)
  mlp_selected.fit(X_test, Y_test)

  Y_pred_train = mlp_selected.predict(X_train).round()
  training_accuracy.append(accuracy_score(Y_train, Y_pred_train))

  # Y_pred_test = mlp_selected.predict(X_test).round()
  # acc_score = accuracy_score(Y_test,Y_pred_test)
  # testing_accuracy.append(acc_score)
  
  cardio_predict(X_test, Y_test, mlp_selected) 

# print(training_accuracy[-1])


