import numpy as np
import matplotlib.pyplot as plt

with open("V1_START.txt") as a, open("V1_STOP.txt") as b:
    start=np.array(a.read().split("\n")).astype(np.float)[:8000]
    stop=np.array(b.read().split("\n")).astype(np.float)[:8000]
    latency=(stop-start)*1000
    print("latency",latency,len(latency))
    mean_latncy=np.mean(latency)

    print("mean latency",mean_latncy, "ms")

    #x= np.linspace(0, 130, len(latency))
    plt.plot(latency,'c')
    plt.ylabel('response time for fog server (ms)')
    plt.xlabel('number of samples')
    plt.show()




