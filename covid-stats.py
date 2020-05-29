#!/usr/bin/python

import argparse
import json
import datetime
import operator

parser = argparse.ArgumentParser(description='Statistici Covid')
parser.add_argument('-f', '--file', help='Fisier cu date', type=str)
args = parser.parse_args()

print ("Parsing %s" %args.file)

f = open(args.file)
json = json.loads(f.read())

todayStats = json["currentDayStats"]
today = todayStats["parsedOnString"]
print ("Date: %s Infected: %s Cured: %s Died: %s" %(today, todayStats["numberInfected"], todayStats["numberCured"], todayStats["numberDeceased"]))

dt = datetime.datetime.strptime(today, '%Y-%m-%d')
yday = dt - datetime.timedelta(days=1)
str_yesterday = yday.strftime('%Y-%m-%d')
print ("Yesterday: %s" %str_yesterday)

counties = {}

data_yesterday = json["historicalData"][str_yesterday]

for x in todayStats["countyInfectionsNumbers"].keys():
    counties[x] = todayStats["countyInfectionsNumbers"][x] - data_yesterday["countyInfectionsNumbers"][x]

sorted_counties = sorted(counties.items(), key=operator.itemgetter(1))

print (sorted_counties)
