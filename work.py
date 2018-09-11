#!/usr/bin/env python
import util,dms,time
from util import *
import platform,os,datetime
import shutil

#variables for working directories
HOSTNAME,HERE,WORK = platform.node().split(".")[0], os.path.realpath(os.path.dirname(__file__)), os.path.join(os.environ["HOME"],"work")
TMP,GPT,GDAL,TEST = os.path.join(WORK,"tmp"), WORK+"/snap/bin/gpt", "/usr/bin/gdal", False

#function for downloading products
def download (url, folder, filename, md5sum=None):
  target = os.path.join(folder, filename)
  if os.path.exists(target): os.remove(target) #overwrite!
  rsp = util.urlOpen(url)
  cl = rsp.headers.getheader("Content-Length")
  size = int(cl) if cl else -1
  list_of_files = os.listdir("D:\\test\\work\\tmp\\")
  for each_file in list_of_files:
    if each_file.startswith('S1'):
      #before download starts, delete folders older than 5 days
      nw = time.time()
      if ((nw - os.path.getctime("D:\\test\\work\\tmp\\"+each_file))/(3600*24) > 5.0) :
        shutil.rmtree("D:\\test\\work\\tmp\\"+each_file)
  #fetching products
  if md5sum:
    import hashlib
    md5hash=hashlib.md5()
  with open(target,"wb") as f: #do not read as a whole into memory:
    written, started = 0, datetime.datetime.now()
    print(started)
    for block in iter(lambda:rsp.read(8192),""): #urllib.retrieve() has 8KiB as default block size, shutil.copyfileobj() 16KiB.
      f.write(block); written += len(block)
      if md5sum: md5hash.update(block)
    ended = datetime.datetime.now()
    print(ended)
  written = os.path.getsize(target)
  #verify:
  if size>-1 and written!=size:
    raise ValueError("%s: size mismatch, %d bytes written but expected %d bytes to write!"%(target, written,size))
  elif md5sum:
    calculated,expected = md5hash.hexdigest(), md5sum.lower()
    if calculated!=expected:
      raise ValueError("%s: MD5 mismatch, calculated %s but expected %s!"%(target, calculated,expected))
  print("download complete?")
  return target, (ended-started).total_seconds()

#function for unzipping the downloaded product zip file
def unpack (zipFull):
  notify("Unpacking...",False)
  import zipfile; zipfile.main(["-e", zipFull, TMP])
  os.remove(zipFull)
  result = os.path.splitext(zipFull)[0]+".SAFE"
  notify(result)
  return result

#function for executing the commands on the prompt
def spawn (cmdline):
  import subprocess
  notify(cmdline)
  started = datetime.datetime.now()
  subprocess.check_call(cmdline.split())
  notify((datetime.datetime.now()-started).total_seconds())

#def nodata (path, value): #since "gdal_edit -a_nodata 0" has no effect!
#  with open(path+".aux.xml","w") as aux: aux.write("<PAMDataset><PAMRasterBand band='1'><NoDataValue>%d</NoDataValue></PAMRasterBand><PAMRasterBand band='2'><NoDataValue>%d</NoDataValue></PAMRasterBand><PAMRasterBand band='3'><NoDataValue>%d</NoDataValue></PAMRasterBand></PAMDataset>"%(value,value,value))

#function for automating process (checking for existence, downloading, unzipping)
def single (title, test=False):
  notify("")
  FMT,started = "%Y-%m-%d %H:%M", datetime.datetime.now()
  notify("+++++++++++++++++++++++++++++++++++++++++++++ "+started.strftime(FMT))
  global TEST; TEST=test #isinstance(current, basestring)
  notify(title)
  if util.exists(title):
    print("product already exists...")
    return
  import shutil
  if not TEST:
    if len(title)==36: #download directly from DHuS:
      notify("Downloading...",False)
      uuid = title
      md5sum = util.urlOpen(SITE["CHECKSUM"]%uuid).read()
      zipFull,duration = download(SITE["SAFEZIP"]%uuid, TMP, title+".zip", md5sum)
      notify("%s %f"%(md5sum,duration))
    safeDir = unpack(zipFull)
  else:
    safeDir=os.path.join(TMP, title+".SAFE")  #append .SAFE to the product title
  #send uuid of downloaded product to second queue
  dms.send("SP-iddownloaded", uuid)
  ended=datetime.datetime.now()
  notify("--------------------------------------------- %s %d" % (ended.strftime(FMT), (ended-started).total_seconds()))

#function for iterating through available product ids / messages
def cycle ():
  done,started = 0, datetime.datetime.now()
  while True:
    aspirant = dms.next("SP-idavailable")
    if not aspirant:
      break
    single(aspirant); done += 1
  notify("%d %.3f"%(done, (datetime.datetime.now()-started).total_seconds()/3600))

if __name__=="__main__":
  cycle()

