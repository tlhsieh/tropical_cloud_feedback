import numpy as np
import xarray as xr

def load_cmip(model, field, exp='piControl'):
    if exp == 'piControl':
        yrend = '200'
    elif exp == 'abrupt-4xCO2':
        yrend = '150'
    else:
        yrend = '200'

    file_path = f'/tigress/cw55/data/CMIP6_post/CMIP6_post_regrid/{exp}/{model}/{field}/{field}.mon.0001-0{yrend}.nc.r1i1p1f1.1x1.20210826'

    # print(file_path)

    return xr.open_dataset(file_path)

def load_feedback(model):
    return xr.open_dataset(f'/tigress/cw55/data/CMIP6_post/abrupt-4xCO2/{model}/rk/rk.GFDL.toa.0001-0150.nc.r1i1p1f1.2x2.5.2021052021')
