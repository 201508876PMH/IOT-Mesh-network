from paramiko import SSHClient
from scp import SCPClient

class MeshDataFetcher:
    def __init__(self, ip):
        self.ip = ip
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        username = "root" 
        self.ssh.connect(f"{username}@{ip}")

    def fetch_data_from_device(self):
        dir_to_fetch = "/root/logfiles"

        with SCPClient(self.ssh.get_transport()) as scp:
            scp.get(dir_to_fetch)