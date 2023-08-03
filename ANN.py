import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np

# Función para construir el modelo
def createModelClass():
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(36,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])

    return model


def createModelMultiClass():
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(71,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(33, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['accuracy'])

    return model



# Classification model to find if there is a leak or not.
def Ann (data,labels): 
  
  #normalizedData = tf.keras.utils.normalize(data, axis=0)
  x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42)

  model = createModelClass()
  print(x_train.shape)
  model.fit(x_train, y_train, epochs=10)

  model.evaluate(x_test,  y_test, verbose=2) 

  model.save("./models/classification")


def AnnMultiClass (dataPressure,dataFlows,labels): 

  
  normalizedDataPressure = tf.keras.utils.normalize(dataPressure, axis=0)
  normalizedDataFlows = tf.keras.utils.normalize(dataFlows, axis=0)
  normalizedData = np.concatenate((normalizedDataPressure, normalizedDataFlows),axis=1)

  x_train, x_test, y_train, y_test = train_test_split(normalizedData, labels, test_size=0.2, random_state=42)

  model = createModelMultiClass()
  print(x_train.shape)
  model.fit(x_train, y_train, epochs=35,verbose = 1)

  model.evaluate(x_test,  y_test, verbose=2) 

  model.save("./models/multiClass")



#Use previously trained NN to find if there is a leak.
def tryAnn (data ,label,): 
 
  model = tf.keras.models.load_model("./models/classification")
  
  #normalizedData = tf.keras.utils.normalize(data, axis=0)
  results=model.predict(data)

  print (f"Prediction {results}")
  print(f"Real {label}")

  return label,results

def tryAnnMulti (dataPressure,dataFlows ,labelsPipe): 
 

  modelMulti = tf.keras.models.load_model("./models/multiClass")

  normalizedDataPressure = tf.keras.utils.normalize(dataPressure, axis=0)
  normalizedDataFlows = tf.keras.utils.normalize(dataFlows, axis=0)
  normalizedData = np.concatenate((normalizedDataPressure, normalizedDataFlows),axis=1)

  results=modelMulti.predict(normalizedData)


  print (f"Prediction {results}")
  print (f"Prediction index {np.argmax(results)}")
  print (f"Real       {labelsPipe}")
  print (f"Real index       {np.argmax(labelsPipe)}")

  return np.argmax(labelsPipe),np.argmax(results)

  





