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
# x in this case is the impedance (Z) (found in datalog data with the corresponding sensor)

x = []
S = (x/817.14) ** (1/-1.284)
print(S)

# equation 2-14
# RH is relative humidity
# RHn is relative humidity at the Nth hour
# avgRHk is average relative humidity at the first hour (so this value should remain the same throughout the program)
# k is hour one (so like might be 0:00:12 or alternatively 0:30:12)
# Tkavg is the average temperature through the hour
###
RHFDDD = np.array(FDDDRh).astype(float)
N = len(RHFDDD)
avgRH_list = []
for i in range(0,6,N):
    values = RHFDDD[i:i + 5]
    RHavg = s.mean(values[i:i + 5])
    avgRH_list.append(RHavg)
RHnFDDD = s.mean(RHFDDD[-1:-6])
print(RHnFDDD)
###
RHFC67 = [fullFC67RhData]
N = len(RHFC67)
avgRH_list = []
for i in range(0,6,N):
    values = RHFC67[i:i+5]
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