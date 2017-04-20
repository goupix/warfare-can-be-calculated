"""
===========================
@Author  : Linbo<linbo.me>
@Version: 1.0    25/10/2014
This is the implementation of the 
Zhang-Suen Thinning Algorithm for skeletonization.
===========================
"""
import matplotlib
import matplotlib.pyplot as plt
from Tkinter import *
from skimage import io
import numpy as np


"load image data"
pays =  io.imread( 'france-allemagne.png', as_grey=True)      # Gray image, rgb images need pre-conversion

X,Y=pays.shape
for x in range (0,X):
    for y in range(0,Y):

        if(pays[x][y]>0.7):
            pays[x][y]=0
        elif(pays[x][y]<0.3):
            pays[x][y]=2
        else:
            pays[x][y]=3


for x in range (1,X-1):
    for y in range(1,Y-1):
        voisins=[pays[x][y+1],pays[x][y-1],pays[x+1][y],pays[x-1][y]]
        if(pays[x][y]==0 and ((2 in voisins) or (3 in voisins))):
            pays[x][y]=1
        
for x in range (1,X-1):
    for y in range(1,Y-1):
        voisins=[pays[x][y+1],pays[x][y-1],pays[x+1][y],pays[x-1][y]]
        if(pays[x][y]==1 and (0 not in voisins)):
            if(2 in voisins):
                pays[x][y]=2
            else:
                pays[x][y]=3
        


"Writing in a file"
fichier=open('france-allemagnecor.txt','w')
for x in range (0,X):
    for y in range(0,Y):
        fichier.write(str(int(pays[x][y])))
    fichier.write('\n')





