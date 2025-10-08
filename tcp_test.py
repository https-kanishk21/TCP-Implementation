

import socket
import struct
import random
import time
import threading

class SimpleTCP:
    """Simplified TCP implementation for demonstration"""
    
    def __init__(self, port, is_server=False):
        self.port = port
        self.is_server = is_server
        self.seq_num = random.randint(1000, 9999)
        self.ack_num = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', port))
        self.sock.settimeout(2.0)
        self.connected = False
        
    def create_packet(self, flags, data=b''):
        """Create a simple packet: [seq:4][ack:4][flags:1][data]"""
        return struct.pack('!IIB', self.seq_num, self.ack_num, flags) + data
    
    def parse_packet(self, packet):
        """Parse received packet"""
        if len(packet) < 9:
            return None, None, None
        seq, ack, flags = struct.unpack('!IIB', packet[:9])
        data = packet[9:]
        return seq, ack, flags, data
    
    def handshake_server(self):
        """Server-side 3-way handshake"""
        print("\n[SERVER] Waiting for connection...")
        
        # Wait for SYN
        data, client_addr = self.sock.recvfrom(4096)
        seq, ack, flags, _ = self.parse_packet(data)
        
        if flags == 1:  # SYN
            print(f"[SERVER] Received SYN (seq={seq})")
            self.ack_num = seq + 1
            self.client_addr = client_addr
            
            # Send SYN-ACK
            syn_ack = self.create_packet(3)  # SYN+ACK
            self.sock.sendto(syn_ack, client_addr)
            print(f"[SERVER] Sent SYN-ACK (seq={self.seq_num}, ack={self.ack_num})")
            
            # Wait for ACK
            data, _ = self.sock.recvfrom(4096)
            seq, ack, flags, _ = self.parse_packet(data)
            
            if flags == 2:  # ACK
                print(f"[SERVER] Received ACK - Connection ESTABLISHED!")
                self.seq_num += 1
                self.connected = True
                return True
        
        return False
    
    def handshake_client(self, server_port):
        """Client-side 3-way handshake"""
        print("\n[CLIENT] Initiating connection...")
        self.server_addr = ('127.0.0.1', server_port)
        
        # Send SYN
        syn = self.create_packet(1)  # SYN
        self.sock.sendto(syn, self.server_addr)
        print(f"[CLIENT] Sent SYN (seq={self.seq_num})")
        
        try:
            # Wait for SYN-ACK
            data, _ = self.sock.recvfrom(4096)
            seq, ack, flags, _ = self.parse_packet(data)
            
            if flags == 3:  # SYN+ACK
                print(f"[CLIENT] Received SYN-ACK (seq={seq}, ack={ack})")
                self.ack_num = seq + 1
                self.seq_num += 1
                
                # Send ACK
                ack_packet = self.create_packet(2)  # ACK
                self.sock.sendto(ack_packet, self.server_addr)
                print(f"[CLIENT] Sent ACK - Connection ESTABLISHED!")
                self.connected = True
                return True
        except socket.timeout:
            print("[CLIENT] Connection timeout!")
            return False
        
        return False
    
    def send_data(self, message):
        """Send data over connection"""
        if not self.connected:
            print("Not connected!")
            return
        
        data_packet = self.create_packet(2, message.encode())  # ACK flag + data
        addr = self.server_addr if not self.is_server else self.client_addr
        self.sock.sendto(data_packet, addr)
        print(f"[SEND] Sent: '{message}' (seq={self.seq_num})")
        self.seq_num += len(message)
    
    def receive_data(self, timeout=2.0):
        """Receive data from connection"""
        if not self.connected:
            return None
        
        self.sock.settimeout(timeout)
        try:
            data, _ = self.sock.recvfrom(4096)
            seq, ack, flags, msg = self.parse_packet(data)
            
            if len(msg) > 0:
                print(f"[RECV] Received: '{msg.decode()}' (seq={seq})")
                self.ack_num = seq + len(msg)
                return msg.decode()
        except socket.timeout:
            return None
        
        return None
    
    def close(self):
        """Close connection"""
        print("\n[CLOSE] Closing connection...")
        self.sock.close()
        self.connected = False


def run_server():
    """Run server in background thread"""
    server = SimpleTCP(5000, is_server=True)
    
    if server.handshake_server():
        # Receive messages
        for i in range(5):
            data = server.receive_data(timeout=3.0)
            if data:
                time.sleep(0.1)
            else:
                break
        
        # Send response
        time.sleep(0.5)
        server.send_data("Hello from server!")
    
    time.sleep(1)
    server.close()


def run_client():
    """Run client"""
    time.sleep(0.5)  # Wait for server to start
    
    client = SimpleTCP(5001, is_server=False)
    
    if client.handshake_client(5000):
        # Send messages
        for i in range(5):
            client.send_data(f"Message {i+1} from client")
            time.sleep(0.3)
        
        # Receive response
        time.sleep(0.5)
        client.receive_data(timeout=2.0)
    
    time.sleep(0.5)
    client.close()


if __name__ == "__main__":
    print("="*60)
    print("TCP-LIKE PROTOCOL DEMONSTRATION")
    print("="*60)
    print("\nThis demonstrates:")
    print("1. Three-way handshake (SYN, SYN-ACK, ACK)")
    print("2. Data transfer with sequence numbers")
    print("3. Bidirectional communication")
    print("\nStarting in 2 seconds...\n")
    time.sleep(2)
    
    # Run server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run client in main thread
    run_client()
    
    # Wait for server to finish
    server_thread.join(timeout=5)
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE!")
    print("="*60)