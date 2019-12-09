import numpy as np
import xarray as xr
import proplot as plot
import matplotlib.pyplot as plt

from esmtools.stats import*


# abrir arquivo
dset = xr.open_dataset('sst.mnmean.nc')

# média climatológica
baseline = dset['sst'].sel(time=slice('1981-1-1', '2010-12-1'))
wrt = baseline.groupby('time.month').mean('time')

# anomalia
anom = dset['sst'].groupby('time.month') - wrt

# remover tendência linear
anom_dt= rm_poly(anom, 1, dim='time')

# normalizar por desvio-padrão (opcional)
anom_norm = anom_dt / baseline.std('time')

# salvar arquivos (opcional)
#anom_dt.to_netcdf('asstdt.nc')
#anom_norm.to_netcdf('asstdt_norm.nc')

f, ax = plot.subplots(axwidth=4., nrows=1, ncols=1, tight=True, proj='pcarree',
                      proj_kw={'lon_0': 0},)

ax.format(land=False, coast=True, innerborders=True, borders=True,
          large='15px',
          geogridlinewidth=0, labels=True
          )

map1 = ax.contourf(anom_norm['lon'], anom_norm['lat'], anom_norm[0,:,:],
              levels=np.arange(-1.5, 2., 0.5), cmap='Div', extend='both')

ax.colorbar(map1, loc='b', shrink=0.5, extendrect=True)

plt.show()
