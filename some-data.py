import numpy as np
from Initialization import fullFDDDRhData, fullFC67RhData, fullFDDDTempData, fullFC67TempData
import statistics as s
import pandas as pd

# equation 3-15
# x in this case is the impedance (Z) and S is the time
# ^ I don't think that's right I'm gonna double check with Castaneda


x = []
#S = (x/817.14) ** (1/-1.284)
#print(S)

# equation 2-14
# RH is relative humidity
# RHn is relative humidity at the Nth hour
# avgRHk is average relative humidity at the first hour (so this value should remain the same throughout the program)
# k is hour one (so like might be 0:00:12 or alternatively 0:30:12)
# Tkavg is the average temperature through the hour

RHFDDD = [fullFDDDRhData]
N = len(RHFDDD)
avgRH_list = []
for i in range(0,6,N):
    RHFDDDlist = pd['Value'].tolist()
    RHavg = s.mean(RHFDDDlist[i:i + 5])
    avgRH_list.append(RHavg)
RHnFDDD = s.mean(RHFDDD[-1:-6])

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