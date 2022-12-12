
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import xraydb

elements = ['Fe','Mn', 'Ag']
excitationenergy = 50000.0
linewhitelist = ['Ka1','Ka2','Ka3','Kb1','Kb2','Kb3','La1','La2','La3','Lb1','Lb2','Lb3']
y_counts = []
x_energy = []

a = xraydb.xray_lines('Fe', 'K', excitationenergy).items()
print(a['Ka1'])

for element in elements:
    for name, line in xraydb.xray_lines(element, 'K', excitationenergy).items():
        if name in linewhitelist:
            print(f'{element} {name}: {line}')

            



