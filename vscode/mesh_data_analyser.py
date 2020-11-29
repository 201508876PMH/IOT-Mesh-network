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
        self.f = plt.figure()
        self.graph = self.f.add_subplot(111)
        pass

    def load_data_table(self, csv_file_name):
        csv_path = os.path.join(".", "CSV_files/" ,csv_file_name)

        data_frame = panda.read_csv(csv_path, nrows=5)
        #print(tabulate(data_frame, headers='keys', tablefmt='psql'))
        
        return data_frame

    def plot_data(self, data_frame_1, data_frame_4, data_frame_6):
       
        plt.clf()

        # Creates nodes and the relation
        df = panda.DataFrame({'from':['R','R','D04','D04','D06','D06'], 'to':['D04','D06','R','D06','R','D04']})
        G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 

        # Fix the mean value
        speed = 100
        weight_router_to_dongle_04 =  self.normalize_to_speed(((data_frame_1["RX_neighbor1"].values[0]+ data_frame_1["TX_neighbor1"].values[0])/2), speed)
        weight_router_to_dongle_06 = self.normalize_to_speed(((data_frame_1["RX_neighbor2"].values[0]+ data_frame_1["TX_neighbor2"].values[0])/2), speed)
        weight_dongle_04_to_dongle_06 =  self.normalize_to_speed(((data_frame_4["RX_neighbor2"].values[0]+ data_frame_4["TX_neighbor2"].values[0])/2), speed)
        
        # Add weight between nodes
        G['R']['D04']['weight'] = weight_router_to_dongle_04
        G['R']['D06']['weight'] = weight_router_to_dongle_06
        G['D06']['D04']['weight'] = weight_dongle_04_to_dongle_06

        # genereate dist matrix, and estimate x,y coordss
        distance_matrix = self.generate_distance_matrix(weight_router_to_dongle_04, weight_router_to_dongle_06, weight_dongle_04_to_dongle_06)
        print(f"dist_matrix : \n {distance_matrix}")
        x_y_cordinates = self.give_coords(distance_matrix)
        print(f"x,y coords {x_y_cordinates}")

        x_1, y_1 = (x_y_cordinates[0,0]), (x_y_cordinates[0,1])
        x_2, y_2 = (x_y_cordinates[1,0]), (x_y_cordinates[1,1])
        x_3, y_3 = (x_y_cordinates[2,0]), (x_y_cordinates[2,1])

        x_y_casted = [x_1, y_1, x_2, y_2, x_3, y_3]

        for i,elem in enumerate(x_y_casted):
            print(f"value : {elem} , type : {type(elem)}")
            x_y_casted[i] = int(x_y_casted[i])

        print(x_y_casted)
        labelPosDict = {'R':[x_y_casted[0], x_y_casted[1]], 'D04':[x_y_casted[2], x_y_casted[3]], 'D06':[x_y_casted[4], x_y_casted[5]]}
        
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos=labelPosDict, edge_labels=labels)

        plt.axvline(.1, alpha=0.1, color='black')
        plt.axhline(.3, alpha=0.1, color='black')

        #Create a dict of fixed node positions
        nodePosDict = {'R':[x_y_casted[0], x_y_casted[1]], 'D04':[x_y_casted[2], x_y_casted[3]], 'D06':[x_y_casted[4], x_y_casted[5]]}

        # Make the graph - add the pos and connectionstyle arguments
        nx.draw(G,with_labels=True, pos=nodePosDict,
            node_size=1500, alpha=0.3, font_weight="bold", arrows=True,
            connectionstyle='arc3, rad = 0.1')
            
        plt.axis('on')
        #self.graph.plot(x_y_casted)
        plt.draw()
        plt.show()

    def test_plot(self):
        x = np.linspace(0, 6*np.pi, 100)
        y = np.sin(x)

        # You probably won't need this if you're embedding things in a tkinter plot...
        plt.ion()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

        for phase in np.linspace(0, 10*np.pi, 500):
            line1.set_ydata(np.sin(x + phase))
            fig.canvas.draw()
            fig.canvas.flush_events()



    # https://stackoverflow.com/questions/18096783/using-distance-matrix-to-find-coordinate-points-of-set-of-points 
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
        

    def normalize_to_speed(self, value, speed):
        return int((value/255)*100)


    def generate_distance_matrix(self, weight_router_to_dongle_04, weight_router_to_dongle_06, weight_dongle_04_to_dongle_06):
        distance_matric = numpy.zeros((3, 3))

        distance_matric[0][1] =  weight_router_to_dongle_04
        distance_matric[0][2] =  weight_router_to_dongle_06
        distance_matric[1][0] =  weight_router_to_dongle_04
        distance_matric[1][2] =  weight_dongle_04_to_dongle_06
        distance_matric[2][0] =  weight_router_to_dongle_06
        distance_matric[2][1] =  weight_dongle_04_to_dongle_06

        return distance_matric



    # https://math.stackexchange.com/questions/3663043/im-now-stuck-in-how-to-convert-the-distance-matrix-to-the-real-coordinates-of-p
    # https://www.displayr.com/what-is-a-distance-matrix/
    # https://stackoverflow.com/questions/10963054/finding-the-coordinates-of-points-from-distance-matrix
    def plot_xy_values(self, data_frame_1, data_frame_4, data_frame_6):
        
        distance_matric = numpy.zeros((3, 3))
        
        weight_router_to_dongle_04 =  data_frame_1["RX_neighbor1"].values[0]
        weight_router_to_dongle_06 = data_frame_1["RX_neighbor2"].values[0]
        weight_dongle_04_to_dongle_06 =  data_frame_4["RX_neighbor2"].values[0]

        distance_matric[0][1] = weight_router_to_dongle_04
        distance_matric[0][2] = weight_router_to_dongle_06
        distance_matric[1][0] = weight_router_to_dongle_04
        distance_matric[1][2] = weight_dongle_04_to_dongle_06
        distance_matric[2][0] = weight_router_to_dongle_06
        distance_matric[2][1] = weight_dongle_04_to_dongle_06
        print(f"dist matric \n {distance_matric}")
        m_matrix = numpy.zeros((3, 3))

        for i in range(3):
            for j in range(3):
                m_matrix[i][j] = 0.5 * ((distance_matric[1][j]**2) + (distance_matric[i][1]**2) -(distance_matric[i][j]**2))

        print(f"m_matrix \n {m_matrix}")
        eigvals, eigvecs = LA.eig(m_matrix)

        print(f"eigen vals  : \n {eigvals}")
        print(f"eigen vectors  : \n {eigvecs}")

        results = []
        for i in range(3):
            if eigvals[i] != 0:
                results.append(math.sqrt(eigvals[i])*eigvecs[i])
        print(f"results \n {results}")
        coords = numpy.reshape(results, (2,3)).T


        print(coords)
        X_vals = [coords[i][0] for i in range(3)]
        Y_vals = [coords[i][1] for i in range(3)]
    

        plt.annotate(f"Roouter",  xy=(X_vals[0], Y_vals[0]))
        plt.annotate(f"device 4", xy=(X_vals[1], Y_vals[1]))
        plt.annotate(f"device 6", xy=(X_vals[2], Y_vals[2]))
        
        
        plt.scatter(X_vals , Y_vals, s=230, c="black", marker="D")
        plt.scatter(X_vals , Y_vals, s=180, c="red", marker="D" )
        plt.plot([X_vals[0], X_vals[1]], [Y_vals[0], Y_vals[1]], c="red", linewidth=1, linestyle='--')
        plt.plot([X_vals[0], X_vals[2]], [Y_vals[0], Y_vals[2]], c="red", linewidth=1, linestyle='--')
        plt.plot([X_vals[1], X_vals[2]], [Y_vals[1], Y_vals[2]], c="red", linewidth=1, linestyle='--')
        


        dist1 = math.sqrt((X_vals[0]-X_vals[1])**2 + (Y_vals[0]- Y_vals[1])**2)
        dist2 = math.sqrt((X_vals[0]-X_vals[2])**2 + (Y_vals[0]- Y_vals[2])**2)
        dist3 = math.sqrt((X_vals[1]-X_vals[2])**2 + (Y_vals[1]- Y_vals[2])**2)
        
        print(f"dist1 : {dist1}" )
        print(f"dist2 : {dist2}" )
        print(f"dist3 : {dist3}" )
        plt.show()


    def calc_and_plot_xy_values(self):
        
        distance_matric = numpy.zeros((3, 3))

        weight_router_to_dongle_04 =  234
        weight_router_to_dongle_06 =  150
        weight_dongle_04_to_dongle_06 =  231

        distance_matric[0][1] = weight_router_to_dongle_04
        distance_matric[0][2] = weight_router_to_dongle_06
        distance_matric[1][0] = weight_router_to_dongle_04
        distance_matric[1][2] = weight_dongle_04_to_dongle_06
        distance_matric[2][0] = weight_router_to_dongle_06
        distance_matric[2][1] = weight_dongle_04_to_dongle_06

        print(f"dist matric \n {distance_matric}")
        m_matrix = numpy.zeros((3, 3))

        for i in range(3):
            for j in range(3):
                m_matrix[i][j] = 0.5 * ((distance_matric[1][j]**2) + (distance_matric[i][1]**2) -(distance_matric[i][j]**2))

        print(f"m_matrix \n {m_matrix}")
        eigvals, eigvecs = LA.eig(m_matrix)

        print(f"eigen vals  : \n {eigvals}")
        print(f"eigen vectors  : \n {eigvecs}")

        results = []
        for i in range(3):
            if eigvals[i] != 0:
                results.append(math.sqrt(eigvals[i])*eigvecs[i])
        print(f"results \n {results}")
        coords = numpy.reshape(results, (2,3)).T

        print(coords)
        X_vals = [coords[i][0] for i in range(3)]
        Y_vals = [coords[i][1] for i in range(3)]

        plt.annotate(f"Roouter",  xy=(X_vals[0], Y_vals[0]))
        plt.annotate(f"device 4", xy=(X_vals[1], Y_vals[1]))
        plt.annotate(f"device 6", xy=(X_vals[2], Y_vals[2]))
        
        plt.scatter(X_vals , Y_vals, s=230, c="black", marker="D")
        plt.scatter(X_vals , Y_vals, s=180, c="red", marker="D" )
        plt.plot([X_vals[0], X_vals[1]], [Y_vals[0], Y_vals[1]], c="red", linewidth=1, linestyle='--')
        plt.plot([X_vals[0], X_vals[2]], [Y_vals[0], Y_vals[2]], c="red", linewidth=1, linestyle='--')
        plt.plot([X_vals[1], X_vals[2]], [Y_vals[1], Y_vals[2]], c="red", linewidth=1, linestyle='--')

        # Verify distances to given distance matrix
        dist1 = math.sqrt((X_vals[0]-X_vals[1])**2 + (Y_vals[0]- Y_vals[1])**2)
        dist2 = math.sqrt((X_vals[0]-X_vals[2])**2 + (Y_vals[0]- Y_vals[2])**2)
        dist3 = math.sqrt((X_vals[1]-X_vals[2])**2 + (Y_vals[1]- Y_vals[2])**2)
        
        print(f"dist1 : {dist1}" )
        print(f"dist2 : {dist2}" )
        print(f"dist3 : {dist3}" )
        plt.show()
