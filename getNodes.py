import re
import sys
import numpy as np
import logging

"""
Handles information about districts, anchals.
Return list of anchals
Return list of districts
Return list of districts for given anchal
Return nodeNum for a givne district
Return districtName for a given NodeNum
"""

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

#Open the text file with districtName=>NodeNum
#format:: district, NodeNum
with open ('./data/districts.txt') as f:
        log.debug("Reading coordinates from districts file...")
        dlines = f.read().splitlines()

# Add each line to dictionary
distNodes = {}
nodeDists = {}
for dist in range(0,len(dlines)):
        distNum = re.split('\W+',dlines[dist])
        district, nodeNum = distNum[0], distNum[1]
        distNodes[district] = nodeNum
        nodeDists[nodeNum] = district

anchalNodes = {}
# Read anchal file
with open ('./data/anchals.txt') as f:
        log.debug("Reading coordinates from anchal file...")
        alines =  f.read().splitlines()

#format:: Anchal : dist1, dist2, dist3,...
for anchal in range(0, len(alines)):
        #grab anchal, list of districts in this anchal

    anchDistList = re.split('\W+',alines[anchal])
    thisAnchal = anchDistList[0]
    distList = anchDistList[1:]

    anchalNodes[thisAnchal] = []
    # now add each district to respective anchal
    for dists in distList:
            anchalNodes[thisAnchal].append(dists)

def get_DistNode(distName):
        """
        Returns the nodeNumber associated with the given district
        :param districtName: Name of district
        >>> get_DistNode('Baglung')
        '4588144'
        >>> get_DistNode('Kathmandu')
        '4583247'
        >>> get_DistNode('Rautahat')
        '4589418'
        """
        return distNodes[distName]

def get_DistName(nodeNum):
        """
        Returns the nodeNumber associated with the given district
        :param nodeNum: node Number of a district
        >>> get_DistName('4588144')
        'Baglung'
        >>> get_DistName('4583247')
        'Kathmandu'
        >>> get_DistName('4589418')
        'Rautahat'
        """
        return nodeDists[str(nodeNum)]


def get_AnchalDistricts(anchal):
        """
        Returns the list of districts for a given anchal
        :param anchal: name of Anchal

        >>> get_AnchalDistricts('Janakpur')
        ['Dhanusa', 'Mahottari', 'Sarlahi', 'Sindhuli', 'Ramechhap', 'Dolakha']

        >>> get_AnchalDistricts('Dhaulagiri')
        ['Baglung', 'Myagdi', 'Parbat', 'Mustang']

        >>> get_AnchalDistricts('Gandaki')
        ['Gorkha', 'Kaski', 'Lamjung', 'Syangja', 'Tanahun', 'Manang']
        """
        return anchalNodes[anchal]

def get_AnchalList():
        """
        Returns the list of anchals

        >>> get_AnchalList()
        ['Janakpur', 'Bagmati', 'Sagarmatha', 'Gandaki', 'Koshi', 'Dhaulagiri', 'Narayani', 'Karnali', 'Rapti', 'Seti', 'Bheri', 'Lumbini', 'Mechi', 'Mahakali']
        """
        return anchalNodes.keys()

def get_DistList():
        """
        Returns the list of anchals

        >>> get_DistList()
        ['Mugu', 'Darchula', 'Chitwan', 'Jajarkot', 'Tanahun', 'Terhathum', 'Bhojpur', 'Dadeldhura', 'Okhaldhunga', 'Gorkha', 'Baitadi', 'Bajhang', 'Taplejung', 'Sindhupalchowk', 'Siraha', 'Morang', 'Kavrepalanchok', 'Ilam', 'Rasuwa', 'Lalitpur', 'Rolpa', 'Pyuthan', 'Solukhumbu', 'Sunsari', 'Myagdi', 'Panchthar', 'Kalikot', 'Parbat', 'Saptari', 'Gulmi', 'Rautahat', 'Doti', 'Kathmandu', 'Khotang', 'Dolakha', 'Dhading', 'Lamjung', 'Manang', 'Bhaktapur', 'Banke', 'Dhanusa', 'Achham', 'Humla', 'Palpa', 'Nuwakot', 'Ramechhap', 'Udayapur', 'Sarlahi', 'Dang', 'Dolpa', 'Jhapa', 'Jumla', 'Mustang', 'Kapilvastu', 'Kanchanpur', 'Bardiya', 'Dailekh', 'Sankhuwasabha', 'Rukum', 'Nawalparasi', 'Surkhet', 'Mahottari', 'Arghakhanchi', 'Kailali', 'Makwanpur', 'Bara', 'Salyan', 'Parsa', 'Sindhuli', 'Rupandehi', 'Dhankuta', 'Bajura', 'Kaski', 'Baglung', 'Syangja']
        """
        return distNodes.keys()

def get_nodeList():
        """
        Return list of available nodes
        """
        return nodeDists.keys()


def get_DistData(distName):
        """
        Returns the (x,y) dataPoints for given district
        """

        nodeNum = get_DistNode(distName)
        fname = './polyDistricts/poly_'+str(nodeNum)+'.txt'
        data = np.loadtxt(fname, unpack=True)
        return data
