import numpy as np
import sys
from datetime import datetime

infile = open(sys.argv[1])

dates,lats,longs,depths,mags = np.loadtxt(infile,skiprows=1,unpack=True,usecols=(0,1,2,3,4),delimiter=',',dtype=str)

#print dates

newdates = []


for d,lat,long,depth,mag in zip(dates,lats,longs,depths,mags):
    #print d
    year = int(d.split('-')[0])
    month = int(d.split('-')[1])
    day = int(d.split('-')[2].split("T")[0])
    hour = int(d.split("T")[1].split(':')[0])
    min  = int(d.split("T")[1].split(':')[2].split('.')[0])

    #print year,month,day,hour,min

    x = datetime(year, month, day, hour, min)

    newdates.append((x,lat,long,depth,mag))
    
    #print x

sorteddates = sorted(newdates,key=lambda x: x[0])

#print sorteddates

tot_min = 2. # minutes
fps = 30. # frames per second
max_time_diff_in_seconds = (sorteddates[-1][0]-sorteddates[0][0]).total_seconds()
for s in sorteddates:
    time_diff_in_seconds = (s[0]-sorteddates[0][0]).total_seconds()
    newtime = int(60*tot_min*fps*time_diff_in_seconds/max_time_diff_in_seconds)
    print "%d,%d,%d,%d,%s,%s,%s,%s" % (newtime,s[0].year,s[0].month,s[0].day,s[1],s[2],s[3],s[4])

    
