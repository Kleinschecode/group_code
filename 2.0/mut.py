import numpy as np
import operator as op

basis ={0:"",1:"e1",2:"e2",3:"e12",4:"e3",5:"e13",6:"e23",7:"e123",
        8:"e0",9:"e10",10:"e20",11:"e120",12:"e30",13:"e130",14:"e230",15:"e1230"}

np.set_printoptions(precision=3)
np.random.seed(8)

def mut(*args, field=None, dim=3):

    if not args: #empty
        if field is None:
            b = np.random.randint(0, 16, size=(2, 2))
            v = np.random.rand(2, 2)*10
        else: #3d-vf
            b = np.array([1,2,4], ndmin=2)
            v = np.random.rand(4,dim)*10
    else:
        if field is None:
            b = np.array(list(args[::2]), ndmin=2)
            v = np.array(list(args[1::2]),ndmin=2)
        else:
            b = np.array([1,2,4], ndmin=2)
            v = np.array(args, ndmin=2).reshape(-1,3)

    return (b,v) #(1,m),(n,m)

def conv(a,b,nv:int=8,null=False):
    if null&(a>=nv)&(b>=nv):
        return 0
    f = 0 ; a >>= 1
    while a != 0: f += (a&b).bit_count() ; a >>= 1 ;
    return (-1)**(f%2)

metric = np.zeros(shape=(16, 16))
metric_ni = np.zeros(shape=(16, 16))
for x in basis:
    for y in basis:
        metric[x][y] = conv(x,y,null=True)
        metric_ni[x][y] = conv(x,y)

def sign(x,y): 
    X,Y = np.expand_dims(x, tuple(range(1, x.ndim*2, 2))),np.expand_dims(y, tuple(range(0, y.ndim*2, 2)))
    return metric[X,Y].reshape(np.multiply(x.shape, y.shape))

def gkron(a,b,o=op.__mul__,inner=False):
    if inner: ae,be = np.expand_dims(a, axis=2) ,np.expand_dims(b, axis=1)
    else: ae,be = tuple(range(1, a.ndim*2, 2)), tuple(range(0, b.ndim*2, 2))
    A,B = np.expand_dims(a, ae),np.expand_dims(b, be)
    return (o(A,B)).reshape(np.multiply(a.shape, b.shape))

def gp(m1:mut,m2:mut):
    a,b = m1[0],m2[0]
    return (gkron(a,b,o=op.__xor__), sign(a,b)*np.kron(m1[1],m2[1]))

def ap(m1:mut,m2:mut):
    b1,b2 = m1[0], m2[0]
    v1,v2 = m1[1], m2[1]
    s1 = tuple(max(a, b) for a, b in zip(b1.shape,b2.shape))
    s2 = tuple(max(a, b) for a, b in zip(v1.shape,v2.shape))
    
    return (np.array(b1+b2), np.array(v1+v2))


def group(m):
    b=m[0] ; v=m[1]
    u, i = np.unique(b[0], return_inverse=True)
    num_u = len(u)
    num_v = v.shape[0]
    c = np.zeros((num_v, num_u), dtype=v.dtype)
    np.add.at(c, (slice(None), i), v)
    return (u[np.newaxis,:], c)

import math
from itertools import accumulate
def t_ep(m, lamb:float=.005, generator:int=3,deg=2):
    v1 = np.array([lamb**n/math.factorial(n) for n in range(deg+1)])
    v2 = np.array([lamb**n/math.factorial(n) for n in range(deg+1)]) ; v2[1]*=-1
    b = np.array([0]+list(accumulate([generator]*deg, op.xor)))
    t1,t2 = (b[np.newaxis,:],v1[np.newaxis,:]),(b[np.newaxis,:],v2[np.newaxis,:])
    return gp(t2,gp(m,t1))

def val(m,blade:int):
    b = m[0] ; v = m[1]
    return v[np.where(b==blade)]

import matplotlib.colors
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 8))
limit = 2
plt.xlim(-limit, limit)
plt.ylim(-limit, limit)

def vector_to_rgb(axlim,angle,absolute,sv=0.3):
    max_abs = axlim
    angle = angle % (2*np.pi)
    if angle < 0: angle += 2*np.pi
    HSV = (angle/2/np.pi, absolute/max_abs, (absolute/max_abs+sv).clip(0, .8))
    return matplotlib.colors.hsv_to_rgb(HSV)

def recur_ep(m:mut, p:int=3):
    if p==0: return m
    else:
        n = group(t_ep(m))
        v = np.array([val(n,1), val(n,2)]).flatten()
        a,m = np.arctan2(v[1], v[0]),np.linalg.norm(v)
        c = vector_to_rgb(limit, a, m)
    if p % 10 == 0: plt.quiver(0, 0,*v, angles='xy', scale_units='xy',scale=1, color=c, alpha=0.8)
    return recur_ep(n, p-1)
#recur_ep(mut(1,1), p=620)
