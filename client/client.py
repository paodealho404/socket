import socket
import os
import platform 

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6656
ADDR = (HOST, PORT)
SIZE = 4096
FORMAT = "utf-8" 
DISCONNECT_MSG = "!DISCONNECT"

def list_files(caminho):
    # files = os.listdir(caminho)
    files = os.scandir(caminho)
    # print(files)
    for path in files:
        if path.is_file():
            print(f"FILE\t {path.name}")
        elif path.is_dir():
            print(f"DIR\t {path.name}")

def get_path(file): 
    separator = os.sep
    return f"{os.getcwd()}{separator}{file}"

def send_file(socket, file_path, receiver):
    try:
        file = open(file_path, 'rb')
        file_name = file_path.split(os.sep)[-1]
    except PermissionError:
        return "some default data"
    else:
        with file:
            bytes = file.read()
            
            socket.send(file_name.encode(FORMAT))
            socket.send(bytes)
            # socket.send(f"{file_name}>{bytes}".encode(FORMAT))
            


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {HOST}: {PORT}")
    
    connected = True
    while connected:
        # list_files('files')
        
        file_path = get_path(input("> "))
        
        send_file(client, file_path, ' ')
        # msg = input("> ")
        
        
        # client.send(msg.encode(FORMAT))
        
        if file_path == DISCONNECT_MSG:
            connected = False
        else:
            file_path = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {file_path}")

if __name__ == "__main__":
    main()
