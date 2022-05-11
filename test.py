import numpy as np
import statistics as s
import pandas as pd
import csv
import matplotlib.pyplot as plt
import datetime

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
    FDDDRhTimestamps.append(col['Date'])
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
    FC67RhTimestamps.append(col['Date'])
    FC67Rh.append(col['Values'])

#convert all timestamps to unix
# see https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-timestamp-in-python/amp/
# and https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# for overall documentation on what everything means
# this is the given format for a date from the sensors
date_example = "6/20/15 12:04:01 PM"
# below translates into %month/%day/%year %Hour:%Minute:%Seconds %pM or AM
date_format = "%m/%d/%y %H:%M:%S %p"
# now we can convert this into unix time
timestamp_format = datetime.datetime.strptime(date_example, date_format)
unix_time = datetime.datetime.timestamp(timestamp_format)

# ImpedanceTimestamps is already in Unix! Woohoo!

# FDDDRh to Unix
FDDDRhTimestampsUnix = []
i = 0
for x in FDDDRhTimestamps:
    timestamp_format = datetime.datetime.strptime(FDDDRhTimestamps[i], date_format)
    Unix = datetime.datetime.timestamp(timestamp_format)
    FDDDRhTimestampsUnix.append(Unix)
    i =+ 1
    if i == x:
        break

# FDDDTemp to Unix
FDDDTempTimestampsUnix = []
i = 0
for x in FDDDTempTimestamps:
    timestamp_format = datetime.datetime.strptime(FDDDTempTimestamps[i], date_format)
    Unix = datetime.datetime.timestamp(timestamp_format)
    FDDDTempTimestampsUnix.append(Unix)
    i =+ 1
    if i == x:
        break

# FC67Temp to Unix
FC67TempTimestampsUnix = []
i = 0
for x in FC67TempTimestamps:
    timestamp_format = datetime.datetime.strptime(FC67TempTimestamps[i], date_format)
    Unix = datetime.datetime.timestamp(timestamp_format)
    FC67TempTimestampsUnix.append(Unix)
    i =+ 1
    if i == x:
        break

# FC67Rh to Unix
FC67RhTimestampsUnix = []
i = 0
for x in FC67RhTimestamps:
    timestamp_format = datetime.datetime.strptime(FC67RhTimestamps[i], date_format)
    Unix = datetime.datetime.timestamp(timestamp_format)
    FC67TempTimestampsUnix.append(Unix)
    i =+ 1
    if i == x:
        break

# equation 3-15
# x in this case is the impedance (Z)

# k is hour one (so might be 0:00:12 or alternatively 0:30:12)
# Tkavg is the average temperature through the hour
###
RHFDDD = [FDDDRh]
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
RHFC67 = [FC67Rh]
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
TkFDDD = [FDDDTemp]
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


TkFC67 = [FC67Temp]
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

#fig, ax = plt.subplots()
#ax.plot(FC67Rh, FC67RhTimestamps)
#fig.show()
