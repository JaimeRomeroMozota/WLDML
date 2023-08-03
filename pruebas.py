import wntr
import numpy as np
import ANN

def getEpanetData():
    
    inp_file = "./Networks/Epanet.inp"
    wn = wntr.network.WaterNetworkModel(inp_file)

    pipeNames=wn.pipe_name_list 
    pipeNamesSorted = sorted(pipeNames, key=lambda x: int(x))

    # Create numpy array
    pressure= np.zeros((1, len(wn.node_name_list)))
    label = np.zeros((1,1))
    labelsPipe = np.zeros((1,len(pipeNamesSorted)+1))
    flows =  np.zeros((1,35))


    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    # Plot results on the network
    pressure[0, :] = results.node['pressure'].loc[5 * 3600, :]
    flows[0,:] = results.link['flowrate'].loc[5 * 3600, :]
    label [0,0] = 1

    index= pipeNamesSorted.index("26")
    labelsPipe[0,index] = 1


    return pressure,flows,label,labelsPipe

if __name__ == "__main__":
    pressure,flows,label,labelsPipe = getEpanetData()

    resultReal,resultPred = ANN.tryAnn(pressure, label)

    if resultReal == 1:
        resultRealMulti ,resultPredMulti= ANN.tryAnnMulti(pressure,flows,labelsPipe)
    else:
        resultRealMulti = resultPredMulti= None
