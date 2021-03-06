import numpy as np
import matplotlib.pyplot as plt

def F(r,S,ku,kv,dx,Du,Dv, u, v, i):

	newu=r*u[i]*(1-u[i]/S)-kv*v[i]+Du*((u[i+1]-2*u[i]+u[i-1])/(dx**2))
	newv=r*v[i]*(1-v[i]/S)-ku*u[i]+Dv*((v[i+1]-2*v[i]+v[i-1])/(dx**2))
	
	return(newu, newv)





def euler(r,S,ku,kv,dx,Du,Dv,ti,tf, L, h, F):

	u_init=[200]*(int(L/2))+[0]*(int(L/2))
	v_init=[0]*(int(L/2))+[200]*(int(L/2))


	T=int((tf-ti)/h)
	D=int(L/dx)
	u=np.zeros((T,D))
	v=np.zeros((T,D))
	u[0]=u_init
	v[0]=v_init
    
	x=np.linspace(0,L,D)
 
	for i in range(0,T-1):
		for j in range(1,D-1):

			fu,fv=F(r,S,ku,kv,dx,Du,Dv, u[i], v[i], j)

			if((h*fu+u[i][j])<0):
				u[i+1][j]=0
			else:
				u[i+1][j]=h*fu+u[i][j]

			if((h*fv+v[i][j])<0):
				v[i+1][j]=0
			else:
				v[i+1][j]=h*fv+v[i][j]
	    
		u[i+1][0]=u[i+1][1]
		v[i+1][0]=v[i+1][1]

		u[i+1][D-1]=u[i+1][D-2]
		v[i+1][D-1]=v[i+1][D-2]
	return(x,u,v)




x,u,v=euler(0.01,1000,10,0,1,0.1,0.1,0,10000,100,1, F)


plt.plot(x,u[90])
plt.plot(x,v[90])
plt.show()
