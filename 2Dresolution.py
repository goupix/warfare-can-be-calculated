import numpy as np
import plotly 
import plotly.graph_objs as go


def F(r,S,ku,kv,dx, dy, Du,Dv, ux, uy, vx, vy, x,y):

	newu=r*ux[x]*(1-ux[x]/S)-kv*vx[x]+Du*((ux[x+1]-2*ux[x]+ux[x-1])/(dx**2)+(uy[y+1]-2*uy[y]+uy[y-1])/(dy**2))
	newv=r*vx[x]*(1-vx[x]/S)-ku*ux[x]+Dv*((vx[x+1]-2*vx[x]+vx[x-1])/(dx**2)+(vy[y+1]-2*vy[y]+vy[y-1])/(dy**2))
	
	return(newu, newv)





def euler(r,S,ku,kv,dx,dy,Du,Dv,ti,tf, L, H, h, F):

	T=int((tf-ti)/h)
	X=int(L/dx)
	Y=int(H/dy)

	u_init=np.zeros((Y,X))
	v_init=np.zeros((Y,X))
	'''
	u_init[:,0:(X/2)]=200
	v_init[:,(X/2):X]=200
	'''
	u_init[:,0:(X/2)]=200
	v_init[:,(X/2):X]=200

	u_init[0:20,:]=400

	u=np.zeros((T,Y,X))
	v=np.zeros((T,Y,X))

	u[0]=u_init
	v[0]=v_init

	xseq=np.linspace(0,L).tolist()
	yseq=np.linspace(0,H).tolist()

    

	for t in range(0,T-1):
		for y in range(1,Y-1):
			for x in range(1,X-1):

				fu,fv=F(r,S,ku,kv,dx, dy,Du,Dv, u[t][y], u[t][:,x], v[t][y], v[t][:,x], x, y)

				if((h*fu+u[t][y][x])<0):
					u[t+1][y][x]=0
				else:
					u[t+1][y][x]=h*fu+u[t][y][x]

				if((h*fv+v[t][y][x])<0):
					v[t+1][y][x]=0
				else:
					v[t+1][y][x]=h*fv+v[t][y][x]
		
		u[t+1][:,0]=u[t+1][:,1]
		v[t+1][:,0]=v[t+1][:,1]

		u[t+1][:,X-1]=u[t+1][:,X-2]
		v[t+1][:,X-1]=v[t+1][:,X-2]

		u[t+1][0,:]=u[t+1][1,:]
		v[t+1][0,:]=v[t+1][1,:]

		u[t+1][Y-1,:]=u[t+1][Y-2,:]
		v[t+1][Y-1,:]=v[t+1][Y-2,:]


	return(xseq,yseq,u,v)


xseq,yseq,u,v=euler(0.01,1000,10,0.1,1,1, 0.1,0.1,0,100,100,50,1, F)


data = [go.Heatmap(z=v[90].tolist(),x=xseq,y=yseq,colorscale='Red')]
plotly.offline.plot(data, filename='u-heatmap.html')


