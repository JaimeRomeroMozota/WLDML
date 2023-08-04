import dataset
import ANN
import numpy as np

def createDataset(text):
    nCases = int(text)
    dataset.createDataset(nCases)


def trainNeuralNetwork():

    # get stored datasets
    allLabels = np.load("./datasets/labels.npy")
    allLabelsPipe = np.load("./datasets/labelsPipe.npy")
    dataPressure = np.load("./datasets/dataPressure.npy")
    dataFlows = np.load("./datasets/dataFlows.npy")

    #2000 random cases for yes/no ANN
    random_indices = np.random.choice(len(dataPressure), size=2000, replace=False)
    data = dataPressure[random_indices]
    labels = allLabels[random_indices]
    split_index = len(dataPressure) // 2

    # Use slicing to get the second half of the arrays
    second_half_dataPressure = dataPressure[split_index:]
    second_half_dataFlows = dataFlows[split_index:]

    ANN.Ann(data, labels)
    ANN.AnnMultiClass(second_half_dataPressure, second_half_dataFlows, allLabelsPipe)

def tryModel(leakChoice,leakPipe=5,leakSplit=0.5):

    dataPressureTry, dataFlowsTry, labelTry, labelsPipeTry = dataset.createCase(leakChoice,leakPipe,leakSplit)
    resultReal,resultPred = ANN.tryAnn(dataPressureTry, labelTry)

    if resultReal == 1:
        resultRealMulti ,resultPredMulti= ANN.tryAnnMulti(dataPressureTry,dataFlowsTry,labelsPipeTry)
    else:
        resultRealMulti = resultPredMulti= None

    return resultReal,resultPred , resultRealMulti,resultPredMulti

