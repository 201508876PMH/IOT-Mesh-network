import pandas as panda
import os
import matplotlib.pyplot as plt
import networkx as nx
from tabulate import tabulate
import numpy as np
import sympy

class MeshDataAnalyser():
    def __init__(self):
        pass

    def load_data_table(self, csv_file_name):
        csv_path = os.path.join(".", "CSV_files/" ,csv_file_name)

        data_frame = panda.read_csv(csv_path, nrows=5)
        #print(tabulate(data_frame, headers='keys', tablefmt='psql'))
        
        return data_frame

    def plot_data(self, data_frame_1, data_frame_4, data_frame_6, result):
       
        df = panda.DataFrame({'from':['R','R','D04','D04','D06','D06'], 'to':['D04','D06','R','D06','R','D04']})
        G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 

        weight_router_to_dongle_04 =  ((data_frame_1["RX_neighbor1"].values[0]+ data_frame_1["TX_neighbor1"].values[0])/2)
        weight_router_to_dongle_06 = ((data_frame_1["RX_neighbor2"].values[0]+ data_frame_1["TX_neighbor2"].values[0])/2)
        weight_dongle_04_to_dongle_06 =  ((data_frame_4["RX_neighbor2"].values[0]+ data_frame_4["TX_neighbor2"].values[0])/2)
         
        print(weight_router_to_dongle_06)

        
        G['R']['D04']['weight'] = weight_router_to_dongle_04
        G['R']['D06']['weight'] = weight_router_to_dongle_06
        G['D06']['D04']['weight'] = weight_dongle_04_to_dongle_06

        #pos = nx.spring_layout(G)
        #instead of spring, set the positions yourself
        #labelPosDict = {'R':[0.1,0.3], 'D04':[0.5,.9], 'D06':[.9,.18]}
        print(result)


        x_1, y_1 = (result[0,0]), (result[0,1])
        x_2, y_2 = (result[1,0]), (result[1,1])
        x_3, y_3 = (result[2,0]), (result[2,1])

        test_list = [x_1, y_1, x_2, y_2, x_3, y_3]

        lort = []
        for i,elem in enumerate(test_list):
            element_to_add = elem
            print(type(element_to_add))

            lort.append(int(element_to_add).real)

        print(lort)


        labelPosDict = {'R':[lort[0], lort[1]], 'D04':[lort[2], lort[3]], 'D06':[lort[4], lort[5]]}
        
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos=labelPosDict, edge_labels=labels)

        plt.axvline(.1, alpha=0.1, color='green')
        plt.axhline(.3, alpha=0.1, color='green')

        #Create a dict of fixed node positions
        #nodePosDict = {'R':[0.1,0.3], 'D04':[0.5,.9], 'D06':[.9,.18]}
        nodePosDict = {'R':[lort[0], lort[1]], 'D04':[lort[2], lort[3]], 'D06':[lort[4], lort[5]]}

        # Make the graph - add the pos and connectionstyle arguments
        nx.draw(G,with_labels=True, pos=nodePosDict,
                node_size=1500, alpha=0.3, font_weight="bold", arrows=True,
            connectionstyle='arc3, rad = 0.1')

        plt.axis('on')
        plt.show()

    def give_coords(self, distances):
        distances = np.array(distances)

        n = len(distances)
        X = sympy.symarray('x', (n, n - 1))

        for row in range(n):
            X[row, row:] = [0] * (n - 1 - row)

        for point2 in range(1, n):

            expressions = []

            for point1 in range(point2):
                expression = np.sum((X[point1] - X[point2]) ** 2) 
                expression -= distances[point1,point2] ** 2
                expressions.append(expression)

            X[point2,:point2] = sympy.solve(expressions, list(X[point2,:point2]))[1]

        return X