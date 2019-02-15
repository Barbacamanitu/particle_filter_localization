import numpy as np
from math import *


def translation_matrix(x, y):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
        ],dtype=np.float)


def rotation_matrix(theta):
    return np.array([
        [np.cos(theta), np.sin(theta), 0],
        [-np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ], dtype=np.float)


def scale_matrix(x,y):
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1]
        ], dtype=np.float)



def v2(x,y=0):
    if x is tuple:
        tnflat = np.array(x)
        tflat = tnflat.flatten()
        xx,yy = tflat[0],tflat[1]
        return np.array([xx, yy, 1.0], dtype=float)
    else:
        return np.array([x,y,1.0],dtype=float)


import math

def tmat(transform,vec):
    x,y = vec
    vec2 = x,y,1.0
    vx,vy,vz = transform@vec2
    return vx,vy


def v2_dis(pt1,pt2):
    x1, y1 = pt1[0], pt1[1]
    x2, y2 = pt2[0], pt2[1]
    return math.sqrt((x2-x1)**2+(y2-y1)**2)