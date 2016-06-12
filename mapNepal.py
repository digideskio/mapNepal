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
        make_plots(data)
    elif args.anch:
        data = get_dist_data(getNodes.get_AnchalDistricts(anchals))
        make_plots(data)
    elif args.allDist:
        data = get_dist_data(getNodes.get_DistList())
        make_plots(data)
    elif args.nodeN:
        data = get_dist_data([getNodes.get_DistName(str(args.nodeN))])
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
    return parser

def make_plots(data):
    fig, ax = plt.subplots(figsize=(10,8))
    #ax.set_aspect("equal")
    log.debug("Making plot...")
    for key,val in data.iteritems():
        plt.fill(val['lat'],val['long'],lw=2,color=np.random.rand(3,1))#,label=key)

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
        dfitems[dist] = pd.read_csv(fname,delim_whitespace=True,header=None,names=['lat','long'])
    return dfitems

#TODO: Keep things under the hood
#Color

if __name__ == "__main__":
    main()
