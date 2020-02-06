Copernicus-Earth-Observation-Infrastructure-II
--------------------------------------------------
* *Automate water detection from Sentinel-1 satellite imagery using Telekom cloud archietecture.

* The aim of the project is to automate water detection from Sentinel-1 satellite imagery.
* This repository contains scripts to get this process running. The python scripts are for searching, downloading and ingesting, unzipping and storing Sentinel-1 products on a virtual machine on the OTC. Moreover, the product ids are being sent to DMS queues in the OTC.  
* The batch files have to be placed in cron jobs (Linux) / task scheduler jobs (Windows) for automatic execution after a specific time period. The xml files are needed for pre-processing of Sentinel-1 satellite imagery.
OTC access is needed.
* Used telekom cloud archietecture for storage and processing i.e. automatic extraction of water from large datasets.

### Team : Akhil Patil, Raphael Witt, Shenaha Sivakumar, Christopher Rohtermundt
