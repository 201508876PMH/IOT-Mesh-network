from mesh_data_parser import * 
from mesh_data_analyser import *
from mesh_data_fetcher import * 


if __name__ == "__main__":
    router = "10.1.0.1"
    data_fetcher = MeshDataFetcher(router)
    data_fetcher.fetch_data_from_device()

    data_parser = MeshDataParser()

    data_parser.parse_log_to_csv("../Logfiles/logfile_node01.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node06.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node04.txt")

    mesh_data_analyser = MeshDataAnalyser()
    data_frame_1 = mesh_data_analyser.load_data_table("logfile_node01.csv")
    data_frame_4 = mesh_data_analyser.load_data_table("logfile_node04.csv")
    data_frame_6 = mesh_data_analyser.load_data_table("logfile_node06.csv")
    
    #mesh_data_analyser.plot_data(data_frame_1, data_frame_4, data_frame_6)




    
    
    