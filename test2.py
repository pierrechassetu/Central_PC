from curses import BUTTON2_DOUBLE_CLICKED
import math as m
import numpy as np
from evdev import InputDevice, categorize
import src.central_pc.central_pc.GAMEPAD as GAMEPAD
import matplotlib.pyplot as plt

a = [1.,0.,0.,1.,0.,0.,1.,0.,0.]

b =np.array([a[:3],a[3:6],a[6:]])
c = np.array(a).reshape(3,3)
print(b,c,a)