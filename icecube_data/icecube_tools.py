import numpy as np
import matplotlib.pylab as plt
import mpl_toolkits.mplot3d.art3d as a3

from fileio import read,write
import gzip 

################################################################################
def get_collisions(infile,verbose=False):

    ev=None

    events = []

    while 1:
        ev = read(infile)

        if ev is None:
            break
        else:
            events.append(ev)

    return events

    

################################################################################
def get_detector_info(collision):

    x=[];y=[];z=[];q=[];t=[]

    for h in collision.hits:
        q.append(h[0])
        t.append(h[1])
        x.append(h[2])
        y.append(h[3])
        z.append(h[4])

    q=np.array(q)
    t=np.array(t)
    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    return q,t,x,y,z

################################################################################
def display_icecube_detectors(collision):

    fig = plt.figure(figsize=(7,5),dpi=100)
    ax = fig.add_subplot(1,1,1)
    ax = fig.gca(projection='3d')
    plt.subplots_adjust(top=0.98,bottom=0.02,right=0.98,left=0.02)

    q,t,x,y,z = get_detector_info(collision)
    ax.scatter(x,y,z,s=20*q)

