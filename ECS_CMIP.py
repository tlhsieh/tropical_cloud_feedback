import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from load import load_feedback
from cmip import model_list

from scipy import stats
import yaml

import warnings
warnings.filterwarnings("ignore")

"""
From Gregory et al. (2004):
dR = lambda*dT + 2*ERF # ERF is defined for 2xCO2, so adding a factor of 2 for 4xCO2
ECS = -ERF/lambda
"""

def corr(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    return slope, intercept

ECS_all = dict()

for model in model_list():
    ECS_all[model] = dict()

    ds = load_feedback(model)

    dT = ds['dts_gm'].resample(time='1Y', closed='left').mean() # global mean surface temperature change

    dR_lw = ds['dR_lw_gm'].resample(time='1Y', closed='left').mean() # global mean longwave flux change
    dR_sw = ds['dR_sw_gm'].resample(time='1Y', closed='left').mean() # global mean shortwave flux change

    dR = dR_lw + dR_sw

    slope, intercept = corr(dT, dR)
    ERF = intercept/2
    ECS = -ERF/slope

    ECS_all[model]['ECS'] = float(ECS)
    ECS_all[model]['dT'] = float(np.mean(dT.isel(model=0)[100:]))

with open('data/ECS.yaml', 'w') as f: 
    yaml.dump(ECS_all, f, default_flow_style=False)