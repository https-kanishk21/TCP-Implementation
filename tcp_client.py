import socket

HOST = '127.0.0.1'  # localhost
PORT = 9999

# Create socket and connect to server
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))
print(f"[CLIENT] Connected to {HOST}:{PORT}")

for i in range(3):
    msg = f"Message {i+1} from client"
    client_sock.sendall(msg.encode())
    reply = client_sock.recv(1024)
    print(f"[CLIENT] Received: {reply.decode()}")

client_sock.close()
print("[CLIENT] Connection closed.")
