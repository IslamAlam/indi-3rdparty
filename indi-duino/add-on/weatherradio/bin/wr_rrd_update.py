#!/usr/bin/python

#-----------------------------------------------------------------------
# Script for updating the RRD time series.
#
# Copyright (C) 2020 Wolfgang Reissenberger <sterne-jaeger@t-online.de>
#
# This application is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# Based upon ideas from indiduinoMETEO (http://indiduino.wordpress.com).
#-----------------------------------------------------------------------

import sys
from indiclient import *
from weatherradio import *
import argparse
import rrdtool

parser = argparse.ArgumentParser(description="Fetch weather data and store it into the RRD file")
parser.add_argument("-v", "--verbose", action='store_true',
                    help="Display progress information")

args = parser.parse_args()
data = None

try:
    if (args.verbose):
        print "Updating data from \"%s\"@%s:%s" % (INDIDEVICE,INDISERVER,INDIPORT)

    # open connection to the INDI server
    indi=indiclient(INDISERVER,int(INDIPORT))

    # ensure that the INDI driver is connected to the device
    connect = connect(indi)

    if (connect):
        if (args.verbose):
            print "Connection established to \"%s\"@%s:%s" % (INDIDEVICE,INDISERVER,INDIPORT)

        data = readWeather(indi)

        if (args.verbose):
            print "Weather parameters read from \"%s\"@%s:%s" % (INDIDEVICE,INDISERVER,INDIPORT)
    else:
        print "Establishing connection FAILED to \"%s\"@%s:%s" % (INDIDEVICE,INDISERVER,INDIPORT)


    indi.quit()

except:
    print "Updating data from \"%s\"@%s:%s FAILED!" % (INDIDEVICE,INDISERVER,INDIPORT)
    indi.quit()
    sys.exit()


updateString="N"
templateString=""

if data is not None:
    for key in data.keys():
        updateString=updateString+":"+str(data[key])
        if templateString:
            templateString += ":"
        templateString += key

    ret = rrdtool.update(RRDFILE, "--template", templateString ,updateString);
    if ret:
	print rrdtool.error() 
