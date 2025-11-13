import socket
import json
import from_client_packets
import time
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.connect(('127.0.0.1', 12345))
    dct = from_client_packets.FirstConnectionRequest("amit the king").to_dict()
    sock.send(json.dumps(dct).encode())
    print("sent")
    data = json.loads(sock.recvfrom(1024)[0])
    player_id = data['player_id']
    print("player_id:", player_id)
    player_status_dict = {'id': from_client_packets.FromClientPackets.PLAYER_STATUS.value,
                          'player_id': player_id,
                          'pos': (50, 50),
                          'projectile': None }
    json_player_status = json.dumps(player_status_dict)

    while True:
        sock.send(json_player_status.encode())
        print("sent status")
        print(sock.recvfrom(1024))

    sock.close()

if __name__ == '__main__':
    main()