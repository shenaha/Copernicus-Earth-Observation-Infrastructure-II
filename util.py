#projectid
PROJECTID = "" 

import os,boto3
CONCERN,TODOSNAP,TODOARC,RESULT = "concern/%s", "todo/snap/%s", "todo/arc/%s", "snap/%s"

SITE = dict()
#two data hub options: scihub or code-de
#site,collspec = "https://scihub.copernicus.eu/", "producttype:GRD"
site,collspec = "https://code-de.org/", "platformname:Sentinel-1+AND+producttype:GRD+AND+sensoroperationalmode:IW"

#constructing URLs for querying the data hub
base = site+"dhus/"
coords = "5.8664000+50.3276000,9.4623000+50.3276000,9.4623000+52.5325000,5.8664000+52.5325000,5.8664000+50.3276000"
SITE["SEARCH"] = base + "search?format=xml&sortedby=beginposition&order=desc&rows=100&q="+collspec+"+AND+beginPosition:[NOW-{}DAYS+TO+NOW]+AND+footprint:%22Intersects(POLYGON(("+ coords +")))%22&start="
product = base + "odata/v1/Products('%s')/"
SITE["CHECKSUM"], SITE["SAFEZIP"] = product+"Checksum/Value/$value", product+"$value"

import sys
#function for printing notification in cmd
def notify (text, newline=True):
  print text,
  if newline: print
  sys.stdout.flush()

import datetime
def greet ():
  notify("### "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

#base64 encoded password for data hub, format is "username:password"
BASIC64 = "Basic "+os.environ["BASIC64"]

#functions for opening and authorizing URL
def urlOpen (url):
  import urllib2
  req = urllib2.Request(url)
  req.add_header("Authorization", BASIC64)
  return urllib2.urlopen(req)
import openstack,requests
def authorized (verb, url, **kwargs):
  rsp = getattr(requests,verb)(url, headers={"X-Auth-Token":openstack.connect().authorize()}, **kwargs)
  rsp.raise_for_status()
  return rsp

#function for checking if product already has been downloaded
def exists (title):
  from os import listdir 
  from os.path import isfile,join
  folderlist = os.listdir("D:\\test\\work\\tmp\\")
  for elem in folderlist:
    if(elem == title+".SAFE"):
      print(elem)
      return True
