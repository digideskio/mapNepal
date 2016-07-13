import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse
import re
import getNodes

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

#default fig size
FIGURE_SIZE = (6,5)

def main():
    parser = mapNepal_arg_parser()
    args = parser.parse_args()

    #fig = plt.figure(figsize=FIGURE_SIZE)
    data = None
    anchalDistricts = []
    if args.dist:
        for dist in args.dist:
            anchalDistricts.append(dist)
        print anchalDistricts
        data = get_dist_data(anchalDistricts)
    elif args.anch:
        anchalDistricts = []
        for anchal in args.anch:
#            log.debug("Ancha: %s, Districts: %s",anchal,
#                      getNodes.get_AnchalDistricts(anchal))
            anchalDistricts.extend(getNodes.get_AnchalDistricts(anchal))
        data = get_dist_data(anchalDistricts)
    elif args.allDist:
        anchalDistricts.extend(getNodes.get_DistList())
        data = get_dist_data(getNodes.get_DistList())
    elif args.nodeNum:
        data = get_dist_data([getNodes.get_DistName(str(args.nodeNum))])
    else:
        return

    #data is a list of dict. of DataFrames for each dist with dist as key
    #concat to same df?
    make_plots(data)
    return


def mapNepal_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="dist", nargs="+", type=str, default=[],
        help="District Name")
    parser.add_argument(
        "-a", dest="anch", nargs="+", type=str, default=[],
        help="Anchal Name")
    parser.add_argument(
        "-n", dest="nodeNum", nargs="?", type=int, const=4588144,
        help = "Node Number. Default:4588144")
    parser.add_argument(
        "-all",dest="allDist",action='store_true',
        help="All Districts")
    #parser.add_argument(
        #"-df",dest="dataFrame",nargs='+',
        #help="All Districts")

    #-data: fill heatmap/or other maps
    return parser

def make_plots(data):
    #data is list of dict==>dataframe
    fig, ax = plt.subplots(figsize=(10,8))
    #ax.set_aspect("equal")
#    log.debug("Making plot...")
    midPointsX = []
    midPointsY = []
    labels = []
    for key,val in data.iteritems():
        #midPoints.append(tuple([val['lat'].mean(),val['long'].mean()]))
        midPointsX.append(val['lat'].mean())
        midPointsY.append(val['long'].mean())
        labels.append(key[0:2])
        plt.fill(val['lat'],val['long'],lw=2,color=np.random.rand(3,1))
    print midPointsX, midPointsY
    for label, xpt, ypt in zip(labels, midPointsX,midPointsY):
        #print xpt, ypt, label
        plt.text(xpt, ypt,label)

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.grid()

    plt.show()


def get_dist_data(distNames):
    # input list of district names, output=>[dist=>dataFrame]
#    log.debug("Getting district data...")

    #read data from district file, and get corresponding node Number
    with open ('./data/districts.txt') as f:
        dlines = f.read().splitlines()
        distNodes = {}
        nodeDists = {}
        for dist in range(0,len(dlines)):
            distNum = re.split('\W+',dlines[dist])
            district, nodeNum = distNum[0], distNum[1]
            #Only interested in districts that user asked for
            if district in distNames:
                distNodes[district] = nodeNum
                nodeDists[nodeNum] = district
    # Latitude, Longitude for each dist
    dfitems = {}

    for dist in distNames:
        cols = ['lat','long']
        #log.debug("Making adataframe for %s",dist)
        fname = ""
        fname = './polyDistricts/poly_'+str(distNodes[dist])+'.txt'
        dfitems[dist] = pd.read_csv(fname,delim_whitespace=True,header=None,names=cols)
        #print dfitems[dist].head()
    return dfitems

#TODO: Keep things under the hood
#Color
#Basemap,patchcollection+polygons?
if __name__ == "__main__":
    main()
