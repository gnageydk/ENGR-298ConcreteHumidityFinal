import math
import numpy as np

# equation 3-15
# x in this case is the impedance (Z) and S is the time
# ^ I don't think that's right I'm gonna double check with Castaneda
x = []
#S = (x/817.14) ** (1/-1.284)
#print(S)

# equation 2-14
# RH is relative humidity
# RHn is relative humidity at the nth hour
# avgRHk is average relative humidity at the first hour (so this value should remain the same throughout the program)
# k is hour one (so like might be 0:00:12 or alternatively 0:30:12)
# avgTk is the average temperature through the first hour

RH = RHn - "sum of k=1 through N" * (.0156)*(avgRHk)*(2.54**(-0.3502*k))/(1 + (avgTk - 25)/100)

### I have a meeting with Forsyth tomorrow so I will get this sorted out ^^
### I tested the equation to the right of the "sum of..." and it works