#!/usr/bin/env python
import os
import sys
import subprocess
import numpy as np
from os import listdir
import argparse


from isis3 import utils
from isis3 import info
from isis3 import _core
import isis3.importexport as importexport
import isis3.mathandstats as mathandstats

if __name__ == "__main__":

    try:
        _core.is_isis3_initialized()
    except:
        print "ISIS3 has not been initialized. Please do so. Now."
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="Source PDS dataset(s)", required=True, type=str, nargs='+')
    parser.add_argument("-f", "--filters", help="Require filter(s) or exit", required=False, type=str, nargs='+')
    parser.add_argument("-t", "--targets", help="Require target(s) or exit", required=False, type=str, nargs='+')
    args = parser.parse_args()

    filters = args.filters if args.filters is not None else []
    targets = args.targets if args.targets is not None else []

    filters = [f.upper() for f in filters]
    targets = [t.upper() for t in targets]

    matching_files = []

    for f in args.data:
        if f[-3:].upper() != "CUB":
            print "File %s is not supported, skipping"%f
            continue
        target = None
        try:
            target = info.get_target(f)
        except:
            pass

        filter1, filter2 = None, None
        try:
            filter1, filter2 = info.get_filters(f)
        except:
            pass
        if len(targets) > 0 and  target.upper() not in targets:
            continue
        elif len(filters) > 0 and (filter1.upper() not in filters and filter2.upper() not in filters):
            continue
        else:
            matching_files.append(f)

    values = []
    for f in matching_files:
        _min, _max = mathandstats.get_data_min_max(f)
        values.append(_min)
        values.append(_max)
        print _min, _max


    minimum = np.min(values)
    maximum = np.max(values)

    print "Minimun:", minimum, "Maximum:", maximum
    #maximum -= ((maximum - minimum) * 0.45)
    #minimum += ((maximum - minimum) * 0.35)

    for f in matching_files:
        totiff = f[:-4]+".tif"
        print totiff
        importexport.isis2std_grayscale(f, totiff, minimum=minimum, maximum=maximum)
