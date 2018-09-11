#!/usr/bin/env python
import util,dms
from util import SITE,notify

#function for searching data products
def search (daysBack=7):
  import xml.etree.cElementTree as ET
  url = SITE["SEARCH"].format(daysBack)
  news,offset,rowsBreak,keys,ns = dict(),0,50000,[], {"atom":"http://www.w3.org/2005/Atom", "opensearch":"http://a9.com/-/spec/opensearch/1.1/"}
  while offset<rowsBreak: #next pagination page:
    rsp = util.urlOpen(url + str(offset))
    root = ET.ElementTree(file=rsp).getroot()
    if offset==0:
      rowsBreak = int(root.find("opensearch:totalResults",ns).text)
    for e in root.iterfind("atom:entry",ns):
      title,uuid = e.find("atom:title",ns).text, e.find("atom:id",ns).text
      if not util.exists(title): news[uuid] = title
   
    offset += 100 #ultimate DHuS pagination page size limit (rows per page).
  notify("%d/%d"%(len(news),rowsBreak))
  return news

#function for sending product id (uuid) to queue
def submit (news, start=False):
  count = len(news)
  if count>0:
    import openstack
    otc = openstack.connect()
    for uuid,title in news.viewitems():
      notify("%s %s"%(uuid,title),False)
      dms.send("SP-idavailable", uuid) #name of the queue to send to (title = name of product, uuid = id of product)
      notify("")
  return count

if __name__=="__main__":
  util.greet()
  submit(search(), True)

