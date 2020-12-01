import pandas as panda
import os
import numpy
from numpy import linalg as LA
import matplotlib.pyplot as plt
import math
import networkx as nx
from tabulate import tabulate
import numpy as np
import sympy


class MeshDataAnalyser():
    def __init__(self):
        # Turn interative mode on
        plt.ion()
        # show any figures (This will NOT block if interactive mode is on)
        plt.show()
        

    def load_data_table(self, csv_file_name):
        csv_path = os.path.join(".", "CSV_files/" ,csv_file_name)

        data_frame = panda.read_csv(csv_path, nrows=5)
        #print(tabulate(data_frame, headers='keys', tablefmt='psql'))
        
        return data_frame


    def plot_data(self, data_frame_1, data_frame_4, data_frame_6):
        plt.clf()
        axes = plt.gca()
        axes.set_xlim([-0.5,8])
        axes.set_ylim([-0.5,8])
        # Creates nodes and the relation
        df = panda.DataFrame({'from':['R','R','D04','D04','D06','D06'], 'to':['D04','D06','R','D06','R','D04']})
        G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 
        
        # TODO find a solutionen later
        # weight for the metrics 
        metric_router_to_d04 = data_frame_1["device1_metric"][0]
        metric_router_to_d06 = data_frame_1["device2_metric"][0]
        metric_d04_to_d06    = data_frame_1["devive2_neighbor_metric"][0]   

        print(f"wegiht 1 {metric_router_to_d04}")
        print(f"wegiht 2 {metric_router_to_d06}")
        print(f"wegiht 3 {metric_d04_to_d06}")
        # Add weight between nodes
        
        
        #G.add_edge("R","D06",color='black',weight=2)
        #G.add_edge("R","D04",color='black',weight=2)
        #G.add_edge("D04","D06",color='red',weight=2)
        G['R']['D04']['weight'] = metric_router_to_d04 
        G['R']['D06']['weight'] = metric_router_to_d06 
        G['D06']['D04']['weight'] = metric_d04_to_d06
        
        G['R']['D04']['color'] = "red" 
        G['R']['D06']['color'] = "black"
        G['D06']['D04']['color'] = "black"

        #G["R"]["D04"]['color'] = "blue"
        labelPosDict = {'R':[1, 1], 'D04':[3,3], 'D06':[5,1]}
        
        labels = nx.get_edge_attributes(G,'weight')

        edges = G.edges()    
        nodes_pos = nx.spring_layout(G)  
        nx.draw_networkx_edge_labels(G,pos=labelPosDict, edge_labels=labels)
        #nx.draw_networkx_edges(G,nodes_pos, edges, 8, 0.5, 'r')
        nx.draw_networkx_edges(G,nodes_pos, edgelist=edges,  width=8,alpha=0.5,edge_color='r')

        #print(list(G.edges()))

        #Create a dict of fixed node positions
        nodePosDict = {'R':[1, 1], 'D04':[3,3], 'D06':[5,1]}
       
        
   
        print(list(edges))
        #colors = [G[u][v]["color"] for u,v in edges]
        # Make the graph - add the pos and connectionstyle arguments
        nx.draw(G,with_labels=True, pos=nodePosDict, node_size=1500, alpha=0.3, font_weight="bold", arrows=True)
             
        plt.axis('on')
        plt.draw()
        plt.pause(1)



