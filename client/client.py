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
MSG_SEP = "|"

def handle_deletion(socket):
    asda =''
    return True

def handle_upload(socket):
    file_path = input("Enter the absolute path of the file to be sent> ")
    send_file(socket, file_path)
    server_response = socket.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {server_response}")
    return True

def handle_download(socket):
    ad=''
    return True
    
def handle_show_files(socket):
    asd =''   
    return True

def handle_default(socket):
    print("This command is not currently recognized by this socket application!")
    return True
    
def handle_help(socket):
    help_commands = "This is the list of commands that are currently available:\n\nUPLD (Sends a file to the server from a client's given absolute path) \
    \nDWLD (Gets a file that matches the given filename from the server's current working directory)\nDELT (Removes a file that matches the given filename from the server)\n"
    print(help_commands)
    return True

def handle_disconnect(socket):
    return False
def list_files(caminho):
    # files = os.listdir(caminho)
    files = os.scandir(caminho)
    # print(files)
    for path in files:
        if path.is_file():
            print(f"FILE\t {path.name}")
        elif path.is_dir():
            print(f"DIR\t {path.name}")

def send_file(socket, file_path):
    try:
        file = open(file_path, 'rb')
        file_size = os.path.getsize(file_path)
        file_name = file_path.split(os.sep)[-1]
        
    except PermissionError:
        return "This is not a valid absolute path or there's no permission to access the file!"
    else:
        with file:
            bytes = file.read()
            socket.send(f"UPLD{MSG_SEP}{file_size}{MSG_SEP}{file_name}".encode(FORMAT))
            socket.sendall(bytes)


def main():
    commands = { 
        "UPLD": handle_upload,
        "DWLD": handle_download,
        "SHOW": handle_show_files,
        "DELT": handle_deletion,
        "HELP": handle_help,
        "DISC": handle_disconnect,
    }
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {HOST}: {PORT}")
    
    connected = True
    while connected:
        cmd = input('> ').upper()
        connected = commands.get(cmd,handle_default)(client)
        

if __name__ == "__main__":
    main()
