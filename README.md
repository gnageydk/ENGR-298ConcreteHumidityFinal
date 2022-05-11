# ENGR-298ConcreteHumidityFinal

Recreating graphical analysis done in MatLab by using Python. Data samples taken from research done by Dr. Castaneda on relative humidity in concrete.
Using equations given in research documents, graphs were generated in order to display readings from sensors taken over the course of a year.

We are concerned with graphing these two values (Relative Humidity and Saturation) over time to observe the wetting and drying cycles of concrete over a year
in order to look into what might cause the deterioration of concrete. 

water-cycle-edquations used to write equations and solve for variables as well as plot graphs. Initialization used to parse through files given from sensors.

Packages used: numpy & matplotlib

Walkthrough: Files loaded into script for parsing, equations written with important variables labelled and answers stored into empty list. Used matpoltlib to graph
values against time, which were values given from separate .csv file.



Two days worth of time data (not a lot in the grand scheme of time frame) do not show up on the graph, which was an unresolved error we found when implementing
the equations into the graphs.

