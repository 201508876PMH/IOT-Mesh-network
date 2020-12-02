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
    
    #    
    while(1):
        time.sleep(1)
        data_fetcher.fetch_data_from_device()
#
        data_parser.parse_log_to_csv("logfiles/logfile_node01.txt")
        data_parser.parse_log_to_csv("logfiles/logfile_node06.txt")
        data_parser.parse_log_to_csv("logfiles/logfile_node04.txt")

        data_frame_1 = mesh_data_analyser.load_data_table("logfile_node01.csv")
        data_frame_4 = mesh_data_analyser.load_data_table("logfile_node04.csv")
        data_frame_6 = mesh_data_analyser.load_data_table("logfile_node06.csv")

        mesh_data_analyser.plot_data(data_frame_1, data_frame_4, data_frame_6)
        print(tabulate(data_frame_1, headers='keys', tablefmt='psql'))
#
    #
    




    
    
    