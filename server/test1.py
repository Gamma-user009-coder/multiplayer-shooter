import socket
import json
import from_client_packets

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.connect(('127.0.0.1', 12345))
    dct = from_client_packets.FirstConnectionRequest("amit the king").to_dict()
    sock.send(json.dumps(dct).encode())
    print("sent")
    print(sock.recvfrom(1024)[0].decode())
    sock.close()

if __name__ == '__main__':
    main()