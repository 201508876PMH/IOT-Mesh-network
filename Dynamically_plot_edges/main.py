from mesh_data_parser import * 
from mesh_data_analyser import *
from mesh_data_fetcher import * 
import time 

if __name__ == "__main__":
    router_ip = "10.1.0.1"
    router_username = "root"
    data_fetcher = MeshDataFetcher(router_ip, router_username)

    data_parser = MeshDataParser()
   
    mesh_data_analyser = MeshDataAnalyser()   
    mesh_data_analyser_2 = MeshDataAnalyser()
    mesh_data_analyser_3 = MeshDataAnalyser() 
    
    #While(1) for continuous plotting    
    while(1):
        time.sleep(1)

        #UnComment the following for real data
        
        #data_fetcher.fetch_data_from_device()
        #data_parser.parse_log_to_csv("logfiles/logfile_node01.txt")
        #data_parser.parse_log_to_csv("logfiles/logfile_node06.txt")
        #data_parser.parse_log_to_csv("logfiles/logfile_node04.txt")

        data_frame_1 = mesh_data_analyser.load_data_table("logfile_node01.csv")
        data_frame_4 = mesh_data_analyser.load_data_table("logfile_node04.csv")
        data_frame_6 = mesh_data_analyser.load_data_table("logfile_node06.csv")

        mesh_data_analyser.plot_data(data_frame_1, data_frame_4, data_frame_6, data_frame_1, 'addr:10.1.0.4')
        mesh_data_analyser_2.plot_data(data_frame_1, data_frame_4, data_frame_6, data_frame_1, 'addr:10.1.0.6')
        mesh_data_analyser_3.plot_data(data_frame_1, data_frame_4, data_frame_6, data_frame_4, 'addr:10.1.0.6')
        print(tabulate(data_frame_1, headers='keys', tablefmt='psql'))

    
    




    
    
    