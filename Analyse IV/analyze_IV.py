import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_folder = ""

def variation_rate(current, voltage):
    dI = []
    dV = []
    dI = savgol_filter(current, 100, 9, 1)
    I = savgol_filter(current, 100, 9, 0)
    
    plt.scatter(voltage, current, marker='.', alpha=0.1)
    plt.plot(voltage, I)
    plt.show()
    for index, iterator in enumerate(current):
        if(index == 0):
            continue
        #dI.append(current[index] - current[index - 1])
        dV.append(voltage[index] - voltage[index - 1])
    #dI = np.array(dI)
    dV = np.array(dV)
    dI = np.delete(dI, 0)
    current = np.delete(current, 0)
    voltage = np.delete(voltage, 0)
    return (1 / current) * (dI / dV)
    #return dI / dV
         
     

if __name__ == "__main__":

    #data_reverse = np.genfromtxt(data_folder + "Reverse/50.00_53.00_0.01_411.txt", skip_header=1)
    data_reverse = np.genfromtxt(data_folder + "Reverse/51.00_53.00_0.01_414.txt", skip_header=1)
    change = variation_rate(data_reverse[:, 1], data_reverse[:, 0])
    #plt.scatter(data_reverse[:, 0], data_reverse[:, 1], marker='.')
    #plt.show()
    plt.scatter(data_reverse[1:, 0], change, marker='.')
    plt.show()