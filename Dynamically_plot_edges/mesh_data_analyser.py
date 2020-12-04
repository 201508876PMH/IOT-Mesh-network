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
    def __init__(self, title, do_simu = False):
        # Turn interative mode on
        self.do_simu = do_simu
        self.title = title
        self.simulation_counter = 50
        self.figure = plt.figure()
        plt.ion()
        # show any figures (This will NOT block if interactive mode is on)
        plt.show()
        

    def load_data_table(self, csv_file_name):
        csv_path = os.path.join(".", "CSV_files/" ,csv_file_name)

        data_frame = panda.read_csv(csv_path, nrows=5)
        #print(tabulate(data_frame, headers='keys', tablefmt='psql'))
        
        return data_frame


    def plot_data(self, data_frame_1, data_frame_4, data_frame_6, start_node, arrival_node_ip):
        plt.figure(self.figure.number)
        plt.clf()
        axes = plt.gca()
        axes.set_xlim([-0.1,6])
        axes.set_ylim([-0.1,6])
        # Creates nodes and the relation
        df = panda.DataFrame({'from':['R','R','D04','D04','D06','D06'], 'to':['D04','D06','R','D06','R','D04']})
        G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 
        
        # TODO find a solutionen later
        # weight for the metrics 
        metric_router_to_d04 = data_frame_1["device1_metric"][0]
        metric_router_to_d06 = data_frame_1["device2_metric"][0]
        metric_d04_to_d06    = data_frame_1["devive1_neighbor_metric"][0]   
        metric_d04_to_d06 -= self.simulation_counter if self.do_simu else 0  

        # Add weight between nodes
        G['R']['D04']['weight'] = metric_router_to_d04 
        G['R']['D06']['weight'] = metric_router_to_d06 
        G['D06']['D04']['weight'] = metric_d04_to_d06

        #G["R"]["D04"]['color'] = "blue"
        labelPosDict = {'R':[1, 1], 'D04':[3,3], 'D06':[5,1]}
        labels = nx.get_edge_attributes(G,'weight')
        edges = G.edges()    

        nodePosDict = {'R':[1, 1], 'D04':[3,3], 'D06':[5,1]}
        nx.draw_networkx_edge_labels(G,pos=labelPosDict, edge_labels=labels)

        # Draw edges with color black (default color)
        nx.draw_networkx_edges(G,nodePosDict, edgelist=edges,  width=1,alpha=0.5)
           
        # Overlap original edges with shortest path and with color red
        shortest_path_edges, dongle_06_next_hop_mac = self.find_smallest_path(start_node, arrival_node_ip, self.do_simu) 
        nx.draw_networkx_edges(G,nodePosDict, edgelist=shortest_path_edges,  width=3,alpha=0.8,edge_color='r')

        # Make the graph - add the pos and connectionstyle arguments
        nx.draw(G,with_labels=True, pos=nodePosDict, node_size=1500, alpha=0.3, font_weight="bold", arrows=True)
        plt.title(self.title)     
        plt.axis('on')
        plt.draw()
        plt.pause(0.5)


    def get_mac_from_ip(self, IP_address):
        fetched_mac = {'addr:10.1.0.4' : ('e4:95:6e:4b:be:d3', 'D04'),
                       'addr:10.1.0.6' : ('e4:95:6e:4b:b7:13', 'D06'),
                       'addr:10.1.0.1' : ('94:83:c4:02:8c:0e', 'R')}
        return fetched_mac[IP_address]
    

    def get_label_from_mac(self, mac):
        fetched_mac = {'e4:95:6e:4b:be:d3' : 'D04',
                       'e4:95:6e:4b:b7:13' : 'D06',
                       '94:83:c4:02:8c:0e' : 'R'}
        return fetched_mac[mac]

    def find_smallest_path(self, routing_table, destination_node, do_simu = False):
        start_path = (2^32)-1
        shortest_path_edgelist = []
        current_node_mac, current_node_label = self.get_mac_from_ip(routing_table['ip'][0])
        destination_mac, destination_label = self.get_mac_from_ip(destination_node)

        #Check first layer neighbours
        if(routing_table["mac_device1"][0] == destination_mac):
            #print("direct acces 1")
            start_path = routing_table['device1_metric'][0]
            shortest_path_edgelist.append((current_node_label, destination_label))
            dongle_06_next_hop_mac=routing_table["mac_device1"][0]
        else:
            #print("direct acces 2")
            start_path = routing_table['device2_metric'][0]
            shortest_path_edgelist.append((current_node_label, destination_label))
            dongle_06_next_hop_mac=routing_table["mac_device2"][0]

        #Check second layer neighbours
        if(routing_table['mac_devive1_neighbor'][0] == destination_mac):
            distance_layer_01 = int(routing_table['device1_metric'][0])
            distance_layer_01 -= self.simulation_counter if do_simu else 0  

            distance_layer_02 = int(routing_table['devive1_neighbor_metric'][0])
            combined_metric = distance_layer_01 + distance_layer_02
       
            #print("combined 1 " , combined_metric, "currect smalleest", start_path)
            if(combined_metric <  start_path):
                shortest_path_edgelist.clear()
                start_path = combined_metric
                shortest_path_edgelist.append((current_node_label, self.get_label_from_mac(routing_table['mac_device1'][0])))
                shortest_path_edgelist.append((self.get_label_from_mac(routing_table['mac_device1'][0]), destination_label))
                dongle_06_next_hop_mac=routing_table["mac_device1"][0]

        else:
            distance_layer_01= int(routing_table['device2_metric'][0])
            #print("dist layer 1 ", distance_layer_01)
            distance_layer_01 -= self.simulation_counter if do_simu else 0  

            distance_layer_02 = int(routing_table['devive2_neighbor_metric'][0])
            combined_metric = distance_layer_01 + distance_layer_02
            #print("combined 2 " , combined_metric, "currect smalleest", start_path)
            if(combined_metric <  start_path):
                shortest_path_edgelist.clear()
                start_path = combined_metric
                shortest_path_edgelist.append((current_node_label, self.get_label_from_mac(routing_table['mac_device2'][0])))
                shortest_path_edgelist.append((self.get_label_from_mac(routing_table['mac_device2'][0]), destination_label))
                dongle_06_next_hop_mac=routing_table["mac_device2"][0]

        self.simulation_counter += 50 if do_simu else 0  
        #print(self.simulation_counter)
        return shortest_path_edgelist, dongle_06_next_hop_mac


    def show_routing_table(self, node1, node1_next_hop, node2, node2_next_hop):
        route_dongles = [(node1, node1_next_hop), (node2, node2_next_hop)]
        print(tabulate(route_dongles, headers=["Destination", "Next Hop"]))   
        print("\n\r")    


    def show_routing_tables(self, data_frame_1, data_frame_4, data_frame_6):

        shortest_path_edges, dongle_04_next_hop_mac = self.find_smallest_path(data_frame_1, 'addr:10.1.0.4', do_simu=False)
        shortest_path_edges, dongle_06_next_hop_mac = self.find_smallest_path(data_frame_1, 'addr:10.1.0.6', do_simu=False)

        dongle_04_next_hop=self.get_label_from_mac(dongle_04_next_hop_mac)
        dongle_06_next_hop=self.get_label_from_mac(dongle_06_next_hop_mac)
        print("\nROUTER ROUTING TABLE\n")
        self.show_routing_table("D04", dongle_04_next_hop, "D06", dongle_06_next_hop)


        shortest_path_edges, router_next_hop_mac = self.find_smallest_path(data_frame_4, 'addr:10.1.0.1',  do_simu=False)
        shortest_path_edges, dongle_06_next_hop_mac = self.find_smallest_path(data_frame_4, 'addr:10.1.0.6',  do_simu=False)

        router_next_hop=self.get_label_from_mac(router_next_hop_mac)        
        dongle_06_next_hop=self.get_label_from_mac(dongle_06_next_hop_mac)
        print("\nDONGLE 04 ROUTING TABLE\n")
        self.show_routing_table("R", router_next_hop, "D06", dongle_06_next_hop)


        shortest_path_edges, dongle_04_next_hop_mac = self.find_smallest_path(data_frame_6, 'addr:10.1.0.4',  do_simu=False)
        shortest_path_edges, router_next_hop_mac = self.find_smallest_path(data_frame_6, 'addr:10.1.0.1',  do_simu=False)

        router_next_hop=self.get_label_from_mac(router_next_hop_mac)        
        dongle_04_next_hop=self.get_label_from_mac(dongle_04_next_hop_mac)
        print("\nDONGLE 06 ROUTING TABLE\n")
        self.show_routing_table("R", router_next_hop, "D04", dongle_04_next_hop)

            



