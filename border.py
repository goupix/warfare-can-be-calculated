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
france =  io.imread( 'france2.png')      # Gray image, rgb images need pre-conversion


X,Y=france.shape
for x in range (0,X):
    for y in range(0,Y):

        if(france[x][y]>100):
            france[x][y]=0
        else:
            france[x][y]=2


for x in range (1,X-1):
    for y in range(1,Y-1):
        voisins=[france[x][y+1],france[x][y-1],france[x+1][y],france[x-1][y]]
        if(france[x][y]==0 and (2 in voisins)):
            france[x][y]=1
        
for x in range (1,X-1):
    for y in range(1,Y-1):
        voisins=[france[x][y+1],france[x][y-1],france[x+1][y],france[x-1][y]]
        if(france[x][y]==1 and (0 not in voisins)):
            france[x][y]=2
        


"Writing in a file"
fichier=open('france.txt','w')
for x in range (0,X):
    for y in range(0,Y):
        fichier.write(str(france[x][y]))
    fichier.write('\n')





