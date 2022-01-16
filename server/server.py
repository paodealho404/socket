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
MSG_SEP = "|"

def handle_upload(socket, header):
    
    file_size, file_name = header.split(MSG_SEP,1) 
    file_path = f"{os.getcwd()}{os.sep}files{os.sep}{file_name}"
    # print(file_name, file_size)
    
    try:
        os.mkdir(f"{os.getcwd()}{os.sep}files")
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
    
    
    msg = f"File {file_name} received and uploaded to the server."
    
    socket.send(msg.encode(FORMAT))

def handle_download(socket, file_name):
    return

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {ADDR} connected")
    
    connected = True
    commands = { 
        "UPLD": handle_upload,
        "DWLD": handle_download,
        # "SHOW": handle_show_files,
        # "DELT": handle_deletion,
        # "HELP": handle_help,
        # "DISC": handle_disconnect,
    }
    while connected:
        cmd, msg = conn.recv(SIZE).decode(FORMAT).split(MSG_SEP,1) 
        
        commands.get(cmd)(conn, msg)
        

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
