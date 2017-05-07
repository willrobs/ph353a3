
# coding: utf-8

# In[1]:

import numpy as np
import sys

def bootstrap(spring_const,mass,lattice_spacing,num_config,num_lat_points,num_boot_samples):
    mu=spring_const
    m=mass
    a=lattice_spacing
    niter=num_config
    points=num_lat_points
    bootstrap_samples=num_boot_samples
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

    f=open('2binned_data'+name+'.txt' , 'r')
    data=f.readlines()
    datap=len(data)
    
    energies=[]
    sum2=0
    for p in range(bootstrap_samples):
        
        random_sample=np.random.choice(data,datap)
        sum1=0
        for x in random_sample:
            
            sum1=sum1 + eval(x)
        
        energy=(mu**2)*(sum1/datap)
        energies=np.append(energies, energy)
        sum2=sum2+energy
        
    menergy=sum2/bootstrap_samples
    
    sum1=0
    for q in energies:
        sum1=sum1+(q-menergy)**2
    
    std=((1/bootstrap_samples)*sum1)**(0.5)
    
    print('Internal energy: ' ,menergy)
    print('error: ',std)
    
    g=open('info'+name+'.txt', 'a')
    g.write('col1' + '\t' + 'col2' + '\n')
    g.write(str(menergy) + '\t' + str(std) + '\n')
    g.close()
    
    
num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
a=float(sys.argv[3])
num_boot_samples=int(sys.argv[4])

mass=float(sys.argv[5])
mu=float(sys.argv[6])

    
bootstrap(mu,mass,a,num_config,num_lat_points,num_boot_samples)

