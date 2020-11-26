from mesh_data_parser import * 


if __name__ == "__main__":
    data_parser = MeshDataParser()

    data_parser.parse_log_to_csv("../Logfiles/logfile_node01.txt")


    