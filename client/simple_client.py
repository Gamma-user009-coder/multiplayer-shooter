import socket

# Define the target server's IP address and port
SERVER_IP = "172.20.20.23"  # Use "localhost" or the server's actual IP
SERVER_PORT = 54321       # The port the server is listening on

# Create a UDP socket
# AF_INET specifies the address family (IPv4)
# SOCK_DGRAM specifies the socket type (UDP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Message to send to the server
message = "Hello, UDP Server!"

try:
    # Send the message to the server
    # The message must be encoded to bytes
    client_socket.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
    print(f"Sent: '{message}' to {SERVER_IP}:{SERVER_PORT}")

    # Optionally, receive a response from the server
    # 1024 is the buffer size for receiving data
    data, addr = client_socket.recvfrom(1024)
    print(f"Received response from {addr}: {data.decode('utf-8')}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket
    client_socket.close()
    print("Socket closed.")