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
    if args.dist:
        data = get_dist_data(args.dist)
    elif args.anch:
        anchalDistricts = []
        for anchal in args.anch:
            log.debug("Ancha: %s, Districts: %s",anchal,
                      getNodes.get_AnchalDistricts(anchal))
            anchalDistricts.extend(getNodes.get_AnchalDistricts(anchal))
        data = get_dist_data(anchalDistricts)
    elif args.allDist:
        data = get_dist_data(getNodes.get_DistList())
    elif args.nodeN:
        data = get_dist_data([getNodes.get_DistName(str(args.nodeN))])
    else:
        return
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
    fig, ax = plt.subplots(figsize=(10,8))
    #ax.set_aspect("equal")
    log.debug("Making plot...")
    for key,val in data.iteritems():
        plt.plot(val['lat'],val['long'],lw=2,color=np.random.rand(3,1))

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.grid()

    plt.show()


def get_dist_data(distNames):
    log.debug("Getting district data...")

    #read data from district file, and get corresponding node Number
    with open ('districts.txt') as f:
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
    return dfitems

#TODO: Keep things under the hood
#Color
#Basemap,patchcollection+polygons?
if __name__ == "__main__":
    main()
