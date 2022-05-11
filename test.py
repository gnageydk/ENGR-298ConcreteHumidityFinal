import numpy as np
from Initialization import fullFDDDRhData, fullFC67RhData, fullFDDDTempData, fullFC67TempData
import statistics as s
import pandas as pd
import csv
import matplotlib.pyplot as plt

#initialize data from csv files
#initialize impedance values
filename = open('Sensor_Impedance_Values.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
ImpedanceTimestamps =[]
FC67Impedance = []
FDDDImpedance = []
#Column 0 is timestamps, Column 1 is FC67, Column 2 is FDDD
for col in file:
    ImpedanceTimestamps.append(col['Date'])
    FC67Impedance.append(col['FC67'])
    FDDDImpedance.append(col['FDDD'])

#initialize FDDD values
filename = open('FDDD_Temp_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FDDDTempTimestamps = []
FDDDTemp = []
#Column 0 is timestamps, Column 1 is Temp
#Columns don't have headers on these files for some reason, so we identify them via their first object
for col in file:
    FDDDTempTimestamps.append(col['Date'])
    FDDDTemp.append(col['Values'])

filename = open('FDDD_Rh_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FDDDRhTimestamps = []
FDDDRh = []
#Column 0 is timestamps, Column 1 is Rh
for col in file:
    #FDDDRhTimestamps(col['Date'])
    FDDDRh.append(col['Values'])

#initialize FC67 values
filename = open('FC67_Temp_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FC67TempTimestamps = []
FC67Temp = []
#Column 0 is timestamps, Column 1 is Temp
for col in file:
    FC67TempTimestamps.append(col['Date'])
    FC67Temp.append(col['Values'])

filename = open('FC67_Rh_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FC67RhTimestamps = []
FC67Rh = []
#Column 0 is timestamps, Column 1 is Rh
for col in file:
    #FC67RhTimestamps(col['Date'])
    FC67Rh.append(col['Values'])

# equation 3-15
# x in this case is the impedance (Z)

# k is hour one (so might be 0:00:12 or alternatively 0:30:12)
# Tkavg is the average temperature through the hour
###
RHFDDD = [fullFDDDRhData]
RHFDDD = np.array(FDDDRh).astype(float)
N = len(RHFDDD)
avgRH_list = []
for i in range(0,6,N):
#    RHFDDDlist = pd[',Value'].tolist()
#    RHavg = s.mean(RHFDDDlist[i:i + 5])
    values = RHFDDD[i:i+5]
    RHavg = np.average(values[i:i+5])
    avgRH_list.append(RHavg)

RHnFDDD = np.average(RHFDDD[-1:-6])

###
RHFC67 = [fullFC67RhData]
RHFC67 = np.array(FC67Rh).astype(float)
N = len(RHFC67)
avgRH_list = []
for i in range(0,6,N):
    values = RHFC67[i:i+5]
    RHavg = np.average(values)
    avgRH_list.append(RHavg)
RHnFC67 = np.average(RHFC67[-1:-6])

# now that the values that require averages are calculated, we can finally use equ. 2-14
# equation involves a summation between parameters, which we can use a for loop to do

# Tk is the temperature at a given hour
# M is just N in this case to represent the Mth hour
TkFDDD = [fullFDDDTempData]
TkFDDD = np.array(FDDDTemp).astype(float)
M = len(TkFDDD)
avgTk_list = []
for i in range(0,6,M):
    values = TkFDDD[i:i+5]
    Tkavg = np.average(values)
    avgTk_list.append(Tkavg)

Sum_Function = 0

N = len(avgRH_list)
for k in range(0,N):
    Sum_Function += (.0156) * (avgRH_list[k]) * (2.54 ** (-0.3502 * k)) / (1 + (Tkavg - 25) / 100)
    RH1 = RHnFDDD - Sum_Function


TkFC67 = [fullFC67TempData]
TkFC67 = np.array(FC67Temp).astype(float)
M = len(TkFC67)
avgTk_list = []
for i in range(0,6,M):
    values = TkFC67[i:i+5]
    Tkavg = np.average(values)
    avgTk_list.append(Tkavg)

Sum_Function = 0

N = len(avgRH_list)
for k in range(0,N):
    Sum_Function = (.0156) * (avgRH_list[k]) * (2.54 ** (-0.3502 * k)) / (1 + (Tkavg - 25) / 100)
    RH1 = RHnFDDD - Sum_Function

fig, ax = plt.subplots()
ax.plot(FC67Rh, FC67RhTimestamps)
fig.show()
