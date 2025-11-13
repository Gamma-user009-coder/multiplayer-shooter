import json
import socket
import threading
from queue import Queue

from typing import List

TIMEOUT = 3


class Connection:
    def __init__(self, client_ip: str, client_port: int, server_ip: str, server_port: int):
        self.ip = client_ip
        self.port = client_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((self.ip, self.port))
        self.exit = threading.Event()
        self.client_socket.settimeout(TIMEOUT)
        self.listener = threading.Thread(target=self.listener_function)
        self.listener.start()
        self.receiver_queue = Queue()

    def listener_function(self):
        print("Listening...")
        while not self.exit.is_set():
            try:
                raw_data, addr = self.client_socket.recvfrom(1024)
                data = json.loads(raw_data.decode())
                self.receiver_queue.put((data, addr))
            except socket.timeout:
                pass

    def send(self, data: dict):
        print(f"Sending... {data}")
        self.client_socket.sendto(json.dumps(data).encode(), (self.server_ip, self.server_port))

    def get_packets(self) -> List[tuple[dict, tuple[str, int]]]:
        packets = []
        while not self.receiver_queue.empty():
            data, addr = self.receiver_queue.get()
            packets.append((data, addr))
        return packets

    def disconnect(self):
        self.exit.set()
        self.listener.join()
        self.client_socket.close()


if __name__ == '__main__':
    connection = Connection("127.0.0.1", 8000)
