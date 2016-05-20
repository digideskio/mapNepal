import os
import sys

import numpy as np
import matplotlib.pyplot as plt

#f_indexes = range(4583210,4583223+1) ## District nodes in Dhaulagiri Anchal
f_indexes =range(4588143,4588146+1)

list_of_files = []

for ind in f_indexes:
#    list_of_files.append('./polyAnchals/poly_'+str(ind)+'.txt')
    list_of_files.append('./polyDistricts/poly_'+str(ind)+'.txt')


for fnames in list_of_files:
    plt.plot(*np.loadtxt(fnames,unpack=True), linewidth=2.0)

plt.title('14 Anchals')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.grid()
plt.savefig('Dhaulagiri.gif')
#plt.savefig('14Anchals.gif')
plt.show()
plt.close()
