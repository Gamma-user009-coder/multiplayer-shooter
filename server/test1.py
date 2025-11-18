import socket
import json
import from_client_packets
import to_client_packets
import time

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.connect(('127.0.0.1', 54321))
    dct = from_client_packets.FirstConnectionRequest("amit the king").to_dict()
    sock.send(json.dumps(dct).encode())
    print("sent")
    data = json.loads(sock.recvfrom(1024)[0])
    player_id = data['player_id']
    print("player_id:", player_id)
    player_status_dict = {'id': from_client_packets.FromClientPackets.PLAYER_STATUS.value,
                          'player_id': player_id,
                          'pos': (50, 50),
                          'projectile': (50, 50, 50) }
    json_player_status = json.dumps(player_status_dict)
    i = 0
    while True:
        if i == 250:
            player_status_dict['projectile'] = None
            json_player_status = json.dumps(player_status_dict)
            print(json_player_status)
        sock.send(json_player_status.encode())
        data, connection = sock.recvfrom(1024)
        data = json.loads(data)
        if data['id'] == to_client_packets.ToClientPackets.START_GAME.value:
            print(data)
        if data['id'] == to_client_packets.ToClientPackets.GAME_STATUS.value:
            print("game status: ", data)
        if i == 252:
            time.sleep(10)
        i += 1

    sock.close()

if __name__ == '__main__':
    main()