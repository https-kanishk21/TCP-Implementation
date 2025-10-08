import socket

HOST = '127.0.0.1'  # localhost
PORT = 9999         # any port > 1024

# Create socket, bind, and listen
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(1)
print(f"[SERVER] Listening on {HOST}:{PORT}")

conn, addr = server_sock.accept()
print(f"[SERVER] Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"[SERVER] Received: {data.decode()}")
    conn.sendall(b"ACK: " + data)
    
conn.close()
server_sock.close()
print("[SERVER] Connection closed.")
