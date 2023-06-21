import numpy as np
import xarray as xr

def crop(da, xlim, ylim):
    """Crop the given DataArray to the given boundaries"""

    return da.sel({xname: slice(xlim[0], xlim[1]), yname: slice(ylim[0], ylim[1])})

##### from gfd.py #####

def get_land(da_source=None):
    """For use in TC seed tracker with HiRAM land data"""
    
    if da_source is None:
        land_frac = xr.open_dataset('/tigress/hsiehtl/HiRAM_land_static.nc')['frac'][0]
    else:
        land_frac = da_source
        
    land_bool = land_frac.values/land_frac.values
    land_bool[np.isnan(land_bool)] = 0
    return xr.DataArray(land_bool, coords=[land_frac[land_frac.dims[-2]], land_frac[land_frac.dims[-1]]], dims=['lat', 'lon'])

from scipy.interpolate import interp2d

def xrinterp(da, target):
    """interpolation to target's grid"""
    
    da = nan2zero(da) # some data have nan on land, which breaks interp2d
    npinterp = interp2d(da[da.dims[-1]], da[da.dims[-2]], da)(target[target.dims[-1]], target[target.dims[-2]])
    da2 = xr.DataArray(npinterp, coords=[target[target.dims[-2]], target[target.dims[-1]]], dims=[target.dims[-2], target.dims[-1]], name=da.name)
    return da2