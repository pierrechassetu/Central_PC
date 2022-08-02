from curses import BUTTON2_DOUBLE_CLICKED
import math as m
import numpy as np
from evdev import InputDevice, categorize
import src.central_pc.central_pc.GAMEPAD as GAMEPAD
import matplotlib.pyplot as plt

circles = []
r = 1
n = 200
time = np.linspace(0, 2*np.pi, n, endpoint=False)
for t in time :
    x = r * np.cos(t)
    y = r * np.sin(t)
    circles.append([x, y])
circles = np.array(circles)
fig, ax = plt.subplots()
ax.scatter(circles[:,0], circles[:,1])
ax.set_aspect('equal')
plt.show()
# print(circles)