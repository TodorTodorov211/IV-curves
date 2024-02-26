import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

data_folder = ""

def linear(x, a, b):
    return a * x + b


def remove_outliers(raw_data):
    outliers = []
    index = 0 
    while index < len(raw_data) - 1:
        if raw_data[index, 1] <  raw_data[index+1, [1]] / 5:
            print("deleting")
            raw_data = np.delete(raw_data, index+1, axis=0)
            index -= 1
        index += 1
    
    
    return raw_data


def variation_rate(current, voltage):
    dI = []
    dV = []
    dI = savgol_filter(current, 100, 9, 1)
    I = savgol_filter(current, 100, 9, 0)
    
    plt.scatter(voltage, current, marker='.', alpha=0.1)
    plt.plot(voltage, I)
    plt.ylabel("Current[mA]")
    plt.xlabel("Voltage[V]")
    plt.tight_layout()
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


def pick_range(raw_data, begin, end):
    selected_data = np.array([[-1, -1]])
    for index in range(0, len(raw_data)):
        if raw_data[index, 1] > begin and raw_data[index, 1] < end:
            selected_data = np.append(selected_data, [raw_data[index, :]], axis=0)
    
    selected_data = np.delete(selected_data, 0, axis=0)
    return selected_data


def find_quenching_resistance(raw_data, begin, end):
    selection = pick_range(raw_data, begin, end)
    popt, pcov = curve_fit(linear, selection[:, 0], selection[:, 1])
    plt.scatter(selection[:, 0], selection[:, 1], marker='.')
    plt.plot(selection[:, 0], linear(selection[:, 0], *popt))
    print(popt)
    print(np.sqrt(np.diag(pcov)))
    plt.show()
    


def reverse_procedure(sipm_no):
    filename = "Reverse/50.00_54.00_0.01_"+ str(sipm_no) +".txt"
    data_reverse = np.genfromtxt(data_folder + filename, skip_header=1)
    data_reverse = remove_outliers(data_reverse)
    change = variation_rate(data_reverse[:, 1], data_reverse[:, 0])
    max_loc = np.argmax(change[1:])
    print(data_reverse[max_loc+2, 0])
    plt.scatter(data_reverse[1:, 0], change, marker='.')
    plt.show()


def forward_procedure(sipm_no):
    filename = "Forward/0.00_0.40_0.00_" + str(sipm_no) + ".txt"
    data_forward = np.genfromtxt(data_folder + filename, skip_header=1)
    #find_quenching_resistance(data_forward, 5, 6)
    plt.scatter(data_forward[:, 0], data_forward[:, 1], marker='.')
    plt.show()
    

         
     

if __name__ == "__main__":

    forward_procedure(413)

