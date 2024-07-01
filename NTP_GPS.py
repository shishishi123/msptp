import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def transform_timestamp(timestamp):
    current_time=int(timestamp[14])*600+int(timestamp[15])*60+int(timestamp[17])*10+int(timestamp[18])
    return current_time

def retrive_ID(line):
    end_index=20
    for i in range(100):
        if line[20+i]!=" ":
            end_index=end_index+1
        else:
            break
    return line[20:end_index], end_index

def retrieve_offset(line,end_index):
    first_index=0
    last_index=0
    for i in range(100):
        if line[end_index+i]!=" ":
            first_index=end_index+i+11
            break
    last_index=first_index
    for i in range(100):
        if line[first_index + i] != " ":
            last_index=last_index+1
        else:
            break
    return line[first_index:last_index]


def read_log_file(file_path):
    time=[]
    ID=[]
    offset=[]
    with open(file_path) as f:
        f = f.readlines()
    for line in f:
        time.append(line[0:19])
        current_id, current_end_index=retrive_ID(line)
        ID.append(current_id)
        current_offset=retrieve_offset(line,current_end_index)
        offset.append(current_offset)
    return time, ID, offset


def organize_data(time, ID, offset):
    node_1_time=[]
    node_1_offset=[]
    node_2_time =[]
    node_2_offset =[]
    node_3_time =[]
    node_3_offset =[]
    node_4_time = []
    node_4_offset = []
    node_5_time = []
    node_5_offset = []
    for i in range(len(ID)):
        if ID[i]=="192.48.105.15":
            node_1_time.append(time[i])
            node_1_offset.append(offset[i])
        elif ID[i]=="2604:2dc0:202:300::3c0":
            node_2_time.append(time[i])
            node_2_offset.append(offset[i])
        elif ID[i]=="2607:5600:182:500::1":
            node_3_time.append(time[i])
            node_3_offset.append(offset[i])
        elif ID[i]=="74.207.242.234":
            node_4_time.append(time[i])
            node_4_offset.append(offset[i])
        else:
            node_5_time.append(time[i])
            node_5_offset.append(offset[i])
    return np.array(node_1_time),np.array(node_1_offset),np.array(node_2_time),np.array(node_2_offset),np.array(node_3_time),np.array(node_3_offset),np.array(node_4_time),np.array(node_4_offset), np.array(node_5_time), np.array(node_5_offset)

def brents_aggregation(honest_clocks, byzantine_clocks, f):
    measurements=np.zeros(3*f + 1)
    measurements[0:2*f + 1]=honest_clocks
    measurements[2*f + 1:]=byzantine_clocks
    scores = np.zeros(3*f + 1)
    distances=np.zeros(3*f + 1)
    for i in range(3*f + 1):
        distances=np.abs(measurements-measurements[i])
        distances.sort()
        scores[i]=np.sum(np.square(distances[1:2*f+1]))
    indices=scores.argsort()
    output=np.sum(measurements[indices[0:2 *f]])/(2*f)
    return output

def series_aggregation(offset1, offset2, offset3):
    brents_output=[]
    for i in range(len(offset1)):
        brents_output.append(brents_aggregation(np.array([offset1[i],offset2[i],offset3[i]]),np.array([0.1]),1))
    return np.mean(np.array(brents_output)), np.std(np.array(brents_output))


def main():
    file_path="Attack_Results/statistics.log"
    time, ID, offset=read_log_file(file_path)
    time1,offset1,time2,offset2,time3,offset3,time4,offset4,time5,offset5=organize_data(time, ID, offset)
    mean1, std1=series_aggregation(offset2, offset3, offset1)
    mean2, std2 = series_aggregation(offset2, offset3, offset5)

    print("mean1",1000*mean1)
    print("mean1", 1000*std1)
    print("mean1", 1000*mean2)
    print("mean1", 1000*std2)
main()

