import numpy as np
import matplotlib.pyplot as plt

def F(r,S,ku,kv,dx,Du,Dv, u, v, i):

	newu=r*u[i]*(1-u[i]/S)-kv*v[i]+Du*((u[i+1]-2*u[i]+u[i-1])/(dx**2))
	newv=r*v[i]*(1-v[i]/S)-ku*u[i]+Dv*((v[i+1]-2*v[i]+v[i-1])/(dx**2))
	if(newu<0):
		newu=0
	if(newv<0):
		newv=0

	return(newu, newv)





def euler(r,S,ku,kv,dx,Du,Dv,ti,tf, L, h, F, u_init, v_init):
    
	T=int((tf-ti)/h)
	D=int(L/dx)
	u=np.zeros((T,D))
	v=np.zeros((T,D))
	u[0]=u_init
	v[0]=v_init
    
	temps=np.linspace(ti,tf,T)
 
	for i in range(0,T-1):
		for j in range(1,D-1):

			fu,fv=F(r,S,ku,kv,dx,Du,Dv, u[i], v[i], j)
			
			u[i+1][j]=round(h*fu+u[i][j],2)
			v[i+1][j]=round(h*fv+v[i][j],2)

	return(temps, u,v)

u_init=[0]*50+[200]*50
v_init=[200]*50+[0]*50


temps,u,v=euler(0.01,1000,0.1,0.2,0.1,0.1,0.1,0,100,10,1, F, u_init, v_init)


print(temps,u[0])
plt.plot(temps,u[6])
plt.plot(temps,v[6])
plt.show()
