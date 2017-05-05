
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
    g=open('action'+name+'.txt', 'w') #### stores relevant action terms for each configuration to use in reweighting
    g.write('delx2' + '\t' + 'x2')
    
    for m in range(ttime): #### thermalizaing state

        state=metro(state,points,0,0) #### config,num_lat_points
    sum1=0
    sum2=0
    for h in range(points):
        f.write(str(state[h]) + '\n')
        
        if h== (points-1):
            sum1=sum1+(state[0]-state[points-1])**2  ####boundary conds
            sum2=sum2+(state[points-1])**2
        else:
            sum1=sum1+(state[h+1]-state[h])**2
            sum2=sum2+(state[h])**2
    
    g.write('\n' + str(sum1) + '\t' + str(sum2))

    delx2=sum1
    x2=sum2
    for m in range(niter):

        array=metro(state,points,delx2,x2) #### config,num_lat_points
        state=array[0]
        delx2=array[1]
        x2=array[2]
        for h in range(int(points)):
            f.write(str(state[h]) + '\n') 
        g.write('\n' + str(delx2) + '\t' + str(x2))
        
    f.close()
    g.close()
    print("Raw data gathered.")
    
def metro(config,num_lat_points,delx2,x2):
    
    state=config
    points=num_lat_points
    if delx2 ==0 and x2 ==0:
        skip=True
    else:
        skip=False
     
    for n in range(points):

        x_t=(np.random.uniform((state[n]-step), (state[n]+step)))
        if n==0:
            delta=daction(state[n+1],state[n],state[points-1],x_t)

            if np.exp(-delta)> (np.random.uniform(0,1)):
                
                t1=(state[0] - state[points-1])**2
                t2=(state[1]-state[0])**2
                t3=(x_t-state[points-1])**2
                t4=(state[1]-x_t)**2
                delx2=delx2-(t1+t2)+t3+t4
                x2=x2-(state[0])**2 + x_t**2
                 
                np.put(state,[n],[x_t])
            else:
                pass

        elif n==(points-1):
            delta=daction(state[0],state[n],state[n-1],x_t)

            if np.exp(-delta)> (np.random.uniform(0,1)):
                
                t1=(state[points-1] - state[points-2])**2
                t2=(state[0]-state[points-1])**2
                t3=(x_t-state[points-2])**2
                t4=(state[0]-x_t)**2
                delx2=delx2-(t1+t2)+t3+t4
                x2=x2-(state[points-1])**2 + x_t**2
                
                np.put(state,[n],[x_t])
            else:
                pass
        else:
            delta=daction(state[n+1],state[n],state[n-1],x_t)

            if  np.exp(-delta) > (np.random.uniform(0,1)):
                
                t1=(state[n] - state[n-1])**2
                t2=(state[n+1]-state[n])**2
                t3=(x_t-state[n-1])**2
                t4=(state[n+1]-x_t)**2
                delx2=delx2-(t1+t2)+t3+t4
                x2=x2-(state[n])**2 + x_t**2
                
                np.put(state,[n],[x_t])
            else:
                pass
    if skip==True:
        return(state)
    
    else:
        return(state,delx2,x2)
    
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

