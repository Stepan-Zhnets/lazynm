from typing import List
import subprocess

class NetworkManager():
    def __init__(self) -> None:
        ...

    @staticmethod
    def __split_on_device(self, list:List[str], rows:int, cols:int) -> List[List[str]]:
        try:
            matrix = []
            for r in range(rows):
                row = []
                for c in range(cols):
                    index = r * cols + c
                    if index < len(list):
                        row.append(list[index])
                    else:
                        row.append(None)
                matrix.append(row)
            return matrix
        except EnvironmentError as e:
            return e

    @staticmethod
    def __split_on_wifi_list(list:List[str]) -> List[List[str]]:
        try:
            # Extracting headers and data lines
            headers = list[0].split()
            data_lines = list[1:]

            matrix = []
            for line in data_lines:
                fields = line.split()
                # print(fields)
                # Create a row with the required format
                if fields[0] != '*':
                    fields.insert(0, '')
                else:
                    None
                row = [
                    fields[0],                            # IN-USE
                    fields[1],                            # BSSID
                    fields[2],                            # SSID
                    fields[3],                            # MODE
                    fields[4],                            # CHAN
                    fields[5],                            # RATE - num
                    # fields[6],                            # RATE - Mbit/s
                    fields[7],                            # SIGNAL
                    fields[8],                            # BARS
                    "WEP" if "WEP" in fields else "WPA"  # SECURITY (assumed based on presence of WEP/WPA)
                ]
                matrix.append(row)
            print()
            return matrix
        except EnvironmentError as e:
            return e

    def device_scan(self) -> str:
        try:
            device_list = []
            device_scan_command = ["nmcli", "device", "show"]
            output = subprocess.check_output(device_scan_command)
            output = output.decode().splitlines()
            for line in output:
                if line.startswith('GENERAL.DEVICE'):
                    device_list.append(line.split()[1])
                if line.startswith('GENERAL.TYPE'):
                    device_list.append(line.split()[1])
            matrix = self.__split_on_device(list=device_list, rows=1, cols=2)
            if matrix[0][1] == 'wifi':
                return matrix[0][0]
            else:
                return "None"
        except EnvironmentError as e:
            return e

    def net_scan(self) -> List[str]:
        try:
            net_scan_command = ["nmcli", "device", "wifi", "list"]
            output = subprocess.check_output(net_scan_command)
            output = output.decode().splitlines()
            matrix = self.__split_on_wifi_list(output)
            return matrix
        except EnvironmentError as e:
            return e

    def connect(self, ssid:str, password:str) -> None:
        try:
            connect_command = ["nmcli", "device", "wifi", "connect", seff.ssid, "password", self.password, "ifname", device_scan()]
            subprocess.run(connect_command)
        except EnvironmentError as e:
            return e

    def disconnect(self) -> None:
        try:
            disconnect_command = ["nmcli", "disconnect", device_scan()]
            subprocess.run(disconnect_command)
        except EnvironmentError as e:
            return e

if __name__ == "__main__":
    manager = NetworkManager()
    # print(manager.connect("my_ssid", "my_password"))
    # print(manager.disconnect())
    # print(manager.device_scan())
    # print('|==============================|')
    print(manager.net_scan())
