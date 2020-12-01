class MeshData:
    def __init__(self):
        self.time_stamp = "bla"
        self.neighbors = []
        self.ip = "10.0.0.0"         


class MeshDataParser:

    def __init__(self):
        pass

    def parse_log_to_csv(self, log_path):
        log_splited_array = log_path.split("/")
        csv_file_name = log_splited_array[len(log_splited_array)-1].split(".")[0] + ".csv"

        with open("CSV_files/" + csv_file_name,"w") as csv_file:
             with open(log_path, "r") as log_file:
                csv_file.write("ip,iterations,timestamp,"
                               "neighbor1,RX_neighbor1,TX_neighbor1," +
                               "neighbor2,RX_neighbor2,TX_neighbor2," +
                               "neighbor3, RX_neighbor3,TX_neighbor3")
                csv_file.write("\n")               
                
                log_lines = log_file.readlines() 

                ip_current      = log_lines[0].split()[2]
                time_stamp      = log_lines[1].split()[2]
                iterations      = log_lines[2].split()[4]
                neighbor1_mac   = log_lines[4].split()[0]
                neighbor1_tx    = log_lines[5].split()[16]
                neighbor1_rx    = log_lines[6].split()[16]
                neighbor2_mac   = log_lines[7].split()[0]
                neighbor2_tx    = log_lines[8].split()[16]
                neighbor2_rx    = log_lines[9].split()[16]

                csv_file.write(ip_current + ", " +
                               iterations + ", " +
                               time_stamp + ", " +
                               neighbor1_mac + ", " +
                               neighbor1_rx + ", " +
                               neighbor1_tx + ", " +
                               neighbor2_mac + ", " +
                               neighbor2_rx + ", " +
                               neighbor2_tx + "\n")
                        
        





