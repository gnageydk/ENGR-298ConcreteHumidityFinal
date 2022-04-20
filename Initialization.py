#import in any necessary python modules to use
import scipy
import numpy
import math
import statistics

#initialize the datasets, define a path to use
path = '/00000000_SpecialCase/20141221_NoRail_FC67_RH.csv'
RH_dataDec12_21 = np.loadtxt(path, skiprows=20, delimiter="")
