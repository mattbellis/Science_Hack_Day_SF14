import struct
from icecube_tools import get_collisions,display_icecube_detectors,get_detector_info

import sys

infilename = sys.argv[1]
infile = open(infilename, "rb")
collisions = get_collisions(infile)

print(len(collisions))

outfilename = infilename.split('.odf')[0] + '.csv'
print(outfilename)

output = ""

for collision in collisions:
    #print(type(collision))
    q,t,x,y,z = get_detector_info(collision)
    #print(q,t,x,y,z)
    output += "{0}\n".format(len(q))
    for a,b,c,d,e in zip(q,t,x,y,z):
        output += '{0},{1},{2},{3},{4}\n'.format(a,b,c,d,e)


outfile = open(outfilename,'w')
outfile.write(output)
outfile.close()
