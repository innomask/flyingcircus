import matplotlib.pyplot   as plt
import cartopy.crs         as ccrs
import cartopy.feature     as cf
import cartopy             as cartopy
import numpy               as np
import xarray              as xr

from cartopy.mpl.ticker    import LongitudeFormatter, LatitudeFormatter
from cartopy.util 		   import add_cyclic_point


# add the greenwich meridian to your netcdf data
# cross the meridian longitude to select your area
# (it's simple, but very useful code)


##----- read netcdf file
dset  =  xr.open_dataset('sst.mnmean.nc')
var   =  dset['sst'][:,:,:]



##--- select area and time
lat1  =  30. ; lat2  =  -30. ; lon1  =  0. ; lon2  =  360.
time1 = '2001-1-1' ; time2 = '2010-12-1'


# slice dataset
var  =  var.sel(lat=slice(lat1,lat2), lon=slice(lon1,lon2),
				time=slice(time1,time2))



##--- numpy array converting (useful for plotting)
lat  =  np.asarray(var['lat'])
lon  =  np.asarray(var['lon'])
time =  np.asarray(var['time'])




##--- add prime meridian line
lon_idx = var.dims.index('lon')
var_c, lon_c = add_cyclic_point(var.values, 
								coord=lon, axis=lon_idx)



##--- save dataset (optional)
# if you just want to add the meridian line to your data
d = {}
d['time'] = ('time',time)
d['lat'] = ('lat',lat)
d['lon'] = ('lon', lon_c)
d['sst'] = (['time','lat','lon'], var_c)

dset_from_dict = xr.Dataset(d)
print (type(dset_from_dict))

#dset_from_dict.to_netcdf('sstwithmeridian.nc')





##--- select another area
lon   =  dset['lon'][:]  # longitude array from original, unsliced, dataset
lonr = lon.roll(lon=300)

lonr = lon.roll(lon=300)
lonr = lonr.sel(lon=slice(250.,20.)) # select your longitude area here
lonrnp = np.asarray(lonr)
new_lons = lonrnp.copy()
new_lons[1:] += np.cumsum(np.diff(lonrnp) < -180) * 360

# slicing data (you can add time as well)
var  =  var.sel(lat=slice(lat1,lat2),
				lon=lonr)


##--- add prime meridian line (yes, again)
lon_idx = var.dims.index('lon')
var_c, lon_c = add_cyclic_point(var.values, 
								coord=new_lons, axis=lon_idx)


##--- save dataset (optional)
d = {}
d['time'] = ('time',time)
d['lat'] = ('lat',lat)
d['lon'] = ('lon', lon_c)
d['sst'] = (['time','lat','lon'], var_c)

#dset_from_dict = xr.Dataset(d)
#print (type(dset_from_dict))

#dset_from_dict.to_netcdf('sst_crossingthemeridian.nc')





##----------------------- PLOTTING
plt.figure(figsize=(8,4))
proj  =  ccrs.PlateCarree()
ax = plt.axes(projection=proj)

ax.add_feature(cf.LAND,color='grey')          
ax.add_feature(cf.BORDERS)
ax.add_feature(cf.COASTLINE)
ax.coastlines(resolution='50m',color='black')

plt.contourf(lon_c, lat, var_c[0,:,:], 60,
             transform=proj,
             cmap=plt.get_cmap('RdBu_r'))

plt.tight_layout()
plt.show()