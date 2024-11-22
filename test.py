# Task #2
# Cole Good & Max Abrecht
import sys
import numpy as np
import netCDF4 as nc
import scipy.stats
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




file_path = 't_reference_ens_2011122400_pvalues.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

print(data)
