import wntr
import numpy as np
import random


def setRandomRoughness(wn, roughness_min, roughness_max):
    for pipe_name, pipe in wn.pipes():
        pipe.roughness = np.random.uniform(roughness_min, roughness_max)


def setDemand(wn, demand_ratio_min=0.3, demand_ratio_max=1.3, std_dev=0.05):
    for junction_name, junction in wn.junctions():

        demand_ratio = np.random.uniform(demand_ratio_min, demand_ratio_max)
        # Add noise to the baseline demand
        noise = (np.random.normal(0, std_dev)) / 100
        updated_demand = demand_ratio * junction.demand_timeseries_list[0].base_value + abs(noise)
        junction.demand_timeseries_list[0].base_value = updated_demand


def createDataset (nCases):

    inp_file = "./Networks/Djurdevik.inp"
    wn = wntr.network.WaterNetworkModel(inp_file)
    pipeNames=wn.pipe_name_list 
    pipeNamesSorted = sorted(pipeNames, key=lambda x: int(x))


    # Create numpy array
    pressureNoLeak = np.zeros((nCases, len(wn.node_name_list)))
    pressureLeak=np.zeros((nCases, len(wn.node_name_list)))
    flowsNoLeak = np.zeros((nCases, 35))
    flowsLeak = np.zeros((nCases, 35))
    labelsNoLeak = np.zeros((nCases,1))
    labelsLeak=np.zeros((nCases,1))
    labelsPipe = np.zeros((nCases,len(pipeNamesSorted)))

    #Loop to create non-leaking cases
    for i in range(0, nCases):   
            # Create a water network model
        inp_file = "./Networks/Djurdevik.inp"
        wn = wntr.network.WaterNetworkModel(inp_file)
        # Assign random Roughness to the pipe with uniform distribution
        setRandomRoughness(wn, 0.01, 0.03)

        # Iterate over the user nodes in the network
        setDemand(wn)
                
            
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()
        # Plot results on the network
        pressureNoLeak[i, :] = results.node['pressure'].loc[5 * 3600, :]
        flowsNoLeak[i, : ] = results.link['flowrate'].loc[5 * 3600, :]

        labelsNoLeak [i,0] = 0

    
    #loop to create Leaking cases
    for i in range(0,nCases):

        inp_file = "./Networks/Djurdevik.inp"
        wn = wntr.network.WaterNetworkModel(inp_file)
        
        # Assign random Roughness to the pipe with uniform distribution
        setRandomRoughness(wn, 0.01, 0.03)

        # Iterate over the user nodes in the network
        setDemand(wn)
        
        pipeName = wn.pipe_name_list
        pipeLeak = random.choice(pipeName)


        wn = wntr.morph.split_pipe(wn, pipeLeak, "leak_pipe", 'leak_node',split_at_point=random.random())
        leak_node = wn.get_node('leak_node')
        leak_node.add_leak(wn, area=0.05, start_time=2*3600, end_time=12*3600)

        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()

        pressureLeakNode = results.node['pressure'].loc[5 * 3600, :]
        pressureFinal=pressureLeakNode.pop('leak_node')
        pressureLeak[i, :] = pressureFinal

        flowsLeakLink = results.link['flowrate'].loc[5 * 3600, :]
        flowFinal=flowsLeakLink.pop('leak_pipe')
        flowsLeak[i, :] = flowFinal

        index= pipeNamesSorted.index(pipeLeak)
        labelsLeak [i,0] = 1
        labelsPipe [i,index] = 1

    dataPressure = np.concatenate((pressureNoLeak, pressureLeak),axis=0)
    dataFlows = np.concatenate((flowsNoLeak, flowsLeak),axis=0)
    data = np.concatenate((dataPressure, dataFlows),axis=1)
    labels = np.concatenate((labelsNoLeak, labelsLeak),axis=0)
    
    
    np.save("./datasets/dataPressure",dataPressure)
    np.save("./datasets/dataFlows",dataFlows)
    np.save("./datasets/data",data)
    np.save("./datasets/labels",labels)
    np.save("./datasets/labelsPipe",labelsPipe)


def createCase (leakChoice, pipeChoice,splitChoice):
    
    inp_file = "./Networks/Djurdevik.inp"
    wn = wntr.network.WaterNetworkModel(inp_file)

    pipeNames=wn.pipe_name_list 
    pipeNamesSorted = sorted(pipeNames, key=lambda x: int(x))

    # Create numpy array
    pressure= np.zeros((1, len(wn.node_name_list)))
    label = np.zeros((1,1))
    labelsPipe = np.zeros((1,len(pipeNamesSorted)+1))
    flows =  np.zeros((1,35))
     

    # Assign random Roughness to the pipe with uniform distribution
    setRandomRoughness(wn, 0.01, 0.03)

    # Iterate over the user nodes in the network
    setDemand(wn)

    if (leakChoice == "y"):

        wn = wntr.morph.split_pipe(wn, pipeChoice, "leak_pipe", 'leak_node',split_at_point=splitChoice)
        leak_node = wn.get_node('leak_node')
        leak_node.add_leak(wn, area=0.05, start_time=2*3600, end_time=12*3600)

        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()

        pressureNoLeakNode = results.node['pressure'].loc[5 * 3600, :]
        pressureFinal=pressureNoLeakNode.pop('leak_node')
        pressure[0,:] = pressureFinal
        flowsLeakLink = results.link['flowrate'].loc[5 * 3600, :]
        flowFinal=flowsLeakLink.pop('leak_pipe')
        flows[0, :] = flowFinal
        label [0,0] = 1

        index= pipeNamesSorted.index(pipeChoice)
        labelsPipe[0,index] = 1

    else:
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()
        # Plot results on the network
        pressure[0, :] = results.node['pressure'].loc[5 * 3600, :]
        flows[0,:] = results.link['flowrate'].loc[5 * 3600, :]
        label [0,0] = 0

    return pressure,flows,label,labelsPipe
