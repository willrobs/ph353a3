
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
import pandas
import sys


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
    print(std_num)
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
    print(std_dnm)    
        
    energy=(mu**2)*(boot_av_num/boot_av_dnm)
    std=abs(energy)*((std_num/boot_av_num)**2 + (std_dnm/boot_av_dnm)**2)**0.5
    
    print('reweighted energy', energy)
    print('uncertainty', std)
    
############################################################### fee    
    num=[]
    dnm=[]
    for m in range(corrt):

        sum1=0
        sum2=0
        for n in range(niter):

            x0=eval(data[n*points])
            xnm1=eval(data[n*points + m])
            xn=eval(data[n*points + m+1])
            
            t1=c1p*ssps.delx2[n]
            t2=c2p*ssps.x2[n]
            
            sum1=sum1+(x0*xn)*np.exp(t1 + t2)
            sum2=sum2+(x0*xnm1)*np.exp(t1 + t2)

        num=np.append(num, sum1/niter)
        dnm=np.append(dnm, sum2/niter)
        
    effe=-(1/a)*np.log(num/dnm)
    
    lat_time=np.arange(0,len(effe),1)
    
    plt.figure(3)
    plt.xlabel('Lattice time')
    plt.ylabel('Energy gap')
    plt.title('Determining plateau')
    plt.plot(lat_time, effe)
    ediff=(9*mu**2/(4*mass))**0.5 - (mu**2/(4*mass))**0.5
    plt.plot([0,max(lat_time)],[ediff,ediff])
    plt.show()
    

num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
lattice_spacing=float(sys.argv[3])
corrt=int(sys.argv[4])
bootstraps=int(sys.argv[5])
mass_prime=float(sys.argv[6])
spring_const_prime=float(sys.argv[7])

m=float(sys.argv[8])
mu=float(sys.argv[9])



reweighting(mu,m,lattice_spacing,num_config,num_lat_points,mass_prime,spring_const_prime,corrt,bootstraps)