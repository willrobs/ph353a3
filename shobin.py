
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

def corr(spring_const,mass,lattice_spacing,num_config,num_lat_points):
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
    
    f=open('data'+name+'.txt' , 'r')
    data=f.readlines()
    f.close()
    corr=[]
    for n in range(corrt):
        
        sum1=0
        sum2=0
        for m in range(points):
            sum1=sum1+(eval(data[m])*eval(data[m+((n+1)*points)]))
        corr=np.append(corr,sum1/points)
    
    corr_time=np.arange(corrt)
    corr=corr/(max(corr))
    
    popt, pcov = curve_fit(exp_fun, corr_time, corr)
    
    plt.figure(1)
    plt.xlabel('Correlation time')
    plt.ylabel('Correlation')
    plt.title('Correlation graph')
    plt.plot(corr_time, exp_fun(corr_time, *popt))
    plt.plot(corr_time, corr)
    plt.savefig('corr_t'+name+'.pdf')
    
    print("Correlation time determined.")
    size_of_bin=int(1/popt[1] + 1)
    g=open('info'+name+'.txt', 'w')
    g.write(str(size_of_bin) + '\n')
    g.close()
    
    return (data, size_of_bin)

def binning(spring_const,mass,lattice_spacing,num_config,num_lat_points,size_of_bin,raw_data):
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
    
    data=raw_data
    
    bin_size=size_of_bin
    num_bins=int(niter/bin_size)
        
    f=open('2binned_data'+name+'.txt' , 'w')
    x=0
    for n in range(num_bins):
        
        sum1=0
        for m in range(bin_size):
            
            for l in range(points):
                num=eval(data[x])
                x=x+1
                sum1=sum1+num**2
            
        f.write(str(sum1/(points*bin_size)) + '\n')
    
    f.close()
    
    print("binned data produced")
    
def exp_fun(x, a, b, c):
    return  a*(np.exp(-b*x)) + c
    
num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
a=float(sys.argv[3])
corrt=int(sys.argv[4])

mass=float(sys.argv[5])
mu=float(sys.argv[6])


array=corr(mu,mass,a,num_config,num_lat_points)
binning(mu,mass,a,num_config,num_lat_points,array[1],array[0])

