import re
import numpy as np
import matplotlib.pyplot as plt

with open("Bit_Rate.txt","r") as file:
    time=list()
    bytes_rx=list()
    for line in file:
        byte=re.findall("\s+([0-9.]+)",line)[0]
        bytes_rx.append(byte)
        t=re.findall("([0-9.]+)",line)[0]
        time.append(t)

    time=np.array(time).astype(float)
    bytes_rx=np.array(bytes_rx).astype(float)

    print(time)
    print(bytes_rx)
    print(np.mean(bytes_rx))
    print("total",np.sum(bytes_rx))
    num_sec=time[-1]-time[0]

    x=np.linspace(0,num_sec,len(time))
    plt.ylabel("Bytes received")
    plt.xlabel("Time (sec)")
    plt.plot(x,bytes_rx,".")
    plt.show()





