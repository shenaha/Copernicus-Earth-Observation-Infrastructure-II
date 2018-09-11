import os,sys
import os.path
import datetime


def notify (text, newline=True):
  print text,
  if newline: print
  sys.stdout.flush()

def spawn (cmdline):
  import subprocess
  notify(cmdline)
  started = datetime.datetime.now()
  subprocess.check_call(cmdline.split())
  notify((datetime.datetime.now()-started).total_seconds())
  
def nodata (path, value): 
  with open(path+".aux.xml","w") as aux: aux.write("<PAMDataset><PAMRasterBand band='1'><NoDataValue>%d</NoDataValue></PAMRasterBand><PAMRasterBand band='2'><NoDataValue>%d</NoDataValue></PAMRasterBand><PAMRasterBand band='3'><NoDataValue>%d</NoDataValue></PAMRasterBand></PAMDataset>"%(value,value,value))


GPT = r"C:\ProgramFiles\bin\gpt"
graphImg = "cgo6"
BigTifImg = "BigTIFF2"
inFile = "D:\\test\\work\\tmp"
writeImg = "D:\\FinalOutput\\"
writeImgTmp = ""

# for every downloaded product, perform preprocessing and water detection steps 
list_of_files = os.listdir(os.path.join(inFile))
for each_file in list_of_files:
  if each_file.startswith('S1'):
    # print each_file[:-5]
    writeImgTmp = writeImg+each_file[:-5]+"op.dim" 
    # preprocessing of raster
    starttime = datetime.datetime.now()
    print "start preprocessing: ",starttime
    spawn(GPT+" %s.xml -Pread=%s -Pwrite=%s"%
          (os.path.join(graphImg),os.path.join(inFile,each_file,"manifest.safe"),os.path.join(writeImgTmp)))
    endtime = datetime.datetime.now()
    print "preprocessing finished: ",endtime
    print "Total GPT time: ",(endtime-starttime).total_seconds()
    mainDir = os.path.join("D:\\FinalOutput\\",writeImg+each_file[:-5]+"op.data\\main")
    sideDir = os.path.join("D:\\FinalOutput\\",writeImg+each_file[:-5]+"op.data\\side")
    mainExp = os.path.join(mainDir,"export.tif")
    sideExp = os.path.join(sideDir,"export.tif")

    # Convert .dim to .tif 
    print "Converting dim to tif: ",datetime.datetime.now()
    spawn("C:\\Program Files\\snap\\bin\\gpt %s.xml -Pread=%s -Pmain=%s -Pside=%s"%(os.path.join(BigTifImg),os.path.join(writeImgTmp),mainExp,sideExp))
    print "start GDAL: ",datetime.datetime.now()
    
    ################################### WATER DETECTION ######################################
    # GDAL
    GDAL = "C:\\Program Files\\QGIS 2.18\\bin"
    WARP = "C:\\Program Files\\QGIS 2.18\\bin\\gdalwarp -t_srs EPSG:3857 -r bilinear -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 %s %s" # Alternatively -r bilinear
    STATS = "C:\\Program Files\\QGIS 2.18\\bin\\gdalinfo -stats -hist %s"
    ADDO = "C:\\Program Files\\QGIS 2.18\\bin\\gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config GDAL_TIFF_OVR_BLOCKSIZE 512 -ro %s 2 4 8 16 32 64"
    FINISH = "C:\\Program Files\\QGIS 2.18\\bin\\gdal_translate -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR -co COPY_SRC_OVERVIEWS=YES -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 %s %s"

    # handling nodata
    nodata(mainExp,0); nodata(sideExp,255)
    mainND,sideND = mainExp,sideExp
    
    # info of tif
    spawn(STATS%mainND); spawn(STATS%sideND)
    # image pyramids
    spawn(ADDO%mainND); spawn(ADDO%sideND)
    # final tif
    mainFin,sideFin = os.path.join(mainDir,"final.tif"), os.path.join(sideDir,"final.tif")
    spawn(FINISH%(mainND,mainFin))
    spawn(FINISH%(sideND,sideFin))
    print "scene completed...\n: ",datetime.datetime.now()
  else :
    print "File not readable"
