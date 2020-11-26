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

    def plot_data(self, data_frame_1, data_frame_4, data_frame_6):
       
        G=nx.Graph()
        ip_dongle_04 = data_frame_4["ip"][0]
        ip_dongle_06 = data_frame_6["ip"][0]

        # a list of nodes:
        G.add_node("Router")
        G.add_nodes_from([ip_dongle_04, ip_dongle_06])
        G.add_edges_from([("Router", ip_dongle_04), ("Router", ip_dongle_06), (ip_dongle_04, ip_dongle_06)])

        weight_router_to_dongle_04 =  ((data_frame_1["RX_neighbor1"].values[0]+ data_frame_1["TX_neighbor1"].values[0])/2)
        weight_router_to_dongle_06 = ((data_frame_1["RX_neighbor2"].values[0]+ data_frame_1["TX_neighbor2"].values[0])/2)
        weight_dongle_04_to_dongle_06 =  ((data_frame_4["RX_neighbor2"].values[0]+ data_frame_4["TX_neighbor2"].values[0])/2)

        G["Router"][ip_dongle_04]['weight'] = weight_router_to_dongle_04
        G["Router"][ip_dongle_06]['weight'] = weight_router_to_dongle_06
        G[ip_dongle_06][ip_dongle_04]['weight'] = weight_dongle_04_to_dongle_06
        
        # 255
        # 200      (255-200  = 50)
        # 240      (255-240  = 15)
        print("Nodes of graph: ")
        print(G.nodes())
        print("Edges of graph: ")
        print(G.edges())    

 
        nx.draw(G, with_labels=True)
        pos = nx.spring_layout(G)

        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
        
        plt.axis()
        plt.show() # display
        #plt.scatter(router_cords[0], router_cords[1], s=300, c="black",  label=f"Router", alpha=0.6)
        #plt.scatter(router_cords[0], router_cords[1], s=200, c="red",  label=f"Router", alpha=0.6)
        #plt.scatter(neighbor1[0], neighbor1[1], s=200, c="blue",  label=f"neigbor1", alpha=0.6)
        #plt.scatter(neighbor2[0], neighbor2[1], s=200, c="yellow",  label=f"neigbor2", alpha=0.6)
        #plt.show()
        #print(f"n1 {neighbor1}")
        #print(f"n2 {neighbor2}")