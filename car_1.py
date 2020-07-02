from threading import Thread
import time
import socket
from timeit import default_timer as timer


Fog_server= str(input("Input FOG SERVER IP"))
if Fog_server=="":
    Fog_server="10.0.0.81"

Fog_port=5555
Fog_CONN = (Fog_server, Fog_port)

Vehicle_ip=socket.gethostbyname(socket.gethostname())
Vehicle_port=6901
Vehicle_CONN=(Vehicle_ip,Vehicle_port)

global start_timer
global stop_timer

def fn_client(string, *args):
    global start_timer
    cs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    handle = open("V1_START.txt", "w")
    while True:
        handle = open("V1_START.txt", "a")
        data = "P"+str(Vehicle_port)+ # insert random data
        start_timer = timer()
        cs.sendto(data.encode("utf-8"), Fog_CONN)
        print("ST",start_timer)
        handle.write(str(start_timer) + "\n")
        handle.close()
        time.sleep(0.02)

def fn_server(string, *args):
    global stop_timer
    ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(Vehicle_CONN)
    handle = open("V1_STOP.txt", "w")
    while True:
        handle = open("V1_STOP.txt", "a")
        print ("Server received '%s'" % (ss.recv(1024)))
        stop_timer = timer()
        print("ET", stop_timer,"\n")
        handle.write(str(stop_timer)+"\n")
        handle.close()
        time.sleep(0.02)

if __name__=='__main__':
    a = 0
    try:
        Thread(target=fn_client, args=(a, 1)).start()
        Thread(target=fn_server, args=(a, 1)).start()
    except Exception as errtxt:
        print(errtxt)