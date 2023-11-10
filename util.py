import numpy as np
import xarray as xr

def _dgpi(vshear, mshear, omega, absvort):
    return (2.0 + 0.1*vshear)**(-1.7)*(5.5 - mshear*1e5)**(2.3)*(5.0 - 20*omega)**(3.4)*(5.5 + abs(absvort*1e5))**(2.4)*np.exp(-11.8) - 1.0 # following Murakami and Wang (2022) https://www.nature.com/articles/s43247-022-00410-z

def dgpi(vshear, mshear, omega, absvort, sst):
    """Calculate the dynamical genesis potential index of Murakami and Wang (2022)"""

    if np.sum(np.isnan(sst)) == 0:
        print('Warning: land region in SST needs to be NaN')

    if np.max(sst.lat) < 25 or np.min(sst.lat) > -25:
        print('Warning: SST data needs to cover 30S-30N to calculate tropical mean SST')

    index = _dgpi(vshear, mshear, omega, absvort)
    index = index*(abs(index.lat) > 5) # zero out data within 5S-5N # following Murakami and Wang (2022)

    sst_anomaly = sst - sst.sel(lat=slice(-30, 30)).mean(['lat', 'lon'])
    index = index*(sst_anomaly > 0) # zero out data where SST anomaly < 0 # following Murakami and Wang (2022)

    return index

def crop(da, xlim, ylim):
    """Crop the given DataArray to the given boundaries"""

    xname = da.dims[-1]
    yname = da.dims[-2]

    return da.sel({xname: slice(xlim[0], xlim[1]), yname: slice(ylim[0], ylim[1])})

##### from X-SHiELD #####

def _op_2d_to_3d(func2d, da3d):
    dim0 = da3d.dims[0]
    computed = [func2d(da3d[i]) for i in range(len(da3d[dim0]))]
    element = computed[0]

    if len(element.dims) == 2:
        coords = [da3d[dim0], element[element.dims[-2]], element[element.dims[-1]]]
        dims = [dim0, element.dims[-2], element.dims[-1]]
    elif len(element.dims) == 1:
        coords = [da3d[dim0], element[element.dims[-1]]]
        dims = [dim0, element.dims[-1]]
    else:
        coords = [da3d[dim0]]
        dims = [dim0]
    
    return xr.DataArray(computed, coords=coords, dims=dims, name=da3d.name)

def _op_2d_to_4d(func2d, da4d):
    dim0 = da4d.dims[0]
    dim1 = da4d.dims[1]
    computed = [[func2d(da4d[i, j]) for j in range(len(da4d[dim1]))] for i in range(len(da4d[dim0]))]
    element = computed[0][0]

    if len(element.dims) == 2:
        coords = [da4d[dim0], da4d[dim1], element[element.dims[-2]], element[element.dims[-1]]]
        dims = [dim0, dim1, element.dims[-2], element.dims[-1]]
    elif len(element.dims) == 1:
        coords = [da4d[dim0], da4d[dim1], element[element.dims[-1]]]
        dims = [dim0, dim1, element.dims[-1]]
    else:
        coords = [da4d[dim0], da4d[dim1]]
        dims = [dim0, dim1]
    
    return xr.DataArray(computed, coords=coords, dims=dims, name=da4d.name)

def op_2d_to_nd(func2d, da):

    ndim = len(da.dims)
    if ndim == 2:
        return func2d(da)
    elif ndim == 3:
        return _op_2d_to_3d(func2d, da)
    elif ndim == 4:
        return _op_2d_to_4d(func2d, da)
    else:
        print("ndim needs to be 2, 3 or 4")
        
##### from gfd.py #####

def area_weighted_mean_2d(da, lat_name=None):
    if lat_name == None:
        lat_name = da.dims[-2]

    # print('lat axis name:', lat_name)
        
    area_weights = np.cos(np.deg2rad(da[lat_name]))
    da_mean = np.nansum(da*area_weights)/np.nansum(np.isfinite(da)*area_weights)

    return da_mean

def get_fcor(lat):
    return 2*2*np.pi/86164*np.sin(lat/180*np.pi)

def get_beta(lat):
    return 2*2*np.pi/86164/6371e3*np.cos(lat/180*np.pi)
    
def geoaxes(axes, land=True):
    """Axes settings for geographical maps
    
    Args:
        axes: array of axes or plt.gca()
    """
    
    if not (type(axes) == np.ndarray):
        axes = [axes]
        
    if land:
        coastlines = get_land()
        
    for i in range(len(axes)):
        if land:
            coastlines.plot.contour(ax=axes[i], colors='k', linewidths=1)
        if i == len(axes) - 1: # label the last plot
            axes[i].set_xlabel('Longitude')
        else:
            axes[i].set_xlabel('')
        axes[i].set_ylabel('Latitude')
        axes[i].set_xticks(range(0, 360+1, 60))
        axes[i].set_yticks(range(-90, 90+1, 15))
        
def get_land(da_source=None):
    """For use in TC seed tracker with HiRAM land data"""
    
    if da_source is None:
        try:
            land_frac = xr.open_dataset('/tigress/hsiehtl/HiRAM_land_static.nc')['frac'][0]
        except FileNotFoundError:
            land_frac = xr.open_dataset('/home/tlh/ipy/HiRAM_land_static.nc')['frac'][0]
    else:
        land_frac = da_source
        
    land_bool = land_frac.values/land_frac.values
    land_bool[np.isnan(land_bool)] = 0
    return xr.DataArray(land_bool, coords=[land_frac[land_frac.dims[-2]], land_frac[land_frac.dims[-1]]], dims=['lat', 'lon'])

def nan2zero(da):
    nparray = da.values
    nparray[np.isnan(nparray)] = 0
    return xr.DataArray(nparray, coords=da.coords)

from scipy.interpolate import interp2d

def xrinterp(da, target):
    """interpolation to target's grid"""
    
    da = nan2zero(da) # some data have nan on land, which breaks interp2d
    npinterp = interp2d(da[da.dims[-1]], da[da.dims[-2]], da)(target[target.dims[-1]], target[target.dims[-2]])
    da2 = xr.DataArray(npinterp, coords=[target[target.dims[-2]], target[target.dims[-1]]], dims=[target.dims[-2], target.dims[-1]], name=da.name)
    return da2

##### from spi.py #####

def Zparam(f, b, U=20): 
    """the non-dimensional Z parameter defined in Hsieh et al. (2020): Z = L_beta/L_f
    
    Args:
        f: the cyclonic absolute vorticity
        b: meridional gradient of the absolute vorticity
        U: the characteristic velocity scale for pre-seed disturbances
    """
    
    return np.maximum(f, 0)/abs(b)**0.5/U**0.5

def Z2prob(Z, sigma=0.69):
    """convert Z to the probability of transition from a convective cluster to a seed"""
    
    return 1/(1 + Z**(-1/sigma))

def spi(omega500, vort850):
    """the seed propensity index defined in Hsieh et al. (2022)"""
    
    fcor = get_fcor(vort850.lat)
    beta = get_beta(vort850.lat)

    absvort = (fcor + vort850)*np.sign(fcor) # such that positive is cyclonic
    effbeta = beta + vort850.differentiate('lat')*(1/111e3) # 1 deg lat \approx 111 km
    
    seed_propensity_index = np.maximum(-omega500, 0)*Z2prob(Zparam(absvort, abs(effbeta)))
    
    return seed_propensity_index