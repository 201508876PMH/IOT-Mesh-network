import pandas as panda
import os
import matplotlib.pyplot as plt
import networkx as nx
from tabulate import tabulate

class MeshDataAnalyser():
    def __init__(self):
        pass

    def load_data_table(self, csv_file_name):
        csv_path = os.path.join(".", "CSV_files/" ,csv_file_name)

        data_frame = panda.read_csv(csv_path, nrows=5)
        print(tabulate(data_frame, headers='keys', tablefmt='psql'))
        
        return data_frame

    def plot_data(self, data_frame):
        router_cords = (0,0)
        print(data_frame.keys())
        neighbor1 = (0, (data_frame["RX_neighbor1"].values[0]+ data_frame["TX_neighbor1"].values[0])/2)
        neighbor2 = (0, (data_frame["RX_neighbor2"].values[0] + data_frame["TX_neighbor2"].values[0])/2 )

        #G=nx.Graph()
        ## a list of nodes:
        #G.add_nodes_from(["router","neigbor1", "neigbor2"])
        #G.add_edge("router", )
#
#
        plt.scatter(router_cords[0], router_cords[1], s=300, c="black",  label=f"Router", alpha=0.6)
        plt.scatter(router_cords[0], router_cords[1], s=200, c="red",  label=f"Router", alpha=0.6)
        plt.scatter(neighbor1[0], neighbor1[1], s=200, c="blue",  label=f"neigbor1", alpha=0.6)
        plt.scatter(neighbor2[0], neighbor2[1], s=200, c="yellow",  label=f"neigbor2", alpha=0.6)
        plt.show()
        print(f"n1 {neighbor1}")
        print(f"n2 {neighbor2}")