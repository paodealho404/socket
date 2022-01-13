import socket
import threading
import os

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6656
ADDR = (HOST, PORT)
SIZE = 4096
FORMAT = "utf-8" 
DISCONNECT_MSG = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {ADDR} connected")
    
    connected = True
    while connected:
        file_name = conn.recv(SIZE).decode(FORMAT)
        print(file_name)
        data = conn.recv(SIZE)
        # if msg == DISCONNECT_MSG:
        #     connected = False
        
        # file_name, data = msg.split(">", 1)
        
        # print(f"[{addr}] {data}")
        print(f"[{addr}]")
        
        msg = f"File {file_name} received"
        # data = wikipedia.summary(data, sentences=1)
        conn.send(msg.encode(FORMAT))
        
        try:
            os.mkdir("files")
        except:
            pass  
        
        file = open(f"files/{file_name}", 'wb')
        file.write(data)
        file.close()
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}: {PORT}")
    while True: 
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
