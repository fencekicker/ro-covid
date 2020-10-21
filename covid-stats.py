#!/usr/bin/python


import argparse
import json
import datetime
import operator
import requests

url="https://datelazi.ro/latestData.json"
# url="https://di5ds1eotmbx1.cloudfront.net/latestData.json"
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

def getCountiesDelta(startDict, endDict, numEntries = 5):
    counties = {}
    for x in startDict["countyInfectionsNumbers"].keys():
        counties[x] = endDict["countyInfectionsNumbers"][x] - startDict["countyInfectionsNumbers"][x]

    sorted_counties = sorted(counties.items(), key=operator.itemgetter(1), reverse=True)

    cases_delta = endDict["numberInfected"] - startDict["numberInfected"]
    print ("> Delta between %s and %s: %d" %(startDict["parsedOnString"], endDict["parsedOnString"], cases_delta))

    print (">> Top %d growth by county" %(numEntries))
    for x in range(0, numEntries):
        print ("%d: %s" %(x + 1, sorted_counties[x]))
    

parser = argparse.ArgumentParser(description='Statistici Covid')
parser.add_argument('-f', '--file', help='Fisier cu date', type=str)
parser.add_argument('-w', '--week', help='Top pe ultima saptamana', default=False, action='store_true')
parser.add_argument('-t', '--top', help='Cate entry-uri', type=int, default = 5)
parser.add_argument('-d', '--days', help='Numar zile in urma de afisat', type=int, default = 1)
parser.add_argument('-D', '--days-delta', help='Afiseaza total si top pe ultimele X zile', type=int, default=1)
args = parser.parse_args()

if args.file:
    print ("Parsing %s" %args.file)

    f = open(args.file)
    json = json.loads(f.read())
else:
    print ("Fetching latest data from %s" %url)
    r = requests.get(url)
    json = json.loads(r.content)

todayStats = json["currentDayStats"]
today = todayStats["parsedOnString"]
print ("Last update: %s" %json["lasUpdatedOnString"])
print ("Date: %s Infected: %s Cured: %s Died: %s" %(today, todayStats["numberInfected"], todayStats["numberCured"], todayStats["numberDeceased"]))

days_delta = 1
if args.week:
    days_delta = 7
elif args.days_delta:
    days_delta = args.days_delta

dt = datetime.datetime.strptime(today, '%Y-%m-%d')
if days_delta > 1:
    prev = dt - datetime.timedelta(days=days_delta)
    str_prev = prev.strftime('%Y-%m-%d')
    prevStats = json["historicalData"][str_prev]
    getCountiesDelta(prevStats, todayStats, args.top)
else:
    yday = dt - datetime.timedelta(days=1)
    str_yesterday = yday.strftime('%Y-%m-%d')

    yesterdayStats = json["historicalData"][str_yesterday]

    getCountiesDelta(yesterdayStats, todayStats, args.top)

    crtDay = yday
    dayStats = yesterdayStats
    for x in range(0, args.days - 1):
        dayBefore = crtDay - datetime.timedelta(days=1)
        dayBeforeStr = dayBefore.strftime('%Y-%m-%d')
        dayBeforeStats = json["historicalData"][dayBeforeStr]
        getCountiesDelta(dayBeforeStats, dayStats, args.top)
        dayStats = dayBeforeStats
        crtDay = dayBefore
