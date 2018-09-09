from ecmwfapi import ECMWFDataServer
from datetime import datetime, timedelta


'''
Download ECMWF gridded datasets.

see more examples here:
https://confluence.ecmwf.int/display/WEBAPI/Python+ERA-interim+examples
https://retostauffer.org/code/Download-ERA-INTERIM/
https://csyhuang.github.io/2018/02/23/ECMWF-download/


'''



##--- datestring
'''use this to define a data range for monthly values;
this is necessary if you want to download ERA20C data, for example.

Found this here: https://confluence.ecmwf.int/display/CKB/How+to+specify+dates+for+ERA-Interim+daily+and+monthly+data+using+Python

'''


start = datetime(1980, 1, 1)
end = datetime(1982, 12, 1)
  
datelist = [start.strftime('%Y-%m-%d')]
while start <= end:
    start += timedelta(days=32)
    datelist.append( datetime(start.year, start.month, 1).strftime('%Y-%m-%d') )
datestring = "/".join(datelist)

server = ECMWFDataServer()
  


##--- describe what you want to download
''' a parameter list can be found here:
http://apps.ecmwf.int/codes/grib/param-db

'''

args = {
         "dataset"  : "era20c",
         "class"    : "e2",
         "expver"   : "1",
         "stream"   : "moda",
         "type"     : "an",
         "date"     : datestring,
         "grid"     : "2.0/2.0",
         "levtype"  : "sfc",
         "format"   : "netcdf",
         "param"    : "167.128", # this is for t2m
         "target"   : "temp.nc",
      }


server.retrieve(args) # this gets your data

