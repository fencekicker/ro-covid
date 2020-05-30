#!/usr/bin/python


import argparse
import json
import datetime
import operator

def getCountiesDelta(startDict, endDict, numEntries = 5):
    counties = {}
    for x in startDict["countyInfectionsNumbers"].keys():
        counties[x] = endDict["countyInfectionsNumbers"][x] - startDict["countyInfectionsNumbers"][x]

    sorted_counties = sorted(counties.items(), key=operator.itemgetter(1), reverse=True)

    print ("> Top %d growth between %s and %s" %(numEntries, startDict["parsedOnString"], endDict["parsedOnString"]))
    for x in range(0, numEntries):
        print ("%d: %s" %(x + 1, sorted_counties[x]))
    

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

yesterdayStats = json["historicalData"][str_yesterday]

getCountiesDelta(yesterdayStats, todayStats)

crtDay = yday
dayStats = yesterdayStats
for x in range(0, 5):
    dayBefore = crtDay - datetime.timedelta(days=1)
    dayBeforeStr = dayBefore.strftime('%Y-%m-%d')
    dayBeforeStats = json["historicalData"][dayBeforeStr]
    getCountiesDelta(dayBeforeStats, dayStats)
    dayStats = dayBeforeStats
    crtDay = dayBefore
