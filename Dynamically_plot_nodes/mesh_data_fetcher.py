import subprocess
import os

class MeshDataFetcher:
    def __init__(self, ip, user):
        self.ip = ip
        self.username = user


    def fetch_data_from_device(self):
        dir_to_fetch = "/root/logfiles"
        path = os.getcwd()
        subprocess.check_call(["scp", "-r", f"{self.username}@{self.ip}:{dir_to_fetch}",  f"{path}/"], cwd=path)

 
