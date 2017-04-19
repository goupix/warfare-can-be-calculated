import numpy as np
import plotly 
import plotly.graph_objs as go


def F(r,S,ku,kv,dx, dy,Du,Dv, ux, uy, vx, vy, x,y):

	
	newu=r*ux[x]*(1-ux[x]/S)-kv*vx[x]+Du[y,x]*((ux[x+1]-2*ux[x]+ux[x-1])/(dx**2)+(uy[y+1]-2*uy[y]+uy[y-1])/(dy**2))
	newv=r*vx[x]*(1-vx[x]/S)-ku*ux[x]+Dv[y,x]*((vx[x+1]-2*vx[x]+vx[x-1])/(dx**2)+(vy[y+1]-2*vy[y]+vy[y-1])/(dy**2))
	
	return(newu, newv)





def euler(r,S,ku,kv,dx,dy,Du,Dv,ti,tf, L, H, h, F, state):

	T=int((tf-ti)/h)
	X=int(L/dx)
	Y=int(H/dy)

	u_init=np.zeros((Y,X))
	v_init=np.zeros((Y,X))
	
	u_init[:,0:(X/2)]=400
	v_init[:,(X/2):X]=400

	for y in range(0,Y):
		for x in range(0,X):
			if(state[y,x]==0):
				u_init[y][x]=0
				v_init[y][x]=0
	
	u=np.zeros((T,Y,X))
	v=np.zeros((T,Y,X))

	u[0]=u_init
	v[0]=v_init


	xseq=np.linspace(0,L).tolist()
	yseq=np.linspace(0,H).tolist()


    

	for t in range(0,T-1):

		for y in range(1,Y-1):
			for x in range(1,X-1):

				if(state[y,x]>1):


					fu,fv=F(r,S,ku,kv,dx, dy, Du,Dv, u[t][y], u[t][:,x], v[t][y], v[t][:,x], x, y)

					if((h*fu+u[t][y][x])<0):
						u[t+1][y][x]=0
					else:
						u[t+1][y][x]=h*fu+u[t][y][x]

					if((h*fv+v[t][y][x])<0):
						v[t+1][y][x]=0
					else:
						v[t+1][y][x]=h*fv+v[t][y][x]
		

		for y in range(1,Y-1):
			for x in range(1,X-1):

				if(state[y,x]==1):
				
					for voisin in [(y,x+1),(y,x-1),(y+1,x),(y-1,x)]:
						if(state[voisin]==2):

							u[t][y,x]=u[t][voisin]
							v[t][y,x]=v[t][voisin]





	return(xseq,yseq,u,v)


"Getting obstacle matrix from a file"
pays=open('france.txt','r')

m=[]
for line in pays.read().split():
	ligne=[]
	for elt in line:
		ligne.append(int(elt))
	m.append(ligne)
H=len(m)
L=len(m[0])

"Diffusion matrix"

Du=0.1*np.ones((H,L))
Dv=0.1*np.ones((H,L))
"Modeling \"massif central\" mountains with a lower diffusion coef"
Du[20:30,40:60]=0.01 
Dv[20:30,40:60]=0.01




"Creating an obstacle matrix"
'''
L=100
H=50

state=2*np.ones((H,L))
state[:,[0,99]]=0
state[[0,49],:]=0

state[1:49,[1,98]]=1
state[[1,48],1:49]=1

state[19:31,[39,61]]=1
state[[19,31],40:60]=1


state[20:30,40:60]=0

print(state)
'''
xseq,yseq,u,v=euler(0.01,500,10,0,1,1,Du,Dv,0,100,L,H,1, F, np.asarray(m))


data = [go.Heatmap(z=u[90].tolist(),x=xseq,y=yseq,colorscale='bone')]
data2 = [go.Heatmap(z=v[10].tolist(),x=xseq,y=yseq,colorscale='Reds')]
plotly.offline.plot(data, filename='u-heatmap.html')
