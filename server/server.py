import socket
import threading
import os

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6656
ADDR = (HOST, PORT)
SIZE = 4096
FORMAT = "utf-8" 
MSG_SEP = "|"

def handle_upload(socket, header):
    
    file_size, file_name = header.split(MSG_SEP,1) 
    file_path = f"{os.getcwd()}{os.sep}server_files{os.sep}{file_name}"
    
    try:
        os.mkdir(f"{os.getcwd()}{os.sep}server_files")
    except:
        pass  
    
    to_receive = int(file_size)
    
    with open(file_path, 'wb') as file:
        while True:
            if to_receive > 0:
                bytes_read = socket.recv(min(to_receive, SIZE))               
                file.write(bytes_read)
                to_receive -= len(bytes_read)
            else:
                break
    
    
    msg = f"File {file_name} received on the server."
    socket.send(msg.encode(FORMAT))
    return True

def handle_download(socket, file_name):
    file_path = f"{os.getcwd()}{os.sep}server_files{os.sep}{file_name}"
    if os.path.exists(file_path):
        msg = "ACCEPT"
        socket.send(msg.encode(FORMAT))  
         
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as file:  
            bytes = file.read()
            socket.send(f"{file_size}{MSG_SEP}{file_name}".encode(FORMAT))
            socket.sendall(bytes)
        
        response = f"File {file_name} sended from to the server."

    else:
        msg = "REFUSE"
        socket.send(msg.encode(FORMAT))
        response = "File doesn't exist in server's folder"
        
    socket.send(response.encode(FORMAT))
    return True

def handle_show_files(socket, msg):
    files = os.scandir(f"{os.getcwd()}{os.sep}server_files")
    msg_files = '\n'
    for path in files:
        if path.is_file():
            msg_files += f"FILE\t {path.name}\n"
        elif path.is_dir():
            msg_files += f"DIR\t {path.name}\n"
            
    socket.send(msg_files.encode(FORMAT))
    return True

def handle_deletion(socket, file_name):
    file_path = f"{os.getcwd()}{os.sep}server_files{os.sep}{file_name}"
    if os.path.exists(file_path): 
        os.remove(file_path)
        response = f"File {file_name} deleted from to the server's folder."
    else:
        response = "File doesn't exist in server's folder"
        
    socket.send(response.encode(FORMAT))
    return True

def handle_disconnect(socket, msg):
    msg = "Disconnected"
    socket.send(msg.encode(FORMAT))
    socket.close()
    return False
        
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {ADDR} connected")
    
    connected = True
    commands = { 
        "UPLD": handle_upload,
        "DWLD": handle_download,
        "SHOW": handle_show_files,
        "DELT": handle_deletion,
        "DISC": handle_disconnect,
    }

    while connected:
        cmd, msg = conn.recv(SIZE).decode(FORMAT).split(MSG_SEP,1)
        connected = commands.get(cmd)(conn, msg)
        print(f"[CLIENT] {addr} COMMAND: ({cmd})")

    # conn.close()

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
