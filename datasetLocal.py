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
 
    #selected pipes and nodes
    selectedNodes = ["1","23","24","25","26","27","33"]
    selectedPipes = ["23","24","25","26","27","38","39"]

    # Create numpy array
    pressureNoLeak = np.zeros((nCases, len(selectedNodes)))
    pressureLeak=np.zeros((nCases, len(selectedNodes)))
    flowsNoLeak = np.zeros((nCases, len(selectedPipes)))
    flowsLeak = np.zeros((nCases, len(selectedPipes)))
    labelsNoLeak = np.zeros((nCases,1)) 
    labelsLeak=np.zeros((nCases,1))
    labelsPipe = np.zeros((nCases,len(selectedPipes)))

    #Loop to create non-leaking cases
    for i in range(0, nCases):

        inp_file = "./Networks/Djurdevik.inp"
        wn = wntr.network.WaterNetworkModel(inp_file)
        # Assign random Roughness to the pipe with uniform distribution
        setRandomRoughness(wn, 0.01, 0.03)

        # Iterate over the user nodes in the network
        setDemand(wn)    
            
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()
        # Plot results on the network
        pressureNoLeak[i, :] = results.node['pressure'].loc[5 * 3600, selectedNodes]
        flowsNoLeak[i, : ] = results.link['flowrate'].loc[5 * 3600, selectedPipes]

        labelsNoLeak [i,0] = 0


    
    #loop to create Leaking cases
    for i in range(0,nCases):

        inp_file = "./Networks/Djurdevik.inp"
        wn = wntr.network.WaterNetworkModel(inp_file)
        
        # Assign random Roughness to the pipe with uniform distribution
        setRandomRoughness(wn, 0.01, 0.03)

        # Iterate over the user nodes in the network
        setDemand(wn)
        
        pipeLeak = random.choice(selectedPipes)


        wn = wntr.morph.split_pipe(wn, pipeLeak, "leak_pipe", 'leak_node',split_at_point=random.random())
        leak_node = wn.get_node('leak_node')
        leak_node.add_leak(wn, area=0.05, start_time=2*3600, end_time=12*3600)

        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()

        
        pressureLeak[i, :] = results.node['pressure'].loc[5 * 3600, selectedNodes]
        flowsLeak[i, :] = results.link['flowrate'].loc[5 * 3600, selectedPipes]

        index= selectedPipes.index(pipeLeak)
        labelsLeak [i,0] = 1
        labelsPipe [i,index] = 1

    dataPressure = np.concatenate((pressureNoLeak, pressureLeak),axis=0)
    dataFlows = np.concatenate((flowsNoLeak, flowsLeak),axis=0)
    data = np.concatenate((dataPressure, dataFlows),axis=1)
    labels = np.concatenate((labelsNoLeak, labelsLeak),axis=0)
    
    
    np.save("./datasetsLocal/dataPressure",dataPressure)
    np.save("./datasetsLocal/dataFlows",dataFlows)
    np.save("./datasetsLocal/data",data)
    np.save("./datasetsLocal/labels",labels)
    np.save("./datasetsLocal/labelsPipe",labelsPipe)



def createCase (leakChoice, pipeChoice,splitChoice):

    selectedNodes = ["1","23","24","25","26","27","33"]
    selectedPipes = ["23","24","25","26","27","38","39"]
    
    inp_file = "./Networks/Djurdevik.inp"
    wn = wntr.network.WaterNetworkModel(inp_file)

    # Create numpy array
    pressure= np.zeros((1, len(selectedNodes)))
    label = np.zeros((1,1))
    labelsPipe = np.zeros((1,len(selectedPipes)))
    flows =  np.zeros((1,len(selectedPipes)))
     

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

        pressure[0,:] = results.node['pressure'].loc[5 * 3600,selectedNodes]
        
        flows[0, :] = results.link['flowrate'].loc[5 * 3600, selectedPipes]
        
        label [0,0] = 1

        index= selectedPipes.index(pipeChoice)
        labelsPipe[0,index] = 1

    else:
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()
        # Plot results on the network
        pressure[0, :] = results.node['pressure'].loc[5 * 3600,selectedNodes]
        flows[0,:] = results.link['flowrate'].loc[5 * 3600, selectedPipes]
        label [0,0] = 0


    return pressure,flows,label,labelsPipe


