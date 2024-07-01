import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def transform_timestamp(timestamp):
    current_time=int(timestamp[14])*600+int(timestamp[15])*60+int(timestamp[17])*10+int(timestamp[18])+int(timestamp[20])*0.1+int(timestamp[21])*0.01+int(timestamp[22])*0.001+int(timestamp[23])*0.0001+int(timestamp[24])*0.00001+int(timestamp[25])*0.000001
    return current_time

def transform_data(file_path):
    stats = pd.read_csv(file_path)
    timestamp = stats['# Timestamp']
    offset_data = stats[' Offset From Master']
    time=np.zeros(len(timestamp)+2)
    offset=np.zeros(len(timestamp)+2)
    time[0] = transform_timestamp(timestamp[0]) - 1
    offset[0] = 0
    time[1]=transform_timestamp(timestamp[0])-0.0001
    offset[1]=0
    for i in range(len(timestamp)):
        time[i+2]=transform_timestamp(timestamp[i])
        offset[i+2]=offset_data[i]
    return time, offset

def main():
    file_path_1='Attack_Results/ptpd_attack_1.stats'
    file_path_2 = 'Attack_Results/ptpd_attack_2.stats'
    file_path_3 = 'Attack_Results/ptpd_attack_3.stats'
    file_path_4 = 'Attack_Results/ptpd_benchmark.stats'

    cu_time, cu_offset= transform_data(file_path_3)
    cs_time, cs_offset = transform_data(file_path_1)
    rd_time, rd_offset = transform_data(file_path_2)
    bc_time, bc_offset = transform_data(file_path_4)
    #print(cu_offset)
    #print(cs_offset)
    #print(rd_offset)
    #print(bc_offset)
    plt.figure(figsize=(7,5.8))
    plt.plot(cu_time-cu_time[0], 1000*np.abs(cu_offset)/2, label="cumulative", color='r')
    #plt.plot(cs_time-cs_time[0], 1000*np.abs(cs_offset)/2, label="constant", color='r') #ms=5, marker='o'
    #plt.plot(rd_time-rd_time[0], 1000*np.abs(rd_offset)/2, label="random", color='r')
    plt.plot(bc_time-bc_time[0], 1000*np.abs(bc_offset)/2, label="no attack", color='b')
    plt.xlabel("Attack Elapsed Time (s)", fontsize=18)
    plt.ylabel("System time offsets (ms)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(range(0,150,30),fontsize=16)
    plt.legend(fontsize=16)
    plt.show()

main()