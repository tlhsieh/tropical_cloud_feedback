import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from load import load_feedback
from util import crop, op_2d_to_nd, area_weighted_mean_2d, get_land, xrinterp
from param import boundaries
from cmip import model_list

from scipy import stats
import yaml

def corr(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    return slope, intercept, r_value

feedback_data = load_feedback('GFDL-CM4').dR_c_lw.isel(time=0) # any model would work
land = xrinterp(get_land(), feedback_data) # interpolate land to feedback data grid

lambda_c_all = dict()

for domain in ['Global', 'Tropics', 'NH Tropics', 'SH Tropics']:
    lambda_c_all[domain] = dict()
    xlim, ylim = boundaries(domain)

    for model in model_list():
        lambda_c_all[domain][model] = dict()

        ds = load_feedback(model)

        dT = ds['dts_gm'].resample(time='1Y', closed='left').mean() # global mean surface temperature change

        if domain == 'Global':
            criteria = 1
        else:
            criteria = (land < 0.5)

        dR_c_lw = crop(ds['dR_c_lw'].where(criteria), xlim, ylim)
        dR_c_sw = crop(ds['dR_c_sw'].where(criteria), xlim, ylim)

        dR_c_lw = op_2d_to_nd(area_weighted_mean_2d, dR_c_lw) # weighted by latitude, accounting for NaN on land
        dR_c_sw = op_2d_to_nd(area_weighted_mean_2d, dR_c_sw)

        dR_c_lw = dR_c_lw.resample(time='1Y', closed='left').mean()
        dR_c_sw = dR_c_sw.resample(time='1Y', closed='left').mean()

        dR_c = dR_c_lw + dR_c_sw

        slope, intercept, r_value = corr(dT, dR_c)
        lambda_c_all[domain][model]['lambda_c'] = float(slope) # float() to keep format clean in yaml
        lambda_c_all[domain][model]['r_value'] = float(r_value)

        slope, intercept, r_value = corr(dT, dR_c_lw)
        lambda_c_all[domain][model]['lambda_c_lw'] = float(slope)

        slope, intercept, r_value = corr(dT, dR_c_sw)
        lambda_c_all[domain][model]['lambda_c_sw'] = float(slope)

with open('data/Cloud_feedback.yaml', 'w') as f: 
    yaml.dump(lambda_c_all, f, default_flow_style=False)
