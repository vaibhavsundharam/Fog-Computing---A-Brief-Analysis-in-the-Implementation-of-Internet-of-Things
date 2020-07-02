import socket
import threading


PORT = 65000
SERVER_IP = socket.gethostbyname(socket.gethostname())
DISCONNECT_MSG = "Terminate!"
print("SERVER IP:", SERVER_IP, "SERVER PORT:", PORT)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((SERVER_IP,PORT))

def handle_client(conn, addr): # threads to handle multiple clients

    print(f"New connection---> {addr} connected to the server")
    connected = True
    while connected:
        handle = open("../Database.txt", "a")
        data = conn.recv(1024).decode("utf-8")
        if data == DISCONNECT_MSG:
            connected = False
        handle.write(data+"\n")
        handle.close()
        print(f"DATA RECEIVED:[{addr}]--->{data}\n")
        conn.send("DATA RECEIVED BY CLOUD SERVER".encode("utf-8"))
    conn.close()

def start_listening():
    soc.listen()
    print(f"[SERVER LISTENING ON] IP:{SERVER_IP} and PORT:{PORT}\n")
    while True:
        conn, addr = soc.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\nActive connection {threading.activeCount()-3}")

print("[SERVER STARTED]")
start_listening()
