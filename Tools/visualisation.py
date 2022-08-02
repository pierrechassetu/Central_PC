import math as m
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./data_files/run1.csv')

df.plot(x='/mocap_node/SycaBot_W1/ground_pose/x',y='/mocap_node/SycaBot_W1/ground_pose/y')
p1=[-1.352,-0.840]
p2=[-0.088,1.409]
p3=[1.306,-0.948]
p4=[0.869,2.150]
p5=[-1.155,2.208]
p6=[-0.067,-1.547]
p7=[0.,0.]
p8=[0.,-0.4]
p9=[0.3,0.]
points = [p1,p2,p3,p4,p5,p6,p7,p8,p9]
plt.scatter([p[0] for p in points],[p[1] for p in points])
plt.show()