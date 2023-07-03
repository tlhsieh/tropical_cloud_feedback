import numpy as np
import xarray as xr

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

def load_am4_monthly_mean(exp, field):
    if field in ['t_surf', 'omega500', 'ucomp500', 'ucomp850', 'vcomp850', 'ucomp200', 'vcomp200']:
        return xr.open_dataarray(f'/work/tlh/feedback_data/monthly_mean/{exp}/{field}_000201-001112.nc')
    
    return xr.open_dataset(f'/work/tlh/feedback_data/rk_results/{exp}/rk.GFDL.toa.mon.0002-0011.nc')[field].groupby('time.month').mean() # field == dR_c_sw