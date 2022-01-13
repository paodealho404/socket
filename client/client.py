import socket

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6656
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8" 
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {HOST}: {PORT}")
    
    connected = True
    while connected:
        print("Faça sua pesquisa no Wikipedia.")
        msg = input("> ")
        
        client.send(msg.encode(FORMAT))
        
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")

if __name__ == "__main__":
    main()
