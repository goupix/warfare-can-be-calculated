import numpy as np
import plotly 
import plotly.graph_objs as go
from skimage import io

def F(r,S,ku,kv,dx, dy,Du,Dv, ux, uy, vx, vy, x,y):

	
	newu=r*ux[x]*(1-ux[x]/S)-kv*vx[x]+Du[y,x]*((ux[x+1]-2*ux[x]+ux[x-1])/(dx**2)+(uy[y+1]-2*uy[y]+uy[y-1])/(dy**2))
	newv=r*vx[x]*(1-vx[x]/S)-ku*ux[x]+Dv[y,x]*((vx[x+1]-2*vx[x]+vx[x-1])/(dx**2)+(vy[y+1]-2*vy[y]+vy[y-1])/(dy**2))
	
	return(newu, newv)





def euler(r,S,ku,kv,dx,dy,Du,Dv,ti,tf, L, H, h, F, state, u_init, v_init):

	T=int((tf-ti)/h)
	X=int(L/dx)
	Y=int(H/dy)

	

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

def get_shape_matrix(filename):
	pays=open(filename,'r')

	m=[]
	for line in pays.read().split():
		ligne=[]
		for elt in line:
			ligne.append(int(elt))
		m.append(ligne)
	m=np.asarray(m)
	return m


"Initial conditions"
def get_initial_condition(filename, m, ind, s1, s2, s3):

	pop =  io.imread( filename, as_grey=True)      # Gray image, rgb images need pre-conversion
	
	H=len(m)
	L=len(m[0])
	u_init=np.zeros((H,L))

	for y in range(0,H):
		for x in range(0,L):
			if (m[y,x]==ind):
				if (pop[y,x]>0.5):
					u_init[y,x]=s1
				if (pop[y,x]>0.1 and pop[y,x]<0.5):
					u_init[y,x]=s2
				if (pop[y,x]<0.1):
					u_init[y,x]=s3

			if(m[y,x]!=ind and m[y,x]>1):
				u_init[y,x]=0

	return u_init

def get_diffusion_matrix(filename, m, ind, s1,s2,s3,s4):

	pop =  io.imread( filename, as_grey=True)
	
	H=len(m)
	L=len(m[0])
	D=np.zeros((H,L))

	for y in range(0,H):
		for x in range(0,L):
			if (m[y,x]==ind):
				if (pop[y,x]>0.5):
					D[y,x]=s3
				if (pop[y,x]>0.1 and pop[y,x]<0.5):
					D[y,x]=s2
				if (pop[y,x]<0.1):
					D[y,x]=s1

			if(m[y,x]!=ind and m[y,x]>1):
				D[y,x]=s4

	return D

#Indices: France(2), Allemagne (3)
m=get_shape_matrix('france-allemagne.txt')
H=len(m)
L=len(m[0])

Du=get_diffusion_matrix('france-allemagne-pop.png',m, 2, 0.02,0.05,0.1, 0.2)
Dv=get_diffusion_matrix('france-allemagne-pop.png',m, 3, 0.02,0.05,0.1,0.2)


u_init=get_initial_condition('france-allemagne-pop.png',m, 2, 90,100,120)
v_init=get_initial_condition('france-allemagne-pop.png',m, 3, 90,100,120)


xseq,yseq,u,v=euler(0.001,500,50,0,1,1,Du,Dv,0,1000,L,H,1, F, m, u_init, v_init)


data = [go.Heatmap(z=u[900].tolist(),x=xseq,y=yseq,colorscale='bone')]
data2 = [go.Heatmap(z=v[900].tolist(),x=xseq,y=yseq,colorscale='Reds')]
plotly.offline.plot(data2, filename='u-heatmap.html')
