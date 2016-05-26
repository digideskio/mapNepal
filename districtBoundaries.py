#!/usr/bin/env python

import os, sys
import subprocess
from subprocess import call, Popen, STDOUT

from getNodes import get_AnchalList
from getNodes import get_DistList
from getNodes import get_DistNode
from getNodes import  get_AnchalDistricts


#districts = get_DistList()
districts = get_AnchalDistricts('Gandaki')
print districts, len(districts)

distNodes = []

for dist in range(0,len(districts)):
    thisnode = get_DistNode(districts[dist])
    distNodes.append(thisnode)

print distNodes

#subprocess.call(['ls','-ctrlh'])


for node in distNodes:
    yo = 'wget -O ./temp/temp_'
    pal = str(node)+r'.osm'
    getosm = yo+pal + r' "http://overpass-api.de/api/interpreter?data=(rel(' + str(node)+r');>);out;";'
    subprocess.call(getosm, shell=True)
    rel =  r'perl ./rel2poly.pl ./temp/temp_'+str(node)+r'.osm > ./temp/temp_'+str(node)+'.txt'
    #print rel
    subprocess.call(rel, shell=True)

    # only keep 1/3rd of data, remove lines with single columns
    strip = "awk 'NR%3==0 && NF>=2' ./temp/temp_"+str(node)+".txt > ./polyDistricts/poly_"+str(node)+".txt"
    #print strip
    subprocess.call(strip, shell=True)


##TODO:Add exceptions
