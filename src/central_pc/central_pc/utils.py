import math as m
import numpy as np
from scipy.optimize import linear_sum_assignment, minimize


def quat2eul(q, axis='z'):
    '''
    Transform a quaternion to an euler angle.

    arguments :
        q (array) = array containing the for quaternion components [qx,qy,qz,qw]
    ------------------------------------------------
    return :
    '''
    if axis=='z' :
        t1 = 2. * (q[3]*q[2] + q[0]*q[1])
        t2 = 1. - 2.*(q[1]*q[1] + q[2]*q[2])
        angle = m.atan2(t1,t2)
    return angle


# The functions lonely and generate_points are used for c-CAPT and solve the problem discussed in this topic :
# https://stackoverflow.com/questions/19668463/generating-multiple-random-x-y-coordinates-excluding-duplicates
# generate_points was modified a bit to directly give a list of points that are in a x,y rectangle.

def lonely(p,X,r):
    ''' 
    p = candidate
    X = n-d background grid 
    r = minimum distance between points
    '''
    x_bound = X.shape[0]
    y_bound = X.shape[1]
    x0,y0 = p
    x = y = np.arange(-r,r)
    x = x + x0
    y = y + y0

    u,v = np.meshgrid(x,y)

    u[u < 0] = 0
    u[u >= x_bound] = x_bound-1
    v[v < 0] = 0
    v[v >= y_bound] = y_bound-1

    return not np.any(X[u[:],v[:]] > 0)

def generate_points(x_bound=2500, y_bound= 2500, r=71,k=30):
    ''' 
    generate points that are r distant from each other. R Waveshare bots is 0.25, so delta>0.707.
    x_bound,y_bound = extent of sample domain
    r = minimum distance between points
    k = samples before rejection
     
    '''
    active_list = []

    # step 0 - initialize n-d background grid
    X = np.ones((x_bound,y_bound))*-1

    # step 1 - select initial sample
    x0,y0 = np.random.randint(0,x_bound), np.random.randint(0,y_bound)
    active_list.append((x0,y0))
    X[active_list[0]] = 1

    # step 2 - iterate over active list
    while active_list:
        i = np.random.randint(0,len(active_list))
        rad = np.random.rand(k)*3*r+r
        theta = np.random.rand(k)*2*np.pi

        # get a list of random candidates within [r,4r] from the active point
        candidates = np.round((rad*np.cos(theta)+active_list[i][0], rad*np.sin(theta)+active_list[i][1])).astype(np.int32).T

        # trim the list based on boundaries of the array
        candidates = [(x,y) for x,y in candidates if x >= 0 and y >= 0 and x < x_bound and y < y_bound]

        for p in candidates:
            if X[p] < 0 and lonely(p,X,r):
                X[p] = 1
                active_list.append(p)
                break
        else:
            del active_list[i]
            
        x = np.where(X>0)
        pts = np.concatenate((np.expand_dims(x[0],axis=1),np.expand_dims(x[1],axis=1)),axis=1)

    return pts