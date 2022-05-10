import numpy as np
from Initialization import fullFDDDRhData, fullFC67RhData, fullFDDDTempData, fullFC67TempData
import statistics as s
import pandas as pd
import csv

#initialize data from csv files
#initialize impedance values
filename = open('Sensor_Impedance_Values.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FC67Impedance = []
FDDDImpedance = []
#Column 0 is timestamps, Column 1 is FC67, Column 2 is FDDD
for col in file:
    FC67Impedance.append(col['1'])
    FDDDImpedance.append(col['2'])

#initialize FDDD values
filename = open('FDDD_Temp_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FDDDTemp = []
#Column 0 is timestamps, Column 1 is Temp
for col in file:
    FDDDTemp.append(col['23.394'])

filename = open('FDDD_Rh_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FDDDRh = []
#Column 0 is timestamps, Column 1 is Rh
for col in file:
    FDDDRh.append(col['43.159'])

#initialize FC67 values
filename = open('FC67_Temp_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FC67Temp = []
#Column 0 is timestamps, Column 1 is Temp
for col in file:
    FC67Temp.append(col['1'])

filename = open('FC67_Rh_Data.csv', 'r')
file = csv.DictReader(filename)
#setup empty lists of variables we want
FC67Rh = []
#Column 0 is timestamps, Column 1 is Rh
for col in file:
    FC67Rh.append(col['1'])

# equation 3-15
# x in this case is the impedance (Z) and S is the time

#Impedance calculations for FC67
#convert to numpy array to iterate through the list
#and use .astype(float) to convert the list of strings into float values
x1 = np.array(FC67Impedance).astype(float)
S1 = (x1/817.14) ** (1/-1.284)
print(S1)

#Impedance calculations for FDDD
x2 = np.array(FDDDImpedance).astype(float)
S2 = (x2/817.14) ** (1/-1.284)
print(S2)

# equation 2-14
# RH is relative humidity
# RHn is relative humidity at the Nth hour
# avgRHk is average relative humidity at the first hour (so this value should remain the same throughout the program)
# k is hour one (so like might be 0:00:12 or alternatively 0:30:12)
# Tkavg is the average temperature through the hour
###
RHFDDD = [fullFDDDRhData]
N = len(RHFDDD)
avgRH_list = []
for i in range(0,6,N):
    RHFDDDlist = pd[',Value'].tolist()
    RHavg = s.mean(RHFDDDlist[i:i + 5])
    avgRH_list.append(RHavg)
RHnFDDD = s.mean(RHFDDD[-1:-6])
###
RHFC67 = [fullFC67RhData]
N = len(RHFC67)
avgRH_list = []
for i in range(0,6,N):
    values = RHFC67[i:i + 5]
    RHavg = s.mean(values)
    avgRH_list.append(RHavg)
RHnFC67 = s.mean(RHFC67[-1:-6])

# now that the values that require averages are calculated, we can finally use equ. 2-14
# equation involves a summation between parameters, which we can use a for loop to do

# Tk is the temperature at a given hour
# M is just N in this case to represent the Mth hour
TkFDDD = [fullFDDDTempData]
M = len(TkFDDD)
avgTk_list = []
for i in range(0,6,M):
    values = TkFDDD[i:i+5]
    Tkavg = s.mean(values)
    avgTk_list.append(Tkavg)

Sum_Function = 0

N = len(avgRH_list)
for k in range(0,N):
    Sum_Function += (.0156) * (avgRH_list[k]) * (2.54 ** (-0.3502 * k)) / (1 + (Tkavg - 25) / 100)
    RH1 = RHnFDDD - Sum_Function


TkFC67 = [fullFC67TempData]
M = len(TkFC67)
avgTk_list = []
for i in range(0,6,M):
    values = TkFC67[i:i+5]
    Tkavg = s.mean(values)
    avgTk_list.append(Tkavg)

Sum_Function = 0

N = len(avgRH_list)
for k in range(0,N):
    Sum_Function = (.0156) * (avgRH_list[k]) * (2.54 ** (-0.3502 * k)) / (1 + (Tkavg - 25) / 100)
    RH1 = RHnFDDD - Sum_Function

# RH = RHn - "sum of k=1 through N" * (.0156)*(avgRHk)*(2.54**(-0.3502*k))/(1 + (avgTk - 25)/100)

### I tested the equation to the right of the "sum of..." and it works