from mesh_data_parser import * 
from mesh_data_analyser import * 


if __name__ == "__main__":
    data_parser = MeshDataParser()

    data_parser.parse_log_to_csv("../Logfiles/logfile_node01.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node06.txt")
    data_parser.parse_log_to_csv("../Logfiles/logfile_node04.txt")

    mesh_data_analyser = MeshDataAnalyser()
    data_frame_1 = mesh_data_analyser.load_data_table("logfile_node01.csv")
    data_frame_4 = mesh_data_analyser.load_data_table("logfile_node04.csv")
    data_frame_6 = mesh_data_analyser.load_data_table("logfile_node06.csv")

    test = [[0, 243, 33],
           [243, 0, 211],
           [33, 211, 0]]

    # https://stackoverflow.com/questions/18096783/using-distance-matrix-to-find-coordinate-points-of-set-of-points
    result = mesh_data_analyser.give_coords(test)

    mesh_data_analyser.plot_data(data_frame_1, data_frame_4, data_frame_6, result)
