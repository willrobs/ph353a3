
# coding: utf-8

# In[ ]:
import numpy as np
import matplotlib.pyplot as plt
from math import *
import sys


def probd(spring_const,mass,lattice_spacing,num_config,num_lat_points,d_volume,pdsets):
    mu=spring_const
    m=mass
    a=lattice_spacing
    niter=num_config
    points=num_lat_points
    smu=mu,
    sm=m,
    sma=a,
    sniter=niter,
    spoints=points,
    smu=str(smu)
    sm=str(sm)
    sma=str(sma)
    sniter=str(sniter)
    spoints=str(spoints)
    name=smu+sm+sma+sniter+spoints
    
    sets=pdsets ####how many configurations to use
    g=open('info'+name+'.txt', 'r')
    bin_size=eval(g.readline())
    g.close()
    num_bins=int(niter/bin_size)
    
    delta=d_volume/2 #### 'infinitesimal' volume about a point
    ppdensity=[0]
    npdensity=[0]

    g=open('data'+name+'.txt', 'r')
    data=g.readlines()
    g.close()
    
    
    for m in range(sets):
    
        for n in range(points): ############################## Poss change

            dp=eval(data[n + m*points])
            ## Determining Probability density

            if dp >= 0:
                axis=int(dp/delta +1)
                while axis > len(ppdensity): ########
                    ppdensity=np.append(ppdensity,0)

                ppdensity[axis-1]=ppdensity[axis-1] +1

            else:
                mdp=abs(dp)
                axis=int(mdp/delta +1)
                while axis > len(npdensity): ##########
                    npdensity=np.append(npdensity,0)

                npdensity[axis-1]=npdensity[axis-1]+1
                
    #g.close()
    
    print("Probability density determined")
    

    npmax=len(npdensity) -1
    ppmax=len(ppdensity) -1 ######## no -1 because of how np.arange() works, it stops 1 too early
    npdensity=np.fliplr([npdensity])[0]
    
    pdensity=np.append(npdensity,ppdensity)
    position=np.arange(-delta/2 -npmax*delta, delta + ppmax*delta, delta)
    #y_error=(1/pdensity)**0.5
    sum1=0
    for x in pdensity:
        sum1=sum1+x
    area=sum1*delta
    pdensity=(1/area)*pdensity
    #y_error=(1/area)*y_error
    
    x=np.arange(min(position),max(position),0.01)
    xo=1/(mu*(mass**0.5))
    c=1/((pi**0.5)*(xo**0.5))
    
    #plt.errorbar(position,pdensity,yerr=y_error,fmt='.')
    plt.plot(position,pdensity,'bx')
    plt.plot(x,c*np.exp((-x**2)/xo),'r')
    plt.show()
    


num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
lattice_spacing=float(sys.argv[3])
d_volume=float(sys.argv[4])
pdsets=int(sys.argv[5])

mass=float(sys.argv[6])
spring_const=float(sys.argv[7])

probd(spring_const,mass,lattice_spacing,num_config,num_lat_points,d_volume,pdsets)
