# TCP-like Protocol Implementation

A Python implementation of TCP protocol features including three-way handshake, data transfer, and connection management.

## 🎯 Features

- **Three-way handshake** (SYN, SYN-ACK, ACK)
- **Sequence number tracking** for reliable data transfer
- **Flow control** with window management
- **Multithreaded** client-server architecture
- **Connection state management** (10 TCP states)
- **Graceful connection termination** (FIN handshake)

## 📁 Files

- `tcp_implementation.py` - Full TCP implementation with client/server modes
- `tcp_test.py` - Simple single-process demonstration
- `tcp_client.py` - Standalone client (if you have it)
- `tcp_server.py` - Standalone server (if you have it)

## 🚀 Quick Start

### Simple Demo (Single Terminal)

```bash
python3 tcp_test.py
```

This runs a self-contained demonstration showing:
- Three-way handshake
- Data transfer with sequence numbers
- Bidirectional communication

### Full Implementation (Two Terminals)

**Terminal 1 (Server):**
```bash
python3 tcp_implementation.py server
```

**Terminal 2 (Client):**
```bash
python3 tcp_implementation.py
```

## 📊 Example Output

```
=== TCP Client ===
[CONNECT] Starting connection to 127.0.0.1:9999
[CONNECT] Sent SYN with seq=12345
[CONNECT] Received SYN-ACK with seq=67890, ack=12346
[CONNECT] Sent ACK, connection established
Connected!
[SEND] Sent 22 bytes with seq=12346
[SEND] Sent 22 bytes with seq=12368
...
```

## 🛠️ Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 📖 How It Works

### Three-Way Handshake
1. Client sends **SYN** with initial sequence number
2. Server responds with **SYN-ACK** (acknowledges client's SYN + sends its own)
3. Client sends **ACK** (acknowledges server's SYN)
4. Connection **ESTABLISHED**!

### Data Transfer
- Each byte is tracked with sequence numbers
- Receiver sends ACK for received data
- Window size controls flow control

### Connection Termination
1. Active closer sends **FIN**
2. Receiver acknowledges with **ACK**
3. Receiver sends its own **FIN**
4. Original sender sends final **ACK**

## 🎓 Educational Purpose

This project demonstrates:
- TCP state machine implementation
- Network protocol design
- Socket programming (UDP as transport)
- Concurrent programming with threads
- Binary data serialization

**Note:** This uses UDP sockets to simulate the underlying network layer. Real TCP is implemented in the kernel.

## ⚠️ Limitations

- Simplified checksum (not RFC-compliant)
- No retransmission on packet loss
- Basic congestion control
- No delayed ACKs or Nagle's algorithm
- Uses UDP for simulation (not raw sockets)

## 🔧 Troubleshooting

**"Address already in use":**
```bash
# Linux/Mac
sudo lsof -i :9999
sudo fuser -k 9999/udp

# Windows
netstat -ano | findstr :9999
taskkill /PID <pid> /F
```

**Connection timeout:**
- Start server before client
- Check firewall settings
- Ensure ports 9998 and 9999 are available

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request


## 🙏 Acknowledgments

- Based on RFC 793 (TCP Specification)
- Educational project for understanding network protocols

---

**⭐ Star this repo if it helped you understand TCP!**