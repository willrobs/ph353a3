
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
import pandas
import time
from scipy.optimize import curve_fit
import sys

def constant(x,c):
    return c

def reweighting(spring_const,mass,lattice_spacing,num_config,num_lat_points,mass_prime,spring_const_prime,corrt,bootstraps):
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
    smup=spring_const_prime,
    smp=mass_prime,
    smup=str(smup)
    smp=str(smp)
    namep=smup+smp+sma+sniter+spoints
    
    g=open('info'+name+'.txt', 'r')
    bin_size=eval(g.readline())
    g.close()
    
    num_bins=int(niter/bin_size)
    
    f=open('data'+name+'.txt' , 'r')
    data=f.readlines()
    f.close()
    
    mup=spring_const_prime
    mp=mass_prime
    c1p=(m-mp)/(2*a)
    c2p=(a/2)*(mu**2 - mup**2)
    
    ssps=pandas.read_csv('action'+name+'.txt', delim_whitespace = True)
    energies=[]
    essp=[]

    for g in range(num_bins):
        sum1=0
        sum2=0
        for j in range(bin_size):
            t1=c1p*ssps.delx2[j + g*bin_size]
            t2=c2p*ssps.x2[j + g*bin_size]
            sum2=sum2+np.exp(t1 + t2)
            
            for h in range(points):
                
                sum1=sum1+ ((eval(data[h + (j + g*bin_size)*points]))**2)*np.exp(t1 + t2)
        
        energies=np.append(energies, sum1/(points*bin_size)) ####not actually the energies
        essp=np.append(essp,sum2/bin_size)
    
    ####Bootstrap errors and bootstrap estimate
    #### numerator
    boot_ests=[]
    for i in range(bootstraps):
        
        random_sample=np.random.choice(energies,num_bins)
        sum1=0
        for j in random_sample:
            sum1=sum1+j
        sum1=sum1/num_bins
        boot_ests=np.append(boot_ests,sum1)
    sum1=0    
    for i in boot_ests:
        sum1=sum1+i
        
    boot_av_num=sum1/bootstraps
    sum1=0
    for i in boot_ests:
        sum1=sum1+(i-boot_av_num)**2
        
    std_num=((1/bootstraps)*sum1)**0.5
    #### denominator
    boot_ests=[]
    for i in range(bootstraps):
        
        random_sample=np.random.choice(essp,num_bins)
        sum1=0
        for j in random_sample:
            sum1=sum1+j
        sum1=sum1/num_bins
        boot_ests=np.append(boot_ests,sum1)
    sum1=0    
    for i in boot_ests:
        sum1=sum1+i
        
    boot_av_dnm=sum1/bootstraps
    sum1=0
    for i in boot_ests:
        sum1=sum1+(i-boot_av_dnm)**2
        
    std_dnm=((1/bootstraps)*sum1)**0.5 
        
    energy=(mu**2)*(boot_av_num/boot_av_dnm)
    std=abs(energy)*((std_num/boot_av_num)**2 + (std_dnm/boot_av_dnm)**2)**0.5
    
    print('reweighted energy', energy)
    print('uncertainty', std)
    
    g=open('info'+namep+'.txt', 'w')
    g.write('n/a' + '\n')
    g.write(str(energy) + '\t' + str(std) + '\n')
    
############################################################### fee    
    num=[]
    dnm=[]
    b_num=[]
    b_dnm=[]
    for m in range(corrt):
        
        for h in range(num_bins):
            

            sum1=0
            sum2=0
            for n in range(bin_size):

                x0=eval(data[(n + h*bin_size)*points])
                xnm1=eval(data[(n + h*bin_size)*points + m])
                xn=eval(data[(n + h*bin_size)*points + m+1])

                t1=c1p*ssps.delx2[n]
                t2=c2p*ssps.x2[n]

                sum1=sum1+(x0*xn)*np.exp(t1 + t2)
                sum2=sum2+(x0*xnm1)*np.exp(t1 + t2)

            b_num=np.append(b_num, sum1/bin_size) ####binned data point to calc effe(tlat)
            b_dnm=np.append(b_dnm, sum2/bin_size)
######## bootstrapping
    num_error=[]
    dnm_error=[]
    num=[]
    dnm=[]
    effe=[]
    y_error=[]
    for i in range(corrt):
        bdps_num_hold=b_num[i*num_bins:(i+1)*num_bins] ####creates an array holding all binned data points for a given tlat
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
        
    for j in range(corrt):
        bdps_dnm_hold=b_dnm[j*num_bins:(j+1)*num_bins]
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
        
    for q in range(corrt):

        err=abs(num[q]/dnm[q])*((num_error[q]/num[q])**2 + (dnm_error[q]/dnm[q])**2)**0.5
        y_error=np.append(y_error,err)
        
        
    err=(1/a)*np.log(y_error)
    effe=(-1/a)*np.log(num/dnm)
    
    lat_time2=np.arange(corrt)
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
        fit, = plt.plot(lat_time2_hold, yaxis,'g')
        plt.errorbar(lat_time2_hold,effe_hold,yerr=y_error_hold,fmt='.')
        plt.plot(lat_time2_hold,effe_hold,'r')
        analytic, = plt.plot([0,max(lat_time2_hold)],[ediff,ediff],'b')
        plt.legend([fit, analytic], ['Fitted line', 'Analytical'])
        plt.show()

        done=input("Enter 'y' if you are happy with your fit, if not enter 'n'")
        time.sleep(0.1)
    
    
    perr=np.sqrt(np.diag(pcov))
    g.write(str(popt[0]) + '\t' + str(perr[0]))
    g.close()

num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
lattice_spacing=float(sys.argv[3])
corrt=int(sys.argv[4]) #### distance in fee calculation
bootstraps=int(sys.argv[5])
mass_prime=float(sys.argv[6])
spring_const_prime=float(sys.argv[7])

m=float(sys.argv[8])
mu=float(sys.argv[9])



reweighting(mu,m,lattice_spacing,num_config,num_lat_points,mass_prime,spring_const_prime,corrt,bootstraps)