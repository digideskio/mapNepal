import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from getNodes import get_AnchalList
from getNodes import get_DistList
from getNodes import get_DistNode
from getNodes import  get_AnchalDistricts


districts = get_DistList()
#districts = get_AnchalDistricts('Dhaulagiri')
#print districts, len(districts)

distNodes = []

for dist in range(0,len(districts)):
    thisnode = get_DistNode(districts[dist])
    distNodes.append(thisnode)

#print distNodes


list_of_files = []

fig, ax = plt.subplots()

for ind in distNodes:
    #list_of_files.append('./polyAnchals/poly_'+str(ind)+'.txt')
    list_of_files.append('./polyDistricts/poly_'+str(ind)+'.txt')


for fnames in list_of_files:
    #plt.plot(*np.loadtxt(fnames,unpack=True), linewidth=2.0,c=np.random.rand(3,1))
    #fill with random color
    plt.fill(*np.loadtxt(fnames,unpack=True),lw=2,color=np.random.rand(3,1))

plt.title('75 Districts')

plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.grid()

plt.savefig('./plots/75districts.gif')
plt.show()
plt.close()

