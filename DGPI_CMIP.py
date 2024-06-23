import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from load import load_cmip
from util import crop, op_2d_to_nd, get_fcor, get_land, xrinterp, dgpi
from param import boundaries
from cmip import model_list

import yaml

cmip_data = load_cmip('GFDL-CM4', 'wap', 'piControl').isel(time=0).isel(plev=0)
land = xrinterp(get_land(), cmip_data)

def interp_to_1x1(da):
    return xrinterp(da, land)

dgpi_all = dict()

for domain in ['Tropics', 'NH Tropics', 'SH Tropics']:
    dgpi_all[domain] = dict()
    xlim, ylim = boundaries(domain)

    for model in model_list():
        dgpi_all[domain][model] = dict()

        for exp in ['piControl', 'abrupt-4xCO2']:
            data = dict()

            data['ts'] = load_cmip(model, 'ts', exp)

            data['omega500'] = load_cmip(model, 'wap', exp).sel(plev=50000)
            data['u500'] = load_cmip(model, 'ua', exp).sel(plev=50000)

            data['u850'] = load_cmip(model, 'ua', exp).sel(plev=85000)
            data['v850'] = load_cmip(model, 'va', exp).sel(plev=85000)

            data['u200'] = load_cmip(model, 'ua', exp).sel(plev=20000)
            data['v200'] = load_cmip(model, 'va', exp).sel(plev=20000)

            ## monthly mean
            for key in data.keys():
                data[key] = data[key][100*12:].groupby('time.month').mean('time')

            data['ts'] = op_2d_to_nd(interp_to_1x1, data['ts']) # interpolate from 2x2.5 to 1x1 # redundant

            data['absvort850'] = (data['v850'].differentiate('lon') - data['u850'].differentiate('lat'))*(1/111e3) + get_fcor(data['u850'].lat) # 1 deg \approx 111 km
            data['vshear'] = np.sqrt(data['u200']**2 + data['v200']**2) - np.sqrt(data['u850']**2 + data['v850']**2) # vertical shear
            data['mshear500'] = data['u500'].differentiate('lat')*(1/111e3) # meridional shear

            ## remove land and crop domain
            criteria = (land < 0.5)
            for key in data.keys():
                if key == 'ts':
                    data[key] = data[key].where(criteria) # do not crop SST
                else:
                    data[key] = crop(data[key].where(criteria), xlim, ylim)

            index = dgpi(data['vshear'], data['mshear500'], data['omega500'], data['absvort850'], data['ts'])

            dgpi_all[domain][model][exp] = float(np.sum(index))

        print(domain, model, (dgpi_all[domain][model]['abrupt-4xCO2'] - dgpi_all[domain][model]['piControl'])/dgpi_all[domain][model]['piControl'])

with open('data/DGPI.yaml', 'w') as f: 
    yaml.dump(dgpi_all, f, default_flow_style=False)
