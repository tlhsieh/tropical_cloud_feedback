import numpy as np
import xarray as xr

import os
from cmip import model_list

def load_cmip(model, field, exp='piControl'):
    if exp == 'piControl':
        yrend = '200'
    elif exp == 'abrupt-4xCO2':
        yrend = '150'
    else:
        yrend = '200'

    if field == 'ts':
        res = '2x2.5.2022tasts'
    else:
        res = '1x1.20210826'

    file_path = f'/tigress/cw55/data/CMIP6_post/CMIP6_post_regrid/{exp}/{model}/{field}/{field}.mon.0001-0{yrend}.nc.r1i1p1f1.{res}'

    # print(file_path)

    return xr.open_dataarray(file_path).isel(model=0) # remove the model axis

def load_feedback(model):
    return xr.open_dataset(f'/tigress/cw55/data/CMIP6_post/abrupt-4xCO2/{model}/rk/rk.GFDL.toa.0001-0150.nc.r1i1p1f1.2x2.5.2021052021')

if __name__ == '__main__':
    for model in model_list():
        print(model)
        data = load_cmip(model, 'wap', 'abrupt-4xCO2')