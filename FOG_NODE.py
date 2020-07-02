import socket
import re
import math
import threading
from collections import defaultdict
from timeit import default_timer as timer


global GPS_trace
global GPS_TRACE_DICT
#global Timer

GPS_trace = list()
GPS_TRACE_DICT = defaultdict(list)

FOG_PORT = 5555
FOG_IP = socket.gethostbyname(socket.gethostname())

CLOUD_SERVER_IP = str(input("Cloud Server IP: "))
if CLOUD_SERVER_IP=="":
    CLOUD_SERVER_IP='10.0.0.81'

CLOUD_SERVER_PORT = str(input("Cloud Server Port: "))
if CLOUD_SERVER_PORT=="":
    CLOUD_SERVER_PORT=65000

DISCONNECT_MSG = "Terminate!"

print("CLOUD IP:", CLOUD_SERVER_IP, "CLOUD PORT:", CLOUD_SERVER_PORT)


g_force_th = 0  # threshold value of g force
linear_acc_th=0  # threshold value of linear acceleration
orientation_th=0    # threshold value for orientation

soc_rx_v = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket for receiving data from vehicles
soc_rx_v.bind((FOG_IP,FOG_PORT))

S = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # socket for sending data back to the IOT device

global cmd
global Timer

cmd=int(input("Connect to Cloud 1/0"))

if cmd == 1:
    soc_tx_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket to send and receive data from cloud server
    soc_tx_c.connect((CLOUD_SERVER_IP, CLOUD_SERVER_PORT))


def send_data(data):
    send_data = data.encode("utf-8")
    soc_tx_c.send(send_data)

def recv_data():
    recv_data=soc_tx_c.recv(1024).decode("utf-8")
    print(recv_data)

def accelerometer(data):
    accelerometer = re.findall(",\s*3,\s*([0-9\.\+\-]+,\s*[0-9\.\+\-]+,\s*[0-9\.\+\-]+)", data)
    if len(accelerometer) != 0:
        accelerometer = accelerometer[0].split(",")
        acc_x, acc_y, acc_z = float(accelerometer[0]), float(accelerometer[1]), float(
            accelerometer[2])  # accelerometer reading in X, Y, Z direction
        g_force = math.sqrt(
            (acc_x / 9.81) ** 2 + (acc_y / 9.81) ** 2)  # 9.81 is acceleration due to gravity, g_force in X, Y direction
    else:
        acc_x, acc_y, acc_z, g_force = None, None, None, None
    return acc_x, acc_y, acc_z, g_force

def orientation(data):
    orientation = re.findall(",\s*81,\s*([0-9\.\+\-]+,\s*[0-9\.\+\-]+,\s*[0-9\.\+\-]+)", data)
    if len(orientation) != 0:
        orientation = orientation[0].split(",")
        ori_x, ori_y, ori_z = float(orientation[0]), float(orientation[1]), float(
            orientation[2])  # orientation in X, Y, Z direction
    else:
        ori_x, ori_y, ori_z = None, None, None
    return  ori_x, ori_y, ori_z

def gravity(data):
    gravity = re.findall(",\s*83,\s*([0-9\.\+\-]+,\s*[0-9\.\+\-]+,\s*[0-9\.\+\-]+)", data)
    if len(gravity) != 0:
        gravity = gravity[0].split(",")
        g_x, g_y, g_z = float(gravity[0]), float(gravity[1]), float(
            gravity[2])  # gravity reading in X, Y, Z direction
    else:
        g_x, g_y, g_z = None, None, None
    return g_x, g_y, g_z

def linear_acc(data):
    linear_acc = re.findall(",\s*82,\s*([0-9\.\+\-]+,\s*[0-9\.\+\-]+,\s*[0-9\.\+\-]+)", data)
    if len(linear_acc) != 0:
        linear_acc = linear_acc[0].split(",")
        l_x, l_y, l_z = float(linear_acc[0]), float(linear_acc[1]), float(
            linear_acc[2])  # linear acceleration of the car in X, Y, Z direction
    else:
        l_x, l_y, l_z = None, None, None
    return l_x, l_y, l_z

def GPS(data, addr):
    global GPS_trace
    global GPS_TRACE_DICT

    GPS = re.findall(",\s*1,\s*([0-9\.\+\-]+,\s*[0-9\.\+\-]+,\s*[0-9\.\+\-]+)", data)
    if len(GPS) != 0:
        GPS = GPS[0].split(",")
        coordinate = (addr, (float(GPS[0]), float(GPS[1])))  # User, Lat, Long for GPS location
    else:
        coordinate = None

    if coordinate != None:
        if len(GPS_trace) < 10:
            GPS_trace.append(coordinate)
        else:
            GPS_trace.pop(0)
            GPS_trace.append(coordinate)

    for i in GPS_trace:
        if i[1] not in GPS_TRACE_DICT[i[0][0]] and len(GPS_TRACE_DICT[i[0][0]]) < 5:
            GPS_TRACE_DICT[i[0][0]].append(i[1])
        elif i[1] not in GPS_TRACE_DICT[i[0][0]] and len(GPS_TRACE_DICT[i[0][0]]) >= 5:
            GPS_TRACE_DICT[i[0][0]].pop(0)
            GPS_TRACE_DICT[i[0][0]].append(i[1])
    return GPS_trace, GPS_TRACE_DICT

def handle_client(data, addr, cmd): # threads to handle multiple clients
    print(f"New connection---> {addr} connected to the fog server")
    print("Size of incoming data--->", len(data), "bytes")
    data = data.decode("utf-8")
    print("Decoded data--->", data)
    print("Vehicle Tx Address--->", addr)

    try:
        vehicle_rx_port = re.findall("^P([0-9]+)", data)
        vehicle_rx_address = (addr[0], int(vehicle_rx_port[0]))
        print("Vehicle Rx Address--->", vehicle_rx_address)
        Found=True
    except:
        print("Port number not received")
        Found=False
    # ============================================================================================ #
    acc_x, acc_y, acc_z, g_force = accelerometer(data)
    # ============================================================================================ #
    ori_x, ori_y, ori_z = orientation(data)
    # ============================================================================================ #
    g_x, g_y, g_z = gravity(data)
    # ============================================================================================ #
    l_x, l_y, l_z = linear_acc(data)
    # ============================================================================================ #
    GPS_trace, GPS_TRACE_DICT = GPS(data, addr)
    # ============================================================================================ #
    print("Trace dict:", GPS_TRACE_DICT)
    print(addr,"--->",f"G force: {g_force}---", f"Liner acceleration: {l_x,l_y,l_z}---", f"GPS: {GPS_trace}---",
          f"Orientation:{ori_x,ori_y,ori_z}---",f"Gravity:{g_x,g_y,g_z}")
    # ============================================================================================ #
    if g_force > g_force_th:
        print(addr,"---> Accident has occurred")
        if cmd ==1:
            data_server = (addr,GPS_TRACE_DICT[addr[0]])
            print("Data sent to the cloud server:",data_server)
            send_data(str(data_server))
            recv_data()
        print("\n")
        if Found==True:
            x = "Accident has occurred"
            S.sendto(x.encode("utf-8"), vehicle_rx_address)
    else:
        print("Safe\n")

def bit_rate(data,Timer):
    handle=open("Bit_Rate.txt","a")
    handle.write(str(Timer)+" "+str(len(data))+"\n")
    handle.close()

def start_listening():
    global cmd
    global Timer
    print(f"[FOG SERVER LISTENING ON] IP:{FOG_IP} and PORT:{FOG_PORT}\n")
    handle = open("Bit_Rate.txt", "w")
    while True:
        Timer=timer()
        data, addr = soc_rx_v.recvfrom(8192)
        bit_rate(data,Timer)
        print(f"Timer: {Timer} and Data Size: {len(data)}")
        thread = threading.Thread(target=handle_client, args=(data, addr, cmd))
        thread.daemon=True
        thread.start()

def main():
    print("FOG NODE INITIATED")
    start_listening()


main()
