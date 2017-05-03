
# coding: utf-8

# In[ ]:

import numpy as np
import sys

def data(spring_const,mass,lattice_spacing,num_config,num_lat_points):
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
    
    state=0*np.random.random_sample((points,)) #### Initial state
    f=open('data'+name+'.txt' , 'w')
    g=open('action'+name+'.txt', 'w') #### stores the unit action for each configuration
    
    for m in range(ttime): #### thermalizaing state

        state=metro(state,points,0) #### config,num_lat_points
    sum1=0
    for h in range(int(points - 1)):
        f.write(str(state[h]) + '\n')
        sum1=sum1+(state[h+1]-state[h])**2 + state[h]**2
    sum1=sum1+(state[0]-state[points-1])**2 + state[points-1]**2 ####boundary conds
    g.write(str(sum1) + '\n')
        
        
    action=sum1
    for m in range(niter):

        array=metro(state,points,action) #### config,num_lat_points
        state=array[0]
        action=array[1]
        for h in range(int(points - 1)):
            f.write(str(state[h]) + '\n') 
        g.write(str(action) + '\n')
        
    f.close()
    g.close()
    print("Raw data gathered.")
    
def metro(config,num_lat_points,tot_action):
    
    state=config
    points=num_lat_points
    action=tot_action
    if tot_action==0:
        skip=True
    else:
        skip=False
     
    for n in range(points):

        x_t=(np.random.uniform((state[n]-step), (state[n]+step)))
        if n==0:
            delta=daction(state[n+1],state[n],state[points-1],x_t)

            if np.exp(-delta)> (np.random.uniform(0,1)):
                action=action+(x_t-state[n])*(3*(x_t+state[n]) -2*(state[points-1] + state[n+1])) ###bcs
                np.put(state,[n],[x_t])
            else:
                pass

        elif n==(points-1):
            delta=daction(state[0],state[n],state[n-1],x_t)

            if np.exp(-delta)> (np.random.uniform(0,1)):
                action=action+(x_t-state[n])*(3*(x_t+state[n]) -2*(state[n-1] + state[0])) #### bcs
                np.put(state,[n],[x_t])
            else:
                pass
        else:
            delta=daction(state[n+1],state[n],state[n-1],x_t)

            if  np.exp(-delta) > (np.random.uniform(0,1)):
                action=action+(x_t-state[n])*(3*(x_t+state[n]) -2*(state[n-1] + state[n+1]))
                np.put(state,[n],[x_t])
            else:
                pass
    if skip==True:
        return(state)
    
    else:
        return(state,action)
    
def daction(x1,x,xm1,xp):
    dxn=xp-x
    sxn=xp+x
    sx1=x1+xm1
    
    delta_s=dxn*(sxn*(c1 + c2) -sx1*c1)
    
    return delta_s

num_config=int(sys.argv[1])
num_lat_points=int(sys.argv[2])
a=float(sys.argv[3])
step=float(sys.argv[4])
ttime=int(sys.argv[5])

m=float(sys.argv[6])
mu=float(sys.argv[7])

c1=m/a
c2=(a*(mu**2))/2

data(mu,m,a,num_config,num_lat_points)

