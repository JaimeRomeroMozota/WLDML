import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np

# Función para construir el modelo
def createModelClass(inputSize,outputSize):
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(inputSize,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(outputSize, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])

    return model


def createModelMultiClass(inputSize,outputSize):
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(inputSize,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(outputSize, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['accuracy'])

    return model



# Classification model to find if there is a leak or not.
def Ann (data,labels): 
  
  inputSize = len (data[0,:])
  outputSize = 1
  #normalizedData = tf.keras.utils.normalize(data, axis=0)
  x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42)

  model = createModelClass(inputSize,outputSize)
  print(x_train.shape)
  model.fit(x_train, y_train, epochs=10)

  model.evaluate(x_test,  y_test, verbose=2) 

  model.save("./models/classification")


def AnnMultiClass (dataPressure,dataFlows,labels): 


  normalizedDataPressure = tf.keras.utils.normalize(dataPressure, axis=0)
  normalizedDataFlows = tf.keras.utils.normalize(dataFlows, axis=0)
  normalizedData = np.concatenate((normalizedDataPressure, normalizedDataFlows),axis=1)

  inputSize = len (normalizedData[0,:])

  try:
    outputSize = len(labels[0,:])
  except:
    outputSize = 7
    print("len failed)")

  x_train, x_test, y_train, y_test = train_test_split(normalizedData, labels, test_size=0.2, random_state=42)

  model = createModelMultiClass(inputSize,outputSize)
  print(x_train.shape)
  model.fit(x_train, y_train, epochs=35,verbose = 1)

  model.evaluate(x_test,  y_test, verbose=2) 

  model.save("./models/multiClass")



#Use previously trained NN to find if there is a leak.
def tryAnn (data ,label): 
 
  
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

  





