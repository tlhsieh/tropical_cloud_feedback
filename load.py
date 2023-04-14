import numpy as np
import xarray as xr

from param import model_list

def load_cmip(model, field, exp='piControl'):
    return xr.open_dataset(f'/tigress/cw55/data/CMIP6_post/CMIP6_post_regrid/{exp}/{model}/{field}/{field}.mon.0001-0200.nc.r1i1p1f1.1x1.20210826')

def load_feedback(model):
    return xr.open_dataset(f'/tigress/cw55/data/CMIP6_post/abrupt-4xCO2/{model}/rk/rk.GFDL.toa.0001-0150.nc.r1i1p1f1.2x2.5.2021052021')

if __name__ == '__main__':
    for model in model_list('high_res'):
        print(model)

        ds = load_cmip('GFDL-CM4', 'ua')
        ds = load_cmip('GFDL-CM4', 'va')
        ds = load_cmip('GFDL-CM4', 'wap')

        ds = load_feedback('GFDL-CM4')