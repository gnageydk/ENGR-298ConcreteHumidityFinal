# import in any necessary python modules to use
# if you don't have these modules, hover over the red line on the right if using pycharm to then install the package
# in the popup that should show up -- you can also use the python packages tab at the bottom to manually install these:
import numpy as np
import pandas as pd
import datetime
import csv

# we care about Sensor 2 (FC67) and Sensor 4 (FDDD)
# initialize the datasets, define a path to each dataset, so then we can extract it
pathFC67_RH1 = '00000000_SpecialCase/20141221_NoRail_FC67_RH.csv'
pathFC67_TEMP1 = '00000000_SpecialCase/20141221_NoRail_FC67_Temp.csv'
pathFC67_RH2 = '00000000_SpecialCase/20150801_NoRail_FC67_RH.csv'
pathFC67_TEMP2 = '00000000_SpecialCase/20150801_NoRail_FC67_Temp.csv'
pathFC67_RH3 = '00000000_SpecialCase/20150913_NoRail_FC67_RH.csv'
pathFC67_TEMP3 = '00000000_SpecialCase/20150913_NoRail_FC67_Temp.csv'
pathFDDD_RH = '00000000_SpecialCase/YeRail-FDDD_RH.csv'
pathFDDD_TEMP = '00000000_SpecialCase/YeRail-FDDD_Temp.csv'

# define the columns2 we care about, column 0 is timestamp column 2 is RH or Temp data
columns1 = [0, 2]
headers = ['Date', 'Values']
# FDDD temp data
fullFDDDTempData = pd.read_csv(pathFDDD_TEMP, skiprows=20, usecols=columns1)
# create a new file of just the data we care about because dataframes are difficult to work with
fullFDDDTempData.to_csv('FDDD_Temp_Data.csv', header=headers)

# FDDD rh data
fullFDDDRhData = pd.read_csv(pathFDDD_RH, skiprows=20, usecols=columns1)
fullFDDDRhData.to_csv('FDDD_Rh_Data.csv', header=headers)

# FC67 temp data
FC67TempData1 = pd.read_csv(pathFC67_TEMP1, skiprows=20, usecols=columns1)
FC67TempData2 = pd.read_csv(pathFC67_TEMP2, skiprows=20, usecols=columns1)
FC67TempData3 = pd.read_csv(pathFC67_TEMP3, skiprows=20, usecols=columns1)

FC67TempFrames = [FC67TempData1, FC67TempData2, FC67TempData3]
fullFC67TempData = np.concatenate(FC67TempFrames)
# because this is a now a numpy array since we used np.concatenate, we need to use a different method to save it
# we'll convert it back into a pandas dataframe and then save it as a csv file
fullFC67TempDataFrame = pd.DataFrame(fullFC67TempData)
fullFC67TempDataFrame.to_csv('FC67_Temp_Data.csv', header=headers)

# FC67 rh data
FC67RhData1 = pd.read_csv(pathFC67_RH1, skiprows=20, usecols=columns1)
FC67RhData2 = pd.read_csv(pathFC67_RH2, skiprows=20, usecols=columns1)
FC67RhData3 = pd.read_csv(pathFC67_RH3, skiprows=20, usecols=columns1)

FC67RhFrames = [FC67RhData1, FC67RhData2, FC67RhData3]
fullFC67RhData = np.concatenate(FC67RhFrames)
fullFC67RhDataFrame = pd.DataFrame(fullFC67RhData)
fullFC67RhDataFrame.to_csv('FC67_Rh_Data.csv', header=headers)

# import rest of dataset to extract sensor 2 and sensor 4 data
pathDATASET1 = '00000000_SpecialCase/DATALOG-retrieved_at_20141207.csv'
pathDATASET2 = '00000000_SpecialCase/DATALOG-retrieved_at_20141214.csv'
pathDATASET3 = '00000000_SpecialCase/DATALOG-retrieved_at_20141221.csv'
pathDATASET4 = '00000000_SpecialCase/DATALOG-retrieved_at_20150627.csv'
pathDATASET5 = '00000000_SpecialCase/DATALOG-retrieved_at_20150704.csv'
pathDATASET6 = '00000000_SpecialCase/DATALOG-retrieved_at_20150711.csv'
pathDATASET7 = '00000000_SpecialCase/DATALOG-retrieved_at_20150718.csv'
pathDATASET8 = '00000000_SpecialCase/DATALOG-retrieved_at_20150725.csv'
pathDATASET9 = '00000000_SpecialCase/DATALOG-retrieved_at_20150801.csv'
pathDATASET10 = '00000000_SpecialCase/DATALOG-retrieved_at_20150807.csv'
pathDATASET11 = '00000000_SpecialCase/DATALOG-retrieved_at_20150816.csv'
pathDATASET12 = '00000000_SpecialCase/DATALOG-retrieved_at_20150822.csv'
pathDATASET13 = '00000000_SpecialCase/DATALOG-retrieved_at_20150829.csv'
pathDATASET14 = '00000000_SpecialCase/DATALOG-retrieved_at_20150905.csv'
pathDATASET15 = '00000000_SpecialCase/DATALOG-retrieved_at_20150913.csv'

# define columns we care about for the DATASET files
# 1 is timestamp, 7 is sensor 2 data, 11 is sensor 4 data
columns2 = [1, 7, 11]
# we can use the filepath variables to then import the data, usecols to specify what exact data we're grabbing

DATASET1 = pd.read_csv(pathDATASET1, usecols=columns2)
DATASET2 = pd.read_csv(pathDATASET2, usecols=columns2)
DATASET3 = pd.read_csv(pathDATASET3, usecols=columns2)
DATASET4 = pd.read_csv(pathDATASET4, usecols=columns2)
DATASET5 = pd.read_csv(pathDATASET5, usecols=columns2)
DATASET6 = pd.read_csv(pathDATASET6, usecols=columns2)
DATASET7 = pd.read_csv(pathDATASET7, usecols=columns2)
DATASET8 = pd.read_csv(pathDATASET8, usecols=columns2)
DATASET9 = pd.read_csv(pathDATASET9, usecols=columns2)
DATASET10 = pd.read_csv(pathDATASET10, usecols=columns2)
DATASET11 = pd.read_csv(pathDATASET11, usecols=columns2)
DATASET12 = pd.read_csv(pathDATASET12, usecols=columns2)
DATASET13 = pd.read_csv(pathDATASET13, usecols=columns2)
DATASET14 = pd.read_csv(pathDATASET14, usecols=columns2)
DATASET15 = pd.read_csv(pathDATASET15, usecols=columns2)

# concatenate full dataset together
dataframes = [DATASET1, DATASET2, DATASET3, DATASET4, DATASET5, DATASET6, DATASET7, DATASET8, DATASET9, DATASET10,
              DATASET11, DATASET12, DATASET13, DATASET14, DATASET15]
fullDATASET = np.concatenate(dataframes)
# convert back into pandas dataframe
fullDATASETFrame = pd.DataFrame(fullDATASET)
# convert into a csv file we can use in other files
headers2 = ['Date', 'FC67', 'FDDD']
fullDATASETFrame.to_csv('Sensor_Impedance_Values.csv', header=headers2)





