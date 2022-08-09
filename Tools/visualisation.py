import math as m
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./data_files/runFinalPP.csv')

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

fig,ax = plt.subplots(1,1, figsize=(16,8))
ax.scatter([p[0] for p in points],[p[1] for p in points])
ax.scatter(df['/mocap_node/SycaBot_W1/ground_pose/x'],df['/mocap_node/SycaBot_W1/ground_pose/y'], s=0.2, label='measured position')
ax.scatter(df['/SycaBot_W1/visualisation/x'],df['/SycaBot_W1/visualisation/y'], s=0.6, label='position reference')
ax.set_xlim(-3,3)
ax.set_ylim(-3,3)
plt.legend()
plt.show()