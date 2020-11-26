import pandas as pd


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

        with open(csv_file_name,"w") as csv_file:
             with open(log_path, "r") as log_file:
                csv_file.write("ip, iterations, timestamp,"
                               "neighbor1, RX_neighbor1, TX_neighbor1," +
                               "neighbor2, RX_neighbor2, TX_neighbor2," +
                               "neighbor3, RX_neighbor3, TX_neighbor3 \n")
                
                log_lines = log_file.readlines() 

                ip_current_device = "10.0.0.1"
                time_stamp = log_lines[0].split()[2]
                iterations = log_lines[1].split()[4]
                neighbor1_mac = log_lines[3].split()[0]
                neighbor1_tx = log_lines[4].split()[16]
                neighbor1_rx = log_lines[5].split()[16]
                neighbor2_mac = log_lines[6].split()[0]
                neighbor2_tx = log_lines[7].split()[16]
                neighbor2_rx = log_lines[8].split()[16]
                

                print(f"ip_current_device, {ip_current_device}")
                print(f"time_stamp :  {time_stamp}")
                print(f"iterations :  {iterations}")
                print(f"neighbor1_mac : {neighbor1_mac}")
                print(f"neighbor1_tx :  {neighbor1_tx}")
                print(f"neighbor1_rx :  {neighbor1_rx}")
                print(f"neighbor2_mac : {neighbor2_mac}")
                print(f"neighbor2_tx :  {neighbor2_tx}")
                print(f"neighbor2_rx :  {neighbor2_rx}")



            
           


        with  open(csv_file_name,"r") as csv_file:  
            csv_lines = csv_file.readlines()
            for line in csv_lines:
                print(line)

        #with open('log.csv', 'w') as out_file:
        #    writer = csv.writer(out_file)
        #    writer.writerow(('title', 'intro'))
        #    writer.writerows(lines)

        





