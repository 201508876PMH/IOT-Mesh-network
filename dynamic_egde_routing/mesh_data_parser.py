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
                               "mac_device1,device1_metric,mac_devive1_neighbor,devive1_neighbor_metric,"
                               "mac_device2,device2_metric,mac_devive2_neighbor,devive2_neighbor_metric")
                csv_file.write("\n")               
                
                log_lines = log_file.readlines() 

                ip_current      = log_lines[0].split()[2]
                time_stamp      = log_lines[1].split()[2]
                iterations      = log_lines[2].split()[4]

                # check for broacast 
                skip = 3                
                index_for_first_dev = 11
                if log_lines[index_for_first_dev].split()[0] == "ff:ff:ff:ff:ff:ff":
                    index_for_first_dev += skip

                mac_device1 = log_lines[index_for_first_dev].split()[0]
                device1_metric = log_lines[index_for_first_dev].split()[2]
                mac_devive1_neighbor = log_lines[index_for_first_dev+2].split()[0]
                devive1_neighbor_metric = log_lines[index_for_first_dev+2].split()[3].split(",")[0]

                
                index_for_second_dev = index_for_first_dev +3 
                if log_lines[index_for_second_dev].split()[0] == "ff:ff:ff:ff:ff:ff":
                    index_for_second_dev += skip

                mac_device2 = log_lines[index_for_second_dev].split()[0]
                device2_metric = log_lines[index_for_second_dev].split()[2]
                mac_devive2_neighbor = log_lines[index_for_second_dev+2].split()[0]
                devive2_neighbor_metric = log_lines[index_for_second_dev+2].split()[3].split(",")[0]

                csv_file.write(ip_current + ", " +
                               iterations + ", " +
                               time_stamp + ", " +
                               mac_device1 + ", " +
                               device1_metric + ", " +
                               mac_devive1_neighbor + ", " +
                               devive1_neighbor_metric + ", " +
                               mac_device2 + ", " +
                               device2_metric + ", " +
                               mac_devive2_neighbor + ", " +
                               devive2_neighbor_metric + "\n")

        





