import matplotlib.pyplot as plt
import wntr

def showPipes(wn=None):
    if wn == None:
        inp_file = "./Networks/Djurdevik.inp"
        wn = wntr.network.WaterNetworkModel(inp_file)
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    # Plot the nodes
    for node_name, node in wn.nodes():
        plt.plot(node.coordinates[0], node.coordinates[1], 'bo', markersize=5)
        plt.text(node.coordinates[0], node.coordinates[1], node_name, ha='center', va='bottom', fontsize=6)

    # Plot the pipes
    for pipe_name, pipe in wn.pipes():
        start_node = wn.get_node(pipe.start_node)
        end_node = wn.get_node(pipe.end_node)
        x = [start_node.coordinates[0], end_node.coordinates[0]]
        y = [start_node.coordinates[1], end_node.coordinates[1]]
        plt.plot(x, y, 'k-', linewidth=1)
        plt.text(sum(x) / 2, sum(y) / 2, pipe_name, ha='center', va='center', fontsize=12)

    plt.axis('equal')
    plt.axis('off')
    plt.show()

def getPipeNames():
    inp_file = "./Networks/Djurdevik.inp"
    wn = wntr.network.WaterNetworkModel(inp_file)
    pipeNames=wn.pipe_name_list 
    pipeNamesSorted = sorted(pipeNames, key=lambda x: int(x))
    return pipeNamesSorted

if __name__ == "__main__":
    showPipes()