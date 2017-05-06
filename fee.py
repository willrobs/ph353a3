
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import sys

def constant(x,c):
    return c

def fee(num_config,num_lat_points,lattice_spacing,corr_dist,bootstraps,mass,spring_const):
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

    num=[]
    dnm=[]

    b_num=[]
    b_dnm=[]
    bdps_num=[]
    bdps_dnm=[]
    g=open('info'+name+'.txt', 'r')
    bin_size=eval(g.readline())
    g.close()
    num_bins=int(niter/bin_size)

    #sum2=0
    for j in range(corr_dist):
        b_num=np.append(b_num,0)
        b_dnm=np.append(b_dnm,0)
        for g in range(num_bins):
            sum1=0
            sum2=0
            for n in range(bin_size):

                x0=eval(data[(g*bin_size +n)*points])
                xnm1=eval(data[(g*bin_size + n)*points +j])
                xn=eval(data[(g*bin_size +n)*points + j+1])

                sum1=sum1+(x0*xn)
                sum2=sum2+(x0*xnm1)

            sum1=sum1/bin_size
            sum2=sum2/bin_size
            bdps_num=np.append(bdps_num,sum1) #### holds each individual binned data point for bootstrapping later
            bdps_dnm=np.append(bdps_dnm,sum2)
            
    ####errorbars
    num_error=[]
    dnm_error=[]
    num=[]
    dnm=[]
    effe=[]
    y_error=[]
    for j in range(corr_dist):
        bdps_num_hold=bdps_num[j*num_bins:(j+1)*num_bins] ####creates an array holding all binned data points for a given tlat
        boot_avg=[]
        for k in range(bootstraps):

            random_sample=np.random.choice(bdps_num_hold,num_bins)
            sum1=0
            for i in random_sample:
                sum1=sum1+i
            sum1=sum1/num_bins
            boot_avg=np.append(boot_avg,sum1) ####array holding all bootstrap values for numerator
        sum1=0    

        for i in boot_avg:
            sum1=sum1+i
        avg=sum1/bootstraps ####calculates bootstrap average
        num=np.append(num,avg) ####bootstrap average value
        sum1=0
        for i in boot_avg:
            sum1=sum1+(i-avg)**2

        std=((1/bootstraps)*sum1)**0.5

        num_error=np.append(num_error,std)

    for j in range(corr_dist):
        bdps_dnm_hold=bdps_dnm[j*num_bins:(j+1)*num_bins]
        boot_avg=[]
        for k in range(bootstraps):

            random_sample=np.random.choice(bdps_dnm_hold,num_bins)
            sum1=0
            for i in random_sample:
                sum1=sum1+i
            sum1=sum1/num_bins
            boot_avg=np.append(boot_avg,sum1)
        sum1=0    
        for i in boot_avg:
            sum1=sum1+i
        avg=sum1/bootstraps
        dnm=np.append(dnm,avg)
        sum1=0
        for i in boot_avg:
            sum1=sum1+(i-avg)**2

        std=((1/bootstraps)*sum1)**0.5

        dnm_error=np.append(dnm_error,std)

    for q in range(corr_dist):

        err=abs(num[q]/dnm[q])*((num_error[q]/num[q])**2 + (dnm_error[q]/dnm[q])**2)**0.5
        y_error=np.append(y_error,err)

    err=(1/a)*np.log(y_error)
    effe=(-1/a)*np.log(num/dnm)

    lat_time2=np.arange(corr_dist)
    plt.figure(1)
    plt.errorbar(lat_time2,effe,yerr=y_error,fmt='.')
    plt.plot(lat_time2,effe,'r')
    ediff=(9*mu**2/(4*mass))**0.5 - (mu**2/(4*mass))**0.5
    plt.plot([0,max(lat_time2)],[ediff,ediff],'b')
    plt.show()

    done='n'
    while done=='n':
    
        plateau=int(input("Enter the point where the plateau occurs: "))
        effe_hold=effe[0:plateau]
        lat_time2_hold=lat_time2[0:plateau]
        y_error_hold=y_error[0:plateau]
        popt, pcov = curve_fit(constant, lat_time2_hold, effe_hold)
        
        plt.figure(2)
        plt.xlabel('Lattice time')
        plt.ylabel('Energy gap')
        plt.title('Fitted energy gap')
        yaxis=0*np.arange(len(lat_time2_hold))
        yaxis=yaxis+popt[0]
        
        fit, = plt.plot(lat_time2_hold, yaxis,'g', label='line1')
        plt.errorbar(lat_time2_hold,effe_hold,yerr=y_error_hold,fmt='.')
        plt.plot(lat_time2_hold,effe_hold,'r')
        analyitic, = plt.plot([0,max(lat_time2_hold)],[ediff,ediff],'b', label='line2')
        plt.legend([fit, analyitic], ['Fitted line', 'Analytical'])
        plt.show()

        done=input("Enter 'y' if you are happy with your fit, if not enter 'n'")
        time.sleep(0.1)
    perr=np.sqrt(np.diag(pcov))
    
    g=open('info'+name+'.txt', 'a')
    g.write(str(popt[0]) + '\t' + str(perr[0]))
    g.close()
        
num_config=int(sys.argv[1])
points=int(sys.argv[2])
a=float(sys.argv[3])
corr_dist=int(sys.argv[4])
bootstraps=int(sys.argv[5])

mass=float(sys.argv[6])
mu=float(sys.argv[7])
        
fee(num_config,points,a,corr_dist,bootstraps,mass,mu)
