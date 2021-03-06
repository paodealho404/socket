import socket
import os
import platform
import sys

# HOST = '127.0.0.1'
SIZE = 4096
FORMAT = "utf-8" 
MSG_SEP = "|"

def handle_deletion(socket):
    file_name = input("Enter the filename to be DELETED from the server> ")
    server_response = delete_file(socket, file_name)
    print(f"[SERVER]: \n{server_response}")
    return True

def handle_upload(socket):
    file_path = input("Enter the absolute path of the file to be SENT to the server> ")
    server_response = send_file(socket, file_path)
    print(f"[SERVER]: \n{server_response}")
    return True

def handle_download(socket):
    file_name = input("Enter the filename to be DOWNLOADED from the server> ")
    server_response = download_file(socket, file_name)
    print(f"[SERVER]: \n{server_response}")
    return True
    
def handle_show_files(socket): 
    server_response = show_files(socket)
    print(f"[SERVER]: \n{server_response}")
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
    socket.send(f"DISC{MSG_SEP}".encode(FORMAT))
    server_response = socket.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]:\n{server_response}")
    return False

def receive_file(socket):
    file_size, file_name = (socket.recv(SIZE).decode(FORMAT).split(MSG_SEP, 1))
    to_receive = int(file_size)

    with open(f"client_files/{file_name}", 'wb') as file:
        print(file_name)
        while True:
            if to_receive > 0:
                bytes_read = socket.recv(min(to_receive, SIZE))               
                file.write(bytes_read)
                to_receive -= len(bytes_read)
            else:
                break
def download_file(socket, file_name):

    socket.send(f"DWLD{MSG_SEP}{file_name}".encode(FORMAT))
    file_confirmed = socket.recv(6).decode(FORMAT)

    if file_confirmed=='ACCEPT':
        client_files = f"{os.getcwd()}{os.sep}client_files"
        try:
            os.mkdir(client_files)
        except:
            pass  
        receive_file(socket)
    
    return socket.recv(SIZE).decode(FORMAT)

def delete_file(socket, file_name):
    socket.send(f"DELT{MSG_SEP}{file_name}".encode(FORMAT))
    return socket.recv(SIZE).decode(FORMAT)

def show_files(socket):
    socket.send(f"SHOW{MSG_SEP}".encode(FORMAT))
    return socket.recv(SIZE).decode(FORMAT)
        
def send_file(socket, file_path):
    try:
        file = open(file_path, 'rb')
        file_size = os.path.getsize(file_path)
        file_name = file_path.split(os.sep)[-1]
        
    except PermissionError:
        return "This is not a valid absolute path or there's no permission to access the file!\nCheck if you are giving a correct file path, instead of just the folder's path!"
    else:
        with file:
            bytes = file.read()
            socket.send(f"UPLD{MSG_SEP}{file_size}{MSG_SEP}{file_name}".encode(FORMAT))
            socket.sendall(bytes)
    return socket.recv(SIZE).decode(FORMAT)

def client_init():
    try: 
        HOST = sys.argv[1] 
    except:
        HOST = socket.gethostbyname(socket.gethostname())
    try:
        PORT = int(sys.argv[2])
    except:
        PORT = 2343
    return HOST,PORT

def clear():
    if os.name == 'nt': _ = os.system('cls')
    else: _ = os.system('clear')



def main():
    HOST,PORT = client_init()
    ADDR = (HOST,PORT)
    commands = { 
        "UPLD": handle_upload,
        "DWLD": handle_download,
        "SHOW": handle_show_files,
        "DELT": handle_deletion,
        "HELP": handle_help,
        "DISC": handle_disconnect,
    }
    
    menu_commands = ["Send File to the server",
                    "Download File from the server",
                    "List all files in the server",
                    "Delete a File from the server",
                    "Help", 
                    "Quit"]
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {HOST}: {PORT}")
    
    connected = True
    while connected:
        print("Functionalities: ")
        for index, command in enumerate(commands.keys()):
            print(f"- {command}\t {menu_commands[index]}")
        print("Choose one command...")
        
        cmd = input('> ').upper()
        connected = commands.get(cmd,handle_default)(client)
        input("Press enter to continue...")
        clear()

if __name__ == "__main__":
    main()
