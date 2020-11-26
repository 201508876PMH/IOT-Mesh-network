from mesh_data_parser import * 
from mesh_data_analyser import * 


if __name__ == "__main__":
    data_parser = MeshDataParser()

    data_parser.parse_log_to_csv("../Logfiles/logfile_node01.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node06.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node04.txt")

    mesh_data_analyser = MeshDataAnalyser()
    data_frame = mesh_data_analyser.load_data_table("logfile_node01.csv")
    mesh_data_analyser.plot_data(data_frame)
