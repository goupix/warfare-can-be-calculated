
#Definition des conditions initiales
Au=300
Av=800

#Definition de la precision du tracé
p=1000

#Definition des paramètres
L=10
r=0.01
Du=0.1
Dv=0.1
a10=Au/p
a20=Av/p
ku=0.1
kv=0.5

#Vecteur des temps
temps=seq(0,100,1)
xseq=seq(0,10,0.1)

#Vecteurs des solutions du système Lanchester

terme_u=c()
terme_v=c()
u=c()
v=c()


t=5
for(x in xseq){
  for(i in 1:p){
    
    lambda=-(i*pi/L)**2
    
    a1=((-Au*L)/(i*pi))*(sin(i*pi)-sin((i*pi)/2))
    a2=((-Av*L)/(i*pi))*sin((i*pi)/2)
    b1=((Au*L)/(i*pi))*(cos(i*pi)-cos((i*pi)/2))
    b2=((Av*L)/(i*pi))*(cos((i*pi)/2)-1)
    
    delta=(lambda**2)*((Dv-Du)**2)+4*ku*kv
    
    A=2
    B=(2*ku)/(lambda*(Du-Dv)+sqrt(delta))
    
    l1=(1/2)*(2*r+lambda*(Du-Dv)+sqrt(delta))
    l2=(1/2)*(2*r+lambda*(Du-Dv)-sqrt(delta))
      
    alpha=(1/2)*A*exp(l1*t)+(-1/(4*ku))*(lambda*(Du-Dv)+sqrt(delta))*B*exp(l2*t)
    beta=(1/(4*kv))*(lambda*(Dv-Du)+sqrt(delta))*A*exp(l1*t)+(1/2)*B*exp(l2*t)
    
    terme_u[i]=alpha*(a1*cos((i*pi*x)/L)+b1*sin((i*pi*x)/L))
    terme_v[i]=beta*(a2*cos((i*pi*x)/L)+b2*sin((i*pi*x)/L))
  }
  
  
  u[length(u)+1]=a10/2+sum(terme_u)
  v[length(v)+1]=a20/2+sum(terme_v)
  
}


#Plot des solutions

plot(xseq,u, type='l', col='red', ylim=c(0,5000))
lines(xseq, v, type='l', col='blue')



#Vecteurs des solutions du premier système

terme_u=c()
terme_v=c()
u=c()
v=c()

t=5
for(x in xseq){
  for(i in 1:p){
    a1=((-Au*L)/(i*pi))*(sin(i*pi)-sin((i*pi)/2))
    a2=((-Av*L)/(i*pi))*sin((i*pi)/2)
    b1=((Au*L)/(i*pi))*(cos(i*pi)-cos((i*pi)/2))
    b2=((Av*L)/(i*pi))*(cos((i*pi)/2)-1)

    alpha=0.5*exp((r-Du*((i*pi)/L)**2)*t)
    beta=0.5*exp((r-Dv*((i*pi)/L)**2)*t)
    
    terme_u[i]=alpha*(a1*cos((i*pi*x)/L)+b1*sin((i*pi*x)/L))
    terme_v[i]=beta*(a2*cos((i*pi*x)/L)+b2*sin((i*pi*x)/L))
  }
  
  
  u[length(u)+1]=a10/2+sum(terme_u)
  v[length(v)+1]=a20/2+sum(terme_v)

}


#Plot des solutions

plot(xseq,u, type='l', col='red')
lines(xseq, v, type='l', col='blue')