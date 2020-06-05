import sys

import numpy as np
import h5hep 


data = h5hep.initialize()

h5hep.create_group(data, "hits", counter="nhits")
h5hep.create_dataset(data, ["q", "t", "x", "y", "z"], group="hits", dtype=float)

event = h5hep.create_single_event(data)

infilename = sys.argv[1]
infile = open(infilename)

icount = 0
line = None
while 1:

    h5hep.clear_event(event)

    if icount%100 == 0:
        print(icount)

    line = infile.readline()
    if line is '':
        break
    nhits = int(line)
    #print(nhits)
    event['hits/nhits'] = nhits

    for n in range(nhits):
        line = infile.readline()
        vals = np.array(line.split(',')).astype(float)
        #print(vals)
        event['hits/q'].append(vals[0])
        event['hits/t'].append(vals[1])
        event['hits/x'].append(vals[2])
        event['hits/y'].append(vals[3])
        event['hits/z'].append(vals[4])


    icount += 1
    h5hep.pack(data,event)

outfilename = infilename.split('.')[0] + '.h5'
hdfile = h5hep.write_to_file(outfilename, data, comp_type="gzip", comp_opts=9)


