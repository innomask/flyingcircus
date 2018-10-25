#!/usr/bin/env python


'''
 File Name: vort_sfvp.py
 Description: Usage of Windspharm package.
 Observations: 
 Author: Willy Hagi
 E-mail: hagi.willy@gmail.com
 Python Version: 3.6
'''





import matplotlib.pyplot   as plt
import cartopy.crs         as ccrs
import cartopy.feature     as cf
import cartopy             as cartopy
import numpy               as np
import xarray              as xr


from cartopy.mpl.ticker    import LongitudeFormatter, LatitudeFormatter
from cartopy.util 		   import add_cyclic_point
from windspharm.xarray 	   import VectorWind





##--- read data
wind =  ['uwnd.mon.mean.nc', 
		  'vwnd.mon.mean.nc']

dset  =  xr.open_mfdataset(wind)

uwnd  =  dset['uwnd']

vwnd  =  dset['vwnd']

lat   =  dset['lat']
lon   =  dset['lon']
lvl   =  dset['level']


lat  =  np.asarray(lat.lat.values)
lon  =  np.asarray(lon.lon.values)



time1 = '1981-1-1' ; time2 = '2010-12-1'



##--- select level
uwnd  =  uwnd.sel(time=slice(time1,time2),
				  level=200.)
vwnd  =  vwnd.sel(time=slice(time1,time2),
				  level=200.)



##--- windspharm call
w  =  VectorWind(uwnd, vwnd)



##--- streamfunction and velocity potential
vp  =  w.velocitypotential()



##--- divergent wind
uchi, vchi  =  w.irrotationalcomponent()



##--- monthly averaging
vp    =  vp.groupby('time.month').mean('time')
uchi  =  uchi.groupby('time.month').mean('time')
vchi  =  vchi.groupby('time.month').mean('time')



##--- add_cyclic_point
lon_idx = vp.dims.index('lon')

vp_c, lon_c   = add_cyclic_point(vp.values, 
								coord=lon, axis=lon_idx)

uchi_c, lon_c = add_cyclic_point(uchi.values, 
								coord=lon, axis=lon_idx)

vchi_c, lon_c = add_cyclic_point(vchi.values, 
								coord=lon, axis=lon_idx)


# 
vp_c  =  vp_c * 1E-6

#uchi_c = uchi_c[0,:,:]
#vchi_c = vchi_c[0,:,:]



##----------------------- PLOTTING
interc = np.arange(-10,12,2)

##--- DJF velocity potential
plt.figure(figsize=(8,6))
div_int = np.arange(-1.6, 1.8, 0.2)

proj  =  ccrs.PlateCarree(central_longitude=0.)
ax = plt.axes(projection=proj)

ax.add_feature(cf.BORDERS)
ax.add_feature(cf.COASTLINE)
ax.coastlines(resolution='50m',color='black')

CV = plt.contourf(lon_c, lat, vp_c[0,:,:],
		    interc,
            transform=proj,
            cmap=plt.get_cmap('cividis'),extend='both')

plt.colorbar(ax=ax, shrink=0.8, orientation='horizontal',extendrect=True)


ax.quiver(lon_c[::3], lat[::3], uchi_c[0,::3, ::3], vchi_c[0,::3, ::3])



plt.title(r'$\chi$ and Divergent Wind at 200 hPa')

plt.tight_layout()
plt.show()





