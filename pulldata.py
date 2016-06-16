#!/usr/bin/env python

import os, sys
import subprocess
from subprocess import call, Popen, STDOUT
from getNodes import get_AnchalList
from getNodes import get_DistList
from getNodes import get_DistNode
from getNodes import  get_AnchalDistricts
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def main():

    log.debug("Starting...")
    parser = mapNepal_arg_parser()
    args = parser.parse_args()
    cutData = 2
    distNodes = []

    if args.dist:
        print args.dist
        for dist in args.dist:
            thisnode = get_DistNode(dist)
            distNodes.append(thisnode)
    elif args.anch:
        for anch in args.anch:
            dists = get_AnchalDistricts(anch)
            for dist in dists:
                distNodes.append(get_DistNode(dist))
    elif args.allDist:
        districts = get_DistList()
        for dist in range(0,len(districts)):
            thisnode = get_DistNode(districts[dist])
            distNodes.append(thisnode)
    elif args.nodeNum:
        distNodes.extend(args.nodeNum)
    if args.stripby:
        cutData = args.stripby


    print distNodes, cutData

    for node in distNodes:
        yo = 'wget -O ./temp/temp_'
        pal = str(node)+r'.osm'
        getosm = yo+pal + r' "http://overpass-api.de/api/interpreter?data=(rel(' + str(node)+r');>);out;";'
        subprocess.call(getosm, shell=True)
        rel =  r'perl ./rel2poly.pl ./temp/temp_'+str(node)+r'.osm > ./temp/temp_'+str(node)+'.txt'
        #print rel
        subprocess.call(rel, shell=True)

        # only keep 1/3rd of data, remove lines with single columns
        #strip = "awk 'NR%3==0 && NF>=2' ./temp/temp_"+str(node)+".txt > ./polyDistricts/poly_"+str(node)+".txt"
        # TODO::pass cutData as argument to awk
        strip = "awk 'NR%1==0 && NF>=2' ./temp/temp_"+str(node)+".txt > ./tempdir/poly_"+str(node)+".txt"
        #print strip
        subprocess.call(strip, shell=True)


##TODO:Add exceptions

def mapNepal_arg_parser():
    log.debug("Parsing...")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="dist", nargs="+", type=str, default=[],
        help="District Name")
    parser.add_argument(
        "-n", dest="nodeNum", nargs="+", type=str,default=[],
        help = "Node Number. Default:4588144")
    parser.add_argument(
        "-strp", dest="stripby", nargs="?", type=int, const=2,
        help = "Every n lines. Default:2")
    parser.add_argument(
        "-a", dest="anch", nargs="+", type=str, default=[],
        help="Anchal Name")
    parser.add_argument(
        "-all",dest="allDist",action='store_true',
        help="All Districts")

    return parser

if __name__ == "__main__":
    main()
