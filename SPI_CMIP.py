import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from load import load_cmip
from util import crop, get_land, xrinterp, spi
from param import boundaries
from cmip import model_list

import yaml

cmip_data = load_cmip('GFDL-CM4', 'wap', 'piControl').isel(time=0).isel(plev=0)
land = xrinterp(get_land(), cmip_data)

spi_all = dict()

for domain in ['Tropics', 'NH Tropics', 'SH Tropics']:
    spi_all[domain] = dict()
    xlim, ylim = boundaries(domain)

    for model in model_list():
        spi_all[domain][model] = dict()

        for exp in ['piControl', 'abrupt-4xCO2']:
            data = dict()

            data['omega500'] = load_cmip(model, 'wap', exp).sel(plev=50000)
            data['u850'] = load_cmip(model, 'ua', exp).sel(plev=85000)
            data['v850'] = load_cmip(model, 'va', exp).sel(plev=85000)

            ## monthly mean
            for key in data.keys():
                data[key] = data[key][100*12:].groupby('time.month').mean('time')

            data['vort850'] = (data['v850'].differentiate('lon') - data['u850'].differentiate('lat'))*(1/111e3) # 1 deg \approx 111 km

            ## remove land and crop domain
            criteria = (land < 0.5)
            for key in data.keys():
                data[key] = crop(data[key].where(criteria), xlim, ylim)

            index = spi(data['omega500'], data['vort850'])
            
            spi_all[domain][model][exp] = float(np.sum(index))

        print(domain, model, (spi_all[domain][model]['abrupt-4xCO2'] - spi_all[domain][model]['piControl'])/spi_all[domain][model]['piControl'])

with open('data/SPI.yaml', 'w') as f: 
    yaml.dump(spi_all, f, default_flow_style=False)